import copy
import os
import re
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *
from JPsi.MuMu.common.plotData import PlotData
from JPsi.MuMu.common.binedges import BinEdges
from JPsi.MuMu.scaleFitter import ScaleFitter
from JPsi.MuMu.scaleFitter import PhoEtBin
from JPsi.MuMu.scaleFitter import Model
from JPsi.MuMu.scaleFitter import DimuonMassMax
from JPsi.MuMu.scaleFitter import subdet_r9_categories
from JPsi.MuMu.scaleFitModels import ws1

gROOT.LoadMacro('tools.C+');
gROOT.LoadMacro("CMSStyle.C")
ROOT.CMSstyle()

## Get the data
## 715/pb for Vg Summer conferences
# _chains = esChains.getChains('v7')
## 2/fb of LP11 dataset
_chains = esChains.getChains('v11')

## Default fit of strue = Ereco / Egen - 1
struefit = ScaleFitter(
    name = 'strue_mc_NominalFitRange68',
##    name = 'strue_mc_FitRangePositive',
    title = 'strue-Fit, Powheg S4',
    labels = ['Powheg S4 Summer11 MC'],

    source = _chains['z'],
    xName = 's',
    xTitle = 's_{true} = E^{#gamma}_{reco}/E^{#gamma}_{gen} - 1',
    xExpression = '100 * (phoE/phoGenE - 1)',
    cuts = ['isFSR', 'phoGenE > 0'],
    xRange = (-50, 100),
    xUnit = '%',
    nBins = 150,
    pdf = 'gauss',
    graphicsExtensions = ['png'],
    massWindowScale = 1.5,
    massWindow = (87.2, 95.2),
    fitScale = 1.2,
    fitRange = (0,50),

    doAutoBinning = True,
    binContentMax = 200,
    binContentMin = 35,
    canvasStyle = 'landscape',

    doAutoXRange = True,
    doAutoXRangeZoom = True,
    doAutoFitRange = True,

    xRangeSigmaLevel = 5,
    xRangeSigmaLevelZoom = 2,

    fitRangeMode = 'Fraction',
    fitRangeSigmaLevel = 2.0,
    fitRangeNumberOfEntries = 3000,
    fitRangeFraction = 0.68,
    paramLayout = (0.57, 0.92, 0.92),

    useCustomChi2Calculator = True,    
    )

## Default fit of sgen = Egen / Ekingen - 1
mu1 = 'mu1Pt,mu1Eta,mu1Phi,0.1056'
mu2 = 'mu2Pt,mu2Eta,mu2Phi,0.1056'
mu1gen = 'mu1GenPt,mu1GenEta,mu1GenPhi,0.1056'
mu2gen = 'mu2GenPt,mu2GenEta,mu2GenPhi,0.1056'
phogen = 'phoGenEt,phoGenEta,phoGenPhi,0'
mmMassGen = 'twoBodyMass({mu1}, {mu2})'.format(mu1=mu1gen, mu2=mu2gen)
mmgMassGen = 'threeBodyMass({mu1}, {mu2}, {pho})'.format(mu1=mu1gen,
                                                         mu2=mu2gen,
                                                         pho=phogen)
kRatioGen = 'kRatio({mmgMass}, {mmMass})'.format(mmgMass=mmgMassGen,
                                                 mmMass=mmMassGen)

## ----------------------------------------------------------------------------
## Customize below

struefit.applyDefinitions([DimuonMassMax(80)])

struefits =[]
# models = ('gauss lognormal bifurGauss cbShape gamma'.split() +
#            'cruijff gsh bifurGsh bw sumGaussGauss'.split())
models = 'bifurGauss'.split()
# models += 'sumGaussGauss sumGauss3 sumCruijffGauss sumBwGauss'.split()

for subdet_r9_cat in subdet_r9_categories:
    for lo, hi in BinEdges([10, 12, 15, 20, 25, 30, 100]):
