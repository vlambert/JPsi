'''
Let Ereco1/Egen - s1 = Ereco2/Egen - s2 where Ereco_i/Egen -1 are
random variables and s_i are their modes.

Thest how well is Ereco2 approximated by Ereco1 * (1+s2)/(1+s1).

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
name = 'EE_lowR9_e50-60'
outputfile = 'out_phosphor2' + name + '_test.root'
cuts = ['mmMass + mmgMass < 190',
        'isFSR',
        'phoGenE > 0',
        #'60 < mmMass & mmMass < 70', 
        ]
rtarget = 'nominal'

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
    global mmgMass, mmMass, phoERes, mmgMassPhoGenE, phoGenE, phoE, weight
    mmgMass = w.factory('mmgMass[40, 140]')
    mmgMassPhoGenE = w.factory('mmgMassPhoGenE[0, 200]')
    mmMass = w.factory('mmMass[10, 140]')
    phoERes = w.factory('phoERes[-70, 100]')
    phoGenE = w.factory('phoGenE[0,100]')
    phoE = w.factory('phoE[0,100]')
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
    phoE.SetTitle('phoPt * cosh(phoEta)')
    ## Create a preselected tree
    tree = zchain.CopyTree('&'.join(cuts))
    ## Have to copy aliases by hand
    for a in zchain.GetListOfAliases():
        tree.SetAlias(a.GetName(), a.GetTitle())

    ## Get the nominal dataset
    global data
    data = dataset.get(tree=tree, weight=weight, cuts=cuts,
                       variables=[mmgMass, mmMass, phoERes, mmgMassPhoGenE,
                                  phoGenE, phoE])

    ## Set units and nice titles
    for x, t, u in zip([mmgMass, mmgMassPhoGenE, mmMass, phoERes, phoGenE,
                        phoE],
                       ['m_{#mu#mu#gamma}',
                        'm_{#mu#mu#gamma} with E_{gen}^{#gamma}',
                        'm_{#mu^{+}#mu^{-}}',
                        'E_{reco}^{#gamma}/E_{gen}^{#gamma} - 1',
                        'E_{gen}^{#gamma}',
                        'E_{reco}^{#gamma}'],
                       'GeV GeV GeV % GeV GeV'.split()):
        x.SetTitle(t)
        x.setUnit(u)
    ##-- Get Smeared Data ------------------------------------------------------
    ## Enlarge the range of the observable to get vanishing tails.
    ## range_save = (phoERes.getMin(), phoERes.getMax())
    ## phoERes.setRange(-90, 150)
    global calibrator
    calibrator = MonteCarloCalibrator(data, printlevel = 1)
    ## phoERes.setRange(*range_save)
## End of get_data.

##------------------------------------------------------------------------------
def reduce_and_rename(data, oldname, newname):
    'reduce_and_rename(data, oldname, newname)'
    oldvar = data.get()[oldname]
    oldvar.removeMin()
    oldvar.removeMax()
    ## Drop everything except the oldvar.
    newdata = data.reduce(ROOT.RooArgSet(oldvar))
    ## Define the renaming identity newvar = oldvar
    newfunc = ROOT.RooFormulaVar(newname, newname, oldname,
                                 ROOT.RooArgList(oldvar))
    ## Add a column with the identical values but with the new name
    newvar = newdata.addColumn(newfunc)
    ## New data now contains two columns of identical values, one labeled
    ## with the old name and the other with the new name. Keep only the one
    ## with the new name.
    return newdata.reduce(ROOT.RooArgSet(newvar))        
## End of reduce and rename.

##------------------------------------------------------------------------------
init()
get_data()

sdata = calibrator.get_smeared_data(2, 'nominal')
calibrator.phoEResPdf.fitTo(sdata, roo.Range(-50,50))
s1val = calibrator.s0.getVal()
s2val = calibrator.s.getVal()

mydata = data.reduce(ROOT.RooArgSet(phoGenE, phoE, phoERes))
mydata.merge(reduce_and_rename(sdata, 'phoERes', 'phoERes2'))

canvases.next('phoERes')
myrange = (calibrator.s0.getVal() - 5 * calibrator.r0.getVal(),
           calibrator.s0.getVal() + 5 * calibrator.r0.getVal())
hphoERes = ROOT.TH1F('hphoERes', 'hphoERes', 100, myrange[0], myrange[1])
hphoERes.SetLineColor(ROOT.kCyan - 9)
hphoERes.SetFillColor(ROOT.kCyan - 9)
mydata.tree().Draw('phoERes>>hphoERes')
mydata.tree().Draw('phoERes2', '', 'same')

canvases.next('E2overE1')
mydata.tree().Draw('100*(phoGenE * (1 + 0.01 * phoERes2)/phoE - %f)>>h1' %
                   ((1+0.01*s2val)/(1+0.01*s1val)))
h1 = ROOT.gDirectory.Get('h1')
h1.GetXaxis().SetTitle('E2/E1 - (1+s2)/(1+s1) (%)')
h1.Draw()

canvases.update()

if __name__ == '__main__':
    # main()
    import user
