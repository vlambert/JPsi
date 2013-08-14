from makeFsrHistos import *
# gROOT.LoadMacro("resolutionErrors.C")
# selAll  = lyonSel["all"] + "& 87 < mmgMass & mmgMass < 95"
# selFake = lyonSel["fake"] + "& 87 < mmgMass & mmgMass < 95"
selExtra =  "& 87 < mmgMass & mmgMass < 95"
selAll  = templateSel["all"] + selExtra
selFake = templateSel["fake"] + selExtra
ch.Draw("phoPt[g]>>hdata(25,0,100)", selAll)
chainMC.Draw("phoPt[g]>>hmc(25,0,100)", selAll)
chainMC.Draw("phoPt[g]>>hmcfake(25,0,100)",selFake)

hdata = gDirectory.Get("hdata")
hmc = gDirectory.Get("hmc")
hmcfake = gDirectory.Get("hmcfake")

hmc.Scale(2.798e-3)
hmcfake.Scale(2.798e-3)

for h in [hdata, hmc, hmcfake]:
  h.SetStats(0)
  h.SetTitle("")
  h.GetXaxis().SetTitle("P_{#perp}  (#gamma) GeV/c")
  h.GetYaxis().SetTitle("Events / 4 GeV/c")

hmc.SetLineColor(kCyan)
hmc.SetFillColor(kCyan)

hmcfake.SetLineColor(kRed)
hmcfake.SetFillColor(kRed)

hmc.Draw()
hmcfake.Draw("same")
hdata.Draw("same ex")

c1 = gROOT.GetListOfCanvases()[0]
c1.RedrawAxis()