##    for lo, hi in BinEdges([10, 12, 15]):
        for model in models:
            fit = struefit.clone().applyDefinitions([subdet_r9_cat,
                                                     PhoEtBin(lo, hi),
                                                     Model(model)])
            if ('EB_lowR9_PhoEt10-12' in fit.name or
                'EB_lowR9_PhoEt12-15' in fit.name):
                fit.fitRangeFraction -= 0.2
            if 'EE' in fit.name:
                fit.fitRangeFraction += 0.1
                fit.binContentMax = 100
            if fit.fitRangeFraction > 1.:
                fit.fitRangeFraction = 1.
            fit.labels.append('Fit Range Coverage: %.0f%%' %
                              (100 * fit.fitRangeFraction))
            # fit.labels.append('Fit Range: (%.0f, %.0f)%%' % fit.fitRange)
            struefits.append(fit)

_fits = struefits

## Loop over plots
for fitter in _fits[:1]:
    ## Log the current fit configuration
    print "++ Processing", fitter.title
    print "++ Configuration:"
    print fitter.pydump()

    ## Get the data
    fitter.getData(ws1)
    
    ## Load the initial paramter values
    ws1.loadSnapshot(fitter.pdf + '_init')

    ## Make the fit
    fitter.fitToData(ws1)
    fitter.makePlot(ws1)

    ## Save the fit result in the workspace
    ws1.saveSnapshot('sFit_' + fitter.name, fitter.parameters, True)

    ## Make graphics
    if hasattr(fitter, 'graphicsExtensions'):
        for ext in fitter.graphicsExtensions:
            fitter.canvas.Print(fitter.name + '.' + ext)
## <-- loop over fitters


## Print an ASCII report
print '\nASCII report'
is_first_srecofit = True
is_first_struefit = True
is_first_sgenfit = True
is_first_shybfit = True

for plot in _fits:
    if not hasattr(plot, 'niter'):
        continue
    ## Extract the bare name w/o the appended iteration index
    m = re.search('(.*_iter)\d+', plot.name)
    if m:
        bareName = 'sFit_' + m.groups()[0]
    else:
        raise RuntimeError, "Failed to parse fit name `%s'" % plot.name
    for i in range (plot.niter-1, plot.niter):
        ws1.loadSnapshot( bareName + '%d' % i )
        if 'srecofit' in vars() and srecofit.title in plot.title:
            if is_first_srecofit:
                is_first_srecofit = False
                print srecofit.title
        elif 'struefit' in vars() and struefit.title in plot.title:
            if is_first_struefit:
                is_first_struefit = False
                print struefit.title
        elif 'sgenfit' in vars() and sgenfit.title in plot.title:
            if is_first_sgenfit:
                is_first_sgenfit = False
                print sgenfit.title
        elif 'shybfit' in vars() and shybfit.title in plot.title:
            if is_first_shybfit:
                is_first_shybfit = False
                print shybfit.title

        print '%6.2f +/- %4.2f' % ( ws1.var('#Deltas').getVal(),
                                    ws1.var('#Deltas').getError() ),

        if 'srecofit' in vars() and srecofit.title in plot.title:
            print plot.title[len(srecofit.title)+2:],
        elif 'struefit' in vars() and struefit.title in plot.title:
            print plot.title[len(struefit.title)+2:],
        elif 'sgenfit' in vars() and sgenfit.title in plot.title:
            print plot.title[len(sgenfit.title)+2:],
        elif 'shybfit' in vars() and shybfit.title in plot.title:
            print plot.title[len(shybfit.title)+2:],
        else:
            print plot.title,

        print  i, "%.3g" % plot.chi2s[i]
## <-- loop over plots

#ws1.writeToFile('test.root')
#wn1.writeToFile('strue_FitRange71.root')
# ws1.writeToFile('strue_FitRangePositive.root')

if __name__ == "__main__":
    import user
