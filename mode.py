"""
Script CHOP Callbacks

me - this DAT

scriptOp - the OP which is cooking
"""

from typing import Any

P = op('/bouncetruck').par

_mode_state = 0  # persists across cooks, module-level, no TD dependency tracking

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
	global _mode_state
	scriptOp.clear()
	input_chop = scriptOp.inputs[0]
	if input_chop is None:
		return
	coordination = input_chop['coordination'][0]
	high = float(P.Competitionthreshold.eval())
	low = float(P.Partythreshold.eval())
	
	if _mode_state == 0 and coordination > high:
		_mode_state = 1
	elif _mode_state == 1 and coordination < low:
		_mode_state = 0

	scriptOp.numSamples = 1
	c1 = scriptOp.appendChan('mode')
	c1[0] = _mode_state
	return

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
