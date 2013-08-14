import sys
from ROOT import *
import MuMuGammaChain

chains = MuMuGammaChain.getChains(MuMuGammaChain.cfiles,
                                  MuMuGammaChain.cpath
                                  )
for ch in chains.values():
    ch.SetAlias("g", "mmgPhoton")
    ch.SetAlias("mu1", "dau1[mmgDimuon]")
    ch.SetAlias("mu2", "dau2[mmgDimuon]")
    ch.SetAlias("mm", "mmgDimuon")

## Preselection
print "Applying preselection ...\n  ",
for name, ch in chains.items():
    print name,; flush()
    lname = "eventList_%s" % name
    ch.Draw(">>%s" % lname, "isBaselineCand")
    ch.SetEventList(gDirectory.Get(lname))

file = TFile("pixelMatchHistos_Nov4ReReco_Fall10.root", "recreate")

## Cuts
baselineCuts = [
    "isBaselineCand[mm]",
    "orderByVProb[mm] == 0",
    "40 < mass[mm] & mass[mm] < 85",
    "nPhotons > 0",
    "mmgPhoton == 0", # require the hardest photon in the events
    "abs(phoScEta[g]) < 2.5",
    "abs(phoScEta[g]) < 1.4442 || abs(phoScEta[g]) > 1.566",
    "5 < phoPt[g]",
    "60 < mmgMass & mmgMass < 120",
    "mmgDeltaRNear < 1",
    ]

fsrCuts = [
    "phoGenMatchPdgId[g] == 22",
    "abs(phoGenMatchMomPdgId[g]) == 13",
    ]

fsrVeto = [ "!(%s)" % makeSelection(fsrCuts) ]

photonCleaningCuts = [
  "phoSeedRecoFlag[g] != 2",       # EcalRecHit::kOutOfTime = 2
  "phoSeedSeverityLevel[g] != 4",  # EcalSeverityLevelAlgo::kWeird = 4
  "phoSeedSeverityLevel[g] != 5",  # EcalSeverityLevelAlgo::kBad = 5
  "phoSeedSwissCross[g] < 0.95",   # extra spike cleaning check
]

###############################################################################
## Make the eta spectrum histos
###############################################################################
print "\nMaking eta spectrum histos ...\n  ",; flush()

## The variable - its title holds the expression for TTree::Draw
var = RooRealVar("phoEta", "phoEta[g]", -4, 4)
var.setBins(16)
binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())
for dataset, ch in chains.items():
    if dataset in skipDatasets: continue
    print dataset,; flush()
    hname = "h_%s_%s" % (var.GetName(), dataset)
    ## Update the preselection of events
    #lname = "eventList_%s_%s" % (var.GetName(), dataset)
    #ch.Draw(">>" + lname, makeSelection(baselineCuts))
    #ch.SetEventList(gDirectory.Get(lname))
    if dataset == "z":
        ## Make separate plots for FSR and the rest
        expr = "%s>>%sfsr(%s)" % (var.GetTitle(), hname, binning)
        ch.Draw(expr, makeSelection(baselineCuts + fsrCuts), "goff")
        expr = "%s>>%sjets(%s)" % (var.GetTitle(), hname, binning)
        ch.Draw(expr, makeSelection(baselineCuts + fsrVeto), "goff")
    else:
        expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
        if dataset == "data38x":
            ch.Draw(expr, makeSelection(baselineCuts + photonCleaningCuts), "goff")
        else:
            ch.Draw(expr, makeSelection(baselineCuts), "goff")
 ]

file.Write()

