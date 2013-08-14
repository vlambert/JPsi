#!/usr/bin/env python
'''
Smear photon energies and extract the dependence of the position and
width of the mmg mass peak on the photon scale and resolution.
Store results in a workspace in a root file.
'''

## NOTE: PHOton Scale and PHOton Resolution Fit = PhoSPhoR Fit

##------------------------------------------------------------------------------
## Boilerplate imports.

import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf
from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator

## Here starts the meat.

##-- Configuration -------------------------------------------------------------
## Target photon scale and resolution in %
## Scale scan
## stargets = [-25 + 2.5*i for i in range(21)][19:]
## rtargets = [1.5] * len(stargets)
## outputfilename = 'massmorph_scalescan_test.root'

## Resolution scan
## rtargets = [0.05, 0.2] + [0.5 + 0.5 * i for i in range(20)]
## stargets = [0] * len(rtargets)
## outputfilename = 'massmorph_resscan_EB_highR9_phoPt20-25.root'


stargets = [-1, 0, 1,]
rtargets = [1.487] * len(stargets)
outputfilename = 'massmorph_scalescan_test.root'

## Selection
cuts = ['phoIsEB',
        'phoR9 > 0.94',
        '10 <= phoPt & phoPt < 12',
        'mmMass + mmgMass < 190',
        'isFSR',
        'phoGenE > 0',
        ]

##------------------------------------------------------------------------------
def init():
    'Initialize workspace and common variables and functions.'
    ## Create the default workspace
    global w
    w = ROOT.RooWorkspace('w')

    ## Define data observables. 
    global mmgMass, mmMass, phoERes, weight
    mmgMass = w.factory('mmgMass[40, 140]')
    mmMass = w.factory('mmMass[10, 140]')
    phoERes = w.factory('phoERes[-70, 100]')
    weight = w.factory('weight[1]')

    ## Define model parameters.
    global phoScale, phoRes, massScale, massRes, mZ, massPeak, massWidth
    phoScale = w.factory('phoScale[0,-50,50]')
    phoRes = w.factory('phoRes[5,0.01,50]')
    massScale = w.factory('massScale[0, -50, 50]')
    massRes = w.factory('massRes[5, 0.01, 50]')
    mZ = w.factory('mZ[91.2]')
    # % <-> units conversions
    # massPeakSlope = w.factory('LinearVar::massPeakSlope(mZ, 0.01, 0)')
    massPeak = w.factory('''FormulaVar::massPeak("mZ*(0.01*massScale + 1)",
                                                 {massScale, mZ})''')
    massWidth = w.factory('''FormulaVar::massWidth("0.01 * massPeak * massRes",
                                                   {massRes, massPeak})''')

    ## Set units.
    for x, u in zip([phoScale, phoRes, massScale, massRes, mZ,
                     massPeak, massWidth],
                    '% % % % GeV GeV GeV'.split()):
        x.setUnit(u)

    ## Prep for storing fit results in the workspace.
    global phoScaleTarget, phoResTarget, params
    phoScaleTarget = w.factory('phoScaleTarget[0,-50,50]')
    phoResTarget = w.factory('phoResTarget[5,0.01,50]')
    params = ROOT.RooArgSet(phoScaleTarget, phoResTarget,
                            phoScale, phoRes,
                            massScale, massRes)
    w.defineSet('params', params)
## End of init().
    
##------------------------------------------------------------------------------
def get_data(zchain = getChains('v11')['z']):
    'Get the nominal data that is used for smearing.'
    global data, calibrator
    ## The TFormula expression defining the data is given in the titles.
    weight.SetTitle('pileup.weight')
    phoERes.SetTitle('100 * phoERes')

    ## Create a preselected tree
    tree = zchain.CopyTree('&'.join(cuts))
    ## Have to copy aliases by hand
    for a in zchain.GetListOfAliases():
        tree.SetAlias(a.GetName(), a.GetTitle())

    ## Get the nominal dataset
    data = dataset.get(tree=tree, weight=weight, cuts=cuts,
                       variables=[mmgMass, mmMass, phoERes,])

    ## Set units and nice titles
    for x, t, u in zip([mmgMass, mmMass, phoERes],
                       ['m_{#mu#mu#gamma}', 'm_{#mu#mu}',
                        'E_{reco}^{#gamma}/E_{gen}^{#gamma} - 1', ],
                       'GeV GeV %'.split()):
        x.SetTitle(t)
        x.setUnit(u)
    ##-- Get Smeared Data ------------------------------------------------------
    ## Enlarge the range of the observable to get vanishing tails.
    range_save = (phoERes.getMin(), phoERes.getMax())
    phoERes.setRange(-90, 150)
    calibrator = MonteCarloCalibrator(data)
    phoERes.setRange(*range_save)
