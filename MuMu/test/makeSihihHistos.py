## TODO:
## * sihih vs photon pt for both EE and EB
## * unbiased template for the EE
## * closure test of the unbiased templates

import sys
import MuMuGammaChain
from ROOT import *

chains = MuMuGammaChain.getChains(MuMuGammaChain.cfiles,
                                  MuMuGammaChain.cpath
                                  )
skipDatasets = ["zg", "zmg"]

def makeSelection(cuts):
  return " & ".join("(%s)" % cut for cut in cuts)

# handy shortcuts
flush = sys.stdout.flush
for ch in chains.values():
    ch.SetAlias("mm", "mmgDimuon")
    ch.SetAlias("mu1", "dau1[mmgDimuon]")
    ch.SetAlias("mu2", "dau2[mmgDimuon]")
    ch.SetAlias("g", "mmgPhoton")

## Preselection
print "Applying preselection ...\n  ",
for name, ch in chains.items():
    print name,; flush()
    lname = "eventList_%s" % name
    ch.Draw(">>%s" % lname, "isBaselineCand")
    ch.SetEventList(gDirectory.Get(lname))

file = TFile("sihihHistos_Nov4ReReco_Fall10.root", "recreate")

###############################################################################
## Make Dimuon invariant mass histos
print "\nMaking dimuon invariant mass histos ...\n  ",; flush()
var = RooRealVar("mass", "mass", 30, 130, "GeV")
var.setBins(100)
sel = "orderByVProb==0"
binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())
for dataset, ch in chains.items():
    if dataset in skipDatasets: continue
    print dataset,; flush()
    ## variable title holds the expression for TTree::Draw
    hname = "h_%s_%s" % (var.GetName(), dataset)
    expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
    ch.Draw(expr, sel, "goff")

###############################################################################
## Make the mmg invariant mass histos
###############################################################################
print "\nMaking mu-mu-gamma invariant mass histos ...\n  ",; flush()

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


## The variable - its title holds the expression for TTree::Draw
var = RooRealVar("mmgMass", "mmgMass", 60, 120, "GeV")
var.setBins(60)
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


###############################################################################
## Make the EB sigma ihih histos
###############################################################################
print "\nMaking EB sigma ihih histos ...\n  ",; flush()

## Cuts
massWindow = ["abs(mmgMass[g] - 91.19) < 4"]
ebCut = ["abs(phoEta[g]) < 1.5"]
myCuts = baselineCuts + massWindow + ebCut

## The variable - its title holds the expression for TTree::Draw
var = RooRealVar("ebSihih", "phoSigmaIetaIeta[g]", 0., 0.03)
var.setBins(30)
binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())
for dataset, ch in chains.items():
    if dataset in skipDatasets: continue
    print dataset,; flush()
    hname = "h_%s_%s" % (var.GetName(), dataset)
    if dataset == "z":
        expr = "%s>>%sfsr(%s)" % (var.GetTitle(), hname, binning)
        ch.Draw(expr, makeSelection(myCuts+ fsrCuts), "goff")
        expr = "%s>>%sjets(%s)" % (var.GetTitle(), hname, binning)
        ch.Draw(expr, makeSelection(myCuts + fsrVeto), "goff")
    else:
        expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
        if dataset == "data38x":
            ch.Draw(expr, makeSelection(myCuts + photonCleaningCuts), "goff")
        else:
            ch.Draw(expr, makeSelection(myCuts), "goff")


###############################################################################
## Make the EE sigma ihih histos
###############################################################################
print "\nMaking EE sigma ihih histos ...\n  ",; flush()

## Cuts
eeCut = ["abs(phoEta[g]) > 1.5"]
myCuts = baselineCuts + massWindow + eeCut

## The variable - its title holds the expression for TTree::Draw
var = RooRealVar("eeSihih", "phoSigmaIetaIeta[g]", 0., 0.1)
var.setBins(20)
for dataset, ch in chains.items():
    if dataset in skipDatasets: continue
    print dataset,; flush()
    hname = "h_%s_%s" % (var.GetName(), dataset)
    binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())
    if dataset == "z":
        expr = "%s>>%sfsr(%s)" % (var.GetTitle(), hname, binning)
        ch.Draw(expr, makeSelection(myCuts + fsrCuts), "goff")
        expr = "%s>>%sjets(%s)" % (var.GetTitle(), hname, binning)
        ch.Draw(expr, makeSelection(myCuts + fsrVeto), "goff")
    else:
        expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
        if dataset == "data38x":
            ch.Draw(expr, makeSelection(myCuts + photonCleaningCuts), "goff")
        else:
            ch.Draw(expr, makeSelection(myCuts), "goff")




###############################################################################
## Make EB sihih vs DR profiles
###############################################################################
print "\nMaking EB sigma ihih vs DR profiles ...\n  ",; flush()

