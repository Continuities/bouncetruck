"""
Script CHOP Callbacks

me - this DAT

scriptOp - the OP which is cooking
"""

HUE_OFFSET = [0, 0.1, 0.2]    # Colour hue offset for each light

P = op('/bouncetruck').par

import sys, importlib
folder = project.folder
if folder not in sys.path:
  sys.path.insert(0, folder)
import dmx
importlib.reload(dmx)
from dmx import FixtureData, append_dmx_script_channels, fixture_data_to_dmx_values, num_fixtures

def onCook(scriptOp: scriptCHOP):
  """
  Called when the Script CHOP needs to cook.
  """
  global base_colour_angle
  scriptOp.clear()
  scriptOp.isTimeSlice = False
  scriptOp.numSamples = 1
  src = scriptOp.inputs[0]
  if src is None:
    return

  base_hue = float(src['hue'][0]) % 1.0
  angle = float(src['angle'][0]) % 360.0
  modified_hue = (base_hue + angle / 360.0) % 1.0
  brightness = min(max(src['bouncitude'][0], 0.0) + P.Basebrightness.eval(), 1.0)
  data = [FixtureData(
    hue=(modified_hue + HUE_OFFSET[i]) % 1, 
    brightness=brightness
  ) for i in range(num_fixtures())]
  dmx_values = fixture_data_to_dmx_values(data)
  append_dmx_script_channels(dmx_values, scriptOp)

