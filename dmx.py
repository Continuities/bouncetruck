import colorsys
from dataclasses import dataclass

@dataclass(slots=True)
class FixtureType:
  channels: int
  R: int
  G: int
  B: int
  W: int | None = None
  STROBE: int | None = None
  UV: int | None = None
  DIM: int | None = None

@dataclass(slots=True)
class FixtureData:
  hue: float = 0.0
  accent: bool = False
  brightness: float = 1.0
  strobe:bool = False
  uv:float = 0.0

MATT_LIGHT = FixtureType(
  channels=8,
  R=1,
  G=2,
  B=3,
  W=4,
  STROBE=5,
  DIM=0
)

JODY_LIGHT = FixtureType(
  channels=6,
  R=0,
  G=1,
  B=2,
  UV=3,
  STROBE=4,
  DIM=5
)

FIXTURES = {
  1: MATT_LIGHT, 
  9: MATT_LIGHT, 
  17: MATT_LIGHT, 
  25: JODY_LIGHT
}

def num_fixtures() -> int:
  return len(FIXTURES)

def fixture_data_to_dmx_values(fixture_data: list[FixtureData]) -> list[float]:
  last_fixture_addr = max(FIXTURES.keys())
  last_fixture_type = FIXTURES[last_fixture_addr]
  numChannels = last_fixture_addr + last_fixture_type.channels - 1
  values = [0.0] * numChannels
  for idx, fixture_addr in enumerate(FIXTURES.keys()):
    i = fixture_addr - 1
    data = fixture_data[idx]
    fixture = FIXTURES[fixture_addr]

    if fixture.STROBE is not None:
      if fixture == JODY_LIGHT:
        values[i + fixture.STROBE] = 0.372 if data.strobe else 1
      else:
        values[i + fixture.STROBE] = 0.95 if data.strobe else 0

    if data.accent:
      if fixture.W is not None:
        values[i + fixture.W] = 1.0
      else:
        values[i + fixture.R] = 1.0
        values[i + fixture.G] = 1.0
        values[i + fixture.B] = 1.0
      if fixture.DIM is not None:
        values[i + fixture.DIM] = 1.0
      continue

    rgb = colorsys.hsv_to_rgb(data.hue, 1, 1)
    if fixture.DIM is not None:
      values[i + fixture.R], values[i + fixture.G], values[i + fixture.B] = rgb
      values[i + fixture.DIM] = data.brightness
    else:
      values[i + fixture.R] = rgb[0] * data.brightness
      values[i + fixture.G] = rgb[1] * data.brightness
      values[i + fixture.B] = rgb[2] * data.brightness
  return values

def append_dmx_script_channels(dmx_values: list[float], scriptOp:"scriptCHOP"):
  for k, v in enumerate(dmx_values):
    scriptOp.appendChan('dmx%d' % (k + 1))[0] = v