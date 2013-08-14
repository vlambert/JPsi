from basicRoot import *
from MuMuGammaChain import chain as ch
from math import sqrt

# handy shortcut
ch.SetAlias("mm", "mmgDimuon")
ch.SetAlias("g", "mmgPhoton")
canvases = []
legends = []
plotNames = {}
gROOT.ProcessLine(".L tdrstyle.C")
gStyle.SetOptTitle(kFALSE)
gStyle.SetOptStat(kFALSE)
gStyle.SetTitleOffset(1.2, "Y")
gStyle.SetPadLeftMargin(.12)



def customizeTH2(h, xname, yname):
  h.SetMarkerStyle(20)
  h.GetXaxis().SetTitle(xname)
  h.GetYaxis().SetTitle(yname)

def makeTHStack(hlist):
  hs = THStack()
  for h in hlist:
    h.SetFillColor(h.GetLineColor())
    hs.Add(h)
  return hs

def drawTH1s(histos):
  ymax = 0.
  keys = ["r", "s"]
  for k in keys:
    if histos[k].GetMaximum() > ymax:
      ymax = histos[k].GetBinContent(histos[k].GetMaximumBin())
  ymax = ymax + sqrt(ymax) + 1
  for k in keys:
    histos[k].SetMaximum(ymax)
    histos[k].SetMinimum( min( 0.01, histos[k].GetMinimum() ) )
  histos["r"].Draw()
  histos["s"].Draw("ex0 same")
  legend = TLegend(0.6,0.7,0.85,0.85)
  legend.AddEntry(histos["s"], "FSR", "p").SetTextColor(kRed)
  legend.AddEntry(histos["r"], "loose EM", "l")
  legend.SetLineColor(kWhite)
  legend.SetFillColor(kWhite)
  legend.Draw()
  c = canvases[-1]
  c.RedrawAxis()
  plotNames[c] = histos["all"].GetName()
  legends.append(legend)

def drawTH2s(histos, xRange=None, yRange=None):
  if xRange:
    histos["r"].GetXaxis().SetRangeUser(xRange[0], xRange[1])
    histos["s"].GetXaxis().SetRangeUser(xRange[0], xRange[1])
  if yRange:
    histos["r"].GetYaxis().SetRangeUser(yRange[0], yRange[1])
    histos["s"].GetYaxis().SetRangeUser(yRange[0], yRange[1])
  histos["r"].Draw()
  histos["s"].Draw("same")
  legend = TLegend(0.6,0.7,0.85,0.85)
  legend.AddEntry(histos["s"], "FSR", "p").SetTextColor(kRed)
  legend.AddEntry(histos["r"], "loose EM", "p")
  legend.SetLineColor(kWhite)
  legend.SetFillColor(kWhite)
  legend.Draw()
  c = canvases[-1]
  c.RedrawAxis()
  plotNames[c] = histos["all"].GetName()
  legends.append(legend)

def deleteExistingHisto(hname):
  if gDirectory.Get(hname):
    print "Replacing existing histogram", hname, "..."
    gDirectory.Get(hname).Delete()

# Preselection
ch.Draw(">>elist", "isZCand[mm] & charge[mm]==0 & nPhotons > 0 & backToBack < 0.95")
ch.SetEventList(gDirectory.Get("elist"))

sel = "isZCand[mm] & 45<mass[mm] & 45<mmgMass & mmgPhoton==0"
# selMoreSignal = "mmgDeltaRNear < 1 & mass[mm] < 85"
# selMoreSignal = "mass[mm] < 85"
selLooseFsr = "mass[mm] < 80 & 60 < mmgMass & mmgMass < 120"
selTight = " & ".join("""
phoEcalIso[g] < 4.2 + 0.004 * phoPt[g]
phoHcalIso[g] < 2.2 + 0.001 * phoPt[g]
phoTrackIso[g] < 2.0 + 0.001 * phoPt[g]
phoHadronicOverEm[g] < 0.05
((abs(phoEta[g]) > 1.5 & phoSigmaIetaIeta[g] < 0.026) || (phoSigmaIetaIeta[g] < 0.013))
""".split("\n")[1:-1])
selNear = "mmgDeltaRNear < 1.0"
selMoreSignal = "{l} & ({t} | {n})".format(l=selLooseFsr, t=selTight, n=selNear)
selOthers = "!({s})".format(s=selMoreSignal)

