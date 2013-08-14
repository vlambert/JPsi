import os
from ROOT import *

gROOT.LoadMacro("tdrstyle.C");
gROOT.LoadMacro("fitZToMuMuGammaMassUnbinned.C+")

from ROOT import setTDRStyle
from ROOT import fitZToMuMuGammaMassUnbinned

setTDRStyle()
gStyle.SetPadRightMargin(0.05)

def customizeModelParamBox(stats):
    stats.SetX1NDC(0.635)
    stats.SetX2NDC(0.99)
    stats.SetY1NDC(0.45)
    stats.SetY2NDC(0.99)
    stats.Draw()

loc = gROOT.GetListOfCanvases()
canvases, workspaces = [], []

for mcFile, dataFile in [ 
    ("m3_DYToMuMu_powheg_Fall10_EB.dat", "m3_Nov4ReReco_EB.dat"),
    ("m3_DYToMuMu_powheg_Fall10_EE.dat", "m3_Nov4ReReco_EE.dat"),
    ("m3_DYToMuMu_powheg_Winter10_EB.dat", "m3_Dec22ReReco_EB.dat"),
    ("m3_DYToMuMu_powheg_Winter10_EE.dat", "m3_Dec22ReReco_EE.dat") ]:

    mcLabels = ["Endcaps", "Fall10", ]
    dataLabels = ["Endcaps", "Nov4ReReco", ]
    
    mcName   = os.path.splitext(mcFile  )[0]
    dataName = os.path.splitext(dataFile)[0]
    
    c1 = TCanvas("c_" + mcName, mcName + " Unbinned Invariant Mass Fit", 0,0,800,600)
    ws1 = fitZToMuMuGammaMassUnbinned(
        mcFile, # filename
        "NEU", # plotOpt
        60,   # nbins
        )
    customizeModelParamBox( c1.GetPrimitive("model_paramBox") )
    
    
    c2 = TCanvas("c_" + dataName, dataName + " Unbinned Invariant Mass Fit", 0,0,800,600)
    ws2 = fitZToMuMuGammaMassUnbinned(
        dataFile, # filename
        "NEU", # plotOpt
        20,   # nbins
        ws1.var("a_{CB}").getVal(),
        ws1.var("n_{CB}").getVal(),
        )
    customizeModelParamBox( c2.GetPrimitive("model_paramBox") )
    
    canvases.extend([c1,c2])
    workspaces.extend([ws1,ws2])
    
    c1.Print("ubmlFit_" + mcName + ".png")
    c2.Print("ubmlFit_" + dataName + ".png")

if __name__ == "__main__": import user
