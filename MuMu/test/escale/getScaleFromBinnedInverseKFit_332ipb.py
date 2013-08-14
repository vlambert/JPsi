import math
import os
import JPsi.MuMu.common.energyScaleChains as esChains
from ROOT import *

#ebselection = 'r9 > 0.94'
#eeselection = 'r9 > 0.95'

#ebselection = 'r9 < 0.94'
#eeselection = 'r9 < 0.95'

ebselection = '1'
eeselection = '1'

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
tdata.Draw("1/k>>ik_data_eb(40,0,2)", "abs(m3-91.2)<4 & isEB & (%s)" % ebselection)
histo = gDirectory.Get("ik_data_eb")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
ikValData = fit.GetParameter(1)
ikErrData = fit.GetParError(1)
report.append("%30s %10s 1/k: %.4f +/- %.4f" % (name, subdet, ikValData, ikErrData))
histo.SetTitle(c1.GetTitle())
histo.GetXaxis().SetTitle("k^{-1} = E^{#gamma}_{ECAL} / E^{#gamma}_{muons}")
c1.Update()
customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

name = '42x MC'
subdet = "Barrel"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tmc.Draw("1/k>>ik_mc_eb(40,0,2)", "(abs(m3-91.2)<4 & isEB & (%s) ) * pileup.weightOOT " % ebselection)
histo = gDirectory.Get("ik_mc_eb")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
ikValMc = fit.GetParameter(1)
ikErrMc = fit.GetParError(1)
report.append("%30s %10s 1/k: %.4f +/- %.4f" % (name, subdet, ikValMc, ikErrMc))
histo.SetTitle(c1.GetTitle())
histo.GetXaxis().SetTitle("k^{-1} = E^{#gamma}_{ECAL} / E^{#gamma}_{muons}")
c1.Update()
customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

scaleVal = ikValData - ikValMc
scaleErr = oplus(ikErrData, ikErrMc) ## is this correct?
report.append("%30s %10s %%  : %.2f +/- %.2f" % ("relative scale", subdet, 100*scaleVal, 100*scaleErr))

#################
# Endcaps
#################

name = '42x data'
subdet = "Endcaps"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tdata.Draw("1/k>>ik_data_ee(40,0,2)", "abs(m3-91.2)<4 & !isEB & (%s)" % eeselection)
histo = gDirectory.Get("ik_data_ee")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
ikValData = fit.GetParameter(1)
ikErrData = fit.GetParError(1)
report.append("%30s %10s 1/k: %.4f +/- %.4f" % (name, subdet, ikValData, ikErrData))
histo.SetTitle(c1.GetTitle())
histo.GetXaxis().SetTitle("k^{-1} = E^{#gamma}_{ECAL} / E^{#gamma}_{muons}")
c1.Update()
customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

name = '42x MC'
subdet = "Endcaps"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tmc.Draw("1/k>>ik_mc_ee(40,0,2)", "( abs(m3-91.2)<4 & !isEB & (%s) ) * pileup.weightOOT" % eeselection)
histo = gDirectory.Get("ik_mc_ee")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
ikValMc = fit.GetParameter(1)
ikErrMc = fit.GetParError(1)
report.append("%30s %10s 1/k: %.4f +/- %.4f" % (name, subdet, ikValMc, ikErrMc))
histo.SetTitle(c1.GetTitle())
histo.GetXaxis().SetTitle("k^{-1} = E^{#gamma}_{ECAL} / E^{#gamma}_{muons}")
c1.Update()
customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

scaleVal = ikValData - ikValMc
scaleErr = oplus(ikErrData, ikErrMc) ## is this correct?
report.append("%30s %10s %%  : %.2f +/- %.2f" % ("relative scale", subdet, 100*scaleVal, 100*scaleErr))

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

