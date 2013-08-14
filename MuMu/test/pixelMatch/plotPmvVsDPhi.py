import os
from ROOT import *
from array import array
from JPsi.MuMu.common.pmvTrees import getChains

#weight = {
    #"data": 1.,
    #"z"  : 0.030541912803076,
    #"qcd": 0.10306919044126,
    #"w"  : 0.074139194512438,
    #"tt" : 0.005083191122289,
#}

tree = getChains('v15reco')

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

###############################################################################
# Plot PMV eff. vs minDPhi in data for EB
c1 = TCanvas()
c1.SetGridx()
c1.SetGridy()
canvases.append(c1)

# xbins = [0., 0.01, 0.02, 0.03, 0.04, 0.06, 0.1, 1.]
xbins = [0.002 * i for i in range(20)]
xbins.extend( [0.04 + 0.02 * i for i in range(24)] )
xbins.extend( [0.5  + 0.05 * i for i in range(10)] )

h_DPhi = TH1F("h_DPhi_data_eb", "min #Delta #eta (#mu, #gamma)", len(xbins)-1, array("d", xbins))

tree["data"].Draw("minDPhi>>" + h_DPhi.GetName(), "phoIsEB & abs(mmgMass-90)<15")
htot = h_DPhi.Clone(h_DPhi.GetName() + "_tot")

tree["data"].Draw("minDPhi>>" + h_DPhi.GetName(), "phoIsEB & abs(mmgMass-90)<15 & !phoHasPixelMatch")
hpass = h_DPhi.Clone(h_DPhi.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("min#Delta#phi(#mu,#gamma)")
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency")
geff.SetTitle("Dec22ReReco, L = 35.9 pb^{-1}")
geff.Draw("ap")
graphs.append(geff)

latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2011")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
latexLabel.DrawLatex(0.7, 0.2, "Barrel")
c1.SetName( "pmvEff_vs_DPhi_data_EB" )
c1.Update()


###############################################################################
# Plot PMV eff. vs minDPhi in MC for EB
c1 = TCanvas()
c1.SetGridx()
c1.SetGridy()
canvases.append(c1)

xbins = [0.002 * i for i in range(20)]
xbins.extend( [0.04 + 0.02 * i for i in range(24)] )
xbins.extend( [0.5  + 0.05 * i for i in range(10)] )

h_DPhi = TH1F("h_DPhi_mc_eb", "min #Delta #eta (#mu, #gamma)", len(xbins)-1, array("d", xbins))

tree["z"].Draw("minDPhi>>" + h_DPhi.GetName(), "phoIsEB & abs(mmgMass-90)<15")
htot = h_DPhi.Clone(h_DPhi.GetName() + "_tot")

tree["z"].Draw("minDPhi>>" + h_DPhi.GetName(), "phoIsEB & abs(mmgMass-90)<15 & !phoHasPixelMatch")
hpass = h_DPhi.Clone(h_DPhi.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("min#Delta#phi(#mu,#gamma)");
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency");
geff.Draw("ap");
graphs.append(geff)

latexLabel.DrawLatex(0.15, 0.96, "Powheg/Pythia Z#rightarrow#mu#mu+X")
latexLabel.DrawLatex(0.75, 0.96, "Summer11 S4")
latexLabel.DrawLatex(0.7, 0.2, "Barrel")
c1.SetName( "pmvEff_vs_DPhi_MC_EB" )
c1.Update()


###############################################################################
# Plot PMV eff. vs minDPhi in data for EE
c1 = TCanvas()
c1.SetGridx()
c1.SetGridy()
canvases.append(c1)

# xbins = [0., 0.02, 0.04, 0.1, 1.]
xbins = [0.002 * i for i in range(20)]
xbins.extend( [0.04 + 0.02 * i for i in range(24)] )
xbins.extend( [0.5  + 0.05 * i for i in range(10)] )

h_DPhi = TH1F("h_DPhi_data_ee", "min #Delta #eta (#mu, #gamma)", len(xbins)-1, array("d", xbins))

tree["data"].Draw("minDPhi>>" + h_DPhi.GetName(), "!phoIsEB & abs(mmgMass-90)<15")
htot = h_DPhi.Clone(h_DPhi.GetName() + "_tot")

tree["data"].Draw("minDPhi>>" + h_DPhi.GetName(), "!phoIsEB & abs(mmgMass-90)<15 & !phoHasPixelMatch")
hpass = h_DPhi.Clone(h_DPhi.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("min#Delta#phi(#mu,#gamma)")
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency")
geff.SetTitle("Dec22ReReco, L = 35.9 pb^{-1}")
geff.Draw("ap")
graphs.append(geff)

latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2011")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
latexLabel.DrawLatex(0.7, 0.2, "Endcaps")
c1.SetName( "pmvEff_vs_DPhi_data_EE" )
c1.Update()


###############################################################################
# Plot PMV eff. vs minDPhi in MC for EE
c1 = TCanvas()
c1.SetGridx()
c1.SetGridy()
canvases.append(c1)

xbins = [0.002 * i for i in range(20)]
xbins.extend( [0.04 + 0.02 * i for i in range(24)] )
xbins.extend( [0.5  + 0.05 * i for i in range(10)] )

h_DPhi = TH1F("h_DPhi_mc_ee", "min #Delta #eta (#mu, #gamma)", len(xbins)-1, array("d", xbins))

tree["z"].Draw("minDPhi>>" + h_DPhi.GetName(), "!phoIsEB & abs(mmgMass-90)<15")
htot = h_DPhi.Clone(h_DPhi.GetName() + "_tot")

tree["z"].Draw("minDPhi>>" + h_DPhi.GetName(), "!phoIsEB & abs(mmgMass-90)<15 & !phoHasPixelMatch")
hpass = h_DPhi.Clone(h_DPhi.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("min#Delta#phi(#mu,#gamma)");
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency");
geff.Draw("ap");
graphs.append(geff)

latexLabel.DrawLatex(0.15, 0.96, "Powheg/Pythia Z#rightarrow#mu#mu+X")
latexLabel.DrawLatex(0.75, 0.96, "Summer11 S4")
latexLabel.DrawLatex(0.7, 0.2, "Endcaps")

c1.SetName( "pmvEff_vs_DPhi_MC_EE" )
c1.Update()

for c in canvases:
    i = canvases.index(c)
    c.SetWindowPosition(10+20*i, 10+20*i)
    c.Print( c.GetName() + ".eps" )

#geff_DPhi_mc.BayesDivide(h_DPhi_mc_pass, h_DPhi_mc_tot)

#tree["z"].Draw("minDPhi>>h_DPhi", "isEB & abs(mmgMass-90)<15")
#h_DPhi_z_tot = h_DPhi.Clone("h_DPhi_z_tot")

#tree["z"].Draw("minDPhi>>h_DPhi", "isEB & abs(mmgMass-90)<15 & !phoHasPixelMatch")
#h_DPhi_z_pass = h_DPhi.Clone("h_DPhi_z_pass")

#geff.SetTitle("POWHEG+Pythia Z#rightarrow#mu#mu Fall10 MC, FSR events");
