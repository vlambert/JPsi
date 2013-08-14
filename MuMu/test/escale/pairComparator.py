import os
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *
from JPsi.MuMu.common.plotData import PlotData

_chains = esChains.getChains('v7')

_baseCuts = [
    'abs(1/kRatio - 1) < 0.5',
    'abs(mmgMass-91.2) < 4',
]

## ----------------------------------------------------------------------------
## Customize below
leftPlot = PlotData(
    name = 'EB_lowR9_data_new',
    title = 'Barrel, R9 < 0.94, data, new corrections',
    labels = ['Barrel', 'R9 < 0.94', 'data', 'new corr.'],
    source = _chains['data'],
    expression = '100 * (1/newCorrKRatio - 1)',
    cuts = _baseCuts + ['phoIsEB', 'phoR9 < 0.94'],
)

rightPlot = PlotData(
    name = 'EB_lowR9_data_old',
    title = 'Barrel, R9 < 0.94, data, default corrections',
    labels = ['Barrel', 'R9 < 0.94', 'data', 'default corr.'],
    source = _chains['data'],
    expression = '100 * (1/kRatio - 1)',
    cuts = _baseCuts + ['phoIsEB', 'phoR9 < 0.94'],
)

ws1 = RooWorkspace( 'ws1', 'mmg energy scale' )

x = RooRealVar( 's', '100 * (1/kRatio - 1)', -50, 50, '%' )
x.setBins(50)

w = RooRealVar( 'w', '1', 0, 99 )

xw = RooArgSet(x, w)
ws1.Import(xw)

model = ws1.factory("""CBShape::crystalBall( s,
                                             #Deltas[0, -50, 50],
                                             #sigma[20, 0.001, 100],
                                             #alpha[-1.5, -10, 0],
                                             n[1.5, 0.1, 10] )""")


## Get the data for the left plot
x.SetTitle( leftPlot.expression )
data1 = dataset.get( tree = leftPlot.source,
                     variable = x, weight = w, cuts = leftPlot.cuts )
data1.SetName('data1')
ws1.Import(data1)

## Get the data for the right plot
x.SetTitle( rightPlot.expression )
data2 = dataset.get( tree = rightPlot.source,
                     variable = x, weight = w, cuts = rightPlot.cuts )
data2.SetName('data2')
ws1.Import(data2)


## Define observables and parameters
observables = RooArgSet(x)
parameters = model.getParameters(observables)
ws1.defineSet("parameters", parameters)
ws1.saveSnapshot("initial", parameters, True)

## Fit data1
fitResult1 = model.fitTo( data1, Save(), SumW2Error(kTRUE), PrintLevel(-1) )
ws1.saveSnapshot( 'data1', parameters, True )

f1 = 1 + ws1.var('#Deltas').getVal() / 100
f1err = ws1.var('#Deltas').getError() / 100

x.SetTitle('s = E_{RECO}/E_{KIN} - 1')
x.setBins(40)
plot = x.frame( Range(-30, 50) )
data1.SetTitle('data1')
data1.plotOn(plot)
model.plotOn(plot)
model.paramOn( plot,
               Format('NEU', AutoPrecision(2) ),
               Parameters(parameters),
               Layout(.57, 0.92, 0.92) )

c1 = TCanvas()
c1.Divide(2,1)
c1.cd(1)
plot.Draw()

## Fit MC
fitResult2 = model.fitTo( data2, Save(), SumW2Error(kTRUE), PrintLevel(-1) )
ws1.saveSnapshot( 'MC', parameters, True )

f2 = 1 + ws1.var('#Deltas').getVal() / 100
f2err = ws1.var('#Deltas').getError() / 100

x.setBins(40)
plot = x.frame( Range(-30, 50) )
data2.SetTitle('MC')
data2.plotOn(plot)
model.plotOn(plot)
model.paramOn( plot,
               Format('NEU', AutoPrecision(2) ),
               Parameters(parameters),
               Layout(.57, 0.92, 0.92) )

c1.cd(2)
plot.Draw()

from math import sqrt
oplus = lambda x,y: sqrt(x*x + y*y)

f1over2 = f1 / f2
f1over2Err = f1over2 * oplus( f1err / f1, f2err / f2 )

print "Left:", leftPlot.title
print "Right:", rightPlot.title
print "  left/right: %0.4f +/- %0.4f" % ( f1over2, f1over2Err )

c1.Print( 'sFit_%s_and_%s.png' % (leftPlot.name, rightPlot.name) )


if __name__ == "__main__": import user
