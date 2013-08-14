import math
import os
import JPsi.MuMu.common.energyScaleChains as esChains
from ROOT import *

#ebselection = 'r9 > 0.94'
#eeselection = 'r9 > 0.95'

#ebselection = 'r9 < 0.94'
#eeselection = 'r9 < 0.95'

ebselection = 'r9 < 0.94 & pt < 15'
eeselection = 'r9 < 0.95 & pt < 15'
nbins = 20

#ebselection = 'r9 < 0.94'
#eeselection = 'r9 < 0.95'

#ebselection = '1'
#eeselection = '1'

gROOT.LoadMacro("tdrstyle.C");
from ROOT import setTDRStyle
setTDRStyle()
#gStyle.SetPadRightMargin(0.05)
gStyle.SetOptFit(1111)
gStyle.SetOptTitle(1)
gStyle.SetOptStat(1111)
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

name = '42x data'
subdet = "Barrel"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tdata.Draw("1/k-1>>s_data_eb(%d,-1,1)" % nbins, "abs(m3-91.2)<4 & isEB & (%s)" % ebselection)
histo = gDirectory.Get("s_data_eb")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
sValData = fit.GetParameter(1)
sErrData = fit.GetParError(1)
report.append("%30s %10s s: (%.2f +/- %.2f) %%" % (name, subdet, 100*sValData, 100*sErrData))
histo.SetTitle(c1.GetTitle())
histo.GetXaxis().SetTitle("k^{-1} = E^{#gamma}_{ECAL} / E^{#gamma}_{muons}")
c1.Update()
customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

name = '42x MC'
subdet = "Barrel"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tmc.Draw("1/k-1>>s_mc_eb(%d,-1,1)" % nbins, "(abs(m3-91.2)<4 & isEB & (%s) ) * pileup.weightOOT " % ebselection)
histo = gDirectory.Get("s_mc_eb")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
sValMc = fit.GetParameter(1)
sErrMc = fit.GetParError(1)
report.append("%30s %10s s: (%.2f +/- %.2f) %%" % (name, subdet, 100*sValMc, 100*sErrMc))
histo.SetTitle(c1.GetTitle())
histo.GetXaxis().SetTitle("k^{-1} = E^{#gamma}_{ECAL} / E^{#gamma}_{muons}")
c1.Update()
customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

scaleVal = sValData - sValMc
scaleErr = oplus(sErrData, sErrMc) ## is this correct?
report.append("%30s %10s %%: (%.2f +/- %.2f) %%" % ("relative scale", subdet, 100*scaleVal, 100*scaleErr))

#################
# Endcaps
#################

name = '42x data'
subdet = "Endcaps"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tdata.Draw("1/k-1>>s_data_ee(%d,-1,1)" % nbins, "abs(m3-91.2)<4 & !isEB & (%s)" % eeselection)
histo = gDirectory.Get("s_data_ee")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
sValData = fit.GetParameter(1)
sErrData = fit.GetParError(1)
report.append("%30s %10s s: (%.2f +/- %.2f) %%" % (name, subdet, 100*sValData, 100*sErrData))
histo.SetTitle(c1.GetTitle())
histo.GetXaxis().SetTitle("k^{-1} = E^{#gamma}_{ECAL} / E^{#gamma}_{muons}")
c1.Update()
customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

name = '42x MC'
subdet = "Endcaps"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tmc.Draw("1/k-1>>s_mc_ee(%d,-1,1)" % nbins, "( abs(m3-91.2)<4 & !isEB & (%s) ) * pileup.weightOOT" % eeselection)
histo = gDirectory.Get("s_mc_ee")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
sValMc = fit.GetParameter(1)
sErrMc = fit.GetParError(1)
report.append("%30s %10s s: (%.2f +/- %.2f) %%" % (name, subdet, 100*sValMc, 100*sErrMc))
histo.SetTitle(c1.GetTitle())
histo.GetXaxis().SetTitle("k^{-1} = E^{#gamma}_{ECAL} / E^{#gamma}_{muons}")
c1.Update()
customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

scaleVal = sValData - sValMc
scaleErr = oplus(sErrData, sErrMc) ## is this correct?
report.append("%30s %10s %%: (%.2f +/- %.2f) %%" % ("relative scale", subdet, 100*scaleVal, 100*scaleErr))

#######################################
## Outro
#######################################

for c in canvases:
    i = canvases.index(c)
    c.SetWindowPosition(10+20*i, 10+20*i)
    c.Print("binnedInverseKFit_" + c.GetName() + ".png")

print
print
print "\n".join(report)

