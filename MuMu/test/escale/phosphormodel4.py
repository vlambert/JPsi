'''
Photon Energy Scale (PhoES) and Photon Energy Resolution (PHOSPHOR) Fit model 4.

Jan Veverka, Caltech, 28 January 2012.
'''
   
##- Boilerplate imports --------------------------------------------------------
import math
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf
from JPsi.MuMu.common.parametrizedndkeyspdf import ParametrizedNDKeysPdf
from JPsi.MuMu.escale.logphoereskeyspdf import LogPhoeresKeysPdf
from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator
from JPsi.MuMu.escale.phosphormodel4 import PhosphorModel4

##-- Configuration -------------------------------------------------------------
## Selection
name = 'EE_highR9_pt12to15'
outputfile = 'out_phosphor2' + name + '_test.root'
cuts = ['mmMass + mmgMass < 190',
        'isFSR',
        'phoGenE > 0',
        #'60 < mmMass & mmMass < 70', 
        ]
strain = 'nominal'
rtrain = 'nominal'

sfit = 'nominal'
rfit = 'nominal'

##------------------------------------------------------------------------------
def parse_name_to_cuts():
    'Parse the name and apply the relevant cuts.'
    if 'EB' in name:
        cuts.append('phoIsEB')
        if 'highR9' in name:
            cuts.append('phoR9 > 0.94')
        elif 'lowR9' in name:
            cuts.append('phoR9 < 0.94')
    elif 'EE' in name:
        cuts.append('!phoIsEB')
        if 'highR9' in name:
            cuts.append('phoR9 > 0.95')
        elif 'lowR9' in name:
            cuts.append('phoR9 < 0.95')

    if 'pt' in name:
        ## Split the name into tokens.
        for tok in name.split('_'):
            ## Get the token with the pt
            if 'pt' in tok:
                if '-' in tok:
                    separator = '-'
                elif 'to' in tok:
                    separator = 'to'
                else:
                    raise RuntimeError, 'Error parsing %s in %s!' % (tok, name)
                lo, hi = tok.replace('pt', '').split(separator)
                cuts.append('%s <= phoPt & phoPt < %s' % (lo, hi))
## End of parse_name_to_cuts().

##------------------------------------------------------------------------------
def init():
    'Initialize workspace and common variables and functions.'
    global plots
    plots = []
    parse_name_to_cuts()
    ## Create the default workspace
    global w
    w = ROOT.RooWorkspace('w')

    ## Define data observables. 
    global mmgMass, mmMass, phoERes, mmgMassPhoGenE, weight
    mmgMass = w.factory('mmgMass[40, 140]')
    mmgMassPhoGenE = w.factory('mmgMassPhoGenE[0, 200]')
    mmMass = w.factory('mmMass[10, 140]')
    phoERes = w.factory('phoERes[-70, 100]')
    weight = w.factory('weight[1]')

    ## Define model parameters.
    global phoScale, phoRes, phoScaleTrue, phoResTrue
    phoScale = w.factory('phoScale[0,-50,50]')
    phoRes = w.factory('phoRes[1.5,0.01,50]')
    phoScaleTrue = w.factory('phoScaleTrue[0,-50,50]')
    phoResTrue = w.factory('phoResTrue[1.5,0.01,50]')

    ## Set units.
    for x, u in zip([phoScale, phoRes],
                    '% %'.split()):
        x.setUnit(u)

    ## Prep for storing fit results in the workspace.
    global phoScaleTarget, phoResTarget, params
    phoScaleTarget = w.factory('phoScaleTarget[0,-50,50]')
    phoResTarget = w.factory('phoResTarget[5,0.01,50]')
    params = ROOT.RooArgSet(phoScaleTarget, phoResTarget)
    w.defineSet('params', params)

    global xfunc
    xfunc = w.factory('''FormulaVar::xfunc(
        "0.5 * (1 - mmMass^2 / mmgMass^2)",
        {mmMass, mmgMass}
        )''')

    global xmean
    xmean = w.factory('xmean[0.1, 0, 1]')

    global mmgMassPeak, mmgMassWidth
    mmgMassPeak = w.factory('mmgMassPeak[91.2, 0, 200]')
    mmgMassWidth = w.factory('mmgMassWidth[5, 0.1, 200]')
    
## End of init().


