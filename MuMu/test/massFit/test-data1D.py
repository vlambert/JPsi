import data1D
from ROOT import *

canvases = []

## Get and plot k
x = RooRealVar('k', 'kRatio', 0.5, 1.5)
# data1D._variable = x
data = data1D.getDataSet(variable = x)
x.SetTitle('k = E_{kin}/E_{reco}')
plot = x.frame()
data.plotOn(plot)
canvases.append( TCanvas() )
plot.Draw()

## Get and plot s
x = RooRealVar('s', '100*(1/kRatio-1)', -50, 50, "%")
data = data1D.getDataSet(variable = x)
x.SetTitle('s = E_{reco}/E_{kin} - 1')
plot = x.frame()
data.plotOn(plot)
canvases.append( TCanvas() )
plot.Draw()


## Get and plot -log(k)
x = RooRealVar('logik', '-log(kRatio)', -0.5, 0.5)
data = data1D.getDataSet(variable = x)
x.SetTitle('log(E_{reco}/E_{kin})')
plot = x.frame()
data.plotOn(plot)
canvases.append( TCanvas() )
plot.Draw()
