import os
from ROOT import *
from array import array
import JPsi.MuMu.common.energyScaleChains as esChains

## get trees
tree = {}
tree = esChains.getChains('v4')
esChainsV2 = esChains.getChains('v2')
tree['w'] = esChainsV2['w']
tree['tt'] = esChainsV2['tt']
tree['qcd'] = esChainsV2['qcd']

tree['hgg'] = TTree('gg', 'gg tree excerpt')
#tree['hgg'].ReadFile('phoPt/F:phoEta:phoHaxPixelMatch/I')

cweight = {
    "data": 1.,
    'z'  : 0.17175592557735 * 1795714. / 2008540., ## read events Spring11 / Summer11
    'tt' : 0.019860956416475,
    'w'  : 0.54974976060237,
    'qcd': 0.27884236321449,

}

puWeight = {
    'data': '1.',

    'z'  : 'pileup.weightOOT',
    'tt' : 'pileup.weightOOT',
    'w'  : 'pileup.weightOOT',
    'qcd': 'pileup.weightOOT',

}

canvases = []
graphs = {}

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

## make histos of pmv vs deta

###############################################################################
# Plot PMV eff. vs photon pt in data for EB
c1 = TCanvas()
canvases.append(c1)

xbins = [5., 10., 20., 50.]

h_Pt = TH1F("h_Pt_data_eb", "p_{T}^#gamma", len(xbins)-1, array("d", xbins))

selection = "phoIsEB & abs(mmgMass-90)<15 & (minDEta > 0.04 | minDPhi > 0.3)"
tree["data"].Draw("phoPt>>" + h_Pt.GetName(), selection)
htot = h_Pt.Clone(h_Pt.GetName() + "_tot")

tree["data"].Draw("phoPt>>" + h_Pt.GetName(), selection + "& !phoHasPixelMatch")
hpass = h_Pt.Clone(h_Pt.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("p_{T}^{#gamma}")
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency")
geff.SetTitle("Dec22ReReco, L = 35.9 pb^{-1}")
geff.Draw("ap")
graphs["data"] = geff

latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
latexLabel.DrawLatex(0.7, 0.2, "Barrel")
c1.Update()


###############################################################################
# Plot PMV eff. vs photon pt in Z->mmg MC for EB
c1 = TCanvas()
canvases.append(c1)

xbins = [5, 7.5, 10, 15, 20, 25, 30, 50, 100]

h_Pt = TH1F("h_Pt_mc_eb", "p_{T}^#gamma", len(xbins)-1, array("d", xbins))

selection = "phoIsEB & abs(mmgMass-90)<15 & (minDEta > 0.04 | minDPhi > 0.3)"
tree["z"].Draw("phoPt>>" + h_Pt.GetName(), selection )
htot = h_Pt.Clone(h_Pt.GetName() + "_tot")

tree["z"].Draw("phoPt>>" + h_Pt.GetName(), selection + "& !phoHasPixelMatch")
hpass = h_Pt.Clone(h_Pt.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("p_{T}^{#gamma}");
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency");
geff.Draw("ap");
graphs["z"] = geff

latexLabel.DrawLatex(0.15, 0.96, "Powheg/Pythia Z#rightarrow#mu#mu+X")
latexLabel.DrawLatex(0.75, 0.96, "Winter10")
latexLabel.DrawLatex(0.7, 0.2, "Barrel")
c1.Update()

###############################################################################
# Plot PMV eff. vs photon pt in gamma+jet MC for EB with no photon ID
#c1 = TCanvas()
#canvases.append(c1)

#xbins = [20, 25, 30, 35, 40, 45, 50, 60, 70, 100]

#andCuts = lambda cuts: "&".join( "(%s)" % c for c in cuts )

#idCuts = [
    #"phoHoE < 0.05",
    #"phoTrackIso < 2 + 0.001 * phoPt",
    #"phoEcalIso < 4.2 + 0.003 * phoPt",
    #"phoHcalIso < 2.2 + 0.001 * phoPt",
    #"phoSigmaIetaIeta < 0.01 | (!phoIsEB & phoSigmaIetaIeta < 0.03)",
#]

#genCuts = [
    #"phoMomPdgId == 22",
#]

#kineCuts = [
    #'phoIsEB'
#]

#h_Pt = TH1F("h_Pt_gj_eb", "p_{T}^#gamma", len(xbins)-1, array("d", xbins))

#selection = andCuts(genCuts + kineCuts)

#tree["gj"].Draw("phoPt>>" + h_Pt.GetName(), selection)
#htot = h_Pt.Clone(h_Pt.GetName() + "_tot")

#tree["gj"].Draw("phoPt>>" + h_Pt.GetName(), selection + "& !phoHasPixelMatch")
#hpass = h_Pt.Clone(h_Pt.GetName() + "_pass")

#geff = TGraphAsymmErrors()
#geff.BayesDivide(hpass,htot)
#geff.GetXaxis().SetTitle("p_{T}^{#gamma}");
#geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency");
#geff.Draw("ap");
#graphs["gj_no_id"] = geff

#latexLabel.DrawLatex(0.15, 0.96, "#gamma+jet MC, no #gamma ID")
#latexLabel.DrawLatex(0.75, 0.96, "Winter10")
#latexLabel.DrawLatex(0.7, 0.2, "Barrel")
#c1.Update()


# ###############################################################################
# Plot all on 1 canvas
#c1 = TCanvas()
#canvases.append(c1)

#colors = {
    #"data"          : kBlack     ,
    #"z"             : kAzure - 9 ,
    #"gj_no_id"      : kSpring + 5,
    #"gj_partial_id" : kOrange - 2,
    #"gj_full_id"    : kRed - 3   ,
#}

#markers = {
    #"data"          : 20,
    #"z"             : 21,
    #"gj_no_id"      : 22,
    #"gj_partial_id" : 23,
    #"gj_full_id"    : 24,
#}

#for tag, gr in graphs.items():
    #gr.SetMarkerColor( colors[tag] )
    #gr.SetLineColor  ( colors[tag] )
    #gr.SetMarkerStyle( markers[tag] )

#graphs["z"].Draw("ap")
#graphs["z"].GetYaxis().SetRangeUser(0.85, 1.1)

#for tag in "gj_no_id gj_partial_id gj_full_id data".split():
    #graphs[tag].Draw("p")

#legend = TLegend(0.55, 0.6, 0.9, 0.9)
#legend.SetFillColor(0)
#legend.SetShadowColor(0)
#legend.SetBorderSize(0)

#legend.AddEntry( graphs["data"], "Data", "pl" )
#legend.AddEntry( graphs["z"], "Z#rightarrow#mu#mu#gamma", "pl" )
#legend.AddEntry( graphs["gj_no_id"], "#gamma+j no #gamma ID", "pl" )
#legend.AddEntry( graphs["gj_partial_id"], "#gamma+j partial #gamma ID", "pl" )
#legend.AddEntry( graphs["gj_full_id"], "#gamma+j full #gamma ID", "pl" )

#legend.Draw()

#c1.SetGridx()
#c1.SetGridy()

#c1.Print("pmvVsPt_data_z_gj_variousID.eps")
#c1.Print("pmvVsPt_data_z_gj_variousID.C")

