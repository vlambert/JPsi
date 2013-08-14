'''
Photon Energy Scale (PhoES) and Photon Energy Resolution (PHOSPHOR) Fit model 3.
Strategy to build a 1D model f(m|s) for the observable m=mmgMass depending
on continuous parameter s=PhoES.

Strategy:
1. Build a 1D KEYS PDF fM(m|s0,r0) for m = mmgMass for the nominal scale
   s=s0 and resolution r=r0 from the simulation.

2. Introduce the dependence on the scale s through the scaling of the
   observable m -> m * (1 - x*(s-s0))
   f(m|s) ~ f(m * (1 - x*(s-s0)|s0)
   where x is the mmgMass sensitivity factor to the photon energy:
   x = (d log m) / (d log E)
     = (1 - mmMass^2 / mmgMass^2) / 2
   with m=mmgMass and E=photon energy.

3. Scan NLL given data as a function os s in the neighborgood of the minimum.

4. Repeat 1-3 for different values of the resolution r0.

5. Construct NLL as a function of the photon energy scale and resolution
   by putting together the various NLL scans.

6. Use migrad to find the minimum of NLL.

Note:
This is a beefed up version of test_mmgMass_photonScale_shift.py

Note:
The MomentMorph seems to be working fine with HistPdf reference shapes, see
massmorphmodel.py v1.2!  (Although there are kinks at the reference values.)
There decide to abandon the likelihood approximation and moving to
transforming in scale and morphing in resolution as a next iteration.

Jan Veverka, Caltech, 25 January 2012.
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

##-- Configuration -------------------------------------------------------------
## Selection
name = 'EB_lowR9_pt15-20'
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
                lo, hi = tok.replace('pt', '').split('-')
                cuts.append('%s <= phoPt & phoPt < %s' % (lo, hi))
    if '_e' in name:
        ## Split the name into tokens.
        for tok in name.split('_'):
            ## Get the token with the pt
            if 'e' == tok[0]:
                lo, hi = tok.replace('e', '').split('-')
                cuts.append('%s <= phoPt * cosh(phoEta)' % lo)
                cuts.append('phoPt * cosh(phoEta) < %s' % hi)
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
init()
get_data()

fitdata = calibrator.get_smeared_data(sfit, rfit)
traindata = calibrator.get_smeared_data(strain, rtrain)

## Get x
traindata.addColumn(xfunc)
xmean.setVal(traindata.mean(traindata.get()['xfunc']))
xmean.setConstant()

mmgMassPdf = ParametrizedKeysPdf('mmgMassPdf', 'mmgMassPdf',
                                 mmgMass, mmgMassPeak,
                                 mmgMassWidth, traindata,
                                 ROOT.RooKeysPdf.NoMirror, 1.5,
                                 forcerange=True)

calibrator.phoEResPdf.fitTo(traindata, roo.Range(-50, 50), roo.Strategy(2),
                            roo.SumW2Error(True))

mmgMass.setRange(50, 130)
mmgMassPdf.fitTo(data, roo.Range(60,120), roo.SumW2Error(True))

phoEResPdf = ParametrizedKeysPdf('phoEResPdf', 'phoEResPdf',
                                 phoERes, phoScaleTrue, phoResTrue, data,
                                 ROOT.RooKeysPdf.NoMirror, 1.5)

phoEResPdf2 = ParametrizedNDKeysPdf('phoEResPdf2', 'phoEResPdf2',
                                    phoERes, phoScaleTrue, phoResTrue, data,
                                    ROOT.RooKeysPdf.NoMirror, 1.5,
                                    forcerange=False)

w.Import(phoEResPdf)
phoEResPdf.fitTo(traindata, roo.Range(-50, 50), roo.Strategy(2),
                 roo.SumW2Error(True))
phoScaleTrue.setConstant(True)
phoResTrue.setConstant(True)
mmgMassSlope = w.factory(
    '''expr::mmgMassSlope("1 - 0.01 * {x}*({s} - {s0})",
                          {{ {s}, {s0}, {x} }})'''.format(
        x=xmean.GetName(), s=phoScale.GetName(), s0=phoScaleTrue.GetName()
        )
    )

mmgMassSlope2 = w.factory(
    'expr::mmgMassSlope2("({a}) + ({b}) * {s}", {{{s}}})'.format(
        a = (mmgMassPdf.shapewidth / mmgMassWidth.getVal() *
             (1 + 0.01 * xmean.getVal() * calibrator.s.getVal())),
        b = - mmgMassPdf.shapewidth / mmgMassWidth.getVal() * 0.01 * xmean.getVal(),
        s = phoScale.GetName(),
        )
    )

mmgMassOffset2 = w.factory('mmgMassOffset2[%f]' % (
    mmgMassPdf.shapemode - mmgMassPdf.shapewidth * mmgMassPeak.getVal() /
    mmgMassWidth.getVal()
    ))

## BEWARE: There seems to be a problem with normalization integral when using
## RooKeysPdf + RooLinearVar which introduces a bias in the scale mesurement.
## Use slow but biasfree FormulaVar instead.
## mmgMassSubs = w.factory('LinearVar::mmgMassSubs(mmgMass, mmgMassSlope, 0)')
## mmgMassSubs2 = w.factory(
##     'LinearVar::mmgMassSubs2(mmgMass, mmgMassSlope2, mmgMassOffset2)'
##     )
mmgMassSubs = w.factory(
    'expr::mmgMassSubs("mmgMass*mmgMassSlope", {mmgMass, mmgMassSlope})'
    )
mmgMassSubs2 = w.factory(
    '''expr::mmgMassSubs2("mmgMass*mmgMassSlope2 + mmgMassOffset2",
                          {mmgMass, mmgMassSlope2, mmgMassOffset2})'''
    )

cust = ROOT.RooCustomizer(mmgMassPdf.shape, 'subs')
cust.replaceArg(mmgMass, mmgMassSubs)
mmgMassModel = cust.build()
mmgMassModel.SetName('mmgMassModel')

cust2 = ROOT.RooCustomizer(mmgMassPdf.shape, 'subs2')
cust2.replaceArg(mmgMass, mmgMassSubs2)
mmgMassModel2 = cust2.build()
mmgMassModel2.SetName('mmgMassModel2')

calibrator.phoEResPdf.fitTo(fitdata, roo.Range(-50, 50))
mmgMassModel.fitTo(fitdata, roo.Range(60, 120), roo.SumW2Error(True),
                   roo.Strategy(2), roo.InitialHesse(True), roo.Minos(True),
                   roo.Timer(True))
res1 = (phoScale.getVal(), phoScale.getError())
mmgMassModel2.fitTo(fitdata, roo.Range(60, 120), roo.SumW2Error(True),
                   roo.Strategy(2), roo.InitialHesse(True), roo.Minos(True),
                   roo.Timer(True))
res2 = (phoScale.getVal(), phoScale.getError())

##------------------------------------------------------------------------------
canvases.next('data')
plot = mmgMass.frame(roo.Range(70, 110))
data.plotOn(plot)
mmgMassPdf.shape.plotOn(plot)
## mmgMass.setRange(50, 130)
## mmgMassPdf.fitTo(data, roo.Range(60,120), roo.SumW2Error(True),
##                  roo.InitialHesse(True), roo.Minos(True), roo.Strategy(2),
##                  roo.Timer(True))
mmgMassPdf.plotOn(plot, roo.LineColor(ROOT.kRed), roo.LineStyle(ROOT.kDashed))
print 'Plotting', plot.GetName(), 'on', canvases.canvases[-1].GetName()
plot.Draw()
Latex(
    ['m(E^{#gamma}_{reco}/E^{#gamma}_{gen}-1): %.3f #pm %.3f %%' % (
        calibrator.s.getVal(), calibrator.s.getError()
        ),
     '#sigma_{eff}(E^{#gamma}_{reco}/E^{#gamma}_{gen}-1): %.3f #pm %.3f %%' % (
         calibrator.r.getVal(), calibrator.r.getError()
         ),
     'm(m_{#mu#mu#gamma})',
     '  shape: %.3f GeV' % mmgMassPdf.shapemode,
     '  fit: %.3f #pm %.3f GeV' % (
         mmgMassPeak.getVal(), mmgMassPeak.getError()
         ),
     '#sigma_{eff}(m_{#mu#mu#gamma})',
     '  shape: %.3f GeV' % mmgMassPdf.shapewidth,
     '  fit: %.3f #pm %.3f GeV' % (
         mmgMassWidth.getVal(), mmgMassWidth.getError()
         )
    ],
    position = (0.2, 0.8)
    ).draw()

##------------------------------------------------------------------------------
canvases.next('fit')
xmean.setConstant(True)
phoScaleTrue.setConstant(True)
mmgMassPeak.setConstant(True)
mmgMassWidth.setConstant(True)
plot = mmgMass.frame(roo.Range(70, 110))
fitdata.plotOn(plot)
mmgMassModel.plotOn(plot)
mmgMassModel2.plotOn(plot, roo.LineColor(ROOT.kRed),
                     roo.LineStyle(ROOT.kDashed))
plot.Draw()
Latex(
    ['m(E^{#gamma}_{reco}/E^{#gamma}_{gen}-1)',
     '  true: %.3f #pm %.3f %%' % (calibrator.s.getVal(),
                                   calibrator.s.getError()),
     '   fit 1: %.3f #pm %.3f %%' % res1,
     '   fit 2: %.3f #pm %.3f %%' % res2,
    ],
    position = (0.2, 0.8)
    ).draw()


##------------------------------------------------------------------------------
canvases.update()

if __name__ == '__main__':
    # main()
    import user
