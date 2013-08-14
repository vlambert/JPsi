import math
import os
from ROOT import *

filenameData = "Nov4ReReco.dat"
filenameMC   = "DYToMuMu_powheg_Fall10.dat"
#filenameData = "Dec22ReReco.dat"
#filenameMC   = "DYToMuMu_Winter10_Powheg.dat"

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
tdata = TTree("tdata", "real data");
tmc   = TTree("tmc", "MC");
leafVariables = [
    "run/I"     , #  1. run                       
    "lumi"      , #  2. lumi                      
    "event"     , #  3. event                     
    "isEB"      , #  4. isEB                      
    "pt/F"      , #  5. phoPt[g]                  
    "muNearPt"  , #  6. muPt[mnear]               
    "muFarPt"   , #  7. muPt[mfar]                
    "eta"       , #  8. phoEta[g]                 
    "muNearEta" , #  9. muEta[mnear]              
    "muFarEta"  , # 10. muEta[mfar]               
    "phi"       , # 11. phoPhi[g]                 
    "muNearPhi" , # 12. muPhi[mnear]              
    "muFarPhi"  , # 13. muPhi[mfar]               
    "r9"        , # 14. phoR9                     
    "m2"        , # 15. mass[mm]                  
    "m3"        , # 16. mmgMass                   
    "dr"        , # 17. mmgDeltaRNear             
    "k"         , # 18. kRatio(mmgMass,mass[mm])  
]
tdata.ReadFile(filenameData, ":".join(leafVariables))
tmc  .ReadFile(filenameMC  , ":".join(leafVariables))


################# 
# Barrel + Endcaps
#################

name = os.path.splitext(filenameData)[0]
subdet = "All"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tdata.Draw("k>>k_data(20,0,2)", "abs(m3-91.2)<4")
histo = gDirectory.Get("k_data")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
kValData = fit.GetParameter(1)
kErrData = fit.GetParError(1)
report.append("%30s %10s k: %.4f +/- %.4f" % (name, subdet, kValData, kErrData))
histo.SetTitle(c1.GetTitle())
histo.GetXaxis().SetTitle("k = E^{#gamma}_{muons} / E^{#gamma}_{ECAL}")
c1.Update()
customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

name = os.path.splitext(filenameMC)[0]
subdet = "All"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tmc.Draw("k>>k_mc(20,0,2)", "abs(m3-91.2)<4")
histo = gDirectory.Get("k_mc")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
kValMc = fit.GetParameter(1)
kErrMc = fit.GetParError(1)
report.append("%30s %10s k: %.4f +/- %.4f" % (name, subdet, kValMc, kErrMc))
histo.SetTitle(c1.GetTitle())
histo.GetXaxis().SetTitle("k = E^{#gamma}_{muons} / E^{#gamma}_{ECAL}")
c1.Update()
customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

scaleVal = 1/kValData - 1/kValMc
scaleErr = oplus(kErrData/pow(kValData,2), kErrMc/pow(kValMc,2)) ## is this correct?
report.append("%30s %10s %%: %.2f +/- %.2f" % ("relative scale", subdet, 100*scaleVal, 100*scaleErr))


################# 
# Barrel
#################

name = os.path.splitext(filenameData)[0]
subdet = "Barrel"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tdata.Draw("k>>k_data_eb(20,0,2)", "abs(m3-91.2)<4 & isEB")
histo = gDirectory.Get("k_data_eb")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
kValData = fit.GetParameter(1)
kErrData = fit.GetParError(1)
report.append("%30s %10s k: %.4f +/- %.4f" % (name, subdet, kValData, kErrData))
histo.SetTitle(c1.GetTitle())
histo.GetXaxis().SetTitle("k = E^{#gamma}_{muons} / E^{#gamma}_{ECAL}")
c1.Update()
customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

name = os.path.splitext(filenameMC)[0]
subdet = "Barrel"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tmc.Draw("k>>k_mc_eb(20,0,2)", "abs(m3-91.2)<4 & isEB")
histo = gDirectory.Get("k_mc_eb")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
kValMc = fit.GetParameter(1)
kErrMc = fit.GetParError(1)
report.append("%30s %10s k: %.4f +/- %.4f" % (name, subdet, kValMc, kErrMc))
histo.SetTitle(c1.GetTitle())
histo.GetXaxis().SetTitle("k = E^{#gamma}_{muons} / E^{#gamma}_{ECAL}")
c1.Update()
customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

scaleVal = 1/kValData - 1/kValMc
scaleErr = oplus(kErrData/pow(kValData,2), kErrMc/pow(kValMc,2)) ## is this correct?
report.append("%30s %10s %%: %.2f +/- %.2f" % ("relative scale", subdet, 100*scaleVal, 100*scaleErr))

################# 
# Endcaps
#################

name = os.path.splitext(filenameData)[0]
subdet = "Endcaps"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tdata.Draw("k>>k_data_ee(20,0,2)", "abs(m3-91.2)<4 & !isEB")
histo = gDirectory.Get("k_data_ee")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
kValData = fit.GetParameter(1)
kErrData = fit.GetParError(1)
report.append("%30s %10s k: %.4f +/- %.4f" % (name, subdet, kValData, kErrData))
histo.SetTitle(c1.GetTitle())
histo.GetXaxis().SetTitle("k = E^{#gamma}_{muons} / E^{#gamma}_{ECAL}")
c1.Update()
customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

name = os.path.splitext(filenameMC)[0]
subdet = "Endcaps"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tmc.Draw("k>>k_mc_ee(20,0,2)", "abs(m3-91.2)<4 & !isEB")
histo = gDirectory.Get("k_mc_ee")
histo.Fit("gaus")
fit = histo.GetFunction("gaus")
kValMc = fit.GetParameter(1)
kErrMc = fit.GetParError(1)
report.append("%30s %10s k: %.4f +/- %.4f" % (name, subdet, kValMc, kErrMc))
histo.SetTitle(c1.GetTitle())
histo.GetXaxis().SetTitle("k = E^{#gamma}_{muons} / E^{#gamma}_{ECAL}")
c1.Update()
customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

scaleVal = 1/kValData - 1/kValMc
scaleErr = oplus(kErrData/pow(kValData,2), kErrMc/pow(kValMc,2)) ## is this correct?
report.append("%30s %10s %%: %.2f +/- %.2f" % ("relative scale", subdet, 100*scaleVal, 100*scaleErr))

#######################################
## Outro
#######################################

for c in canvases:
    i = canvases.index(c)
    c.SetWindowPosition(10+20*i, 10+20*i)
    c.Print("binnedKFit_" + c.GetName() + ".png")

print
print
print "\n".join(report) 

