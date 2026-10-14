"""
Execute DAT

me - this DAT

Make sure the corresponding toggle is enabled in the Execute DAT.
"""

import sys
folder = project.folder
if folder not in sys.path:
  sys.path.append(folder)

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
    if not active:
      debug("Competition started!")
      active = True
      score = 0.0
    quiet_seconds = 0.0
    score = max(score, bouncitude)
  elif active and mode != 1:
    quiet_seconds += dt
    if quiet_seconds >= quiet_seconds_to_end:
      debug("Competition ended!")
      debug("Scaling score %f by %f" % (score, P.Scorescale.eval()))
      final_score = int(score * P.Scorescale.eval())
      debug("Final score: %d" % final_score)
      active = False
      if final_score >= P.Minscore.eval():
        debug("Score is high enough to print!")
        from printer import print_highscore
        print_highscore(final_score)
  return
