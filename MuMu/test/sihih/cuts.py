import histos
import common

xnames = histos.histos.keys()
datasets = common.chains.keys()

## Dictionary of dictionaries of 2-tuples
## key1 .. name of plotted variable
## key2 .. label of produced histogram
## value[0] .. dataset key in common.chains, e.g. "z"
## value[1] .. list of strings defining TChain cuts
cuts = {}

## Initialize cuts with empty cuts and labels equal to dataset keys
for x in xnames:
    cuts[x] = {}
    for d in datasets:
        cuts[x][d] = (d, [])


## Define lists of cuts
dimuonCuts = [
    "isBaselineCand",
    "orderByVProb == 0"
    ]

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

mcTruthFsrCuts = [
    "phoGenMatchPdgId[g] == 22",
    "abs(phoGenMatchMomPdgId[g]) == 13",
    ]

mcTruthFsrVeto = [ "!(%s)" % common.makeSelection(mcTruthFsrCuts) ]

photonCleaningCuts = [
  "phoSeedRecoFlag[g] != 2",       # EcalRecHit::kOutOfTime = 2
  "phoSeedSeverityLevel[g] != 4",  # EcalSeverityLevelAlgo::kWeird = 4
  "phoSeedSeverityLevel[g] != 5",  # EcalSeverityLevelAlgo::kBad = 5
  #"phoSeedSwissCross[g] < 0.95",   # extra spike cleaning check
  ]

massWindow = ["abs(mmgMass[g] - 91.19) < 4"]

ebCut = ["abs(phoEta[g]) < 1.5"]
eeCut = ["abs(phoEta[g]) > 1.5"]

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

## Updated version retreived in Dec 10
photonIdCuts = [
    "phoPt[g] > 10",
    "phoEcalIso[g] < 4.2 + 0.006 * phoPt[g]",
    "phoHcalIso[g] < 2.2 + 0.0025 * phoPt[g]",
    "phoTrackIso[g] < 2.0 + 0.001 * phoPt[g]",
    "phoHadronicOverEm[g] < 0.05",
    "((abs(phoEta[g]) > 1.5 & phoSigmaIetaIeta[g] < 0.03) || (phoSigmaIetaIeta[g] < 0.013))",
    "!phoHasPixelSeed", # optional
    ]

ubebCuts = [
    "mmgDeltaRNear > 0.1",
    "phoPt[g] > 10"
    ]

lyonCuts = [
    "abs(phoScEta[g]) < 2.5",
    "abs(phoScEta[g]) < 1.4442 || abs(phoScEta[g]) > 1.566",
    #"phoSeedRecoFlag[g] != 2",       # DATA ONLY! EcalRecHit::kOutOfTime = 2
    #"phoSeedSeverityLevel[g] != 4",  # DATA ONLY! EcalSeverityLevelAlgo::kWeird = 4
    #"phoSeedSeverityLevel[g] != 5",  # DATA ONLY! EcalSeverityLevelAlgo::kBad = 5
    "muIsGlobalMuon[mu1]",
    "muIsGlobalMuon[mu2]",
    "muIsTrackerMuon[mu1]",
    "muIsTrackerMuon[mu2]",
    "muSiHits[mu1] > 10",
    "muSiHits[mu2] > 10",
    "muGlobalNormalizedChi2[mu1] < 10",
    "muGlobalNormalizedChi2[mu2] < 10",
    "abs(muEta[mu1]) < 2.4",
    "abs(muEta[mu2]) < 2.4",
    "muTrackIso[mu1] < 3",
    "muTrackIso[mu2] < 3",
    "min(abs(muEta[mu1]),muEta[mu2]) < 2.1",
    "charge == 0",
    "muPt[mu1] > 10",
    "muPt[mu2] > 10",
    "phoPt[g] > 10",
    "40 <= mass[mm] & mass[mm] <= 80",
    "mmgDeltaRNear <= 0.8",
    "87.2 <= mmgMass && mmgMass <= 95.2",
    "muEcalIso[mmgMuonFar] <= 1.0",
    "muPt[mmgMuonFar] >= 30",
    "muHcalIso[mmgMuonNear] <= 1.0"
    ]


escaleCuts = [
    "isBaselineCand[mm]",
    "orderByVProb[mm] == 0",
    "mass[mm] > 40",
    "mass[mm] < 80", ## originally 85
#     "abs(mmgMass-zMassPdg()) < 4",
    "nPhotons > 0",
    "mmgPhoton == 0", # require the hardest photon in the events
    "abs(phoScEta[g]) < 2.5",
    "abs(phoScEta[g]) < 1.4442 || abs(phoScEta[g]) > 1.566",
    "5 < phoPt[g]", ## originally 5
#     "phoSeedRecoFlag[g] != 2",       # DATA ONLY! EcalRecHit::kOutOfTime = 2
#     "phoSeedSeverityLevel[g] != 4",  # DATA ONLY! EcalSeverityLevelAlgo::kWeird = 4
#     "phoSeedSeverityLevel[g] != 5",  # DATA ONLY! EcalSeverityLevelAlgo::kBad = 5
    "phoSeedSwissCross[g] < 0.95",   # extra spike cleaning check
    "mmgDeltaRNear < 0.5 || (%s)" % common.makeSelection(photonIdCuts),
    ]


ebr9Cuts = ["phoR9[g] < 0.94"] + ebCut
eer9Cuts = ["phoR9[g] < 0.95"] + eeCut

muGenMatchCuts = [
    "muGenPt[mu1] > 0",
    "muGenPt[mu2] > 0"
    ]

