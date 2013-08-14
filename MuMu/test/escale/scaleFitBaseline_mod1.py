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

sreco_fitrange = 90

## Get the data
## 715/pb for Vg Summer conferences
# _chains = esChains.getChains('v7')
## 2/fb of LP11 dataset
_chains = esChains.getChains('v11')

## Default fit of s = Ereco / Ekin - 1
srecofit = ScaleFitter(
    name = 'sreco_mc',
    title = 'sreco-Fit, Powheg S4',
    labels = ['Powheg S4'],
    cuts = [],
    source = _chains['z'],
    xName = 's',
    xTitle = 's_{reco} = E^{#gamma}_{reco}/E^{kin}_{reco} - 1',
    xExpression =  '100 * (1/kRatio - 1)',
    xRange = (-50, 100),
    xUnit = '%',
    nBins = 150,
    pdf = 'cbShape',
    graphicsExtensions = ['png'],
    massWindowScale = 1.5,
    massWindow = (87.2, 95.2),
    fitScale = 1.2,
    fitRange = (-50,100),
    doAutoBinning = True,
    binContentMax = 200,
    binContentMin = 35,
    canvasStyle = 'landscape',
    doAutoXRange = False,
    doAutoXRangeZoom = True,
    xRangeSigmaLevelZoom = 5,
    paramLayout = (.45, 0.75, 0.5),
    useCustomChi2Calculator = True,
    )

# srecofit.name += ('_FitRange%d' % int(sreco_fitrange))
srecofit.title += (', Fit Range %d%%' % int(sreco_fitrange))
srecofit.labels.append('Fit Range: %d%%' % int(sreco_fitrange))
srecofit.doAutoFitRange = True
srecofit.fitRangeMode = 'Fraction'
srecofit.fitRangeFraction = float(sreco_fitrange) / 100.


