import os
from ROOT import *
from array import array
from JPsi.MuMu.common.pmvTrees import getChains

tree = getChains('v15reco')

canvases = []
graphs = {}

## Set TDR style
macroPath = "tdrstyle.C"
if os.path.exists(macroPath):
    gROOT.LoadMacro(macroPath)
    ROOT.setTDRStyle()
    gROOT.ForceStyle()

gStyle.SetPadRightMargin(0.05)
gStyle.SetPadLeftMargin(0.2)
gStyle.SetPadTopMargin(0.05)
wWidth = 600
wHeight = 600
canvasDX = 20
canvasDY = 20

latexLabel = TLatex()
latexLabel.SetNDC()


## make histos of pmv vs nvtx

###############################################################################
# Plot PMV eff. vs photon pt in data for EB
c1 = TCanvas()
canvases.append(c1)

xbins = [0., 5., 7, 8, 9, 10, 11, 12, 13, 15, 20.]

h_Nvtx = TH1F("h_Nvtx_data_eb", "p_{T}^#gamma", len(xbins)-1, array("d", xbins))

# selection = "phoIsEB & phoR9 > 0.94 & abs(mmgMass-90)<15 & (minDEta > 0.04 | minDPhi > 0.3)"
# selection = "phoIsEB & phoR9 < 0.94 & abs(mmgMass-90)<15 & (minDEta > 0.04 | minDPhi > 0.3)"
# selection = "!phoIsEB & phoR9 > 0.95 & abs(mmgMass-90)<15 & (minDEta > 0.08 | minDPhi > 0.3)"
selection = "!phoIsEB & phoR9 < 0.95 & abs(mmgMass-90)<15 & (minDEta > 0.08 | minDPhi > 0.3)"

## label = "Barrel, R9 > 0.94"
## label = "Barrel, R9 < 0.94"
## label = "Endcaps, R9 > 0.95"
label = "Endcaps, R9 < 0.95"

tree["data"].Draw("nVertices>>" + h_Nvtx.GetName(), selection)
htot = h_Nvtx.Clone(h_Nvtx.GetName() + "_tot")

