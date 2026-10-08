"""
Script CHOP Callbacks

me - this DAT

scriptOp - the OP which is cooking
"""

FIXTURE_ADDRS = [1]           # DMX start address of each floodlight
FIXTURE_CHANNELS = 4          # channels per fixture
R, G, B, DIM = 0, 1, 2, None  # offsets within a fixture; set DIM = None if no dimmer

from typing import Any

# press 'Setup Parameters' in the OP to call this function to re-create the
# parameters.
def onSetupParameters(scriptOp: scriptCHOP):
  """
  Called to setup custom parameters for the Script CHOP.
  """
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
  scriptOp.clear()
  scriptOp.isTimeSlice = False
  scriptOp.numSamples = 1
  src = scriptOp.inputs[0]
  if src is None:
    return

  brightness = min(max(src['bouncitude'][0], 0), 1)
  rgb = [0, 255, 0] # TODO: Generate from inputs

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
