import os
from ROOT import *
from array import array

# path = "/home/veverka/Work/data/pmv"
path = "/raid2/veverka"

## Restrict the maximum number of events used for plotting to speed
## up debugging trunaround. 
maxevents = -1

fileName = {
    # "data": "PMVTrees_v1/pmvTree_Mu_Run2010AB-Dec22ReReco_v1_json_V3.root",
    # 'data': 'PMVTrees_v6/pmvTree_ZMu_May10ReReco-42X-v3_Plus_PromptSkim-v4_42X-v5_V6.root',
    #'data': 'pmvTrees/pmvTree_V15_05Jul2011ReReco_05Aug2011_03Oct2011-v1_PromptReco-v1B.root',
    # 'data' : 'pmvTrees/pmvTree_V21_DoubleMu_Run2011AB-16Jan2012-v1_condor_Dimuon_AOD-42X-v10.root',
    'data' : 'pmvTrees/pmvTree_V15_05Jul2011ReReco_05Aug2011_03Oct2011-v1_PromptReco-v1B_RECO.root',
    #"z"  : "PMVTrees_v1/pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v2_V3.root",
    #"z"   : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v1_V3.root",
    'z' : 'PMVTrees_v6/pmvTree_DYToMuMu_pythia6_AOD-42X-v4_V6.root',
#    'z' : 'pmvTrees/pmvTree_V12_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9.root',
    #"tt"  : "pmvTree_TTJets_TuneZ2-madgraph-Winter10_V2.root",
    #"w"   : "",
    #"qcd" : "",
    #"gj"  : "PMVTrees_v1/pmvTree_GJets_TuneD6T_HT-40To100-madgraph_Winter10_V3_numEvents40k.root",
    "gj"  : "PMVTrees_v6/pmvTree_G_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_Summer11_AOD_42X-v4_V6.root",
    #'gj' : 'pmvTrees/pmvTree_V12_G_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_S4-v1_condor_Inclusive_AOD-42X-v9.root',
}

weight = {
    "data": 1.,
    "z"  : 0.030541912803076,
    "qcd": 0.10306919044126,
    "w"  : 0.074139194512438,
    "tt" : 0.005083191122289,
}

if maxevents < 0:
    maxevents = 1000000000

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

## open files
file = {}
for tag, name in fileName.items():
    file[tag] = TFile(os.path.join(path, name))

## get trees
tree = {}
for tag, f in file.items():
    tree[tag] = f.Get("pmvTree/pmv")

import JPsi.MuMu.common.pmvTrees as pmvtrees
treev15reco = pmvtrees.getChains('v15reco')
tree['z'] = treev15reco['z']
tree['data'] = treev15reco['data']

## make histos of pmv vs deta

###############################################################################
# Plot PMV eff. vs photon pt in data for EB
c1 = TCanvas()
canvases.append(c1)

#xbins = [0., 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5]
xbins = [0.1 * i for i in range(26)]

h_Eta = TH1F("h_Eta_data_eb", "#eta^#gamma", len(xbins)-1, array("d", xbins))

selection = " abs(mmgMass-90)<15 & (minDEta > 0.04 | minDPhi > 0.3)"
eventweight = selection
tree["data"].Draw("abs(phoEta)>>" + h_Eta.GetName(), eventweight, '', 
                  maxevents)
htot = h_Eta.Clone(h_Eta.GetName() + "_tot")

eventweight = selection + "& !phoHasPixelMatch"
tree["data"].Draw("abs(phoEta)>>" + h_Eta.GetName(), eventweight, '', 
                  maxevents)
