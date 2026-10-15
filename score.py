"""
Execute DAT

me - this DAT

Make sure the corresponding toggle is enabled in the Execute DAT.
"""

import sys
folder = project.folder
if folder not in sys.path:
  sys.path.append(folder)
from printer import print_highscore

MODE_CHOP = 'mode'   # CHOP with truck mode: 0 = party, 1 = competition
CREST_CHOP = 'crest' # CHOP with crest
DIP_CHOP = 'dip'     # CHOP with dip

P = op('/bouncetruck').par

active = False
high_score = 0.0
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
  global active, high_score, quiet_seconds

  dt = 1.0 / project.cookRate
  quiet_seconds_to_end = P.Quietseconds.eval()

  mode = op(MODE_CHOP)[0].eval()
  score = max(op(CREST_CHOP)[0].eval(), op(DIP_CHOP)[0].eval())

  if mode == 1:
    if not active:
      debug("Competition started!")
      active = True
      high_score = 0.0
    quiet_seconds = 0.0
    high_score = max(score, high_score)
  elif active and mode != 1:
    quiet_seconds += dt
    if quiet_seconds >= quiet_seconds_to_end:
      debug("Competition ended!")
      debug("Scaling score %f by %f" % (high_score, P.Scorescale.eval()))
      final_score = int(high_score * P.Scorescale.eval())
      debug("Final score: %d" % final_score)
      active = False
      if final_score >= P.Minscore.eval():
        debug("Score is high enough to print!")
        print_highscore(final_score)
  return
