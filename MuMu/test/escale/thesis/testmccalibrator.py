'''
Given a selection and photon scale and resolution,
fetch a RooDataSet of mmgMass MC data smeared such that the photon detector
responce Ereco/Etrue has the same shape as the nominal MC but has the given
scale and resolution.
'''

import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf
from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator

## Target photon energy scale and resolution of the smeared data.
targets = 0
targetr = 2.0

##------------------------------------------------------------------------------
## Here starts the meat.

## Selection
cuts = ['phoIsEB',
        'phoR9 > 0.94',
        '20 < phoPt & phoPt < 25',
        'mmMass + mmgMass < 190',
        'isFSR',
        'phoGenE > 0',
        ]
cutlabels = [
    'reco E_{T}^{#gamma} #in [20, 25] GeV',
    'm_{#mu#mu} + m_{#mu#mu#gamma} < 190 GeV',
    'Barrel',
    'R_{9} > 0.94',
    'FSR'
    ]

## Create the default workspace
w = ROOT.RooWorkspace('w')

## Define data variables 
mmgMass = w.factory('mmgMass[40, 140]')
mmMass = w.factory('mmMass[10, 140]')
phoERes = w.factory('phoERes[-70, 100]')
mmgMassPeak = w.factory('mmgMassPeak[91.2, 0, 200]')
mmgMassWidth = w.factory('mmgMassWidth[5, 0.1, 200]')
mmgMassSmearPeak = w.factory('mmgMassSmearPeak[91.2, 0, 200]')
mmgMassSmearWidth = w.factory('mmgMassSmearWidth[5, 0.1, 200]')
phoScale = w.factory('phoScale[0,-50,50]')
phoRes = w.factory('phoRes[5,0.01,50]')
weight = w.factory('weight[1]')

## The TFormula expression defining the data is given in the titles.
weight.SetTitle('pileup.weight')
phoERes.SetTitle('100 * phoERes')

## Create a preselected tree
zchain = getChains('v11')['z']
tree = zchain.CopyTree('&'.join(cuts))
## Have to copy aliases by hand
for a in zchain.GetListOfAliases():
    tree.SetAlias(a.GetName(), a.GetTitle())

## Get the nominal dataset
data = dataset.get(tree=tree, weight=weight, cuts=cuts,
                   variables=[mmgMass, mmMass, phoERes,])

## Set units and nice titles
for x, t, u in zip([mmgMass, mmMass, phoERes, mmgMassPeak, mmgMassWidth,
                    phoScale, phoRes],
                   ['m_{#mu#mu#gamma}', 'm_{#mu#mu}',
                    'x = E^{#gamma}/E_{true}^{#gamma} - 1', 'm_{peak}',
                    '#sigma_{eff}/m_{Z}', '#gamma scale',
                    '#gamma resolution'],
                   ['GeV', 'GeV', '%', 'GeV', 'GeV', '%', '%']):
    x.SetTitle(t)
    x.setUnit(u)

##------------------------------------------------------------------------------
## Enlarge the range of the observable to get vanishing tails.
range_save = (phoERes.getMin(), phoERes.getMax())
phoERes.setRange(-90, 150)
calibrator = MonteCarloCalibrator(data)
phoERes.setRange(*range_save)

## Get the smeared data
sdata = calibrator.get_smeared_data(targets, targetr)

## Get the parametrized model for the photon energy resolution
phoEResPdf = calibrator.phoEResPdf
phoScale = calibrator.s
phoRes = calibrator.r
calibrator.w.loadSnapshot('sr0_mctruth')
phoScaleRef = calibrator.s0.getVal()
phoResRef = calibrator.r0.getVal()

## Get the parametrized model for the mmg mass
mmgMassPdf = ParametrizedKeysPdf('mmgMassPdf', 'mmgMassPdf',
                                 mmgMass, mmgMassPeak,
                                 mmgMassWidth, data,
                                 ROOT.RooKeysPdf.NoMirror, 1.5)
mmgMassPdf.fitTo(data, roo.Range(60,120), roo.SumW2Error(False))

## Get the parametrized model for the smeared mmg mass
mmgMass.Print()
mmgMassSmearPdf = ParametrizedKeysPdf('mmgMassSmearPdf', 'mmgMassSmearPdf',
                                      mmgMass, mmgMassSmearPeak,
                                      mmgMassSmearWidth, sdata,
                                      ROOT.RooKeysPdf.NoMirror, 1.5)
