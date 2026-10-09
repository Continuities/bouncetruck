"""
Script CHOP Callbacks

me - this DAT

scriptOp - the OP which is cooking
"""

FIXTURE_ADDRS = [1]           # DMX start address of each floodlight
FIXTURE_CHANNELS = 4          # channels per fixture
R, G, B, DIM = 0, 1, 2, None  # offsets within a fixture; set DIM = None if no dimmer


from typing import Any
import colorsys

base_colour_angle = 0.0

# press 'Setup Parameters' in the OP to call this function to re-create the
# parameters.
def onSetupParameters(scriptOp: scriptCHOP):
  """
  Called to setup custom parameters for the Script CHOP.
  """
  page = scriptOp.appendCustomPage('Custom')
  p1 = page.appendFloat('Colourcyclespeed', label='Colour Cycle Speed')
  p1.default = 1
  p1.min = 0
  p1.clampMin = True
  p1.max = 3
  p1.clampMax = True
  p2 = page.appendFloat('Basebrightness', label='Base Brightness')
  p2.default = 0.5
  p2.min = 0
  p2.clampMin = True
  p2.max = 1
  p2.clampMax = True
  return

def onPulse(par: Any):
  """
  Called when a custom pulse parameter is pushed.
  
  Args:
    par: The parameter that was pulsed
  """
  return

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

  base_colour_angle += float(scriptOp.par.Colourcyclespeed.eval())
  modified_angle = base_colour_angle + src['angle'] % 360
  hue = modified_angle / 360.0
  rgb = colorsys.hsv_to_rgb(hue, 1, 1)

  brightness = min(max(src['bouncitude'][0], 0) + scriptOp.par.Basebrightness.eval(), 1)

  numChannels = max(FIXTURE_ADDRS) + FIXTURE_CHANNELS - 1
  values = [0.0] * numChannels
  for addr in FIXTURE_ADDRS:
    i = addr - 1
    if DIM is not None:
      values[i + R], values[i + G], values[i + B] = rgb
      values[i + DIM] = brightness * 255
    else:
      values[i + R] = rgb[0] * brightness
      values[i + G] = rgb[1] * brightness
      values[i + B] = rgb[2] * brightness
  
  for k, v in enumerate(values):
    scriptOp.appendChan('dmx%d' % (k + 1))[0] = v

def onGetCookLevel(scriptOp: scriptCHOP) -> CookLevel:
  """
  Sets the scriptOp's cook level, the conditions necessary to cause a cook.

  Return one of the following:
    CookLevel.AUTOMATIC - inputs changed and output being used. TD default
                behavior.
    CookLevel.ON_CHANGE - inputs changed, output used or not.
    CookLevel.WHEN_USED - every frame when output is being used
    CookLevel.ALWAYS - every frame
  """

  return CookLevel.AUTOMATIC
