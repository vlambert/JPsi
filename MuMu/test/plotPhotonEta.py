from makeFsrHistos import *
# gROOT.LoadMacro("resolutionErrors.C")
# selAll  = lyonSel["all"] + "& 87 < mmgMass & mmgMass < 95"
# selFake = lyonSel["fake"] + "& 87 < mmgMass & mmgMass < 95"
selExtra = "" #"& 87 < mmgMass & mmgMass < 95"
selAll  = templateSel["all"] + selExtra
selFake = templateSel["fake"] + selExtra
binning = "(60,60,120)"
quantity = "mmgMass"
ch.Draw(quantity + ">>hdata" + binning, selAll)
chainMC.Draw(quantity + ">>hmc" + binning, selAll)
chainMC.Draw(quantity + ">>hmcfake" + binning, selFake)

hdata = gDirectory.Get("hdata")
hmc = gDirectory.Get("hmc")
hmcfake = gDirectory.Get("hmcfake")

hmc.Scale(2.798e-3)
hmcfake.Scale(2.798e-3)

binWidth = hmc.GetBinWidth(1)

for h in [hdata, hmc, hmcfake]:
  h.SetStats(0)
  h.SetTitle("")
  h.GetXaxis().SetTitle("m(#mu#mu#gamma)")
  h.GetYaxis().SetTitle("Events / %.2g GeV" % binWidth)

hmc.SetLineColor(kCyan)
hmc.SetFillColor(kCyan)

hmcfake.SetLineColor(kRed)
hmcfake.SetFillColor(kRed)

hmc.Draw()
hmcfake.Draw("same")
hdata.Draw("same ex")

c1 = gROOT.GetListOfCanvases()[0]
c1.RedrawAxis()
