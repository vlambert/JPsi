'''
Test RooMomentMorph of RooHistPdfs in photon energy resolution. RooHistPdfs are
sampled from parametrized RooKeysPdfs and interpolated to first order.

Jan Veverka, Caltech, 26 January 2012.

'''
   
##- Boilerplate imports --------------------------------------------------------
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases

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
name = 'EB_lowR9_pt25-30'
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

sdata4 = calibrator.get_smeared_data('nominal', 4)
sdata6 = calibrator.get_smeared_data('nominal', 5)
sdata8 = calibrator.get_smeared_data('nominal', 6)

mirror = ROOT.RooKeysPdf.NoMirror

mode4 = w.factory('mode4[91,60,120]')
mode8 = w.factory('mode8[91,60,120]')

seff4 = w.factory('seff4[4,0.1,50]')
seff8 = w.factory('seff8[4,0.1,50]')

pdf4 = ParametrizedKeysPdf('pdf4', 'pdf4', mmgMass, mode4, seff4,
                           sdata4, mirror, 1.5)
pdf8 = ParametrizedKeysPdf('pdf8', 'pdf8', mmgMass, mode8, seff8,
                           sdata8, mirror, 1.5)

mmgMass.setRange(50, 130)

pdf4.fitTo(sdata4, roo.Range(60, 120))
h4 = pdf4.createHistogram('h4', mmgMass, roo.Binning(1000))

pdf8.fitTo(sdata8, roo.Range(60, 120))
h8 = pdf8.createHistogram('h8', mmgMass, roo.Binning(1000))

d4 = ROOT.RooDataHist('d4', 'd4', ROOT.RooArgList(mmgMass), h4)
d8 = ROOT.RooDataHist('d8', 'd8', ROOT.RooArgList(mmgMass), h8)

f4 = ROOT.RooHistPdf('f4', 'f4', ROOT.RooArgSet(mmgMass), d4, 1)
f8 = ROOT.RooHistPdf('f8', 'f8', ROOT.RooArgSet(mmgMass), d8, 1)

w.Import(f4)
w.Import(f8)

fm = w.factory('MomentMorph::fm(phoRes, {mmgMass}, {f4, f8}, {4, 6})')

canvases.next('pdf4')
plot = mmgMass.frame(roo.Range(70, 110))
sdata4.plotOn(plot)
pdf4.shape.plotOn(plot)
f4.plotOn(plot, roo.LineColor(ROOT.kRed), roo.LineStyle(ROOT.kDashed))
plot.Draw()

canvases.next('pdf8')
plot = mmgMass.frame(roo.Range(70, 110))
sdata8.plotOn(plot)
pdf8.shape.plotOn(plot)
f8.plotOn(plot, roo.LineColor(ROOT.kRed), roo.LineStyle(ROOT.kDashed))
plot.Draw()

canvases.next('sdata6')
plot = mmgMass.frame(roo.Range(70, 110))
sdata6.plotOn(plot)
## Limited fit range is crucial.  It doesn't work without it.
fm.fitTo(sdata6, roo.Range(60, 120))
# fm.fitTo(sdata6)
fm.plotOn(plot)
fm.paramOn(plot)
plot.Draw()

canvases.update()

if __name__ == '__main__':
    # main()
    import user
