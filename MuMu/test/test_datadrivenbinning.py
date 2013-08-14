import ROOT

## This is needed to make RooFit work in PyROOT on MacOS X
import JPsi.MuMu.common.basicRoot

import JPsi.MuMu.common.canvases as canvases
from JPsi.MuMu.datadrivenbinning import DataDrivenBinning

nbins = 100
nentries = 5000
minBinContent = 5
maxBinContent = 500

canvases.wwidth = 800
canvases.wheight = 800

## Define a workspace
ws = ROOT.RooWorkspace('ws', 'test data-driven binning')

## Build a model
model = ws.factory('CBShape::model(x[-15,5], m[0], s[1], a[1.5], n[3])')

## Get the observable from the workspace
x = ws.var('x')

## Generate toy data
data = model.generate(ROOT.RooArgSet(x), nentries)

## Plot the data and the model overlaid
plot = x.frame(nbins)
plot.SetTitle('Default Binning')
data.plotOn(plot)
model.plotOn(plot)

## Display the plot
canvas1 = canvases.next('Data_Driven_Binning')
canvas1.Divide(2,2)
canvas1.cd(1)
plot.Draw()

## Create the DataDrivenBinning object
n = data.tree().Draw(x.GetName(), '', 'goff')
bins = DataDrivenBinning(n, data.tree().GetV1(), minBinContent, maxBinContent)

## Use DataDrivenBinning to define a RooBinning
binning = bins.binning(ROOT.RooBinning())
ubinning = bins.uniformBinning(ROOT.RooUniformBinning())

## Make a second plot for comparison.
plot2 = x.frame()
plot2.SetTitle('Data-Driven Binning')

## First plot the data with uniform binning to set the per bin density
data.plotOn(plot2, ROOT.RooFit.Binning(ubinning), ROOT.RooFit.Invisible())

## Plot the data with the custom binning.
data.plotOn(plot2, ROOT.RooFit.Binning(binning))

## Get the histogram of data and set the bin centers equal to medians
hist = plot2.getHist('h_' + data.GetName())
bins.applyTo(hist)

## Overlay the data with the model
model.plotOn(plot2)

## Display the plot with the data-driven binning.
canvas1.cd(3)
plot2.Draw()
canvas1.Update()

## Display the same on log-scale
canvas1.cd(2).SetLogy()
plot.Draw()
canvas1.cd(4).SetLogy()
plot2.Draw()
canvas1.Update()
