##- Boilerplate imports --------------------------------------------------------

import array
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf
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

    ## Define the parametrization of mass width and peak as quadratic
    ## functions of photon energy scale and resolution
    ## Loop over coefficients of polynomial in phoScale
    for i in range(3):
        w.factory('''PolyVar::ms_poly_func_{i}(
            phoRes,
            {{ms_poly_coeff_{i}0[0,-10,10],
              ms_poly_coeff_{i}1[0,-10,10],
              ms_poly_coeff_{i}2[0,-10,10]}})'''.format(i=i))
        w.factory('''PolyVar::mr_poly_func_{i}(
            phoRes,
            {{mr_poly_coeff_{i}0[0,-10,10],
              mr_poly_coeff_{i}1[0,-10,10],
              mr_poly_coeff_{i}2[0,-10,10]}})'''.format(i=i))
    ## End of loop over coefficients of polynoial in phoScale

    massScaleFunc = w.factory('''PolyVar::massScaleFunc(
        phoScale, {ms_poly_func_0, ms_poly_func_1, ms_poly_func_2}
        )''')

    massResFunc = w.factory('''PolyVar::massResFunc(
        phoScale, {mr_poly_func_0, mr_poly_func_1, mr_poly_func_2}
        )''')

    ## Get some very crude initial values for the quadratic functions.
    ## massScale = 0.2 * phoScale
    ## massRes = 3 + 0.1 * phoRes
    w.var('ms_poly_coeff_10').setVal(0.2)    
    w.var('mr_poly_coeff_00').setVal(3)
    w.var('mr_poly_coeff_01').setVal(0.1)
    
    # % <-> units conversions
    mZ = w.factory('mZ[91.2]')
    massPeak = w.factory('''FormulaVar::massPeak(
        "mZ*(0.01*massScaleFunc + 1)",
        {massScaleFunc, mZ})
        ''')
    massWidth = w.factory('''FormulaVar::massWidth(
        "0.01 * massPeak * massResFunc",
        {massResFunc, massPeak}
        )''')
    
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
    global calibrator
    calibrator = MonteCarloCalibrator(data)
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

sw = ROOT.TStopwatch()
sw.Start()
 

if __name__ == '__main__':
    # main()
    import user
