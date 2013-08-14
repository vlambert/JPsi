'''Validates the RooChi2Calculator class'''

import ROOT
import JPsi.MuMu.common.roofit as roofit
import JPsi.MuMu.common.cmsstyle as cmsstyle
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.roochi2calculator import RooChi2Calculator
from JPsi.MuMu.datadrivenbinning import DataDrivenBinning

minBinContent = 35
maxBinContent = 100
numCPU = 3
ntoys = 100
nentries = 1000
epsilonPerBin = 0.01

cmsstyle.cmsstyle()

## Load custom models
ROOT.gSystem.Load('libJPsiMuMu')

w = ROOT.RooWorkspace('w', 'w')

## Unit Gaussian to compare with the distribution of pulls
unitg = w.factory('Gaussian::unitg(pull[-5,5],zero[0],unit[1])')
pull = w.var('pull')

defaultd = ROOT.RooDataSet('defaultd', 'defaultd', ROOT.RooArgSet(pull))
bind = ROOT.RooDataSet('bind', 'bind', ROOT.RooArgSet(pull))
mediand = ROOT.RooDataSet('mediand', 'mediand', ROOT.RooArgSet(pull))
pdgd = ROOT.RooDataSet('pdgd', 'pdgd', ROOT.RooArgSet(pull))

## Build the model
# model = w.factory('Gaussian::gaus(x[-5,5],mean[0,-6,6],sigma[1,0.5,2])')
model = w.factory('RooSechPdf::sech(x[-5,5],mean[0,-6,6],sigma[1,0.5,2])')
x = w.factory('x')

for itoy in range(ntoys):
    ## Use the model to generate a toy dataset
    data = model.generate(ROOT.RooArgSet(x), nentries, roofit.NumCPU(numCPU))

    ## Fit the model to the generated data
    model.fitTo(data, roofit.NumCPU(numCPU), roofit.Verbose(False))

    ## Get custom binning
    nevents = data.tree().Draw(x.GetName(), '', 'goff')
    bins = DataDrivenBinning(nevents, data.tree().GetV1(), minBinContent,
                             maxBinContent)
    binning = bins.binning(ROOT.RooBinning())
    ubinning = bins.uniformBinning(ROOT.RooUniformBinning())

    ## Make sure that there are at least 1./epsilonPerBin curve points
    ## in each bin.  The RooChi2Calculator fails if there is none perhaps
    ## due to a bug in RooCurve::average?  Reason is not understood yet.
    epsilon = epsilonPerBin * ubinning.binWidth(0) / bins.length()

    ## Make frames
    log_plot = x.frame()
    log_plot_bins = x.frame()
    log_plot_medians = x.frame()

    bins.setSigmaLevel(3)
    lin_plot = x.frame(roofit.Range(-3,3))
    lin_plot_bins = x.frame(*bins.bounds())
    lin_plot_medians = x.frame(*bins.bounds())
    bins.setFraction(1)

    log_plot.SetTitle('Default RooFit')
    lin_plot.SetTitle(log_plot.GetTitle())
    log_plot_bins.SetTitle("New - Bin Content > %d" % minBinContent)
    lin_plot_bins.SetTitle(log_plot_bins.GetTitle())
    log_plot_medians.SetTitle("New - Bin Content > %d and Data at Bin Medians" %
                              minBinContent)
    lin_plot_medians.SetTitle(log_plot_medians.GetTitle())


    ## Add the data and fit to the plots
    for plot in [log_plot, lin_plot]:
        data.plotOn(plot)
        model.plotOn(plot, roofit.Precision(epsilon))
        
    for plot in [log_plot_bins, log_plot_medians,
                 lin_plot_bins, lin_plot_medians]:
        data.plotOn(plot, roofit.Invisible(), roofit.Binning(ubinning))
        data.plotOn(plot, roofit.Binning(binning))
        model.plotOn(plot, roofit.Precision(epsilon))
    
    for plot in [log_plot_medians, lin_plot_medians]:
        ## Change the x positions of the data from bin centers to medians.
        hist = plot.getHist('h_' + data.GetName())
        bins.applyTo(hist)

    ## Get the pull distribution
    chi2calc = RooChi2Calculator(log_plot_bins)

    default_pull_hist = log_plot.pullHist()
    bins_pull_hist    = log_plot_bins.pullHist()
    median_pull_hist  = log_plot_medians.pullHist()
    pdg_pull_hist     = chi2calc.pullHist()

    ## Plot the pdg pulls
    ## canvases.wwidth = 600
    ## canvases.wwheight = 800
    ## canvas = canvases.next('toy_%d' % itoy)
    ## canvas.Divide(1,2)
    ## canvas.cd(1)
    ## log_plot_bins.Draw()
    ## canvas.cd(2)
    ## pdg_pull_plot = x.frame()
    ## pdg_pull_plot.addPlotable(pdg_pull_hist, "p")
    ## pdg_pull_plot.Draw()
    ## canvas.Update()
    
    for hist, data in zip([default_pull_hist, bins_pull_hist, median_pull_hist,
                           pdg_pull_hist],
                          [defaultd, bind, mediand, pdgd]):
        row = data.get()
        for i in range(hist.GetN()):
            if (hist.GetErrorY(i) == 0 or
                hist.GetErrorYhigh(i) == 0 or
                hist.GetErrorYlow(i) == 0):
                continue            
            row.first().setVal(hist.GetY()[i])
            data.addFast(row)

## Make the pull plots
defaultp = pull.frame()
binp = pull.frame()
medianp = pull.frame()
pdgp = pull.frame()

defaultp.SetTitle('Default RooFit: Any Bin Content, Interpolate Bin Center')
binp.SetTitle('Bin Content > %d, Interpolate Bin Center' % minBinContent)
medianp.SetTitle('Bin Content > %d, Interpolate Bin Median' % minBinContent)
pdgp.SetTitle('(Almost) PDG: Bin Content > %d, Integrate over Bin' % minBinContent)

## Make the canvas
canvases.wwidth = 800
canvases.wheight = 800
c1 = canvases.next('Fit_Examples')
c1.Divide(2,3)

## Display the plot with y log scale
for i, p, logy in zip([1, 2, 3, 4, 5, 6],
                      [log_plot, lin_plot,
                       log_plot_bins, lin_plot_bins,
                       log_plot_medians, lin_plot_medians],
                      [True, False, True, False, True, False]):
    c1.cd(i)
    if logy:
        ROOT.gPad.SetLogy()
    p.Draw()

c1.Update()

canvases.wwidth = 800
canvases.wheight = 600
c2 = canvases.next('Pulls')
c2.Divide(2,2)

for i, plot, data in zip([1,2,3,4],
                         [defaultp, binp, medianp, pdgp],
                         [defaultd, bind, mediand, pdgd]):
    data.plotOn(plot)
    unitg.plotOn(plot)
    c2.cd(i)
    plot.Draw()
c2.Update()

c3 = c2.DrawClone()
c3.SetName('Pulls_Log')
c3.SetTitle(c3.GetName())
canvases.canvases.append(c3)
for i in range(1,5):
    c3.cd(i).SetLogy()
    

# canvases.make_plots(['png'])

if __name__ == '__main__':
    import user