hpass = h_Eta.Clone(h_Eta.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("|#eta^{#gamma}|")
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency")
geff.SetTitle("Run2011A+B, L = 241 pb^{-1}")
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

# xbins = [0.25 * i for i in range(11)]
xbins = [0.1 * i for i in range(26)]

h_Eta = TH1F("h_Eta_mc_eb", "#eta^#gamma", len(xbins)-1, array("d", xbins))

selection = " abs(mmgMass-90)<15 & (minDEta > 0.04 | minDPhi > 0.3)"
## Want to include pileup weights but the 
## TGraphAsymmErrors::BayesDivide then breaks because it gets 
## fractional numbers of events. TODO: fix this
# eventweight = "pileup.weight * (%s)" % selection
eventweight = "1 * (%s)" % selection
tree["z"].Draw("abs(phoEta)>>" + h_Eta.GetName(), eventweight)
htot = h_Eta.Clone(h_Eta.GetName() + "_tot")

# eventweight = "pileup.weight * (%s)" % (selection + "& !phoHasPixelMatch")
#eventweight = "pileup.weight * (%s)" % (selection + "& !phoHasPixelMatch")
eventweight = "1 * (%s)" % (selection + "& !phoHasPixelMatch")
tree["z"].Draw("abs(phoEta)>>" + h_Eta.GetName(), eventweight)
hpass = h_Eta.Clone(h_Eta.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("|#eta^{#gamma}|");
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency");
geff.Draw("ap");
graphs["z"] = geff

latexLabel.DrawLatex(0.15, 0.96, "Powheg/Pythia Z#rightarrow#mu#mu+X")
latexLabel.DrawLatex(0.75, 0.96, "Winter10")
latexLabel.DrawLatex(0.7, 0.2, "Barrel")
c1.Update()

###############################################################################
# Plot PMV eff. vs photon pt in gamma+jet MC for EB with no photon ID
c1 = TCanvas()
canvases.append(c1)

#xbins = [0.05 * i for i in range(51)]
xbins = [0.1 * i for i in range(26)]
# xbins = [0.25 * i for i in range(11)]

andCuts = lambda cuts: "&".join( "(%s)" % c for c in cuts )

idCuts = [
    "phoHoE < 0.05",
    "phoTrackIso < 2 + 0.001 * phoEta",
    "phoEcalIso < 4.2 + 0.003 * phoEta",
    "phoHcalIso < 2.2 + 0.001 * phoEta",
    "phoSigmaIetaIeta < 0.01 | (!phoIsEB & phoSigmaIetaIeta < 0.03)",
]

genCuts = [
    "phoMomPdgId == 22",
]

kineCuts = [
    'phoIsEB'
]

h_Eta = TH1F("h_Eta_gj_eb", "#eta^#gamma", len(xbins)-1, array("d", xbins))

selection = andCuts(genCuts)

tree["gj"].Draw("abs(phoEta)>>" + h_Eta.GetName(), selection)
htot = h_Eta.Clone(h_Eta.GetName() + "_tot")

tree["gj"].Draw("abs(phoEta)>>" + h_Eta.GetName(), selection + "& !phoHasPixelMatch")
hpass = h_Eta.Clone(h_Eta.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("|#eta^{#gamma}|");
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency");
geff.Draw("ap");
graphs["gj_no_id"] = geff

latexLabel.DrawLatex(0.15, 0.96, "#gamma+jet MC, no #gamma ID")
latexLabel.DrawLatex(0.75, 0.96, "Winter10")
latexLabel.DrawLatex(0.7, 0.2, "Barrel")
c1.Update()

###############################################################################
# Plot PMV eff. vs photon pt in gamma+jet MC for EB with partial photon ID
c1 = TCanvas()
canvases.append(c1)

#xbins = [0.05 * i for i in range(51)]
xbins = [0.1 * i for i in range(26)]
# xbins = [0.25 * i for i in range(11)]

andCuts = lambda cuts: "&".join( "(%s)" % c for c in cuts )

idCuts = [
#     "phoHoE < 0.05",
    "phoTrackIso < 2 + 0.001 * phoEta",
    "phoEcalIso < 4.2 + 0.003 * phoEta",
#     "phoHcalIso < 2.2 + 0.001 * phoEta",
#     "phoSigmaIetaIeta < 0.01 | (!phoIsEB & phoSigmaIetaIeta < 0.03)",
]

genCuts = [
    "phoMomPdgId == 22",
]

kineCuts = [
    'phoIsEB'
]

h_Eta = TH1F("h_Eta_gj_partialID_eb", "#eta^#gamma", len(xbins)-1, array("d", xbins))

selection = andCuts(idCuts + genCuts)

tree["gj"].Draw("abs(phoEta)>>" + h_Eta.GetName(), selection)
htot = h_Eta.Clone(h_Eta.GetName() + "_tot")

tree["gj"].Draw("abs(phoEta)>>" + h_Eta.GetName(), selection + "& !phoHasPixelMatch")
hpass = h_Eta.Clone(h_Eta.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("|#eta^{#gamma}|");
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency");
geff.Draw("ap");
graphs["gj_partial_id"] = geff

latexLabel.DrawLatex(0.15, 0.96, "#gamma+jet MC, partial #gamma ID")
latexLabel.DrawLatex(0.75, 0.96, "Winter10")
latexLabel.DrawLatex(0.7, 0.2, "Barrel")
c1.Update()

###############################################################################
# Plot PMV eff. vs photon pt in gamma+jet MC for EB with full photon ID
c1 = TCanvas()
canvases.append(c1)

# xbins = [0.05 * i for i in range(51)]
xbins = [0.1 * i for i in range(26)]
# xbins = [0.25 * i for i in range(11)]

andCuts = lambda cuts: "&".join( "(%s)" % c for c in cuts )

idCuts = [
    "phoHoE < 0.05",
    "phoTrackIso < 2 + 0.001 * phoEta",
    "phoEcalIso < 4.2 + 0.003 * phoEta",
    "phoHcalIso < 2.2 + 0.001 * phoEta",
    "phoSigmaIetaIeta < 0.01 | (!phoIsEB & phoSigmaIetaIeta < 0.03)",
]

genCuts = [
    "phoMomPdgId == 22",
]

kineCuts = [
    'phoIsEB'
]

h_Eta = TH1F("h_Eta_gj_fullID_eb", "#eta^#gamma", len(xbins)-1, array("d", xbins))

selection = andCuts(idCuts + genCuts)

tree["gj"].Draw("abs(phoEta)>>" + h_Eta.GetName(), selection)
htot = h_Eta.Clone(h_Eta.GetName() + "_tot")

tree["gj"].Draw("abs(phoEta)>>" + h_Eta.GetName(), selection + "& !phoHasPixelMatch")
hpass = h_Eta.Clone(h_Eta.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("|#eta^{#gamma}|");
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency");
geff.Draw("ap");
graphs["gj_full_id"] = geff

latexLabel.DrawLatex(0.15, 0.96, "#gamma+jet MC, full #gamma ID")
latexLabel.DrawLatex(0.75, 0.96, "Winter10")
latexLabel.DrawLatex(0.7, 0.2, "Barrel")
c1.Update()

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
graphs["z"].GetYaxis().SetRangeUser(0.65, 1.)

for tag in "gj_no_id gj_partial_id gj_full_id data".split():
    graphs[tag].Draw("p")

legend = TLegend(0.55, 0.6, 0.9, 0.9)
legend.SetFillColor(0)
legend.SetShadowColor(0)
legend.SetBorderSize(0)

legend.AddEntry( graphs["data"], "Data", "pl" )
legend.AddEntry( graphs["z"], "Z#rightarrow#mu#mu#gamma", "pl" )
legend.AddEntry( graphs["gj_no_id"], "#gamma+j no #gamma ID", "pl" )
legend.AddEntry( graphs["gj_partial_id"], "#gamma+j partial #gamma ID", "pl" )
legend.AddEntry( graphs["gj_full_id"], "#gamma+j full #gamma ID", "pl" )

legend.Draw()

c1.SetGridx()
c1.SetGridy()

print 'c1.Print("pmvVsEta_data_z_gj_variousID_v1.eps")'
#c1.Print("pmvVsEta_data_z_gj_variousID_v1.C")

