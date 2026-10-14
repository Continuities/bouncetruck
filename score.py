"""
Execute DAT

me - this DAT

Make sure the corresponding toggle is enabled in the Execute DAT.
"""

MODE_CHOP = 'mode'        # CHOP with truck mode: 0 = party, 1 = competition
BOUNCITUDE_CHOP = 'crest' # CHOP with bouncitude

P = op('/bouncetruck').par

active = False
score = 0.0
quiet_seconds = 0.0

def onStart():
  """
  Called when the project starts.
  """
  return

def onCreate():
  """
  Called when the DAT is created.
  """
  return

def onExit():
  """
  Called when the project exits.
  """
  return

def onFrameEnd(frame: int):
  """
  Called at the end of each frame.
  
  Args:
    frame: The current frame number
  """
  global active, score, quiet_seconds

  dt = 1.0 / project.cookRate
  quiet_seconds_to_end = P.Quietseconds.eval()

  mode = op(MODE_CHOP)[0].eval()
  bouncitude = op(BOUNCITUDE_CHOP)[0].eval()

  if mode == 1:
    active = True
    quiet_seconds = 0.0
    score = max(score, bouncitude)
  elif active and mode != 1:
    quiet_seconds += dt
    if quiet_seconds >= quiet_seconds_to_end:
      active = False
      if score >= P.Minscore.eval():
        # TODO: print the score
        print("Final score: %d" % int(score * P.Scale.eval()))
  return
