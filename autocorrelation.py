"""
Script CHOP Callbacks

me - this DAT

scriptOp - the OP which is cooking
"""

import numpy as np
from typing import Any

# press 'Setup Parameters' in the OP to call this function to re-create the
# parameters.
def onSetupParameters(scriptOp: scriptCHOP):
	"""
	Called to setup custom parameters for the Script CHOP.
	"""
	page = scriptOp.appendCustomPage('Custom')
	p = page.appendInt('Minlag', label='Min lag')
	p.default = 5
	p.min = 0
	p.clampMin = True
	p.max = 50
	p.clampMax = True
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
	input_chop = scriptOp.inputs[0]
	if input_chop is None or input_chop.numSamples < 10:
		return

	data = input_chop.numpyArray()  # shape (numChannels, numSamples)
	x = data[0] - np.mean(data[0])  # remove DC offset

	autocorr = np.correlate(x, x, mode='full')
	autocorr = autocorr[len(autocorr) // 2:]  # keep zero-lag onward
	min_lag = int(scriptOp.par.Minlag.eval())  # skip the first few samples (trivial self-match near lag 0)
	if autocorr[0] == 0:
		coordination = 0.0
	else:
		autocorr = autocorr / autocorr[0]  # normalize so lag 0 = 1.0
		coordination = float(np.max(autocorr[min_lag:])) if len(autocorr) > min_lag else 0.0


	scriptOp.numSamples = 1
	c1 = scriptOp.appendChan('coordination')
	c1[0] = coordination
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
