'''
Phton Energy Scale and Photon Energy Resolution (PHOESPHOER) Fit model 2.
Strategy to build a 2D model for the mmMass and mmgMass as functions
of PhoES and PhoER.

Key formula:
mmgMass(E1)^2 = mmMass^2 + (mmgMass(E2)^2 - mmMass^2) * (1+s1)/(1+s2) (1)

Strategy:
1. Build a 2D KEYS PDF of X = mmMass and T = mmgMassSmear fXT(x, t| r) for
   mmgMass smeared with a given resolution and the nominal scale.

2. Substitute for T using the key formula
   T -> T1 =  
   to obtain a density in X and Y = mmgMassScaled fXY(x,y|s,r).
   fXY(x,y|s,r) = fXT(x,t3(x,y)|s,r).

Note:
This is a simplified version of phosphor model 1.

Jan Veverka, Caltech, 24 January 2012.
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
outputfile = 'out_phosphor2' + name + '_test.root'
cuts = ['mmMass + mmgMass < 190',
        'isFSR',
        'phoGenE > 0',
        #'60 < mmMass & mmMass < 70', 
        ]
rtarget = 'nominal'
starget = 10

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
    global phoScale, phoRes, t
    phoScale = w.factory('phoScale[0,-50,50]')
    phoRes = w.factory('phoRes[1.5,0.01,50]')
    t = w.factory('t[7,1,20]')

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
def plot_xy():
    'Plot fXY(x,y|s,r) 2D plot with data.'
    c1 = canvases.next('xy')
    if c1:
        c1.SetWindowSize(800, 400)
        c1.Divide(2,1)
        c1.cd(1).SetGrid()
    hd = sdata.createHistogram(mmMass, mmgMass, 50, 50, '', 'hxyd')
    hd.SetTitle('Data')
    hd.GetXaxis().SetTitle(mmMass.GetTitle() + ' (GeV)')
    hd.GetYaxis().SetTitle(mmgMass.GetTitle() + ' (GeV)')
    # hd.GetXaxis().SetTitleOffset(1.3)
    hd.GetXaxis().SetRangeUser(40, 90)
    hd.GetYaxis().SetRangeUser(75, 105)
    hd.Draw('cont0')

    if c1:
        c1.cd(2).SetGrid()
    hf = xypdf.createHistogram('hxyf', mmMass, roo.Binning(100, 40, 90),
                               roo.YVar(mmgMass, roo.Binning(100, 75, 105)))
    hf.SetTitle('PDF')
    # hf.GetXaxis().SetTitleOffset(1.3)
    hf.Draw("cont0")
## End of plot_xy().

##------------------------------------------------------------------------------
init()
get_data()

sdata = calibrator.get_smeared_data(starget, rtarget)

## Build the model fXT(x, t | r) for mmMass vs mmgMass(s0)
global xtpdf
# t.setRange(*t1range)
xtpdf = ROOT.RooNDKeysPdf('xtpdf', 'xtpdf', ROOT.RooArgList(mmMass, mmgMass),
                           data, "a", 1.5)
# xtpdf.setNormValueCaching(2)

## Define the substitution
tsubs = w.factory('''expr::tsubs(
    "sqrt({m}*{m} + ({M}*{M} - {m}*{m}) * (1 + {s1})/(1 + 0.01*{s2}))",
    {{ {m}, {M}, {s2} }}
    )'''.format(m = mmMass.GetName(),
                M = mmgMass.GetName(),
                s1 = 0.01 * calibrator.s0.getVal(),
                s2 = phoScale.GetName()))

tfunc = w.factory('''expr::tfunc(
    "({x} < {lo}) * {lo} +
     ({lo} <= {x} && {x} < {hi}) * {x} +
     ({hi} <= {x}) * {hi}",
     {{{x}}}
    )'''.format(lo=mmgMass.getMin(),
                hi=mmgMass.getMax(),
                x=tsubs.GetName()))

## Build the model fXY(x, y| r, s) through the substitution
## t = t(y, s) using the key relation (1)
calibrator.w.loadSnapshot('sr0_mctruth')

cust = ROOT.RooCustomizer(xtpdf, 'trasform')
cust.replaceArg(mmgMass, tfunc)
xypdf = cust.build()
xypdf.SetName('xypdf')
xypdf.SetTitle('xypdf')
# xypdf.addOwnedComponents(ROOT.RooArgSet(tfunc))

# xypdf.fitTo(sdata)
phoScale.setVal(starget)
plot_xy()

mmgMass.setRange('fit', 60, 120)
mmMassLowest = w.factory('mmMassLowest[40]')
mmMassLowest.setConstant(True)
# mmMass.setRange('fit', mmMassLowest, mmgMass)
mmMass.setRange(40, 100)
## xypdf.fitTo(data, roo.Range('fit'), roo.Save(), roo.NumCPU(8),
##             roo.Verbose(True), roo.Timer(True), roo.SumW2Error(True))

canvases.update()

if __name__ == '__main__':
    # main()
    import user