## Cuts
isrCuts = [
    "isBaselineCand[mm]",
    "orderByVProb[mm] == 0",
    "60 < mass[mm] & mass[mm] < 120",
    "nPhotons > 0",
    "mmgPhoton == 0", # require the hardest photon in the events
    "abs(phoScEta[g]) < 2.5",
    "abs(phoScEta[g]) < 1.4442 || abs(phoScEta[g]) > 1.566",
    "5 < phoPt[g]",
    "phoGenMatchPdgId[g]==22",    # ISR MC truth
    "phoGenMatchMomPdgId[g]==22", # ISR MC truth
    "phoGenMatchMomStatus[g]==3", # ISR MC truth
    "100 < mmgMass", # FSR veto
    "0.7 < mmgDeltaRNear", # FSR veto
    ]

var = RooRealVar("ebSihihVsDR", "phoSigmaIetaIeta[g]:mmgDeltaRNear", 0., 3.)
var.setBins(150)
binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())

## Do the ISR separately
dataset = "zg"
print dataset,; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(isrCuts + ebCut), "goff profile")

## Do the FSR separately
myCuts = baselineCuts + massWindow + ebCut
dataset = "z"
print dataset + "fsr",; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%sfsr(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(myCuts + fsrCuts), "goff profile")

## Do the real data separately
dataset = "data38x"
print dataset,; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(myCuts + photonCleaningCuts), "goff profile")




###############################################################################
## Make EB sihih vs photon pt profiles
###############################################################################
print "\nMaking EB sigma ihih vs photon pt profiles ...\n  ",; flush()

## Cuts
drUbCut = ["0.1 < mmgDeltaRNear"]

var = RooRealVar("ebSihihVsPt", "phoSigmaIetaIeta[g]:phoPt[g]", 0., 50.)
var.setBins(50)
binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())

## Do the ISR separately
dataset = "zg"
print dataset,; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(isrCuts + ebCut + drUbCut), "goff profile")

## Do the FSR separately
myCuts = baselineCuts + massWindow + ebCut + drUbCut
dataset = "z"
print dataset + "fsr",; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%sfsr(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(myCuts + fsrCuts), "goff profile")

## Do the real data separately
dataset = "data38x"
print dataset,; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(myCuts + photonCleaningCuts), "goff profile")

## Do all the MC samples with proper weights
hname = "prof_%s_mc" % (var.GetName())
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
for dataset, ch in chains.items():
    if dataset in skipDatasets: continue
    print dataset,; flush()
    if dataset in skipDatasets + ["data38x"]: continue
    w = MuMuGammaChain.weight30[dataset]
    ch.Draw(expr, "%f * (%s)" % (w, makeSelection(myCuts)), "goff profile")




###############################################################################
## Make EB sihih vs photon E profiles
###############################################################################
print "\nMaking EB sigma ihih vs photon E profiles ...\n  ",; flush()

## Cuts
drUbCut = ["0.1 < mmgDeltaRNear"]

var = RooRealVar("ebSihihVsE", "phoSigmaIetaIeta[g]:phoPt[g]*TMath::CosH(phoEta[g])", 0., 100.)
var.setBins(100)
binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())

## Do the ISR separately
dataset = "zg"
print dataset,; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(isrCuts + ebCut + drUbCut), "goff profile")

## Do the FSR separately
myCuts = baselineCuts + massWindow + ebCut + drUbCut
dataset = "z"
print dataset + "fsr",; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%sfsr(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(myCuts + fsrCuts), "goff profile")

## Do the real data separately
dataset = "data38x"
print dataset,; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(myCuts + photonCleaningCuts), "goff profile")

## Do all the MC samples with proper weights
hname = "prof_%s_mc" % (var.GetName())
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
for dataset, ch in chains.items():
    if dataset in skipDatasets: continue
    print dataset,; flush()
    if dataset in skipDatasets + ["data38x"]: continue
    w = MuMuGammaChain.weight30[dataset]
    ch.Draw(expr, "%f * (%s)" % (w, makeSelection(myCuts)), "goff profile")




###############################################################################
## Make EE sihih vs DR profiles
###############################################################################
print "\nMaking EE sigma ihih vs DR profiles ...\n  ",; flush()

var = RooRealVar("eeSihihVsDR", "phoSigmaIetaIeta[g]:mmgDeltaRNear", 0., 3.)
var.setBins(150)
binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())

## Do the ISR separately
dataset = "zg"
print dataset,; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(isrCuts + eeCut), "goff profile")

myCuts = baselineCuts + massWindow + eeCut

## Do the FSR signal separately
dataset = "z"
print dataset + "fsr",; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%sfsr(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(myCuts + fsrCuts), "goff profile")

## Do the real data separately
dataset = "data38x"
print dataset,; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(myCuts + photonCleaningCuts), "goff profile")

## Do all the MC samples with proper weights
hname = "prof_%s_mc" % (var.GetName())
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
for dataset, ch in chains.items():
    if dataset in skipDatasets: continue
    print dataset,; flush()
    if dataset in skipDatasets + ["data38x"]: continue
    w = MuMuGammaChain.weight30[dataset]
    ch.Draw(expr, "%f * (%s)" % (w, makeSelection(myCuts)), "goff profile")



###############################################################################
## Make EE sihih vs photon pt profiles
###############################################################################
print "\nMaking EE sigma ihih vs photon pt profiles ...\n  ",; flush()

