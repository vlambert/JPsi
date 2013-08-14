import os
from ROOT import *
from array import array

# path = "/home/veverka/Work/data/pmv"
path = "/raid2/veverka/PMVTrees_v6"

vetoCut = 'phoDeltaRToTrack > 0.062'
# vetoCut = '!phoHasPixelMatch'

fileName = {
    #"data": "pmvTree_Mu_Run2010AB-Dec22ReReco_v1_json_V3.root",
#     "data": "pmvTree_ZMu-May10ReReco_V4.root",
    "data": "pmvTree_ZMu-May10ReReco-42X-v3_V6.root",
    #"z"   : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v1_V3.root",
#     "z"  : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v2_V3.root",
    "z"  : "pmvTree_ZMu-May10ReReco-42X-v3_V6.root",
    #"tt"  : "pmvTree_TTJets_TuneZ2-madgraph-Winter10_V2.root",
    #"w"   : "",
    #"qcd" : "",
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

## make histos of pmv vs deta

###############################################################################
# Plot PMV eff. vs minDEta in data for EB
c1 = TCanvas()
canvases.append(c1)

xbins = [0., 0.01, 0.02, 0.03, 0.04, 0.06, 0.1, 1.]

h_DEta = TH1F("h_DEta_data_eb", "min #Delta #eta (#mu, #gamma)", len(xbins)-1, array("d", xbins))

totSelection = "phoIsEB & abs(mmgMass-90)<15"
tree["data"].Draw("minDEta>>" + h_DEta.GetName(), totSelection)
htot = h_DEta.Clone(h_DEta.GetName() + "_tot")

passSelection = totSelection + " & (%s)" % vetoCut
tree["data"].Draw("minDEta>>" + h_DEta.GetName(), passSelection)
hpass = h_DEta.Clone(h_DEta.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("min#Delta#eta(#mu,#gamma)")
geff.GetYaxis().SetTitle("#Delta R to Electron Track > 0.062")
geff.SetTitle("May10ReReco, L = 191 pb^{-1}")
geff.Draw("ap")
graphs.append(geff)

latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2011")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
latexLabel.DrawLatex(0.7, 0.3, "L = 191 pb^{-1}")
latexLabel.DrawLatex(0.7, 0.2, "Barrel")
c1.SetName( "drToTrk_0.062_Eff_vs_DEta_data_EB" )
c1.SetGridx(); c1.SetGridy()
c1.Update()


###############################################################################
# Plot PMV eff. vs minDEta in MC for EB
c1 = TCanvas()
canvases.append(c1)

xbins = [0.01 * i for i in range(5)]
xbins.extend( [0.05] + [0.1 + 0.1 * i for i in range(4)] )
xbins.extend( [0.5, 0.7, 1.0] )

h_DEta = TH1F("h_DEta_mc_eb", "min #Delta #eta (#mu, #gamma)", len(xbins)-1, array("d", xbins))

totSelection = "phoIsEB & abs(mmgMass-90)<15"
tree["z"].Draw("minDEta>>" + h_DEta.GetName(), totSelection)
htot = h_DEta.Clone(h_DEta.GetName() + "_tot")

passSelection = totSelection + " & (%s)" % vetoCut
tree["z"].Draw("minDEta>>" + h_DEta.GetName(), passSelection)
hpass = h_DEta.Clone(h_DEta.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("min#Delta#eta(#mu,#gamma)");
geff.GetYaxis().SetTitle("#Delta R to Electron Track > 0.062");
geff.Draw("ap");
graphs.append(geff)

latexLabel.DrawLatex(0.15, 0.96, "Pythia Z#rightarrow#mu#mu+X")
latexLabel.DrawLatex(0.75, 0.96, "Summer11")
latexLabel.DrawLatex(0.7, 0.2, "Barrel")
c1.SetName( "drToTrk_0.062_Eff_vs_DEta_MC_EB" )
c1.SetGridx(); c1.SetGridy()
c1.Update()


###############################################################################
# Plot PMV eff. vs minDEta in data for EE
c1 = TCanvas()
canvases.append(c1)

xbins = [0., 0.02, 0.04, 0.1, 1.]

h_DEta = TH1F("h_DEta_data_ee", "min #Delta #eta (#mu, #gamma)", len(xbins)-1, array("d", xbins))

totSelection = "!phoIsEB & abs(mmgMass-90)<15"
tree["data"].Draw("minDEta>>" + h_DEta.GetName(), totSelection)
htot = h_DEta.Clone(h_DEta.GetName() + "_tot")

passSelection = totSelection + " & (%s)" % vetoCut
tree["data"].Draw("minDEta>>" + h_DEta.GetName(), passSelection)
hpass = h_DEta.Clone(h_DEta.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("min#Delta#eta(#mu,#gamma)")
geff.GetYaxis().SetTitle("#Delta R to Electron Track > 0.062")
geff.SetTitle("Dec22ReReco, L = 191 pb^{-1}")
geff.Draw("ap")
graphs.append(geff)

latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2011")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
latexLabel.DrawLatex(0.7, 0.3, "L = 191 pb^{-1}")
latexLabel.DrawLatex(0.7, 0.2, "Endcaps")
c1.SetName( "drToTrk_0.062_Eff_vs_DEta_data_EE" )
c1.SetGridx()
c1.SetGridy()
c1.Update()


###############################################################################
# Plot PMV eff. vs minDEta in MC for EE
c1 = TCanvas()
c1.SetGridx(); c1.SetGridy()
canvases.append(c1)

xbins = [0.01 * i for i in range(5)]
xbins.extend( [0.05] + [0.1 + 0.1 * i for i in range(4)] )
xbins.extend( [0.5, 0.7, 1.0] )
# xbins = [0.002 * i for i in range(20)]
# xbins.extend( [0.04 + 0.02 * i for i in range(24)] )
# xbins.extend( [0.5  + 0.05 * i for i in range(10)] )

h_DEta = TH1F("h_DEta_mc_ee", "min #Delta #eta (#mu, #gamma)", len(xbins)-1, array("d", xbins))

totSelection = "!phoIsEB & abs(mmgMass-90)<15"
tree["z"].Draw("minDEta>>" + h_DEta.GetName(), totSelection)
htot = h_DEta.Clone(h_DEta.GetName() + "_tot")

passSelection = totSelection + " & (%s)" % vetoCut
tree["z"].Draw("minDEta>>" + h_DEta.GetName(), passSelection)
hpass = h_DEta.Clone(h_DEta.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("min#Delta#eta(#mu,#gamma)");
geff.GetYaxis().SetTitle("#Delta R to Electron Track > 0.062");
geff.Draw("ap");
graphs.append(geff)

latexLabel.DrawLatex(0.15, 0.96, "Pythia Z#rightarrow#mu#mu+X")
latexLabel.DrawLatex(0.75, 0.96, "Summer11")
latexLabel.DrawLatex(0.7, 0.2, "Endcaps")
c1.SetName( "drToTrk_0.062_Eff_vs_DEta_MC_EE" )
c1.Update()

for c in canvases:
    i = canvases.index(c)
    c.SetWindowPosition(10+20*i, 10+20*i)
    c.Print( c.GetName() + ".eps" )

#geff_DEta_mc.BayesDivide(h_DEta_mc_pass, h_DEta_mc_tot)

#tree["z"].Draw("minDEta>>h_DEta", "isEB & abs(mmgMass-90)<15")
#h_DEta_z_tot = h_DEta.Clone("h_DEta_z_tot")

#tree["z"].Draw("minDEta>>h_DEta", "isEB & abs(mmgMass-90)<15 & !phoHasPixelMatch")
#h_DEta_z_pass = h_DEta.Clone("h_DEta_z_pass")

#geff.SetTitle("POWHEG+Pythia Z#rightarrow#mu#mu Fall10 MC, FSR events");
