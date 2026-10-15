"""
Script CHOP Callbacks

me - this DAT

scriptOp - the OP which is cooking
"""
import sys, importlib
folder = project.folder
if folder not in sys.path:
  sys.path.insert(0, folder)
import dmx
importlib.reload(dmx)
from dmx import FixtureData, num_fixtures, fixture_data_to_dmx_values, append_dmx_script_channels


P = op('/bouncetruck').par
current_level:int = 0
drop_timer:float = 0.0
accent_timer:float = 0.0
accent_index:int = 0

def get_level(force:float) -> int:
  if force >= P.Level3threshold.eval():
    return 3
  elif force >= P.Level2threshold.eval():
    return 2
  elif force >= P.Level1threshold.eval():
    return 1
  return 0

def get_fixture_data(index: int, base_hue:float, crest:float, dip:float) -> FixtureData:
  strobe = 0.5 if current_level >= 3 else 0.0
  if current_level >= 2 and index == accent_index:
    return FixtureData(accent=True, strobe=strobe)
  brightness = min(max(crest, dip) + P.Basebrightness.eval(), 1.0)
  hue_shift = float(P.Crestshift.eval()) if crest > dip else float(P.Dipshift.eval())
  return FixtureData(
    hue=(base_hue + hue_shift) % 1.0, 
    brightness=brightness,
    strobe=strobe
  )

def onCook(scriptOp: scriptCHOP):
  """
  Called when the Script CHOP needs to cook.
  """
  global current_level, drop_timer, accent_timer, accent_index
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

  if (current_level > 1):
    accent_speed = P.Accentspeed.eval()
    accent_timer += dt
    if accent_timer >= accent_speed:
      accent_timer = accent_timer % accent_speed
      accent_index = (accent_index + 1) % num_fixtures()

  data = [get_fixture_data(i, base_hue, crest, dip) for i in range(num_fixtures())]
  dmx_values = fixture_data_to_dmx_values(data)
  append_dmx_script_channels(dmx_values, scriptOp)