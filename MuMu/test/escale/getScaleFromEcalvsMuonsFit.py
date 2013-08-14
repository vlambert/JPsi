import math
import os
from ROOT import *

#filenameData = "Nov4ReReco.dat"
#filenameMC   = "DYToMuMu_powheg_Fall10.dat"
filenameData = "Dec22ReReco.dat"
filenameMC   = "DYToMuMu_Winter10_Powheg.dat"

gROOT.LoadMacro("tdrstyle.C");
from ROOT import setTDRStyle
setTDRStyle()
#gStyle.SetPadRightMargin(0.05)
gStyle.SetOptFit(1111)
gStyle.SetOptTitle(1)
gStyle.SetOptStat(1111)
#gStyle.SetStatFontSize(0.05)
gStyle.SetStatW(0.2)
#gStyle.SetStatH(0.2)

canvases = []
report = []
graphs = []

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
# Barrel
#################

name = os.path.splitext(filenameData)[0]
subdet = "Barrel"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tdata.Draw("k*pt*cosh(eta):pt*cosh(eta)>>evse_data_eb(20,0,2)", "abs(m3-91.2)<4 & isEB")
fit1 = TF1("fit1" , "pol1")
fit1.FixParameter(0,0)
gr1 = TGraph(tdata.GetSelectedRows(), tdata.GetV1(), tdata.GetV2())
gr1.Fit("fit1")
gr1.Draw("ap")
p1ValData = fit1.GetParameter(1)
p1ErrData = fit1.GetParError(1)
report.append("%30s %10s p1: %.4f +/- %.4f" % (name, subdet, p1ValData, p1ErrData))
gr1.SetTitle(c1.GetTitle())
gr1.GetXaxis().SetTitle("E^{#gamma}_{muons}")
gr1.GetYaxis().SetTitle("E^{#gamma}_{ECAL}")
c1.Update()
#customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

name = os.path.splitext(filenameMC)[0]
subdet = "Barrel"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tmc.Draw("k*pt*cosh(eta):pt*cosh(eta)>>evse_mc_eb(20,0,2)", "abs(m3-91.2)<4 & isEB")
fit2 = TF1("fit2" , "pol1")
fit2.FixParameter(0,0)
gr2 = TGraph(tmc.GetSelectedRows(), tmc.GetV1(), tmc.GetV2())
gr2.Fit("fit2")
gr2.Draw("ap")
p1ValMc = fit2.GetParameter(1)
p1ErrMc = fit2.GetParError(1)
report.append("%30s %10s p1: %.4f +/- %.4f" % (name, subdet, p1ValMc, p1ErrMc))
gr2.SetTitle(c1.GetTitle())
gr2.GetXaxis().SetTitle("E^{#gamma}_{muons}")
gr2.GetYaxis().SetTitle("E^{#gamma}_{ECAL}")
c1.Update()
#customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

scaleVal = p1ValData - p1ValMc
scaleErr = oplus(p1ErrData, p1ErrMc) ## is this correct?
report.append("%30s %10s %%: %.2f +/- %.2f" % ("relative scale", subdet, 100*scaleVal, 100*scaleErr))
graphs.extend([gr1, gr2])

################## 
## Endcaps
##################

name = os.path.splitext(filenameData)[0]
subdet = "Endcaps"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tdata.Draw("k*pt*cosh(eta):pt*cosh(eta)>>evse_data_ee(20,0,2)", "abs(m3-91.2)<4 & !isEB")
fit1 = TF1("fit1" , "pol1")
fit1.FixParameter(0,0)
gr1 = TGraph(tdata.GetSelectedRows(), tdata.GetV1(), tdata.GetV2())
gr1.Fit("fit1")
gr1.Draw("ap")
p1ValData = fit1.GetParameter(1)
p1ErrData = fit1.GetParError(1)
report.append("%30s %10s p1: %.4f +/- %.4f" % (name, subdet, p1ValData, p1ErrData))
gr1.SetTitle(c1.GetTitle())
gr1.GetXaxis().SetTitle("E^{#gamma}_{muons}")
gr1.GetYaxis().SetTitle("E^{#gamma}_{ECAL}")
c1.Update()
#customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

name = os.path.splitext(filenameMC)[0]
subdet = "Endcaps"
c1 = TCanvas(name + "_" + subdet, name + " " + subdet)
tmc.Draw("k*pt*cosh(eta):pt*cosh(eta)>>evse_mc_ee(20,0,2)", "abs(m3-91.2)<4 & !isEB")
fit2 = TF1("fit2" , "pol1")
fit2.FixParameter(0,0)
gr2 = TGraph(tmc.GetSelectedRows(), tmc.GetV1(), tmc.GetV2())
gr2.Fit("fit2")
gr2.Draw("ap")
p1ValMc = fit2.GetParameter(1)
p1ErrMc = fit2.GetParError(1)
report.append("%30s %10s p1: %.4f +/- %.4f" % (name, subdet, p1ValMc, p1ErrMc))
gr2.SetTitle(c1.GetTitle())
gr2.GetXaxis().SetTitle("E^{#gamma}_{muons}")
gr2.GetYaxis().SetTitle("E^{#gamma}_{ECAL}")
c1.Update()
#customizeStats(c1.GetPrimitive("stats"))
canvases.append(c1)

scaleVal = p1ValData - p1ValMc
scaleErr = oplus(p1ErrData, p1ErrMc) ## is this correct?
report.append("%30s %10s %%: %.2f +/- %.2f" % ("relative scale", subdet, 100*scaleVal, 100*scaleErr))
graphs.extend([gr1, gr2])

########################################
### Outro
########################################

for c in canvases:
    i = canvases.index(c)
    c.SetWindowPosition(10+20*i, 10+20*i)
    c.Print("ecalMuonsCorrelationFit_" + c.GetName() + ".png")

print
print
print "\n".join(report) 

