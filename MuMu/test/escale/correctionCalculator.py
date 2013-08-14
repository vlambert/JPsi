import os
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *

ws1 = RooWorkspace( 'ws1', 'mmg energy scale' )

x = RooRealVar( 's', '100 * (1/kRatio - 1)', -50, 50, '%' )
x.setBins(50)

w = RooRealVar( 'w', '1', 0, 99 )

xw = RooArgSet(x, w)
ws1.Import(xw)

# label = 'EB_highR9'
# label = 'EE_highR9'
label = 'EB_lowR9'
# label = 'EE_lowR9'

## Get data
selection = [
    'abs(1/kRatio - 1) < 0.5',
    'abs(mmgMass-91.2) < 4',
]

if label == 'EB_highR9':
    selection.extend( ['phoR9 > 0.94', 'phoIsEB'] )
elif label == 'EB_lowR9':
    selection.extend( ['phoR9 < 0.94', 'phoIsEB'] )
elif label == 'EE_highR9':
    selection.extend( ['phoR9 > 0.95', '!phoIsEB'] )
elif label == 'EE_lowR9':
    selection.extend( ['phoR9 < 0.95', '!phoIsEB'] )
else:
    raise RuntimeError, "Unknown label `%s'" % label

model = ws1.factory("""CBShape::crystalBall( s,
                                             #Deltas[0, -50, 50],
                                             #sigma[20, 0.001, 100],
                                             #alpha[-1.5, -10, 0],
                                             n[1.5, 0.1, 10] )""")

# data = dataset.get( tree = esChains.getChains('v4')['data'],
#                     variable = x,
#                     weight = w,
#                     cuts = selection + ['id.run > 160000'], ## No 2010 data
#                     )

data = dataset.get( tree = esChains.getChains('v4')['z'],
                    variable = x,
                    weight = w,
                    cuts = selection, ## No 2010 data
                    )

data.SetName('data')
ws1.Import(data)

# mc = dataset.get( tree = esChains.getChains('v4')['z'],
#                   variable = x,
#                   weight = w,
#                   cuts = selection )

x.SetTitle( '100 * (phoGenE/(phoPt*cosh(phoEta)*kRatio) - 1)' )
mc = dataset.get( tree = esChains.getChains('v4')['z'],
                  variable = x,
                  weight = w,
                  cuts = selection )

mc.SetName('mc')
ws1.Import(mc)


## Define observables and parameters
observables = RooArgSet(x)
parameters = model.getParameters(observables)
ws1.defineSet("parameters", parameters)
ws1.saveSnapshot("initial", parameters, True)

## Fit data
fitResult1 = model.fitTo( data, Save(), SumW2Error(kTRUE), PrintLevel(-1) )
ws1.saveSnapshot( 'data', parameters, True )

fData = 1 + ws1.var('#Deltas').getVal() / 100
ferrData = ws1.var('#Deltas').getError() / 100

x.SetTitle('s = E_{RECO}/E_{KIN} - 1')
x.setBins(40)
plot = x.frame( Range(-30, 50) )
data.SetTitle('data')
data.plotOn(plot)
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
fitResult2 = model.fitTo( mc, Save(), SumW2Error(kTRUE), PrintLevel(-1) )
ws1.saveSnapshot( 'MC', parameters, True )

fMC = 1 + ws1.var('#Deltas').getVal() / 100
ferrMC = ws1.var('#Deltas').getError() / 100

x.setBins(40)
plot = x.frame( Range(-30, 50) )
mc.SetTitle('MC')
mc.plotOn(plot)
model.plotOn(plot)
model.paramOn( plot,
               Format('NEU', AutoPrecision(2) ),
               Parameters(parameters),
               Layout(.57, 0.92, 0.92) )

c1.cd(2)
plot.Draw()

from math import sqrt
oplus = lambda x,y: sqrt(x*x + y*y)

fCorr = fMC / fData
fCorrErr = fCorr * oplus( ferrData / fData, ferrMC / fMC )

print "%s: %0.4f +/- %0.4f" % ( label, fCorr, fCorrErr )

c1.Print('sFit_mcRecoGen_%s.png' % label)