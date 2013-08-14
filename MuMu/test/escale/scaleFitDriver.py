import os
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *
from JPsi.MuMu.common.plotData import PlotData
from JPsi.MuMu.scaleFitter import ScaleFitter

## Get the data
## 715/pb for Vg Summer conferences
# _chains = esChains.getChains('v7')
## 2/fb of LP11 dataset
_chains = esChains.getChains('v8')

## Cuts common to all plots
_commonCuts = [
    'abs(1/kRatio - 1) < 0.5',
    'abs(mmgMass-91.2) < 4',
]

## ----------------------------------------------------------------------------
## Customize below
_fits = [
    ## Barrel, Data
    ScaleFitter(
        name = 'EB_highR9_data',
        title = 'Barrel, R9 > 0.94, data',
        source = _chains['data'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 > 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} > 0.94', 'L = 2.0 fb^{-1}' ],
    ),
    ScaleFitter(
        name = 'EB_lowR9_data_default',
        title = 'Barrel, R9 < 0.94, data, default corrections',
        source = _chains['data'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'L = 2.0 fb^{-1}',
                   'Default Corr.' ],
    ),
    ScaleFitter(
        name = 'EB_lowR9_data_default_closure',
        title = 'Barrel, R9 < 0.94, data, default corrections, closure test',
        source = _chains['data'],
        expression = '100 * (1/corrKRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'L = 2.0 fb^{-1}',
                   'Default Corr.', 'Closure Test' ],
    ),
    ScaleFitter(
        name = 'EB_lowR9_data_new',
        title = 'Barrel, R9 < 0.94, data, new corrections',
        source = _chains['data'],
        expression = '100 * (1/newCorrKRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'L = 2.0 fb^{-1}',
                   'New Corr.' ],
    ),

    ## Barrel, MC
    ScaleFitter(
        name = 'EB_highR9_mc',
        title = 'Barrel, R9 > 0.94, Powheg S4',
        source = _chains['z'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 > 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} > 0.94', 'Powheg S4' ],
    ),
    ScaleFitter(
        name = 'EB_lowR9_mc_default',
        title = 'Barrel, R9 < 0.94, Powheg S4, default corrections',
        source = _chains['z'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'Powheg S4',
                   'Default Corr.' ],
    ),
    ScaleFitter(
        name = 'EB_lowR9_mc_default_closure',
        title = 'Barrel, R9 < 0.94, Powheg S4, default corrections, closure test',
        source = _chains['z'],
        expression = '100 * (1/corrKRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'Powheg S4',
                   'Default Corr.', 'Closure Test' ],
    ),
    ScaleFitter(
        name = 'EB_lowR9_mc_new',
        title = 'Barrel, R9 < 0.94, Powheg S4, new corrections',
        source = _chains['z'],
        expression = '100 * (1/newCorrKRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'Powheg S4',
                   'New Corr.' ],
    ),

    ## Endcaps, Data
    ScaleFitter(
        name = 'EE_highR9_data',
        title = 'Endcaps, R9 > 0.95, data',
        source = _chains['data'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['!phoIsEB', 'phoR9 > 0.95'],
        labels = [ 'Endcaps', 'R_{9}^{#gamma} > 0.95', 'L = 2.0 fb^{-1}' ],
    ),
    ScaleFitter(
        name = 'EE_lowR9_data_default',
        title = 'Endcaps, R9 < 0.95, data, default corrections',
        source = _chains['data'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['!phoIsEB', 'phoR9 < 0.95'],
        labels = [ 'Endcaps', 'R_{9}^{#gamma} < 0.95', 'L = 2.0 fb^{-1}',
                   'Default Corr.' ],
    ),
    ScaleFitter(
        name = 'EE_lowR9_data_default_closure',
        title = 'Endcaps, R9 < 0.95, data, default corrections, closure test',
        source = _chains['data'],
        expression = '100 * (1/corrKRatio - 1)',
        cuts = _commonCuts + ['!phoIsEB', 'phoR9 < 0.95'],
        labels = [ 'Endcaps', 'R_{9}^{#gamma} < 0.95', 'L = 2.0 fb^{-1}',
                   'Default Corr.', 'Closure Test' ],
    ),
    ScaleFitter(
        name = 'EE_lowR9_data_new',
        title = 'Endcaps, R9 < 0.95, data, new corrections',
        source = _chains['data'],
        expression = '100 * (1/newCorrKRatio - 1)',
        cuts = _commonCuts + ['!phoIsEB', 'phoR9 < 0.95'],
        labels = [ 'Endcaps', 'R_{9}^{#gamma} < 0.95', 'L = 2.0 fb^{-1}',
                   'New Corr.' ],
    ),

    ## Endcaps, MC
    ScaleFitter(
        name = 'EE_highR9_mc',
        title = 'Endcaps, R9 > 0.95, Powheg S4',
        source = _chains['z'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['!phoIsEB', 'phoR9 > 0.95'],
        labels = [ 'Endcaps', 'R_{9}^{#gamma} > 0.95', 'Powheg S4' ],
    ),
    ScaleFitter(
        name = 'EE_lowR9_mc_default',
        title = 'Endcaps, R9 < 0.95, Powheg S4, default corrections',
        source = _chains['z'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['!phoIsEB', 'phoR9 < 0.95'],
        labels = [ 'Endcaps', 'R_{9}^{#gamma} < 0.95', 'Powheg S4',
                   'Default Corr.' ],
    ),
    ScaleFitter(
        name = 'EE_lowR9_mc_default_closure',
        title = 'Endcaps, R9 < 0.95, Powheg S4, default corrections, closure test',
        source = _chains['z'],
        expression = '100 * (1/corrKRatio - 1)',
        cuts = _commonCuts + ['!phoIsEB', 'phoR9 < 0.95'],
        labels = [ 'Endcaps', 'R_{9}^{#gamma} < 0.95', 'Powheg S4',
                   'Default Corr.', 'Closure Test' ],
    ),
    ScaleFitter(
        name = 'EE_lowR9_mc_new',
        title = 'Endcaps, R9 < 0.95, Powheg S4, new corrections',
        source = _chains['z'],
        expression = '100 * (1/newCorrKRatio - 1)',
        cuts = _commonCuts + ['!phoIsEB', 'phoR9 < 0.95'],
        labels = [ 'Endcaps', 'R_{9}^{#gamma} < 0.95', 'Powheg S4',
                   'New Corr.' ],
    ),

]



## Define the workspace
ws1 = RooWorkspace( 'ws1', 'mmg energy scale' )

## Define the quantity to be fitted
x = RooRealVar( 's', '100 * (1/kRatio - 1)', -50, 50, '%' )
w = RooRealVar( 'w', '1', 0, 99 )

xw = RooArgSet(x, w)
ws1.Import(xw)

model = ws1.factory("""CBShape::model( s,
                                       #Deltas[0, -50, 50],
                                       #sigma[20, 0.001, 100],
                                       #alpha[-1.5, -10, 0],
                                       n[1.5, 0.1, 10] )""")

## Define observables and parameters
observables = RooArgSet(x)
parameters = model.getParameters(observables)
ws1.defineSet("parameters", parameters)
ws1.saveSnapshot("initial", parameters, True)

## Loop over plots
for fitter in _fits:
    fitter.fit(ws1)

## <-- loop over plots

## Print a spreadsheet report
print '\nSpreadsheet report'
for plot in _fits:
    ws1.loadSnapshot( plot.name )
    print '%10f\t%10f\t%s' % ( ws1.var('#Deltas').getVal(),
                               ws1.var('#Deltas').getError(),
                               plot.title )
## <-- loop over plots


## Print a latex report
print "\nLatex report"
for plot in _fits:
    ws1.loadSnapshot( plot.name )
    print '  %50s | %6.2f $\pm$ %4.2f \\\\' % (
        plot.title,
        ws1.var('#Deltas').getVal(),
        ws1.var('#Deltas').getError()
    )
## <-- loop over plots


## Print an ASCII report
print '\nASCII report'
for plot in _fits:
    ws1.loadSnapshot( plot.name )
    print '%6.2f +/- %4.2f' % ( ws1.var('#Deltas').getVal(),
                                ws1.var('#Deltas').getError() ), plot.title
## <-- loop over plots


if __name__ == "__main__": import user
