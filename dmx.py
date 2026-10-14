import colorsys
from dataclasses import dataclass

FIXTURE_ADDRS = [1, 9, 17]    # DMX start address of each floodlight
FIXTURE_CHANNELS = 8          # channels per fixture
R, G, B, DIM = 1, 2, 3, 0     # offsets within a fixture; set DIM = None if no dimmer

@dataclass(slots=True)
class FixtureData:
  hue: float
  brightness: float

def num_fixtures() -> int:
  return len(FIXTURE_ADDRS)

def fixture_data_to_dmx_values(fixture_data: list[FixtureData]) -> list[float]:
  numChannels = max(FIXTURE_ADDRS) + FIXTURE_CHANNELS - 1
  values = [0.0] * numChannels
  for idx, data in enumerate(fixture_data):
    rgb = colorsys.hsv_to_rgb(data.hue, 1, 1)
    addr = FIXTURE_ADDRS[idx]
    i = addr - 1
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