var = RooRealVar("eeSihihVsPt", "phoSigmaIetaIeta[g]:phoPt[g]", 0., 50.)
var.setBins(50)
binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())

## Do the ISR separately
dataset = "zg"
print dataset,; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(isrCuts + eeCut + drUbCut), "goff profile")

## Do the FSR separately
myCuts = baselineCuts + massWindow + eeCut + drUbCut
print dataset + "fsr",; flush()
dataset = "z"
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%sfsr(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(myCuts + fsrCuts), "goff profile")

## Do the real data separately
dataset = "data38x"
print dataset,; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(myCuts + photonCleaningCuts), "goff profile")

## Do all the MC samples with proper weights
hname = "prof_%s_mc" % (var.GetName())
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
for dataset, ch in chains.items():
    if dataset in skipDatasets: continue
    print dataset,; flush()
    if dataset in skipDatasets + ["data38x"]: continue
    w = MuMuGammaChain.weight30[dataset]
    ch.Draw(expr, "%f * (%s)" % (w, makeSelection(myCuts)), "goff profile")




###############################################################################
## Make EE sihih vs photon E profiles
###############################################################################
print "\nMaking EE sigma ihih vs photon E profiles ...\n  ",; flush()

var = RooRealVar("eeSihihVsE", "phoSigmaIetaIeta[g]:phoPt[g]*TMath::CosH(phoEta[g])", 0., 100.)
var.setBins(100)
binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())

## Do the ISR separately
dataset = "zg"
print dataset,; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(isrCuts + eeCut + drUbCut), "goff profile")

## Do the FSR separately
myCuts = baselineCuts + massWindow + eeCut + drUbCut
print dataset + "fsr",; flush()
dataset = "z"
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%sfsr(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(myCuts + fsrCuts), "goff profile")

## Do the real data separately
dataset = "data38x"
print dataset,; flush()
hname = "prof_%s_%s" % (var.GetName(), dataset)
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
chains[dataset].Draw(expr, makeSelection(myCuts + photonCleaningCuts), "goff profile")

## Do all the MC samples with proper weights
hname = "prof_%s_mc" % (var.GetName())
expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
for dataset, ch in chains.items():
    if dataset in skipDatasets: continue
    print dataset,; flush()
    if dataset in skipDatasets + ["data38x"]: continue
    w = MuMuGammaChain.weight30[dataset]
    ch.Draw(expr, "%f * (%s)" % (w, makeSelection(myCuts)), "goff profile")




###############################################################################
## Make the unbiased EB sigma ihih histos
###############################################################################
print "\nMaking unbiased EB sigma ihih histos ...\n  ",; flush()

## Cuts
ubCuts = [
    "mmgDeltaRNear > 0.1",
    "phoPt[g] > 10"
    ]

myCuts = baselineCuts + massWindow + ebCut + ubCuts

## The variable - its title holds the expression for TTree::Draw
var = RooRealVar("ubebSihih", "phoSigmaIetaIeta[g]", 0., 0.03)
var.setBins(30)
for dataset, ch in chains.items():
    if dataset in skipDatasets: continue
    print dataset,; flush()
    hname = "h_%s_%s" % (var.GetName(), dataset)
    binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())
    if dataset == "z":
        expr = "%s>>%sfsr(%s)" % (var.GetTitle(), hname, binning)
        ch.Draw(expr, makeSelection(myCuts + fsrCuts), "goff")
        expr = "%s>>%sjets(%s)" % (var.GetTitle(), hname, binning)
        ch.Draw(expr, makeSelection(myCuts + fsrVeto), "goff")
    else:
        expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
        if dataset == "data38x":
            ch.Draw(expr, makeSelection(myCuts + photonCleaningCuts), "goff")
        else:
            ch.Draw(expr, makeSelection(myCuts), "goff")
print




###############################################################################
## Make the unbiased EE sigma ihih histos
###############################################################################
print "\nMaking unbiased EE sigma ihih histos ...\n  ",; flush()

## Cuts
ubCuts = [
    "mmgDeltaRNear > 0.1",
    "phoPt[g] > 10"
    ]

myCuts = baselineCuts + massWindow + ebCut + ubCuts

## The variable - its title holds the expression for TTree::Draw
var = RooRealVar("ubebSihih", "phoSigmaIetaIeta[g]", 0., 0.05)
var.setBins(50)
for dataset, ch in chains.items():
    if dataset in skipDatasets: continue
    print dataset,; flush()
    hname = "h_%s_%s" % (var.GetName(), dataset)
    binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())
    if dataset == "z":
        expr = "%s>>%sfsr(%s)" % (var.GetTitle(), hname, binning)
        ch.Draw(expr, makeSelection(myCuts + fsrCuts), "goff")
        expr = "%s>>%sjets(%s)" % (var.GetTitle(), hname, binning)
        ch.Draw(expr, makeSelection(myCuts + fsrVeto), "goff")
    else:
        expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
        if dataset == "data38x":
            ch.Draw(expr, makeSelection(myCuts + photonCleaningCuts), "goff")
        else:
            ch.Draw(expr, makeSelection(myCuts), "goff")
print




file.Write()
# file.Close()


if __name__ == "__main__": import user
