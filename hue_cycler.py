"""
Execute DAT

me - this DAT

Make sure the corresponding toggle is enabled in the Execute DAT.
"""

P = op('/bouncetruck').par
phase = 0.0

def onFrameEnd(frame: int):
  global phase
  dt = 1.0 / project.cookRate

  phase = (phase + P.Huecyclespeed.eval() * dt) % 1.0
  op('hue').par.value0 = (phase + P.Basehue.eval()) % 1.0