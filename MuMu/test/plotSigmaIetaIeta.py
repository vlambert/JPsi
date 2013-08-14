from makeFsrHistos import *
# gROOT.LoadMacro("resolutionErrors.C")
# selAll  = lyonSel["all"] + "& 87 < mmgMass & mmgMass < 95"
# selFake = lyonSel["fake"] + "& 87 < mmgMass & mmgMass < 95"
selExtra =  "& 87 < mmgMass & mmgMass < 95 & abs(phoEta[g]) > 1.5 & phoPt[g] < 10"
selAll  = templateSel["all"] + selExtra
selFake = templateSel["fake"] + selExtra
binning = "(20,0,0.1)"
ch.Draw("phoSigmaIetaIeta[g]>>hdata" + binning, selAll)
chainMC.Draw("phoSigmaIetaIeta[g]>>hmc" + binning, selAll)
chainMC.Draw("phoSigmaIetaIeta[g]>>hmcfake" + binning, selFake)

hdata = gDirectory.Get("hdata")
hmc = gDirectory.Get("hmc")
hmcfake = gDirectory.Get("hmcfake")

hmc.Scale(2.798e-3)
hmcfake.Scale(2.798e-3)

binWidth = hmc.GetBinWidth(1)

for h in [hdata, hmc, hmcfake]:
  h.SetStats(0)
  h.SetTitle("")
  h.GetXaxis().SetTitle("#sigma_{i#etai#eta}")
  h.GetYaxis().SetTitle("Events / %.2g" % binWidth)

hmc.SetLineColor(kCyan)
hmc.SetFillColor(kCyan)

hmcfake.SetLineColor(kRed)
hmcfake.SetFillColor(kRed)

hmc.Draw()
hmcfake.Draw("same")
hdata.Draw("same ex")

c1 = gROOT.GetListOfCanvases()[0]
c1.RedrawAxis()