selSig = sel+ "& {s}".format(s=selMoreSignal)
selRest = sel + "& {s}".format(s=selOthers)

def plotXY(xy = "mmgMass:mass[mm]",
           hname = "mass3vs2",
           xname = "m(#mu#mu) (GeV/c^{2})",
           yname = "m(#mu#mu#gamma) (GeV/c^{2})",
           binning = ""
           ):

  if len(binning) > 0 and binning[0] != "(":
    binning = "(" + binning + ")"

  # Plot Mass(mmg) vs Mass(mm) for background
  deleteExistingHisto(hname)
  ch.Draw(xy + ">>" + hname + binning, sel)
  h = gDirectory.Get(hname)
  customizeTH2(h, xname, yname)
  h.DrawCopy()

  deleteExistingHisto(hname+"S")
  ch.Draw(xy + ">>" + hname + "S" + binning, selSig, "same")
  hs = gDirectory.Get(hname + "S")
  customizeTH2(hs, xname, yname)
  hs.SetMarkerColor(kRed)
  hs.SetLineColor(kRed)
  hs.DrawCopy("same")

  deleteExistingHisto(hname+"R")
  ch.Draw(xy + ">>" + hname + "R" + binning, selRest, "same")
  hr = gDirectory.Get(hname + "R")
  customizeTH2(hr, xname, yname)
  hs.DrawCopy("same")

  return {"all": h, "s": hs, "r": hr}


def savePlots(prefix = "hZGamma_", extension = "png"):
  """savePlots(prefix = "hZGamma_", extension = "png")"""
  for c in canvases:
    c.Print(prefix + plotNames[c] + "." + extension)

# 15
canvases.append(TCanvas())
hMmgMass = plotXY("mmgMass",
  "mmgMass",
  "m(#mu#mu#gamma) (GeV/c^{2})",
  "Events / 3 GeV",
  "(20,60,120)"
  )
hs = hMmgMass["s"]
hr = hMmgMass["r"]
hr.SetFillStyle(0)
hs.SetFillStyle(3002)
hs.SetFillColor(kRed)
hs.Draw("ex0 hist")
hr.Draw("ex0 hist same")
fit = TF1("fit2", "gaus(0)", 85, 95)
fit.SetLineColor(kRed)
fit.FixParameter(0,0)
hs.SetStats()
hs.Fit(fit)
hs.Draw("ex0 same")

canvases[-1].RedrawAxis()
plotNames[canvases[-1]] = "hMMGFsrMass"

# legend = TLegend(0.72,0.65,0.88,0.85)
# legend.AddEntry(hs, "FSR", "lpf").SetTextColor(kRed)
# legend.AddEntry(hr, "loose EM", "lp")
# legend.SetLineColor(kWhite)
# legend.SetFillColor(kWhite)
# legend.Draw()

# # 16
# canvases.append(TCanvas())
# hDimuonMass = plotXY("mass[mm]",
#   "hDimuonMass",
#   "m(#mu#mu) (GeV/c^{2})",
#   "Events / 4 GeV",
#   "(15,60,120)"
#   )
# drawTH1s(hDimuonMass)

# order canvases

ch.Draw("mmgMass>>h1(45,60,120)", selSig)
ch.Draw("mmgMass>>h5(45,60,120)", selSig + "& phoPt[g]>5")
ch.Draw("mmgMass>>h10(45,60,120)", selSig + "& phoPt[g]>10")

h1  = gROOT.Get("h1")
h5  = gROOT.Get("h5")
h10 = gROOT.Get("h10")

h5.SetFillColor(kRed)
h10.SetFillColor(kBlue)

h1.Draw()
h5.Draw("same")
h10.Draw("same")

legend = TLegend(0.72,0.65,0.88,0.85)
legend.AddEntry(h1,  "p_{#perp}  (#gamma) #in [1, 5] GeV/c")
legend.AddEntry(h5,  "p_{#perp}  (#gamma) #in [5, 10] GeV/c")
legend.AddEntry(h10, "p_{#perp}  (#gamma) > 10 GeV/c")
legend.SetLineColor(kWhite)
legend.SetFillColor(kWhite)
legend.Draw()

from ROOT import TLatex
l = TLatex()
l.DrawLatex(65,10, "L = 2.9 pb^{-1}")

for c in canvases:
  i = canvases.index(c)
  c.SetWindowPosition(10+20*i, 10+20*i)

if __name__ == "__main__": import user