genMatchCuts = muGenMatchCuts + [
    "phoGenPt[g] > 0"
    ]

def setFsrCuts(varname, isrCuts, fsrCuts, commonCuts = []):
    ic = isrCuts + commonCuts
    fc = fsrCuts + commonCuts
    for d in datasets:
        if d == "zg":
            cuts[varname][d]          = (d, ic)
        elif d == "z":
            ## cuts[var][label] = (dataset, cuts)
            del cuts[varname][d]
            cuts[varname][d + "fsr" ] = (d, fc + mcTruthFsrCuts)
            cuts[varname][d + "jets"] = (d, fc + mcTruthFsrVeto)
        elif d == "data38x":
            cuts[varname][d]          = (d, fc + photonCleaningCuts)
        else:
            cuts[varname][d]          = (d, fc)


def setProfileCuts(varname, isrCuts, fsrCuts, commonCuts):
    for d in datasets:
        if d == "zg":
            ## cuts[var][label] = (dataset, cuts)
            cuts[varname][d] = (d, isrCuts + commonCuts)
        elif d == "z":
            del cuts[varname][d]
            cuts[varname][d + "fsr"] = (d, fsrCuts + commonCuts + mcTruthFsrCuts)
        elif d == "data38x":
            cuts[varname][d] = (d, fsrCuts + commonCuts + photonCleaningCuts)
        else:
            del cuts[varname][d]


## Dimuon mass selection
for d in datasets:
    cuts["mass"][d] = (d, dimuonCuts)

## FSR spectra
setFsrCuts("mmgMass"  , isrCuts, baselineCuts)
setFsrCuts("mmgMassEB", isrCuts, baselineCuts, ebCut)
setFsrCuts("mmgMassEE", isrCuts, baselineCuts, eeCut)
setFsrCuts("ebSihih", isrCuts + photonIdCuts, baselineCuts + massWindow, ebCut)
setFsrCuts("eeSihih", isrCuts + photonIdCuts, baselineCuts + massWindow, eeCut)
setFsrCuts("phoPt"  , isrCuts + photonIdCuts, baselineCuts + massWindow)
setFsrCuts("phoEta" , isrCuts + photonIdCuts, baselineCuts + massWindow)
setFsrCuts("ubebSihih", isrCuts + photonIdCuts, baselineCuts + massWindow, ebCut + ubebCuts)
setFsrCuts("phoPtEB", isrCuts + photonIdCuts, baselineCuts + massWindow, ebCut)
setFsrCuts("phoPtEE", isrCuts + photonIdCuts, baselineCuts + massWindow, eeCut)
setFsrCuts("phoE"  , isrCuts + photonIdCuts, baselineCuts + massWindow)
setFsrCuts("phoEEB", isrCuts + photonIdCuts, baselineCuts + massWindow, ebCut)
setFsrCuts("phoEEE", isrCuts + photonIdCuts, baselineCuts + massWindow, eeCut)
setFsrCuts("kRatio", isrCuts + photonIdCuts, baselineCuts + massWindow)
setFsrCuts("kRatio2", isrCuts + photonIdCuts, baselineCuts + massWindow)
setFsrCuts("inverseK", isrCuts + photonIdCuts, baselineCuts + massWindow)
setFsrCuts("inverseK2", isrCuts + photonIdCuts, baselineCuts + massWindow)
setFsrCuts("minusLogK", isrCuts + photonIdCuts, baselineCuts + massWindow)
setFsrCuts("minusLogKEB", isrCuts + photonIdCuts, baselineCuts + massWindow, ebCut)
setFsrCuts("minusLogKEE", isrCuts + photonIdCuts, baselineCuts + massWindow, eeCut)
setFsrCuts("minusLogKEBR9", isrCuts + photonIdCuts, baselineCuts + massWindow, ebr9Cuts)
setFsrCuts("minusLogKEER9", isrCuts + photonIdCuts, baselineCuts + massWindow, eer9Cuts)
setFsrCuts("minusLogK2", isrCuts + photonIdCuts, baselineCuts + massWindow)
setFsrCuts("ikReco"    , isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts)
setFsrCuts("ikRecoEB"  , isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts, ebCut)
setFsrCuts("ikRecoEE"  , isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts, eeCut)
setFsrCuts("ikVReco"   , isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts)
setFsrCuts("ikVRecoEB" , isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts, ebCut)
setFsrCuts("ikVRecoEE" , isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts, eeCut)
setFsrCuts("ikVVReco"  , isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts)
setFsrCuts("ikVVRecoEB", isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts, ebCut)
setFsrCuts("ikVVRecoEE", isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts, eeCut)
setFsrCuts("ikRecoOverGen"  , isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts)
setFsrCuts("ikVRecoOverGen" , isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts)
setFsrCuts("ikVVRecoOverGen", isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts)
setFsrCuts("mmMassRecoOverGen" , isrCuts + photonIdCuts, lyonCuts + massWindow + muGenMatchCuts)
setFsrCuts("mmMassVRecoOverGen", isrCuts + photonIdCuts, lyonCuts + massWindow + muGenMatchCuts)
setFsrCuts("mmgMassRecoOverGen" , isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts)
setFsrCuts("mmgMassVRecoOverGen" , isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts)
setFsrCuts("mmgMassVVRecoOverGen" , isrCuts + photonIdCuts, lyonCuts + massWindow + genMatchCuts)

## sihih profiles
setProfileCuts("eeSihihVsDR", isrCuts, baselineCuts + massWindow, eeCut)
