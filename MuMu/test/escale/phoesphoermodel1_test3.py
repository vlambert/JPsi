'''
Build 1D model fT(t|s,r) for log(mmgMass^2 - mmMass^2) as functions of
PhoES and PhoER through a confolution in t
fT(t|s,r) = fT1(t) * fT2(t|s,r).
Test that it closes on smeared MC.

Jan Veverka, Caltech, 18 January 2012
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
from JPsi.MuMu.escale.logphoereskeyspdf import LogPhoeresKeysPdf
from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator

##-- Configuration -------------------------------------------------------------
## Selection
name = 'EB_highR9_e30-40'
cuts = ['mmMass + mmgMass < 190',
        'isFSR',
        'phoGenE > 0',
        '60 < mmMass & mmMass < 70', 
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
sw = ROOT.TStopwatch()
sw.Start()

init()
get_data()

## Define variables
t = w.factory('t[7,5,10]')

## Get t1 data
t1func = w.factory(
    'expr::t1func("log(mmgMassPhoGenE^2 - mmMass^2)", {mmgMassPhoGenE, mmMass})'
    )
t1func.SetName('t')
data.addColumn(t1func)
t1data = data.reduce(ROOT.RooArgSet(t))
t1func.SetName('t1func')
data = data.reduce(ROOT.RooArgSet(mmgMass, mmMass, phoERes, mmgMassPhoGenE))

## Get t2 data
t.setRange(-1, 1)
t2func = w.factory(
    'expr::t2func("log(0.01 * phoERes + 1)", {phoERes})'
    )
t2func.SetName('t')
data.addColumn(t2func)
t2func.SetName('t2func')
t2data = data.reduce(ROOT.RooArgSet(t))
data = data.reduce(ROOT.RooArgSet(mmgMass, mmMass, phoERes, mmgMassPhoGenE))

## Get t data
t.setRange(5, 10)
tfunc = w.factory('expr::tfunc("log(mmgMass^2 - mmMass^2)", {mmgMass, mmMass})')
tfunc.SetName('t')
data.addColumn(tfunc)
tfunc.SetName('tfunc')
tdata = data.reduce(ROOT.RooArgSet(t))
data = data.reduce(ROOT.RooArgSet(mmgMass, mmMass, phoERes, mmgMassPhoGenE))

## Get t1 v t2
t.setRange(5, 10)
t1 = w.factory('t1[5,10]')
t2 = w.factory('t2[-1,1]')
t1func.SetName('t1')
data.addColumn(t1func)
t1func.SetName('t1func')
t2func.SetName('t2')
data.addColumn(t2func)
t2func.SetName('t2func')
t1vt2data = data.reduce(ROOT.RooArgSet(t1, t2))
data = data.reduce(ROOT.RooArgSet(mmgMass, mmMass, phoERes, mmgMassPhoGenE))

## Get t1+t2 vs t data
t.setRange(5, 10)
t1xt2 = w.factory('t1xt2[5,10]')
t1xt2func = w.factory('expr::t1xt2func("t1func + t2func", {t1func, t2func})')
t1xt2func.SetName('t1xt2')
data.addColumn(t1xt2func)
t1xt2func.SetName('t1xt2func')
tfunc.SetName('t')
data.addColumn(tfunc)
tfunc.SetName('tfunc')
t1xt2vtdata = data.reduce(ROOT.RooArgSet(t, t1xt2))
data = data.reduce(ROOT.RooArgSet(mmgMass, mmMass, phoERes, mmgMassPhoGenE))

## Build the model fT1(t1) for log(mmgMassPhoGenE^2 - mmMass^2)
t.setRange(5, 10)
# t.setVal(8.3)
nomirror = ROOT.RooKeysPdf.NoMirror
## t1pdf = ROOT.RooKeysPdf('t1pdf', 't1pdf', t, t1data, nomirror, 1.5)
t1mode = w.factory('t1mode[8.3,5,10]')
t1width = w.factory('t1width[0.2,0.01,5]')
t1pdf = ParametrizedKeysPdf('t1pdf', 't1pdf', t, t1mode, t1width, t1data,
                            nomirror, 1.5)
t1pdf.fitTo(t1data)
t1mode.setConstant(True)
t1width.setConstant(True)
## TODO: use parametrized KEYS PDF with forced ranges and fit it to data.

## Build the model fT2(t2|s,r) for log(Ereco/Egen) ft2(t2|r,s)
t.setRange(-1, 1)
t.setVal(0)
t2pdf = LogPhoeresKeysPdf('t2pdf', 't2pdf', phoERes, t, phoScale, phoRes, data,
                          rho=1.5)

## Build the model for fT(t|s,r) = fT1(t1) * fT2(t2|s,r)
t.setRange(5, 10)
t.setBins(1000, "cache")
tpdf = ROOT.RooFFTConvPdf('tpdf', 'tpdf', t, t1pdf, t2pdf)
tpdf.setBufferFraction(0.1)

## Plot fT1(t1) with training data.
canvases.next('t1pdf').SetGrid()
t.setRange(5, 10)
t.SetTitle('log(m_{#mu#mu#gamma,E_{gen}^{#gamma}}^{2} - m_{#mu#mu}^{2})')
plot = t.frame(roo.Range(6, 9))
t1data.plotOn(plot)
t1pdf.shape.plotOn(plot)
t1pdf.plotOn(plot, roo.LineColor(ROOT.kRed), roo.LineStyle(ROOT.kDashed))
plot.Draw()
Latex([
    's_{shape}: %.3f' % t1pdf.shapemode,
    's_{fit}: %.3f #pm %.3f' % (t1mode.getVal(),
                                   t1mode.getError()),
    's_{fit} - s_{shape}: %.4f #pm %.4f' % (
        t1mode.getVal() - t1pdf.shapemode,
        t1mode.getError()
        ),
    'r_{shape}: %.3f' % t1pdf.shapewidth,
    'r_{fit}: %.3f #pm %.3f' % (t1width.getVal(), t1width.getError()),
    'r_{fit} - r_{shape}: %.4f #pm %.4f' % (
        t1width.getVal() - t1pdf.shapewidth,
        t1width.getError()),
    'r_{fit}/r_{shape}: %.4f #pm %.4f' % (
        t1width.getVal() / t1pdf.shapewidth,
        t1width.getError() / t1pdf.shapewidth),
    ], position=(0.2, 0.8)).draw()

## Plot fT2(t2|s,r) fitted to training data.
canvases.next('t2pdf').SetGrid()
t.setRange(-1, 1)
t.setVal(0)
t.SetTitle('log(E_{reco}^{#gamma}/E_{gen}^{#gamma})')
phoScale.setVal(t2pdf.s0val)
phoRes.setVal(t2pdf.r0val)
t2pdf.fitTo(t2data, roo.Range(ROOT.TMath.Log(0.5), ROOT.TMath.Log(1.5)))
plot = t.frame(roo.Range(-0.3, 0.3))
t2data.plotOn(plot)
t2pdf.plotOn(plot)
plot.Draw()
Latex([
    's_{shape}: %.3f %%' % t2pdf.s0val,
    's_{fit}: %.3f #pm %.3f %%' % (phoScale.getVal(), phoScale.getError()),
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

## Plot fT(t|s,r) fitted to data
canvases.next('tpdf').SetGrid()
t.setRange(5, 10)
t.SetTitle('log(m_{#mu#mu#gamma}^{2} - m_{#mu#mu}^{2})')
tpdf.fitTo(tdata, roo.Range(5.5, 9.5))
plot = t.frame(roo.Range(6, 9))
tdata.plotOn(plot)
tpdf.plotOn(plot)
tpdf.paramOn(plot)
plot.Draw()

## Plot t2 v t1 data
canvases.next('t1vt2').SetGrid()
t1.SetTitle('log(m_{#mu#mu#gamma,E_{gen}^{#gamma}}^{2} - m_{#mu#mu}^{2})')
t2.SetTitle('log(E_{reco}^{#gamma}/E_{gen}^{#gamma})')
ht1vt2 = t1vt2data.createHistogram(t2, t1, 100, 100, '', 'ht1vt2')
ht1vt2.GetXaxis().SetTitle(t2.GetTitle())
ht1vt2.GetYaxis().SetTitle(t1.GetTitle())
xarange = (t2pdf.s0val - 4 * t2pdf.r0val, t2pdf.s0val + 4 * t2pdf.r0val)
xarange = [math.log(1 + 0.01 * x) for x in xarange]
ht1vt2.GetXaxis().SetRangeUser(*xarange)
ht1vt2.GetYaxis().SetRangeUser(t1pdf.shapemode - 4 * t1pdf.shapewidth,
                               t1pdf.shapemode + 4 * t1pdf.shapewidth)
ht1vt2.Draw('cont0')
Latex([
    '#rho: %.3f' % t1vt2data.correlation(t1, t2),
    ], position=(0.2, 0.75)).draw()

## Plot t1+t2 vs t data
canvases.next('tvt1xt2').SetGrid()
t1xt2.SetTitle(' + '.join([
    'log(m_{#mu#mu#gamma,E_{gen}^{#gamma}}^{2} - m_{#mu#mu}^{2})',
    'log(E_{reco}^{#gamma}/E_{gen}^{#gamma})'
    ]))
t.SetTitle('log(m_{#mu#mu#gamma}^{2} - m_{#mu#mu}^{2})')
htvt = t1xt2vtdata.createHistogram(t1xt2, t, 100, 100, '', 'htvt')
htvt.GetXaxis().SetTitle(t1xt2.GetTitle())
htvt.GetYaxis().SetTitle(t.GetTitle())
htvt.GetXaxis().SetRangeUser(t1pdf.shapemode - 4 * t1pdf.shapewidth,
                             t1pdf.shapemode + 4 * t1pdf.shapewidth)
htvt.GetYaxis().SetRangeUser(t1pdf.shapemode - 4 * t1pdf.shapewidth,
                             t1pdf.shapemode + 4 * t1pdf.shapewidth)
htvt.Draw('cont0')
Latex([
    '#rho: %.3f' % t1xt2vtdata.correlation(t1xt2, t),
    ], position=(0.2, 0.75)).draw()

canvases.update()
sw.Stop()
print 'CPU time:', sw.CpuTime(), 's, real time:', sw.RealTime(), 's'
 

if __name__ == '__main__':
    # main()
    import user