mmgMassSmearPdf.fitTo(sdata, roo.Range(60,120), roo.SumW2Error(False))

##------------------------------------------------------------------------------
def plot_training_phoeres_with_shape_and_fit():
    """Plot the nominal MC data overlayed with the pdf shape and fit."""
    canvases.next('TrainingSampleWithShapeAndFit')
    plot = phoERes.frame(roo.Range(-7.5, 5))
    plot.SetTitle("MC overlayed with PDF shape (blue) and it's parametrized fit"
                  "(dashed red)")
    data.plotOn(plot)
    calibrator.w.loadSnapshot('sr0_mctruth')
    phoScale.setVal(calibrator.s0.getVal())
    phoRes.setVal(calibrator.r0.getVal())
    phoEResPdf.shape.plotOn(plot)
    phoEResPdf.plotOn(plot, roo.LineColor(ROOT.kRed),
                      roo.LineStyle(ROOT.kDashed))
    plot.Draw()
    Latex([
        's_{shape}: %.3f %%' % phoEResPdf.shapemode,
        's_{fit}: %.3f #pm %.3f %%' % (calibrator.s.getVal(),
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
        ], position=(0.18, 0.8)).draw()
## end of plot_training_phoeres_with_shape_and_fit
    
##------------------------------------------------------------------------------
## Plot the smeared data
def plot_smeared_phoeres_with_fit():
    phoEResPdf.fitTo(sdata, roo.PrintLevel(-1), roo.SumW2Error(False),
                     roo.Range(-50, 50))
    canvases.next('SmearedSampleWithFit')
    savtitle = phoERes.GetTitle()
    phoERes.SetTitle('smeared E_{reco}^{#gamma}/E_{gen}^{#gamma} - 1')
    plot = phoERes.frame(roo.Range(-30, 30))
    phoERes.SetTitle(savtitle)
    plot.SetTitle("Smeared MC with paremetrized fit")
    sdata.plotOn(plot)
    phoEResPdf.plotOn(plot)
    # phoEResPdf.paramOn(plot)
    plot.Draw()
    Latex([
        's_{target}: %.3g %%' % targets,
        's_{fit}: %.3g #pm %.3g %%' % (phoScale.getVal(), phoScale.getError()),
        's_{fit} - s_{target}: %.3g #pm %.3g %%' % (
            phoScale.getVal() - targets, phoScale.getError()
            ),
        'r_{target}: %.3g %%' % targetr,
        'r_{fit}: %.3g #pm %.3g %%' % (phoRes.getVal(), phoRes.getError()),
        'r_{fit} - r_{target}: %.3g #pm %.3g %%' % (
            phoRes.getVal() - targetr, phoRes.getError()
            ),
        'r_{fit}/r_{target}: %.3g #pm %.3g %%' % (
            phoRes.getVal() / targetr, phoRes.getError() / targetr
            ),
        ], position=(0.18, 0.75)).draw()
## end of plot_smeared_phoeres_with_fit

##------------------------------------------------------------------------------
def plot_phoeres_with_fit_for_multiple_smearings(name, stargets, rtargets,
                                                 colors, plotrange=(-30, 30)):
    """Plot the smeared photon energy response for a number of different
    smearings."""
    canvases.next(name).SetGrid()
    phoERes.setRange('plot', *plotrange)
    plot = phoERes.frame(roo.Range('plot'))
    #plot.SetTitle("MC with paremetrized fit for multiple smearing scenarious")
    plot.SetTitle("")
    slabels = []
    rlabels = []
    ## Loop over the various smearings.
    for starget, rtarget, color in zip(stargets, rtargets, colors):
        mydata = calibrator.get_smeared_data(starget, rtarget)
        phoEResPdf.fitTo(mydata, roo.PrintLevel(-1), roo.SumW2Error(False))
        mydata.plotOn(plot, roo.LineColor(color), roo.MarkerColor(color))
        phoEResPdf.plotOn(plot, roo.LineColor(color), roo.Range('plot'), roo.NormRange('plot'))
        slabels.append([
            's\' = % 3.f %%,  #Delta s_{fit} = % .2f #pm %.2f %%' % (
                starget, phoScale.getVal() - starget, phoScale.getError()
                ),
            ])
        rlabels.append([
            'r\' = %3.1f %%,  #Delta r_{fit} = % .2f #pm %.2f %%' % (
                rtarget, phoRes.getVal() - rtarget, phoRes.getError()
                ),
            ])
    ## End of loop over the various smearings.
    plot.Draw()
    for i, (labels, color) in enumerate(zip(slabels, colors)):
        latex = Latex(labels, position=(0.18, 0.85 - i*0.055))
        latex.SetTextColor(color)
        latex.draw()
    for i, (labels, color) in enumerate(zip(rlabels, colors)):
        latex = Latex(labels,
                      position=(0.18, 0.85 - (len(slabels) + 1) * 0.055 -  i * 0.055))
        latex.SetTextColor(color)
        latex.draw()
## end of plot_phoeres_with_fit_for_multiple_smearings

##------------------------------------------------------------------------------
def plot_mmgmass_with_fit_for_multiple_smearings(name, stargets, rtargets,
                                                 colors, plotrange=(60, 105)):
    """Plot the smeared mmg mass for a number of different smearings."""
    canvases.next(name).SetGrid()
    mmgMass.setRange('plot', *plotrange)
    plot = mmgMass.frame(roo.Range('plot'))
    plot.SetTitle("")
    slabels = []
    rlabels = []
    ## Loop over the various smearings.
    for starget, rtarget, color in zip(stargets, rtargets, colors):
        mydata = calibrator.get_smeared_data(starget, rtarget)
        model = ParametrizedKeysPdf('model',
                                    'model',
                                    mmgMass, mmgMassSmearPeak,
                                    mmgMassSmearWidth, mydata,
                                    ROOT.RooKeysPdf.NoMirror, 1.5)
        model.fitTo(mydata, roo.PrintLevel(-1), roo.Range(60, 120),
                    roo.SumW2Error(False))
        mydata.plotOn(plot, roo.LineColor(color), roo.MarkerColor(color))
        model.plotOn(plot, roo.LineColor(color), roo.Range('plot'),
                     roo.NormRange('plot'))
        slabels.append([
            's\' = % 3.f %%,  ' % starget +
            '#Delta m_{#mu#mu#gamma} = %.2f #pm %.2f %%' % (
                100 * (mmgMassSmearPeak.getVal() / 91.2 - 1.),
                100 * mmgMassSmearPeak.getError() / 91.2
                ),
            ])
        rlabels.append([
            'r\' = %.1f %%,  ' % rtarget +
            '#sigma_{eff}/#mu(m_{\mu\mu\gamma}) = % .2f #pm %.2f %%' % (
                100 * mmgMassSmearWidth.getVal() / mmgMassSmearPeak.getVal(),
                100 * mmgMassSmearWidth.getError() / mmgMassSmearPeak.getVal(),
                ),
            ])
    ## End of loop over the various smearings.
    plot.Draw()
    for i, (labels, color) in enumerate(zip(slabels, colors)):
        latex = Latex(labels, position=(0.18, 0.85 - i*0.055))
        latex.SetTextColor(color)
        latex.draw()
    for i, (labels, color) in enumerate(zip(rlabels, colors)):
        latex = Latex(labels,
                      position=(0.18, 0.85 - (len(slabels)+1) * 0.055 - i*0.055))
        latex.SetTextColor(color)
        latex.draw()
## end of plot_mmgmass_with_fit_for_multiple_smearings

##------------------------------------------------------------------------------
def plot_nominal_and_smeared_mmgmass():
    canvases.next('SmearedMMGMass').SetGrid()
    plot = mmgMass.frame(roo.Range(75, 105))
    plot.SetTitle("Nominal and smeared m_{#mu#mu#gamma}")
    data.plotOn(plot)
    mmgMassPdf.plotOn(plot, roo.LineColor(ROOT.kBlack))
    sdata.plotOn(plot, roo.MarkerColor(ROOT.kRed), roo.LineColor(ROOT.kRed))
    # mmgMassSmearPdf.fitTo(sdata)
    mmgMassSmearPdf.plotOn(plot, roo.LineColor(ROOT.kRed))
    plot.Draw()    
    Latex(['s_{0}^{#gamma}: %.2g %%' % phoScaleRef,
           'r_{0}^{#gamma}: %.2g %%' % phoResRef,
           '#mu_{0}: %.3f #pm %.3f GeV' % (
               mmgMassPeak.getVal(), mmgMassPeak.getError()
               ),
           '#sigma_{0}^{eff}: %.3f #pm %.3f GeV' % (
               mmgMassWidth.getVal(), mmgMassWidth.getError()
               )],
          position = (0.2, 0.8)).draw()
    Latex(['s^{#gamma}: %.2g %%' % targets,
           'r^{#gamma}: %.2g %%' % targetr,
           '#mu: %.3f #pm %.3f GeV' % (
               mmgMassSmearPeak.getVal(), mmgMassSmearPeak.getError()
               ),
           '#sigma^{eff}: %.3f #pm %.3f GeV' % (
               mmgMassSmearWidth.getVal(), mmgMassSmearWidth.getError()
               )],
          position = (0.65, 0.8),
          color = ROOT.kRed).draw()
## end of plot_nominal_and_smeared_mmgmass
    
##------------------------------------------------------------------------------
## Plot the smeared data for a number of different smearings
def plot_mmgmass_for_multiple_smearings(name, stargets, rtargets,
                                        colors, plotrange=(76, 106)):
    canvases.next(name).SetGrid()
    plot = mmgMass.frame(roo.Range(*plotrange))
    plot.SetTitle("MC for multiple smearing scenarious")
    multilabels = []
    ## Loop over the various smearings.
    for starget, rtarget, color in zip(stargets, rtargets, colors):
        mydata = calibrator.get_smeared_data(starget, rtarget)
        mydata.plotOn(plot, roo.LineColor(color), roo.MarkerColor(color))
        multilabels.append(['s_{target}: %.1f %%' % starget,
                            'r_{target}: %.1f %%'% rtarget,])
    ## End of loop over the various smearings.
    plot.Draw()
    for i, (labels, color) in enumerate(zip(multilabels, colors)):
        latex = Latex(labels, position=(0.2, 0.85 - i*0.11))
        latex.SetTextColor(color)
        latex.draw()
## end of plot_mmgmass_for_multiple_smearings

##------------------------------------------------------------------------------
def main():
    ## plot_training_phoeres_with_shape_and_fit()
    ## plot_smeared_phoeres_with_fit()
    ## plot_nominal_and_smeared_mmgmass()
    #colors = [ROOT.kRed - 3,
              #ROOT.kOrange - 2,
              ## ROOT.kYellow - 7,
              #ROOT.kSpring + 5,
              #ROOT.kAzure - 9,
              #ROOT.kBlack]
    colors = [
        ROOT.kRed + 1,
        ROOT.kGreen + 2,
        #ROOT.kCyan + 1,
        ROOT.kBlue + 1,
        ROOT.kMagenta + 2,
        ROOT.kBlack,
        ]
    #canvases.wheight = 600
    #canvases.wwidth = 600
    ROOT.gStyle.SetPadLeftMargin(0.15)
    #phoERes.setBins(140)
    #plot_phoeres_with_fit_for_multiple_smearings(
        #"PhoEResScaleScan",
        #stargets = [-10, -5, 0, 5, 10][:],
        #rtargets = [2,] * 5,
        #colors = colors,
        #plotrange = (-50, 20)
        #)
    mmgMass.setBins(90)
    plot_mmgmass_with_fit_for_multiple_smearings(
        "MmgMassScaleScan",
        stargets = [-10, -5, 0, 5, 10],
        rtargets = [2,] * 5,
        colors = colors,
        )
    #phoERes.setBins(60)
    #plot_phoeres_with_fit_for_multiple_smearings(
        #"PhoEResResolutionScan",
        #stargets = [0] * 5,
        #rtargets = [1, 1.5, 2, 3, 5],
        #colors = colors,
        #plotrange = (-10, 5)
        #)
    mmgMass.setBins(40)
    plot_mmgmass_with_fit_for_multiple_smearings(
        "MmgMassResolutionScan",
        stargets = [0] * 5,
        rtargets = [1, 1.5, 2, 3, 5],
        colors = colors,
        plotrange = (75, 95),
        )
    canvases.update()
## end of main

##------------------------------------------------------------------------------
## mmgMassSmearPdf = ParametrizedKeysPdf('mmgMassSmearPdf', 'mmgMassSmearPdf',
##                                       mmgMass, mmgMassPeak, mmgMassWidth,
##                                       sdata,
##                                       ROOT.RooKeysPdf.NoMirror, 1.5)



##------------------------------------------------------------------------------
## Footer stuff
if __name__ == "__main__":
    main()
    canvases.update()
    import user

