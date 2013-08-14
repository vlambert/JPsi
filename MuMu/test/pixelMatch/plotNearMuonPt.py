import os
from ROOT import *
from array import array

path = "/home/veverka/Work/data/pmv"

fileName = {
    #"data": "pmvTree_Mu_Run2010AB-Dec22ReReco_v1_json_V3.root",
    "data": "pmvTree_ZMu-May10ReReco_V4.root",
    #"z"   : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v1_V3.root",
    "z"  : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v2_V3.root",
    "tt"  : "pmvTree_TTJets_TuneZ2-madgraph-Winter10_V3.root",
    "w"   : "pmvTree_WJetsToLNu_TuneZ2_7TeV-madgraph_Winter10_V3.root",
    "qcd" : "pmvTree_QCD_Pt-20_MuEnrichedPt-15_Winter10_V3.root",
}

weight = {
    "data": 1.,
    "z"  : 0.030541912803076,
    "qcd": 0.10306919044126,
    "w"  : 0.074139194512438,
    "tt" : 0.005083191122289,
}

canvases = []
graphs = []

## Set TDR style
macroPath = "tdrstyle.C"
if os.path.exists(macroPath):
    gROOT.LoadMacro(macroPath)
    ROOT.setTDRStyle()
    gROOT.ForceStyle()

gStyle.SetPadRightMargin(0.05)
gStyle.SetPadTopMargin(0.05)
wWidth = 600
wHeight = 600
canvasDX = 20
canvasDY = 20

latexLabel = TLatex()
latexLabel.SetNDC()

## open files
file = {}
for tag, name in fileName.items():
    file[tag] = TFile(os.path.join(path, name))

## get trees
tree = {}
for tag, f in file.items():
    tree[tag] = f.Get("pmvTree/pmv")

## make histos of pmv vs mmgMass

#ebSelection = "phoIsEB & abs(mmgMass-90)<15 & (minDEta > 0.04 | minDPhi > 0.3)"
#eeSelection = "!phoIsEB & abs(mmgMass-90)<15 & (minDEta > 0.08 | minDPhi > 0.3)"
selection = "1"

###############################################################################
# Plot mmgMass in data for EB
c1 = TCanvas()
canvases.append(c1)

#h_temp = {}
#h_temp["data"] = TH1F("h_temp_data_eb", "min #Delta #eta (#mu, #gamma)", 60, 60, 120)
h_temp = TH1F("h_temp", "", 100, 0, 100)
h_temp.SetTitle("")
h_temp.SetStats(0)
h_temp.GetYaxis().SetTitle("Events / GeV")
h_temp.GetXaxis().SetTitle("p_{T}^{#gamma} (GeV)")


tree["data"].Draw("mu1Pt * (muNearIndex == 1) + mu2PtphoPt>>h_temp", selection)
hdata = h_temp.Clone(h_temp.GetName() + "_data")

tree["z"].Draw("phoPt>>h_temp", selection)
hmc = h_temp.Clone(h_temp.GetName() + "_mc")

tree["z"].Draw("phoPt>>h_temp", "(%s) && !isFSR" % (selection) )
hbkg = h_temp.Clone(h_temp.GetName() + "_bkgd")

hmc .SetFillColor(kAzure - 9)
hbkg.SetFillColor(kSpring + 5)
hmc .SetLineColor(kAzure - 9)
hbkg.SetLineColor(kSpring + 5)
scale = hdata.GetEntries() / hmc.GetEntries()
hmc.Scale(scale)
hbkg.Scale(scale)

hmc.Draw()
hmc.GetYaxis().SetRangeUser(0, 700)

hbkg.Draw("same")
hdata.Draw("e1same")

c1.RedrawAxis()

latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2011")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
#latexLabel.DrawLatex(0.7, 0.2, "Barrel")
latexLabel.DrawLatex(0.2, 0.875, "May10ReReco + Winter10 MC")
latexLabel.DrawLatex(0.2, 0.8, "Total events: %d" % (int( hdata.GetEntries() ),) )
latexLabel.DrawLatex(0.2, 0.725, "L = 221 pb^{-1}")

c1.Update()