## End of get_data.

##------------------------------------------------------------------------------
def loop_over_smearings():
    "Extract scale and resolution for mass and energy."
    for i, (s, r) in enumerate(zip(stargets, rtargets)):
        ## Get the smeared data.
        phoScaleTarget.setVal(s)
        phoResTarget.setVal(r)
        sdata = calibrator.get_smeared_data(s, r)
        ## Save the smeared data in the workspace.
        sdata.SetName('sdata_%d' % i)
        sdata.SetTitle('smeared mmg data %d' % i)
        w.Import(sdata)
        ## Build the energy and mass models for each smearing since the
        ## shapes may have changed.
        ## Set initial value for the mode calculation of the phoERes shape.
        phoERes.setVal(s)
        ## Define model for the photon energy smearing function Ereco/Etrue - 1.
        phoEResPdf = ParametrizedKeysPdf('phoEResPdf_%d' % i,
                                         'phoEResPdf_%d' % i, phoERes,
                                         phoScale, phoRes, sdata,
                                         ROOT.RooKeysPdf.NoMirror, 1.5)
        ## Set initial value for the mode calculation of the mmgMass shape.
        mmgMass.setVal(91.2 + 0.2 * s)
        ## Define the mmg mass model.
        mmgMassPdf = ParametrizedKeysPdf('mmgMassPdf_%d' % i,
                                         'mmgMassPdf_%d' %i, mmgMass,
                                         massPeak, massWidth, sdata,
                                         ROOT.RooKeysPdf.NoMirror, 1.5)
        ## Guess the right values of the fit parameters.
        phoScale.setVal(phoEResPdf.shapemode)
        phoRes.setVal(phoEResPdf.shapewidth)
        massScale.setVal(100 * (mmgMassPdf.shapemode / mZ.getVal() - 1))
        massRes.setVal(100 * mmgMassPdf.shapewidth / mmgMassPdf.shapemode)
        ## Fit the models.
        phoFit = phoEResPdf.fitTo(sdata,
                                  # roo.Range(-50, 50),
                                  roo.Range(s - 5*r, s + 5*r),
                                  # roo.PrintLevel(-1),
                                  roo.Save())
        massFit = mmgMassPdf.fitTo(sdata,
                                   roo.Range(60, 120),
                                   # roo.PrintLevel(-1),
                                   roo.Save())
        ## Store results in the workspace.
        w.Import(phoEResPdf)
        w.Import(mmgMassPdf)
        w.Import(phoEResPdf.shape)
        w.Import(mmgMassPdf.shape)
        w.Import(phoFit)
        w.Import(massFit)
        w.saveSnapshot('smear_%d' % i, params, True)
## End of loop_over_smearings().


