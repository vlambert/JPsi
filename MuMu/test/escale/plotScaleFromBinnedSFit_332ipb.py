import math
import os
import JPsi.MuMu.common.energyScaleChains as esChains
from ROOT import *

#filenameData = "Nov4ReReco.dat"
#filenameMC   = "DYToMuMu_powheg_Fall10.dat"
filenameData = "Dec22ReReco.dat"
filenameMC   = "DYToMuMu_Winter10_Powheg.dat"

gROOT.LoadMacro("../CMSStyle.C")
import ROOT
ROOT.CMSstyle()

gStyle.SetPadLeftMargin(0.1)
gStyle.SetPadTopMargin(0.05)
gStyle.SetPadRightMargin(0.03)
#gStyle.SetOptFit(1111)
#gStyle.SetOptTitle(1)
#gStyle.SetOptStat(1111)
gStyle.SetOptFit(0)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
#gStyle.SetStatFontSize(0.05)
gStyle.SetStatW(0.2)
gStyle.SetStatH(0.2)

canvases = []
report = []

oplus = lambda x,y: math.sqrt(x*x + y*y)

def customizeStats(stats):
    stats.SetX1NDC(0.65)
    stats.SetY1NDC(0.7)

## Read data set
chains = esChains.getChains()
tdata = chains['data']
tmc   = chains['z']


################# 
# Barrel
#################

name = os.path.splitext(filenameData)[0]
subdet = "Barrel"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tdata.Draw("1/k-1>>s_data_eb(40,-1,1)", "abs(m3-91.2)<4 & isEB", "e")
histo = gDirectory.Get("s_data_eb")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
fit.SetNpx(1000)
fit.SetLineColor(kRed)
fit.SetLineWidth(1)
fit.Draw("same")
histo.SetMarkerSize(1.2)
histo.Draw("same e1")
ikValData = fit.GetParameter(1)
ikErrData = fit.GetParError(1)
report.append("%30s %10s k: %.4f +/- %.4f" % (name, subdet, ikValData, ikErrData))
histo.SetTitle("")
histo.GetXaxis().SetTitle("s = E^{#gamma}_{ECAL} / E^{#gamma}_{kin}-1")
histo.GetYaxis().SetTitle("Events / 0.05")
histo.GetXaxis().SetRangeUser(-0.65, 0.65)
histo.GetYaxis().SetRangeUser(0,350)
histo.GetYaxis().SetTitleOffset(0.7)
histo.SetStats(0)

#customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

latexLabel = TLatex()
latexLabel.SetNDC()
latexLabel.SetTextSize(0.062)

## Final touch
latexLabel.DrawLatex( 0.13, 0.85, "CMS Preliminary 2011" )

latexLabel.DrawLatex( 0.13, 0.775, 
                      "Mean: (%.2f #pm %.2f)%%" % ( 100 * fit.GetParameter(1),
                                                   100 * fit.GetParError(1) ) )
latexLabel.DrawLatex( 0.13, 0.7, "Entries: %d" % int(histo.GetEntries()))

latexLabel.DrawLatex( 0.65, 0.85, "#sqrt{s} = 7 TeV" )
latexLabel.DrawLatex( 0.65, 0.775, "L = 332 pb^{-1}" )
latexLabel.DrawLatex( 0.65, 0.7, "ECAL Barrel" )
#latexLabel.DrawLatex( 0.65, 0.875, "#int L dt = 35.9 pb^{-1}" )

c1.Update()
c1.RedrawAxis()

c1.Print("zmumugamma_eb_data.eps")
c1.Print("zmumugamma_eb_data.C")