##------------------------------------------------------------------------------
def get_data(zchain = getChains('v11')['z']):
    'Get the nominal data that is used for smearing.'
    ## The TFormula expression defining the data is given in the titles.
    weight.SetTitle('pileup.weight')
    phoERes.SetTitle('100 * phoERes')
    mmgMassPhoGenE.SetTitle('threeBodyMass(mu1Pt, mu1Eta, mu1Phi, 0.106, '
                            '              mu2Pt, mu2Eta, mu2Phi, 0.106, '
                            '              phoGenE * phoPt / phoE, '
                            '                     phoEta, phoPhi, 0)')
    ## Create a preselected tree
    tree = zchain.CopyTree('&'.join(cuts))
    ## Have to copy aliases by hand
    for a in zchain.GetListOfAliases():
        tree.SetAlias(a.GetName(), a.GetTitle())

    ## Get the nominal dataset
    global data
    data = dataset.get(tree=tree, weight=weight, cuts=cuts,
                       variables=[mmgMass, mmMass, phoERes, mmgMassPhoGenE])

    ## Set units and nice titles
    for x, t, u in zip([mmgMass, mmgMassPhoGenE, mmMass, phoERes],
                       ['m_{#mu#mu#gamma}',
                        'm_{#mu#mu#gamma} with E_{gen}^{#gamma}',
                        'm_{#mu^{+}#mu^{-}}',
                        'E_{reco}^{#gamma}/E_{gen}^{#gamma} - 1', ],
                       'GeV GeV GeV %'.split()):
        x.SetTitle(t)
        x.setUnit(u)
    ##-- Get Smeared Data ------------------------------------------------------
    global calibrator
    calibrator = MonteCarloCalibrator(data, 1)
## End of get_data.

##------------------------------------------------------------------------------
def get_confint(x, cl=5):
    if x.hasAsymError():
        return (max(x.getVal() + cl * x.getErrorLo(), x.getMin()),
                min(x.getVal() + cl * x.getErrorHi(), x.getMax()))
    else:
        return (max(x.getVal() - cl * x.getError(), x.getMin()),
                min(x.getVal() + cl * x.getError(), x.getMax()))
## End of get_confint().

##------------------------------------------------------------------------------
init()
get_data()

## Cheet a little to spead things up
phoScale.setVal(calibrator.s0.getVal())
phoRes.setVal(calibrator.r0.getVal())

pmlist = []

phortargets = [0.5, calibrator.r0.getVal(), 5, 15]
phortargets.sort()
pm = PhosphorModel4('pm0', 'pm0', mmgMass, phoScale, phoRes, data, w,
                    'nominal', phortargets)

setting = ROOT.Long(ROOT.RooMomentMorph.Linear)
pm.setMode(setting)

pmlist.append(pm)
## phoScale = pm.w.var('phoScale')
## phoRes = pm.w.var('phoRes')

pm.w.Print()

mmgMass.setRange(60, 120)

## phoScale.setError(0.2)
## phoRes.setError(0.5)

fitdata = calibrator.get_smeared_data(sfit, rfit, 'fitdata', 'title', True)

fres = pm.fitTo(fitdata, roo.Range(60, 120),
                roo.Strategy(2),
                roo.Minos(),
                roo.NumCPU(8), roo.Save(), roo.Timer())

canvases.next('mwidth_vs_phor')
graph = pm.make_mctrue_graph()
graph.GetXaxis().SetTitle('photon energy resolution (%)')
graph.GetYaxis().SetTitle('#sigma_{eff}(m_{#mu^{+}#mu^{-}#gamma})')
graph.SetTitle(name)
graph.Draw('ap')

canvases.next('fit')
plot = mmgMass.frame(roo.Range(70, 110))
fitdata.plotOn(plot)
pm.plotOn(plot)
# pm.paramOn(plot)
plot.Draw()
Latex(
    [
        's_{true}: %.3f #pm %.3f %%' % (calibrator.s.getVal(),
                                        calibrator.s.getError()),
        's_{fit}: %.3f ^{+%.3f}_{%.3f} %%' % (phoScale.getVal(),
                                              phoScale.getErrorHi(),
                                              phoScale.getErrorLo()),
        '',
        'r_{true}: %.3f #pm %.3f %%' % (calibrator.r.getVal(),
                                        calibrator.r.getError()),
        'r_{fit}: %.3f ^{+%.3f}_{%.3f} %%' % (phoRes.getVal(),
                                              phoRes.getErrorHi(),
                                              phoRes.getErrorLo()),
        ],
    position=(0.2, 0.8)
    ).draw()


nll = pm.createNLL(fitdata, roo.Range(60, 120))

canvases.next('nll_vs_phos').SetGrid()
plot = pm.w.var('phoScale').frame(roo.Range(*get_confint(phoScale)))
nll.plotOn(plot, roo.ShiftToZero())
plot.GetYaxis().SetRangeUser(0, 10)
plot.Draw()

canvases.next('nll_vs_phor').SetGrid()
plot = pm.w.var('phoRes').frame(roo.Range(*get_confint(phoRes)))
nll.plotOn(plot, roo.ShiftToZero())
# plot.GetYaxis().SetRangeUser(0, 10)
plot.Draw()

canvases.next('nll_vs_phor').SetGrid()
plot = pm.w.var('phoRes').frame(roo.Range(*get_confint(phoRes,1.5)))
nll.plotOn(plot, roo.ShiftToZero())
# plot.GetYaxis().SetRangeUser(0, 10)
plot.Draw()

##------------------------------------------------------------------------------
canvases.update()

if __name__ == '__main__':
    # main()
    import user
