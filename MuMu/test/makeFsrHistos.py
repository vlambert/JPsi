from basicRoot import *
from MuMuGammaChain import *
from math import sqrt

chain = getChains(files, path)
bchain = getChains(bfiles, bpath)

# handy shortcuts
for ch in chain.values() + bchain.values():
  ch.SetAlias("mm", "mmgDimuon")
  ch.SetAlias("mu1", "dau1[mmgDimuon]")
  ch.SetAlias("mu2", "dau2[mmgDimuon]")
  ch.SetAlias("g", "mmgPhoton")

ch = chain["data36x"]
canvases = []
legends = []
plotNames = {}
gROOT.ProcessLine(".L tdrstyle.C")
# gStyle.SetOptTitle(kFALSE)
# gStyle.SetOptStat(kFALSE)
gStyle.SetTitleOffset(1.2, "Y")
gStyle.SetPadLeftMargin(.12)
isRealData = False

fsrCuts = [
  "phoGenMatchPdgId[g] == 22",
  "abs(phoGenMatchMomPdgId[g]) == 13",
  ]

isrCuts = [
  "phoGenMatchPdgId[g] == 22",
  "phoGenMatchMomPdgId[g] != 0",
  "abs(phoGenMatchMomPdgId[g]) < 6 || phoGenMatchMomPdgId[g] == 23",
  ]

def deleteExistingHisto(hname):
  if gDirectory.Get(hname):
    print "Replacing existing histogram", hname, "..."
    gDirectory.Get(hname).Delete()

def savePlots(prefix = "hZGamma_", extension = "png"):
  """savePlots(prefix = "hZGamma_", extension = "png")"""
  for c in canvases:
    c.Print(prefix + plotNames[c] + "." + extension)

def makeSelection(cuts):
  return " & ".join("(%s)" % cut for cut in cuts)

def makeHisto(xy = "mmgMass",
              hname = "mmgMass",
              xname = "m(#mu#mu#gamma) (GeV/c^{2})",
              yname = "Events / GeV",
              binning = "60,60,120",
              selection = ""
              ):

  if len(binning) > 0 and binning[0] != "(":
    binning = "(" + binning + ")"

  deleteExistingHisto(hname)
  ch.Draw(xy + ">>" + hname + binning, selection, "goff")
  h = gDirectory.Get(hname)
  h.SetMarkerStyle(20)
  h.GetXaxis().SetTitle(xname)
  h.GetYaxis().SetTitle(yname)

  return h

def makeSelections(cuts, isrCuts=isrCuts, fsrCuts=fsrCuts):
  selections = {}
  selections["all"] = makeSelection(cuts)
  selections["fsr"] = makeSelection(cuts + fsrCuts)
  selections["isr"] = makeSelection(cuts + isrCuts)
  selections["fake"] = selections["all"] + " & !(%s) & !(%s)" % \
    (selections["fsr"], selections["isr"])
  return selections

# Preselection
ch.Draw(">>elist", "isVbtfBaselineCand[mm]")
ch.SetEventList(gDirectory.Get("elist"))

if 1:
    for iName, ch in chain.items():
        ch.Draw(">>elist" + iName, "isVbtfBaselineCand[mm]")
        ch.SetEventList(gDirectory.Get("elist_" + iName))

lyonCuts = [
#   "backToBack < 0.95",
  "nPhotons > 0",
  "abs(phoScEta[g]) < 2.5",
  "abs(phoScEta[g]) < 1.4442 || abs(phoScEta[g]) > 1.566",
  "mass[mm] > 40",
  "mass[mm] < 80",
  "phoPt[g] > 10",
  "mmgDeltaRNear < 0.8",
  "mmgMass > 60",
  "mmgMass < 120",
  ]

cuts = [
#   "backToBack < 0.95",
  "nPhotons > 0",
  "abs(phoScEta[g]) < 2.5",
  "abs(phoEta[g]) < 1.4442 || abs(phoEta[g]) > 1.566",
  "mass[mm] > 40",
  "mass[mm] < 85",
  "mmgMass > 60",
  "mmgMass < 120",
  ]

photonIdCuts = [
  "phoPt[g] > 10",
  "phoEcalIso[g] < 4.2 + 0.004 * phoPt[g]",
  "phoHcalIso[g] < 2.2 + 0.001 * phoPt[g]",
  "phoTrackIso[g] < 2.0 + 0.001 * phoPt[g]",
  "phoHadronicOverEm[g] < 0.05",
  "((abs(phoEta[g]) > 1.5 & phoSigmaIetaIeta[g] < 0.026) || (phoSigmaIetaIeta[g] < 0.013))",
  ]

# isrCuts = [
#   "nPhotons > 0",
#   "abs(phoScEta[g]) < 2.5",
#   "abs(phoEta[g]) < 1.4442 || abs(phoEta[g]) > 1.566",
#   "abs(mass[mm]-91.19) < 10",
#   "mmgMass > 100",
#   "mmgDeltaRNear > 0.7"
# ]

newCuts = cuts[:] + [
  "phoPt[g] > 5",
  "mmgDeltaRNear < 0.5 | (%s)" % makeSelection(photonIdCuts)
  ]

templateCuts = cuts[:] + [
  "phoPt[g] > 5",
  "mmgDeltaRNear < 1"
  ]

spikeCuts = [
  "phoSeedRecoFlag[g] != 2",       # EcalRecHit::kOutOfTime = 2
  "phoSeedSeverityLevel[g] != 4",  # EcalSeverityLevelAlgo::kWeird = 4
  "phoSeedSeverityLevel[g] != 5",  # EcalSeverityLevelAlgo::kBad = 5
  ]

if isRealData:
  lyonCuts += spikeCuts

isrSihihSel = makeSelections(photonIdCuts[:5] + spikeCuts + isrCuts)
lyonSel = makeSelections(lyonCuts)
# collinearSelections = makeSelections(collinearCuts)
newSel= makeSelections(newCuts)
templateSel = makeSelections(templateCuts)

sel = newSel["fsr"]
hMmgMass = makeHisto("mmgMass", "hMmgMass", "m(#mu#mu#gamma) (GeV/c^{2})", "Events / GeV", "60,60,120", sel)
hPhoPt = makeHisto("phoPt[g]", "hPhoPt", "p_{#perp}^{#gamma}", "Events / 5 GeV", "20,0,100", sel)
hPhoEta = makeHisto("phoEta[g]", "hPhoEta", "#eta^{#gamma}", "Events / 0.5", "12,-3,3", sel)
hDeltaRNear = makeHisto("mmgDeltaRNear", "hDeltaRNear", "min #DeltaR(#mu^{#pm}, #gamma)", "Events / 0.1", "30,0,3", sel)

mcScale = 2.9 * 4998. / 2111268. / 3.
mcScale2 = 0.0027984769557803267 ## from dimuons

if __name__ == "__main__": import user
