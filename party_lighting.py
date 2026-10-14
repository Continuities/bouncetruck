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
from dmx import FIXTURE_ADDRS, FixtureData, append_dmx_script_channels, fixture_data_to_dmx_values

base_colour_angle = 0.0

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

  base_colour_angle += float(P.Colourcyclespeed.eval())
  modified_angle = base_colour_angle + src['angle'][0] % 360
  hue = modified_angle / 360.0
  brightness = min(max(src['bouncitude'][0], 0) + P.Basebrightness.eval(), 1)
  data = [FixtureData((hue + HUE_OFFSET[i]) % 1, brightness) for i in range(len(FIXTURE_ADDRS))]
  dmx_values = fixture_data_to_dmx_values(data)
  append_dmx_script_channels(dmx_values, scriptOp)

