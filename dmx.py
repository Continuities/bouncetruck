import colorsys
from dataclasses import dataclass

FIXTURE_ADDRS = [1, 9, 17]    # DMX start address of each floodlight
FIXTURE_CHANNELS = 8          # channels per fixture
# offsets within a fixture; 
# set DIM = None if no dimmer
#     W = None if no white channel
#     STROBE = None if no strobe channel
R, G, B, W, STROBE, DIM = 1, 2, 3, 4, 5, 0     

@dataclass(slots=True)
class FixtureData:
  hue: float = 0.0
  accent: bool = False
  brightness: float = 1.0
  strobe:float = 0.0 # fast to slow

def num_fixtures() -> int:
  return len(FIXTURE_ADDRS)

def fixture_data_to_dmx_values(fixture_data: list[FixtureData]) -> list[float]:
  numChannels = max(FIXTURE_ADDRS) + FIXTURE_CHANNELS - 1
  values = [0.0] * numChannels
  for idx, data in enumerate(fixture_data):
    addr = FIXTURE_ADDRS[idx]
    i = addr - 1

    if STROBE is not None:
      values[i + STROBE] = data.strobe

    if data.accent:
      if W is not None:
        values[i + W] = 1.0
      else:
        values[i + R] = 1.0
        values[i + G] = 1.0
        values[i + B] = 1.0
      if DIM is not None:
        values[i + DIM] = 1.0
      continue

    rgb = colorsys.hsv_to_rgb(data.hue, 1, 1)
    if DIM is not None:
      values[i + R], values[i + G], values[i + B] = rgb
      values[i + DIM] = data.brightness
    else:
      values[i + R] = rgb[0] * data.brightness
      values[i + G] = rgb[1] * data.brightness
      values[i + B] = rgb[2] * data.brightness
  return values

def append_dmx_script_channels(dmx_values: list[float], scriptOp:"scriptCHOP"):
  for k, v in enumerate(dmx_values):
    scriptOp.appendChan('dmx%d' % (k + 1))[0] = v