## Default fit of strue = Ereco / Egen - 1
struefit = srecofit.clone(
    name = 'strue_mc',
    title = 'strue-Fit, Powheg S4',
    labels = ['Powheg S4'],

    source = _chains['z'],
    xName = 's',
    xTitle = 's_{true} = E^{#gamma}_{reco}/E^{#gamma}_{gen} - 1',
    xExpression = '100 * (phoE/phoGenE - 1)',
    cuts = ['isFSR', 'phoGenE > 0'],
    xRange = (-50, 100),
    xUnit = '%',
    nBins = 150,
    pdf = 'bifurGaus',
    graphicsExtensions = ['png'],
    massWindowScale = 1.5,
    massWindow = (87.2, 95.2),
    fitScale = 1.2,
    fitRange = (-50,100),

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

struefit.applyDefinitions([Model('bifurGauss')])
srecofit.applyDefinitions([Model('cbShape')])
defaultfits = [struefit, srecofit]

for fit in defaultfits:
    fit.applyDefinitions([DimuonMassMax(80)])


srecofits, struefits =[], []

for subdet_r9_cat in subdet_r9_categories:
    for lo, hi in BinEdges([10, 12, 15, 20, 25, 30, 100]):
##    for lo, hi in BinEdges([10, 12, 15]):
        srecofit_cat = srecofit.clone().applyDefinitions([subdet_r9_cat,
                                                          PhoEtBin(lo, hi)])
        struefit_cat = struefit.clone().applyDefinitions([subdet_r9_cat,
                                                          PhoEtBin(lo, hi)])

        if 'EB_lowR9_PhoEt10-12' in struefit_cat.name:
            struefit_cat.fitRangeFraction -= 0.2

        if 'EB_lowR9_PhoEt12-15' in struefit_cat.name:
            struefit_cat.fitRangeFraction -= 0.2

        if 'EE' in struefit_cat.name:
            struefit_cat.fitRangeFraction += 0.1
            struefit_cat.binContentMax = 100
        srecofits.append(srecofit_cat)
        struefits.append(struefit_cat)

_fits = srecofits + struefits

maxIterations = 1
fSigma = 1.5
pullEpsilon = 0.1
mwindows = {}

## Loop over plots
for fitter in _fits[:]:
    ## Log the current fit configuration
    print "++ Processing", fitter.title
    print "++ Configuration:"
    print fitter.pydump()

    ## Get mass window, only perform fit once for a given selection and
    cutsav = ' & '.join(fitter.cuts)
    if not fitter.massWindow:
        fitter.massWindow = mwindows.get(cutsav)
    fitter.getMassCut(ws1)
    ## Store the resulting mass window in mwindows
    mwindows[cutsav] = fitter.massWindow

    ## Get the data
    fitter.getData(ws1)
    try:
        fitScale = fitter.fitScale
    except AttributeError:
        fitScale = fSigma
    name = fitter.name
    Deltas = ws1.var('#Deltas')
    DeltasOld = Deltas.getVal()
    sigmaL = ws1.var('#sigmaL')
    sigmaR = ws1.var('#sigmaR')
    sigma = ws1.var('#sigma')
    k = ws1.function('k')
    m0 = ws1.function('m0')

    for iteration in range(maxIterations):
        print "++ begin iteration", iteration
        if iteration == 0:
            if not hasattr(fitter, 'fitRange'):
                ## Set the fit range automatically to include all data
                xlo = fitter.data.tree().GetMinimum(fitter.x.GetName())
                xhi = fitter.data.tree().GetMaximum(fitter.x.GetName())

                xbinning = fitter.x.getBinning()
                ilo = xbinning.binNumber(xlo)
                ihi = xbinning.binNumber(xhi)

                ## Take one extra bin on each side
                ilo = max(0, ilo - 1)
                ihi = min(ihi + 1, fitter.x.getBins() - 1)

                fitter.fitRange = (xbinning.binLow(ilo), xbinning.binHigh(ihi))
                print ('+++ Setting fit range to [%f, %f]'
                       'to cover all data.' % fitter.fitRange)
        else:
            if fitter.pdf in ['model', 'cbShape', 'gauss']:
                fitter.fitRange = ( Deltas.getVal() - fitScale * sigma.getVal(),
                                    Deltas.getVal() + fitScale * sigma.getVal() )
            elif fitter.pdf in ['cruijff', 'bifurGauss']:
                fitter.fitRange = ( Deltas.getVal() - fitScale * sigmaL.getVal(),
                                    Deltas.getVal() + fitScale * sigmaR.getVal() )
            elif fitter.pdf == 'lognormal':
                fitter.fitRange = ( 100*(m0.getVal() / pow(k.getVal(), fitScale) - 1),
                                    100*(m0.getVal() * pow(k.getVal(), fitScale) - 1) )
            elif fitter.pdf == 'gamma':
                dsVal = Deltas.getVal()
                fsVal = fitScale * sigma.getVal()
                fitter.fitRange = ( dsVal - fsVal / (1+fsVal/100),
                                    dsVal + fsVal )
            else:
                raise RuntimeError, "Unsupported PDF: %s" % fitter.pdf
            print ('+++ Setting fit range to [%f, %f]'
                   'based on previous iteration.' % fitter.fitRange)
        fitter.name = name + '_iter%d' % iteration
        fitter.fitToData(ws1)
        fitter.makePlot(ws1)
        if iteration == 0:
            DeltasOld = Deltas.getVal()
        else:
            pull = ( Deltas.getVal() - DeltasOld ) / Deltas.getError()
            print "pull:", pull
            DeltasOld = Deltas.getVal()
            if abs(pull) < pullEpsilon:
                break
    fitter.niter = iteration + 1
    ws1.saveSnapshot('sFit_' + name, fitter.parameters, True)
    if hasattr(fitter, 'graphicsExtensions'):
        for ext in fitter.graphicsExtensions:
            fitter.canvas.Print('sFit_' + name + '.' + ext)

#     fitter.fitRange = ( ws1.var('#Deltas').getVal() - 20,
#                         ws1.var('#Deltas').getVal() + 20 )
#     fitter.fit(ws1)

## <-- loop over plots

## Print a spreadsheet report
# print '\nSpreadsheet report'
# for plot in _fits:
#     ws1.loadSnapshot( plot.name )
#     print '%10f\t%10f\t%s' % ( ws1.var('#Deltas').getVal(),
#                                ws1.var('#Deltas').getError(),
#                                plot.title )
## <-- loop over plots


## Print a latex report
# print "\nLatex report"
# for plot in _fits:
#     ws1.loadSnapshot( plot.name )
#     print '  %50s | %6.2f $\pm$ %4.2f \\\\' % (
#         plot.title,
#         ws1.var('#Deltas').getVal(),
#         ws1.var('#Deltas').getError()
#     )
## <-- loop over plots


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

# ws1.writeToFile('test.root')
# ws1.writeToFile('mc_mmMass80_EB_lowR9_PhoEt_mmgMass87.2-95.2_cbShape.root')
ws1.writeToFile('mc_sreco_strue_Baseline_mod1.root')
# ws1.writeToFile('mc_mmMass85_EB_lowR9_PhoEt15-20.root')
# ws1.writeToFile('mc_mmMass85_EB_lowR9_PhoEt20-25.root')
# ws1.writeToFile('mc_mmMass85_EB_lowR9_PhoEt25-30.root')
# ws1.writeToFile('mc_mmMass85_EB_lowR9_PhoEt30-100.root')

if __name__ == "__main__":
    import user
