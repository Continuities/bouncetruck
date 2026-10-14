"""
Script CHOP Callbacks

me - this DAT

scriptOp - the OP which is cooking
"""
from dmx import FixtureData, num_fixtures, fixture_data_to_dmx_values, append_dmx_script_channels


P = op('/bouncetruck').par
current_level:int = 0
drop_timer:float = 0.0

def get_level(force:float) -> int:
  if force >= P.Level3threshold.eval():
    return 3
  elif force >= P.Level2threshold.eval():
    return 2
  elif force >= P.Level1threshold.eval():
    return 1
  return 0

def get_fixture_data(index: int, base_hue:float, crest:float, dip:float) -> FixtureData:
  return FixtureData(base_hue, 1.0)

def onCook(scriptOp: scriptCHOP):
  """
  Called when the Script CHOP needs to cook.
  """
  global current_level, drop_timer
  scriptOp.clear()
  scriptOp.isTimeSlice = False
  scriptOp.numSamples = 1
  src = scriptOp.inputs[0]
  if src is None:
    return
  
  dt = 1.0 / project.cookRate
  base_hue = max(min(src['hue'][0], 1.0), 0.0)
  crest = max(min(src['crest'][0], 1.0), 0.0)
  dip = max(min(src['dip'][0], 1.0), 0.0)
  # bouncitude = max(min(src['bouncitude'][0], 1.0), 0.0)

  frame_level = get_level(max(crest, dip))
  if frame_level > current_level:
    debug("Level increased from %d to %d" % (current_level, frame_level))
    current_level = frame_level
    drop_timer = 0.0
  elif frame_level < current_level:
    drop_timer += dt
    if drop_timer >= P.Leveldropseconds.eval():
      debug("Level dropped from %d to %d" % (current_level, frame_level))
      current_level = frame_level
      drop_timer = 0.0

  data = [get_fixture_data(i, base_hue, crest, dip) for i in range(num_fixtures())]
  dmx_values = fixture_data_to_dmx_values(data)
  append_dmx_script_channels(dmx_values, scriptOp)