tree["data"].Draw("nVertices>>" + h_Nvtx.GetName(), selection + "& !phoHasPixelMatch")
hpass = h_Nvtx.Clone(h_Nvtx.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("vertex multiplicity")
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency")
geff.SetTitle("Dec22ReReco, L = 35.9 pb^{-1}")
geff.Draw("ap")
graphs["data"] = geff

latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2011")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
latexLabel.DrawLatex(0.7, 0.2, "Barrel")
c1.Update()


###############################################################################
# Plot PMV eff. vs photon pt in Z->mmg MC for EB
c1 = TCanvas()
canvases.append(c1)

xbins = [0., 5., 7, 8, 9, 10, 11, 12, 13, 15, 20.]
# xbins = [0., 5., 10., 20.]

h_Nvtx = TH1F("h_Nvtx_mc_eb", "p_{T}^#gamma", len(xbins)-1, array("d", xbins))

tree["z"].Draw("nVertices>>" + h_Nvtx.GetName(), selection )
htot = h_Nvtx.Clone(h_Nvtx.GetName() + "_tot")

tree["z"].Draw("nVertices>>" + h_Nvtx.GetName(), selection + "& !phoHasPixelMatch")
hpass = h_Nvtx.Clone(h_Nvtx.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("vertex multiplicity");
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency");
geff.Draw("ap");
graphs["z"] = geff

latexLabel.DrawLatex(0.15, 0.96, "Powheg/Pythia Z#rightarrow#mu#mu+X")
latexLabel.DrawLatex(0.75, 0.96, "Spring10")
latexLabel.DrawLatex(0.7, 0.2, "Barrel")
c1.Update()

# ###############################################################################
# # Plot PMV eff. vs photon pt in gamma+jet MC for EB with no photon ID
# c1 = TCanvas()
# canvases.append(c1)
#
# xbins = [20, 25, 30, 35, 40, 45, 50, 60, 70, 100]
#
# andCuts = lambda cuts: "&".join( "(%s)" % c for c in cuts )
#
# idCuts = [
#     "phoHoE < 0.05",
#     "phoTrackIso < 2 + 0.001 * nVertices",
#     "phoEcalIso < 4.2 + 0.003 * nVertices",
#     "phoHcalIso < 2.2 + 0.001 * nVertices",
#     "phoSigmaIetaIeta < 0.01 | (!phoIsEB & phoSigmaIetaIeta < 0.03)",
# ]
#
# genCuts = [
#     "phoMomPdgId == 22",
# ]
#
# h_Nvtx = TH1F("h_Nvtx_gj_eb", "p_{T}^#gamma", len(xbins)-1, array("d", xbins))
#
# selection = andCuts(genCuts)
#
# tree["gj"].Draw("nVertices>>" + h_Nvtx.GetName(), selection)
# htot = h_Nvtx.Clone(h_Nvtx.GetName() + "_tot")
#
# tree["gj"].Draw("nVertices>>" + h_Nvtx.GetName(), selection + "& !phoHasPixelMatch")
# hpass = h_Nvtx.Clone(h_Nvtx.GetName() + "_pass")
#
# geff = TGraphAsymmErrors()
# geff.BayesDivide(hpass,htot)
# geff.GetXaxis().SetTitle("vertex multiplicity");
# geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency");
# geff.Draw("ap");
# graphs["gj_no_id"] = geff
#
# latexLabel.DrawLatex(0.15, 0.96, "#gamma+jet MC, no #gamma ID")
# latexLabel.DrawLatex(0.75, 0.96, "Winter10")
# latexLabel.DrawLatex(0.7, 0.2, "Barrel")
# c1.Update()
#
# ###############################################################################
# # Plot PMV eff. vs photon pt in gamma+jet MC for EB with partial photon ID
# c1 = TCanvas()
# canvases.append(c1)
#
# xbins = [20, 25, 30, 35, 40, 45, 50, 60, 70, 100]
#
# andCuts = lambda cuts: "&".join( "(%s)" % c for c in cuts )
#
# idCuts = [
# #     "phoHoE < 0.05",
#     "phoTrackIso < 2 + 0.001 * nVertices",
#     "phoEcalIso < 4.2 + 0.003 * nVertices",
# #     "phoHcalIso < 2.2 + 0.001 * nVertices",
# #     "phoSigmaIetaIeta < 0.01 | (!phoIsEB & phoSigmaIetaIeta < 0.03)",
# ]
#
# genCuts = [
#     "phoMomPdgId == 22",
# ]
#
# h_Nvtx = TH1F("h_Nvtx_gj_partialID_eb", "p_{T}^#gamma", len(xbins)-1, array("d", xbins))
#
# selection = andCuts(idCuts + genCuts)
#
# tree["gj"].Draw("nVertices>>" + h_Nvtx.GetName(), selection)
# htot = h_Nvtx.Clone(h_Nvtx.GetName() + "_tot")
#
# tree["gj"].Draw("phoPt>>" + h_Nvtx.GetName(), selection + "& !phoHasPixelMatch")
# hpass = h_Nvtx.Clone(h_Nvtx.GetName() + "_pass")
#
# geff = TGraphAsymmErrors()
# geff.BayesDivide(hpass,htot)
# geff.GetXaxis().SetTitle("vertex multiplicity");
# geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency");
# geff.Draw("ap");
# graphs["gj_partial_id"] = geff
#
# latexLabel.DrawLatex(0.15, 0.96, "#gamma+jet MC, partial #gamma ID")
# latexLabel.DrawLatex(0.75, 0.96, "Winter10")
# latexLabel.DrawLatex(0.7, 0.2, "Barrel")
# c1.Update()
#
# ###############################################################################
# # Plot PMV eff. vs photon pt in gamma+jet MC for EB with full photon ID
# c1 = TCanvas()
# canvases.append(c1)
#
# xbins = [20, 25, 30, 35, 40, 45, 50, 60, 70, 100]
#
# andCuts = lambda cuts: "&".join( "(%s)" % c for c in cuts )
#
# idCuts = [
#     "phoHoE < 0.05",
#     "phoTrackIso < 2 + 0.001 * phoPt",
#     "phoEcalIso < 4.2 + 0.003 * phoPt",
#     "phoHcalIso < 2.2 + 0.001 * phoPt",
#     "phoSigmaIetaIeta < 0.01 | (!phoIsEB & phoSigmaIetaIeta < 0.03)",
# ]
#
# genCuts = [
#     "phoMomPdgId == 22",
# ]
#
# h_Nvtx = TH1F("h_Nvtx_gj_fullID_eb", "p_{T}^#gamma", len(xbins)-1, array("d", xbins))
#
# selection = andCuts(idCuts + genCuts)
#
# tree["gj"].Draw("phoPt>>" + h_Nvtx.GetName(), selection)
# htot = h_Nvtx.Clone(h_Nvtx.GetName() + "_tot")
#
# tree["gj"].Draw("phoPt>>" + h_Nvtx.GetName(), selection + "& !phoHasPixelMatch")
# hpass = h_Nvtx.Clone(h_Nvtx.GetName() + "_pass")
#
# geff = TGraphAsymmErrors()
# geff.BayesDivide(hpass,htot)
# geff.GetXaxis().SetTitle("vertex multiplicity");
# geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency");
# geff.Draw("ap");
# graphs["gj_full_id"] = geff
#
# latexLabel.DrawLatex(0.15, 0.96, "#gamma+jet MC, full #gamma ID")
# latexLabel.DrawLatex(0.75, 0.96, "Winter10")
# latexLabel.DrawLatex(0.7, 0.2, "Barrel")
# c1.Update()

# ###############################################################################
# Plot all on 1 canvas
c1 = TCanvas()
canvases.append(c1)

colors = {
    "data"          : kBlack     ,
    "z"             : kAzure - 9 ,
    "gj_no_id"      : kSpring + 5,
    "gj_partial_id" : kOrange - 2,
    "gj_full_id"    : kRed - 3   ,
}

markers = {
    "data"          : 20,
    "z"             : 21,
    "gj_no_id"      : 22,
    "gj_partial_id" : 23,
    "gj_full_id"    : 24,
}

for tag, gr in graphs.items():
    gr.SetMarkerColor( colors[tag] )
    gr.SetLineColor  ( colors[tag] )
    gr.SetMarkerStyle( markers[tag] )

graphs["z"].Draw("ap")
graphs["z"].GetYaxis().SetTitleOffset(1.5)
# graphs["z"].GetYaxis().SetRangeUser(0.95, 1.0)

graphs["data"].Draw("p")
## for tag in "gj_no_id gj_partial_id gj_full_id data".split():
##     graphs[tag].Draw("p")

legend = TLegend(0.55, 0.75, 0.9, 0.9)
legend.SetFillColor(0)
legend.SetShadowColor(0)
legend.SetBorderSize(0)

legend.AddEntry( graphs["data"], "Data", "pl" )
legend.AddEntry( graphs["z"], "Z#rightarrow#mu#mu#gamma Simulation", "pl" )
## legend.AddEntry( graphs["gj_no_id"], "#gamma+j no #gamma ID", "pl" )
## legend.AddEntry( graphs["gj_partial_id"], "#gamma+j partial #gamma ID", "pl" )
## legend.AddEntry( graphs["gj_full_id"], "#gamma+j full #gamma ID", "pl" )

legend.Draw()

c1.SetGridx()
c1.SetGridy()

# latexLabel.DrawLatex(0.15, 0.96, "Powheg/Pythia Z#rightarrow#mu#mu+X")
# latexLabel.DrawLatex(0.75, 0.96, "Spring10")
latexLabel.DrawLatex(0.25, 0.2, label)

c1.Update()
c1.Print("pmvVsNVtx_data_mc.eps")
#c1.Print("pmvVsPt_data_z_gj_variousID.C")

