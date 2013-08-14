import math
import ROOT
import JPsi.MuMu.common.roofit as roo

ROOT.gSystem.Load('libJPsiMuMu')
ROOT.gROOT.ProcessLine('#include "JPsi/MuMu/interface/tools.h"')
effSigma = ROOT.effSigma

##------------------------------------------------------------------------------
def pdf_effsigma(pdf, obs, nbins=10000):
    'Returns the effective sigma of pdf of observable obs.'
    ## TODO: use the pdf itself instead of sampling it into a histogram?
    hist = pdf.createHistogram(obs.GetName(), nbins)
    hist.Scale(nbins)
    ret = effSigma(hist)
    hist.Delete()
    return ret
## End of pdf_effsigma

##------------------------------------------------------------------------------
def pdf_mode(pdf, obs,
            ## Trick to have static variables zero and minusone
            zero = ROOT.RooConstVar('zero', 'zero', 0),
            minusone = ROOT.RooConstVar('minusone', 'minusone', -100)):
    'Returns the mode of a given pdf in observable RooAbsArg obs.'
    ## Set all parameters constant, remembering their constantness
    saveconst = []
    params = pdf.getParameters(ROOT.RooArgSet(obs))
    itpar = params.createIterator()
    for i in range(params.getSize()):
        p = itpar()
        saveconst.append(p.isConstant())
        p.setConstant(True)
    ## Create the function to be minimized: -pdf
    minuspdf = ROOT.RooPolyVar('minus_' + pdf.GetName(),
                               'Minus ' + pdf.GetTitle(),
                               pdf, ROOT.RooArgList(zero, minusone))
    ## Setup minuit for minization
    minuit = ROOT.RooMinuit(minuspdf)
    ## To be on the safe side.
    minuit.setStrategy(2)
    # minuit.setPrintLevel(-1)
    ## Sample the pdf in 1000 points
    h = pdf.createHistogram(obs.GetName(), 1000)
    ## Find the location of the maximum
    scanmode = h.GetXaxis().GetBinCenter(h.GetMaximumBin()) 
    ## Make sure we have a sensible initial value
    obs.setVal(scanmode)
    ## Find the minimum with minuit    
    minuit.migrad()
    ## Check that the mode from scan is close enough to the mode
    ## from fit
    if math.fabs(obs.getVal() - scanmode) > 2 * h.GetBinWidth(1):
        ## Fit mode is farther than 2 bins form the scan mode.
        ## Use the less-precise, more-robust scan mode.
        obs.setVal(scanmode)
    ## Reset the constantness of the parameters of the pdf and
    itpar.Reset()
    for i in range(params.getSize()):
        itpar().setConstant(saveconst[i])
    return obs.getVal()
## End of pdf_mode