##-- Make Plots ----------------------------------------------------------------
def plot_training_phoeres_with_shape_and_fit():
    """Plot the nominal MC photon energy smearing overlayed with the pdf shape
    and fit."""
    canvases.next('TrainingPhoEResWithShapeAndFit')
    plot = phoERes.frame(roo.Range(-7.5, 5))
    plot.SetTitle("Photon energy smearing overlayed with PDF shape (blue) "
                  "and it's parametrized fit (dashed red)")
    data.plotOn(plot)
    ## Define model for the photon energy smearing function Ereco/Etrue - 1.
    phoEResPdf = ParametrizedKeysPdf('phoEResPdf', 'phoEResPdf', phoERes,
                                     phoScale, phoRes, data,
                                     ROOT.RooKeysPdf.NoMirror, 1.5)
    ## PDF shape
    phoEResPdf.shape.plotOn(plot)
    ## Parametrized fit of the PDF shape
    phoEResPdf.fitTo(data, roo.Range(-50, 50), roo.PrintLevel(-1))
    phoEResPdf.plotOn(plot, roo.LineColor(ROOT.kRed),
                      roo.LineStyle(ROOT.kDashed))
    plot.Draw()
    Latex([
        's_{shape}: %.3f %%' % phoEResPdf.shapemode,
        's_{fit}: %.3f #pm %.3f %%' % (phoScale.getVal(),
                                       phoScale.getError()),
        's_{fit} - s_{shape}: %.4f #pm %.4f %%' % (
            phoScale.getVal() - phoEResPdf.shapemode,
            phoScale.getError()
            ),
        'r_{shape}: %.3f %%' % phoEResPdf.shapewidth,
        'r_{fit}: %.3f #pm %.3f %%' % (phoRes.getVal(), phoRes.getError()),
        'r_{fit} - r_{shape}: %.4f #pm %.4f %%' % (
            phoRes.getVal() - phoEResPdf.shapewidth,
            phoRes.getError()),
        'r_{fit}/r_{shape}: %.4f #pm %.4f' % (
            phoRes.getVal() / phoEResPdf.shapewidth,
            phoRes.getError() / phoEResPdf.shapewidth),
        ], position=(0.2, 0.8)).draw()
## end of plot_training_phoeres_with_shape_and_fit

def plot_nominal_mmgmass_with_shape_and_fit():
    """Plot the nominal MC mmg mass data overlayed with the pdf shape and
    fit."""
    canvases.next('NominalMmgMassWithShapeAndFit')
    plot = mmgMass.frame(roo.Range(75, 105))
    plot.SetTitle("m(#mu#mu#gamma) overlayed with PDF shape (blue) "
                  "and it's parametrized fit (dashed red)")
    data.plotOn(plot)
    ## Define the mmg mass model.
    mmgMassPdf = ParametrizedKeysPdf('mmgMassPdf', 'mmgMassPdf', mmgMass,
                                     massPeak, massWidth, data,
                                     ROOT.RooKeysPdf.NoMirror, 1.5)
    ## PDF shape
    mmgMassPdf.shape.plotOn(plot)
    ## Parametrized fit of the PDF shape
    mmgMassPdf.fitTo(data, roo.Range(60, 120), roo.PrintLevel(-1))
    mmgMassPdf.plotOn(plot, roo.LineColor(ROOT.kRed),
                      roo.LineStyle(ROOT.kDashed))
    plot.Draw()
    sshape = 100 * (mmgMassPdf.shapemode / mZ.getVal() - 1)
    rshape = 100 * mmgMassPdf.shapewidth / mmgMassPdf.shapemode
    Latex([
        's_{shape}: %.3f %%' % sshape,
        's_{fit}: %.3f #pm %.3f %%' % (massScale.getVal(),
                                       massScale.getError()),
        's_{fit} - s_{shape}: %.4f #pm %.4f %%' % (
            massScale.getVal() - sshape,
            massScale.getError()
            ),
        'r_{shape}: %.3f %%' % rshape,
        'r_{fit}: %.3f #pm %.3f %%' % (
            massRes.getVal(), massRes.getError()
            ),
        'r_{fit} - r_{shape}: %.4f #pm %.4f %%' % (
            massRes.getVal() - rshape,
            massRes.getError()),
        'r_{fit}/r_{shape}: %.4f #pm %.4f' % (
            massRes.getVal() / rshape,
            massRes.getError() / rshape),
        ], position=(0.2, 0.8)).draw()
## end of plot_nominal_mmgmass_with_shape_and_fit

##------------------------------------------------------------------------------
def main():
    init()
    get_data()
    ## plot_training_phoeres_with_shape_and_fit()
    ## plot_nominal_mmgmass_with_shape_and_fit()
    ## canvases.update()
    loop_over_smearings()
    w.writeToFile(outputfilename)
## End of main

##-- Footer boilerplate --------------------------------------------------------
if __name__ == '__main__':
    main()
    import user
