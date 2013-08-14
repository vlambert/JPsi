'''
2. Build a 1D KEYS PDF of T2 = log(phoE/phoEGen) depending on
   s = phoScale and r = phoRes fT2(t2|s,r). Note that
   phoERes = 100 * (phoE/phoEGen - 1).
   Thus a substitution
   phoERes = 100 * (1 + exp(t2))
   in the phoEResPdf(phoERes|s,r) can be used.

Jan Veverka, Caltech, 18 January 2012
'''

##- Boilerplate imports --------------------------------------------------------

import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf
from JPsi.MuMu.escale.logphoereskeyspdf import LogPhoeresKeysPdf
from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator

##-- Configuration -------------------------------------------------------------
## Selection
name = 'EB_highR9_pt20-25'
cuts = ['mmMass + mmgMass < 190',
        'isFSR',
        'phoGenE > 0',
        ]

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
                lo, hi = tok.replace('pt', '').split('-')
                cuts.append('%s <= phoPt & phoPt < %s' % (lo, hi))
## End of parse_name_to_cuts().

##------------------------------------------------------------------------------
def init():
    'Initialize workspace and common variables and functions.'
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
    global phoScale, phoRes
    phoScale = w.factory('phoScale[0,-50,50]')
    phoRes = w.factory('phoRes[3,0.01,50]')

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
                       ['reconstructed m_{#mu#mu#gamma}',
                        'reconstructed m_{#mu#mu#gamma} with E_{gen}^{#gamma}',
                        'm_{#mu#mu}',
                        'E_{reco}^{#gamma}/E_{gen}^{#gamma} - 1', ],
                       'GeV GeV GeV %'.split()):
        x.SetTitle(t)
        x.setUnit(u)
    ##-- Get Smeared Data ------------------------------------------------------
    ## Enlarge the range of the observable to get vanishing tails.
    range_save = (phoERes.getMin(), phoERes.getMax())
    phoERes.setRange(-90, 150)
    global calibrator
    calibrator = MonteCarloCalibrator(data)
    phoERes.setRange(*range_save)
## End of get_data.

##------------------------------------------------------------------------------
def main():
    sw = ROOT.TStopwatch()
    sw.Start()

    init()
    get_data()

    canvases.update()
    sw.Stop()
    print 'CPU time:', sw.CpuTime(), 's, real time:', sw.RealTime(), 's'
## End of main()    


##------------------------------------------------------------------------------
sw = ROOT.TStopwatch()
sw.Start()

init()
get_data()

phoEResPdf = ParametrizedKeysPdf(
    'phoEResPdf', 'phoEResPdf', phoERes, phoScale, phoRes, data,
    ROOT.RooKeysPdf.NoMirror, 1.5
    )

phoEResPdf.fitTo(data, roo.Range(-50, 50))

canvases.next('phoEResPdf').SetGrid()
plot = phoERes.frame(roo.Range(-10, 10))
data.plotOn(plot)
phoEResPdf.plotOn(plot)
phoEResPdf.paramOn(plot)
plot.Draw()

t = w.factory('t[0,-1,1]')
t.SetTitle('log(E_{reco}^{#gamma}/E_{gen}^{#gamma})')
tfunc = w.factory('expr::tfunc("log(0.01 * phoERes + 1)", {phoERes})')
tfunc.SetName('t')
data.addColumn(tfunc)

## Build the model for log(Ereco/Egen) ft2(t2|r,s)
t2pdf = LogPhoeresKeysPdf('t2pdf', 't2pdf', phoERes, t, phoScale, phoRes, data,
                          rho=1.5)

## Fit nominal data with ft2(t2|r,s)
canvases.next('t2pdf').SetGrid()
t2pdf.fitTo(data, roo.Range(ROOT.TMath.Log(0.5), ROOT.TMath.Log(2.0)))
plot = t.frame(roo.Range(-0.15, 0.15))
data.plotOn(plot)
t2pdf.plotOn(plot)
plot.Draw()
Latex([
    's_{shape}: %.3f %%' % t2pdf.s0val,
    's_{sfit}: %.3f #pm %.3f %%' % (phoScale.getVal(), phoScale.getError()),
    's_{fit} - s_{shape}: %.4f #pm %.4f %%' % (
        phoScale.getVal() - t2pdf.s0val,
        phoScale.getError()
        ),
    'r_{shape}: %.3f %%' % t2pdf.r0val,
    'r_{fit}: %.3f #pm %.3f %%' % (phoRes.getVal(), phoRes.getError()),
    'r_{fit}/r_{shape}: %.4f #pm %.4f' % (
        phoRes.getVal() / t2pdf.r0val,
        phoRes.getError() / t2pdf.r0val),
    ], position=(0.2, 0.75)).draw()

## Fit scale s=-5 smeared data with ft2(t2|r,s)
canvases.next('t2pdf_sm5').SetGrid()
sdata = calibrator.get_smeared_data(-5, 'nominal')
sdata.addColumn(tfunc)
sdata.SetName('sdata_sm5')
plot = t.frame(roo.Range(-0.15, 0.15))
sdata.plotOn(plot)
t2pdf.fitTo(sdata, roo.Range(-0.7, 0.4))
t2pdf.plotOn(plot)
plot.Draw()
Latex([
    's_{target}: %.3f %%' % -5.,
    's_{sfit}: %.3f #pm %.3f %%' % (phoScale.getVal(), phoScale.getError()),
    's_{fit} - s_{target}: %.4f #pm %.4f %%' % (
        phoScale.getVal() - (-5),
        phoScale.getError()
        ),
    'r_{target}: %.3f %%' % calibrator.r0.getVal(),
    'r_{fit}: %.3f #pm %.3f %%' % (phoRes.getVal(), phoRes.getError()),
    'r_{fit}/r_{target}: %.4f #pm %.4f' % (
        phoRes.getVal() / calibrator.r0.getVal(),
        phoRes.getError() / calibrator.r0.getVal()),
    ], position=(0.5, 0.75)).draw()

## Fit resolution r=3 smeared data with ft2(t2|r,s)
starget, rtarget = calibrator.s0.getVal(), 3.
canvases.next('t2pdf_r3').SetGrid()
sdata = calibrator.get_smeared_data(starget, rtarget)
sdata.addColumn(tfunc)
sdata.SetName('sdata_r3')
plot = t.frame(roo.Range(-0.15, 0.15))
sdata.plotOn(plot)
t2pdf.fitTo(sdata, roo.Range(-0.7, 0.4))
t2pdf.plotOn(plot)
plot.Draw()
Latex([
    's_{target}: %.3f %%' % starget,
    's_{sfit}: %.3f #pm %.3f %%' % (phoScale.getVal(), phoScale.getError()),
    's_{fit} - s_{target}: %.4f #pm %.4f %%' % (
        phoScale.getVal() - calibrator.s0.getVal(),
        phoScale.getError()
        ),
    'r_{target}: %.3f %%' % rtarget,
    'r_{fit}: %.3f #pm %.3f %%' % (phoRes.getVal(), phoRes.getError()),
    'r_{fit}/r_{target}: %.4f #pm %.4f' % (
        phoRes.getVal() / rtarget,
        phoRes.getError() / rtarget),
    ], position=(0.2, 0.75)).draw()

canvases.update()
sw.Stop()
print 'CPU time:', sw.CpuTime(), 's, real time:', sw.RealTime(), 's'
 

if __name__ == '__main__':
    # main()
    import user
