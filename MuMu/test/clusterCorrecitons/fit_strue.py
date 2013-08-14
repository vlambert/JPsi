import copy
import os
import re
import ROOT
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.r9Chains as r9Chains
import JPsi.MuMu.common.cmsstyle as cmsstyle

# from JPsi.MuMu.common.basicRoot import *
# from JPsi.MuMu.common.roofit import *
from JPsi.MuMu.common.plotData import PlotData
from JPsi.MuMu.common.binedges import BinEdges
from JPsi.MuMu.scaleFitter import ScaleFitter
from JPsi.MuMu.scaleFitter import Cut
from JPsi.MuMu.scaleFitter import PhoEtBin
from JPsi.MuMu.scaleFitter import Model
from JPsi.MuMu.scaleFitter import DimuonMassMax
from JPsi.MuMu.scaleFitter import subdet_r9_categories
from JPsi.MuMu.scaleFitModels import ws1

ROOT.gROOT.LoadMacro('tools.C+');

## Get the data
## Private production of various Geant version with 424p2
_chains = r9Chains.getChains('v1')

#------------------------------------------------------------------------------
class BremBin(Cut):
    """Can act on a ScaleFitter object and modify it's name,
    title, labels and cuts to reflect a fit performed for photon within the
    given brem bin [low,high)."""
    def __init__(self, low, high):
        bin_range = (low, high)
        self.bin_range = bin_range
        Cut.__init__(self,
            name = 'Brem%g-%g' % bin_range,
            title = 'brem in [%g, %g)' % bin_range,
            labels = ['#sigma_{#phi}/#sigma_{#eta} #in [%g, %g)' % bin_range],
            cuts = ['%g <= brem' % low, 'brem < %g' % high],
        )

    def __str__(self):
        return self.__class__.__name__ + '(%g, %g)' % self.bin_range
## end of class BremBin

## Default fit of sraw = Eraw / Egen - 1
sfit = ScaleFitter(
    name = 'strue_mc_modulep4',
    title = 'strue-Fit, Powheg S4',
    labels = ['Flat-pt #gamma gun',
              '#eta_{SC} #in [1.16,1.44]',
              '#eta/#phi cracks removed',],
    cuts = ['!isEBEtaGap & !isEBPhiGap',
            '1.16 < abs(scEta) & abs(scEta) < 1.44',
            'scE > 0',
            'genE > 0',],
    source = _chains['g93p01'],
    xName = 's',
    xTitle = 's_{true} = E^{SC}_{corr}/E^{#gamma}_{gen} - 1',
    xExpression =  '100 * (scE/genE - 1)',
    xRange = (-50, 50),
    xUnit = '%',
    nBins = 120,
    fitRange = (-49, 49),
    pdf = 'cruijff',
    graphicsExtensions = ['png'],
    paramLayout = (.2, 0.52, 0.92), # x1, x2, y1
    labelsLayout = (.55, 0.55), # x1, y1
    # In order to define chi2 well
    binContentMin = 10,
    binContentMax = 100,
    canvasStyle = 'extended',
    doAutoXRange = True,
    doAutoXRangeZoom = True,
    doAutoFitRange = True,
    xRangeSigmaLevel = 5,
    xRangeSigmaLevelZoom = 2,
    fitRangeSigmaLevel = 1.5,
    useCustomChi2Calculator = False,
    )

## ----------------------------------------------------------------------------
## Customize below
_fits = []
pdfs = [ROOT.TNamed('bifurGsh', 'Bifur. GSH'),
        #ROOT.TNamed('gsh', 'GSH'),
        #ROOT.TNamed('sech', 'Hyperbolic Secant'),
        #ROOT.TNamed('cruijff', 'Cruijff'),
        #ROOT.TNamed('cbShape', 'Crystal Ball'),
        ROOT.TNamed('gauss', 'Gaussian'),]

for geant in 'g93p01 g94p02 g94cms'.split():
    for pdf in pdfs:
        for lo, hi in BinEdges([0.8,1.2,1.5,2,2.5,3,3.5,4,5,10]):
            fit = sfit.clone(source = _chains[geant], pdf = pdf.GetName())
            fit.name = '_'.join([fit.name, geant, fit.pdf])
            fit.title = ', '.join([fit.title, geant, pdf.GetTitle()])
            fit.labels.extend([geant, pdf.GetTitle()])
            fit.applyDefinitions([BremBin(lo, hi)])
            _fits.append(fit)

maxIterations = 1
fSigma = 2.0
pullEpsilon = 0.01
mwindows = {}

## Loop over plots
for fitter in _fits[:9]:
    ## Log the current fit configuration
    print "++ Processing", fitter.title
    print "++ Configuration:"
    print fitter.pydump()

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
            pass
            ## Set the fit range automatically to include all data
#             xlo = fitter.data.tree().GetMinimum(fitter.x.GetName())
#             xhi = fitter.data.tree().GetMaximum(fitter.x.GetName())
#
#             xbinning = fitter.x.getBinning()
#             ilo = xbinning.binNumber(xlo)
#             ihi = xbinning.binNumber(xhi)
#
#             ## Take one extra bin on each side
#             ilo = max(0, ilo - 1)
#             ihi = min(ihi + 1, fitter.x.getBins() - 1)
#
#             fitter.fitRange = (xbinning.binLow(ilo), xbinning.binHigh(ihi))
        else:
            if fitter.pdf in ['model', 'cbShape', 'gauss', 'sech', 'gsh']:
                fitter.fitRange = ( Deltas.getVal() - fitScale * sigma.getVal(),
                                    Deltas.getVal() + fitScale * sigma.getVal() )
            elif fitter.pdf in ['cruijff', 'bifurGauss', 'bifurSech', 'bifurGsh']:
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
report = []

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
        ws1.loadSnapshot(bareName + '%d' % i)
        report.append([
            '%6.2f +/- %4.2f' % ( ws1.var('#Deltas').getVal(),
                                  ws1.var('#Deltas').getError() ),

            plot.title,
            str(i),
            "%.3g" % plot.chi2s[i]
            ])

for line in report:
    print ', '.join(line)

## <-- loop over plots

# ws1.writeToFile('test.root')
# ws1.writeToFile('mc_mmMass80_EB_lowR9_PhoEt_mmgMass87.2-95.2_cbShape.root')
ws1.writeToFile('geant_versions.root')
# ws1.writeToFile('mc_mmMass85_EB_lowR9_PhoEt15-20.root')
# ws1.writeToFile('mc_mmMass85_EB_lowR9_PhoEt20-25.root')
# ws1.writeToFile('mc_mmMass85_EB_lowR9_PhoEt25-30.root')
# ws1.writeToFile('mc_mmMass85_EB_lowR9_PhoEt30-100.root')

if __name__ == "__main__":
    import user
