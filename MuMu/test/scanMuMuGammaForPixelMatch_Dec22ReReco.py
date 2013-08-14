import sys
import os
import re

print "Switching to batch mode ..."
sys.argv.append( '-b' )

import ROOT
import JPsi.MuMu.common.MuMuGammaChains as mmgChains


## Configuration
sample = "data39x"
# sample = "z"


ROOT.gROOT.LoadMacro("resolutionErrors.C+")

chains = mmgChains.getChains(mmgChains.dfiles,
                             mmgChains.dpath
                             )

chain = chains[sample]

chain.SetAlias("pt1", "muGenPt[dau1]")
chain.SetAlias("pt2", "muGenPt[dau2]")
chain.SetAlias("eta1", "muGenEta[dau1]")
chain.SetAlias("eta2", "muGenEta[dau2]")
chain.SetAlias("phi1", "muGenPhi[dau1]")
chain.SetAlias("phi2", "muGenPhi[dau2]")
chain.SetAlias("mm", "mmgDimuon")
chain.SetAlias("mu1", "dau1[mmgDimuon]")
chain.SetAlias("mu2", "dau2[mmgDimuon]")
chain.SetAlias("g", "mmgPhoton")
chain.SetAlias("mnear", "mmgMuonNear")
chain.SetAlias("mfar", "mmgMuonFar")

chain.SetAlias(
    "minDEta",
    "min(fabs(phoEta[g]-muEta[mu1]), fabs(phoEta[g]-muEta[mu2]))"
)

# FSR MC Ttruth
chain.SetAlias(
    "isFSR",
    "phoGenMatchPdgId[g]==22 && " +\
        "abs(phoGenMatchMomPdgId[g])==13"
)

# ISR MC truth
chain.SetAlias(
    "isISR",
    "phoGenMatchPdgId[g]==22 && " +\
        "phoGenMatchMomPdgId[g]==22 && "+\
        "phoGenMatchMomStatus[g]==3"
)

whitespace = re.compile(r'\s+')
minDPhiExpr = whitespace.sub("",
                  """min(
                          fabs(deltaPhi(phoPhi[g],muPhi[mu1])),
                          fabs(deltaPhi(phoPhi[g],muPhi[mu2]))
                        )"""
              )

minDThetaExpr = whitespace.sub("",
                    """min(
                            fabs(deltaTheta(phoEta[g],muEta[mu1])),
                            fabs(deltaTheta(phoEta[g],muEta[mu2]))
                          )"""
                )


outputVars = """
    nVertices
    mmgMass
    mass
    minDEta
    mmgDeltaRNear
    muPt[mnear]
    muPt[mfar]
    muEcalIso[mnear]
    muEcalIso[mfar]
    muHcalIso[mnear]
    muHcalIso[mfar]
    phoPt[g]
    phoEta[g]
    phoHasPixelSeed
    phoGenMatchPdgId[g]
    phoGenMatchMomPdgId[g]
    phoGenMatchMomStatus[g]
    isFSR
    isISR
    phoEcalIso
    phoHcalIso
    phoTrackIso
    phoTrackIso-muPt[mnear]*(phoTrackIso>=muPt[mnear]&mmgDeltaRNear<0.4)
    phoSigmaIetaIeta
    phoHadronicOverEm
    """.split() + [
      minDPhiExpr,
      minDThetaExpr
    ]

outputExpression = ":".join(outputVars)

# scanOption = "col=6d:4d:10ld:6.3f:6.3f:6.3f:7.4f:7.4f:7.4f:7.4f:7.4f:7.4f:6.3f:6.3f:6.3f:6.4f:6.4f:2d:2d:2d:2d:2d:2d:2d:2d:2d"
# scanOption = "col=6d:4d:10ld:::::::::::::::::2d:2d:2d:2d:2d:2d:2d:2d:2d"
# scanOption = "col=6d:4d:10ld::::::::::::::"
scanOption = (len(outputVars) - 1) * ":"

def makeSelection(cuts):
  return " & ".join("(%s)" % cut for cut in cuts)

## Cuts
#     muPassVbtfBaseline[i] = muPassBaselineTight[i] = 0;
#
#     if (!muIsGlobalMuon[i]) continue;
#     if (muStripHits[i] + muPixelHits[i] < 10) continue;
#     if (muTrackIso[i] > 3.0) continue;
#     if (muPt[i] < 10.) continue;
#     if (TMath::Abs(muEta[i]) > 2.4) continue;
#
#     muPassVbtfBaseline[i] = 1;
#
#     /// more cuts for the tight selection
#     if (TMath::Abs(muDxyBS[i]) > 0.2) continue;
#     if (muGlobalNormalizedChi2[i] > 10.) continue;
#     if (muPixelHits[i] < 1) continue;
#     if (muStations[i] < 2) continue;
#     if (muMuonHits[i] < 1) continue;
#     if (!muIsTrackerMuon[i]) continue;
#     if (TMath::Abs(muEta[i]) > 2.1) continue;
#
#     muPassBaselineTight[i] = 1;
muFarCuts = [
    "muPassBaselineTight[mfar]"
]

muNearCuts = [
    "muIsGlobalMuon[mnear]",
    "muStripHits[mnear] + muPixelHits[mnear] >= 10",
    "muPt[mnear] > 10.",
    "abs(muEta[mnear]) < 2.4",
    "abs(muDxyBS[mnear]) < 0.2",
    "muGlobalNormalizedChi2[mnear] < 10.",
    "muPixelHits[mnear] > 0",
    "muStations[mnear] > 1",
    "muMuonHits[mnear] > 0",
    "muIsTrackerMuon[mnear]",
]

baselineCuts = [
#     "isBaselineCand[mm]",
    "charge[mm] == 0",
    "max(muPt[mu1], muPt[mu2]) > 15"
#     "orderByVProb[mm] == 0",
    "40 < mass[mm] & mass[mm] < 85",
    "nPhotons > 0",
    "mmgPhoton == 0", # require the hardest photon in the events
    "abs(phoScEta[g]) < 2.5",
    "abs(phoScEta[g]) < 1.4442 || abs(phoScEta[g]) > 1.566",
    "5 < phoPt[g]",
    "60 < mmgMass & mmgMass < 120",
#     "mmgDeltaRNear < 1",
    ]

photonCleaningCuts = [
  "phoSeedRecoFlag[g] != 2",       # EcalRecHit::kOutOfTime = 2
  "phoSeedSeverityLevel[g] != 4",  # EcalSeverityLevelAlgo::kWeird = 4
  "phoSeedSeverityLevel[g] != 5",  # EcalSeverityLevelAlgo::kBad = 5
  "phoSeedSwissCross[g] < 0.95",   # extra spike cleaning check
]

massWindow = ["abs(mmgMass[g] - 91.19) < 4"]
ebCut = ["abs(phoEta[g]) < 1.5"]
eeCut = ["abs(phoEta[g]) > 1.5"]
pxMatchVeto = ["!phoHasPixelSeed"]
pxMatch = ["phoHasPixelSeed"]
ubCut = ["minDEta > 0.04 || %s > 0.25" % minDPhiExpr]

## Apply photon cleaning to data only
if sample != "data38x":
    photonCleaningCuts = []

# selection = makeSelection(lyonCuts)
selectionCuts = muFarCuts + muNearCuts + baselineCuts + photonCleaningCuts
selection = makeSelection(selectionCuts)

print "# Dumping `%s'" % outputExpression
print "#   from `%s' " % "', `".join(mmgChains.dfiles[sample])
print "#   to `%s'"    % "STDOUT"
print "#   for `%s'"   % selection
print "#   List of cuts:"
for cut in selectionCuts:
    print "#     %2d. %s" % (selectionCuts.index(cut)+1, cut)

print "#   List of output variables:"

print "# Going trhough %d input entries ..." % chain.GetEntries()
for var in outputVars:
    print "#     %2d. %s" % (outputVars.index(var)+1, var)

chain.SetScanField(0)
chain.Scan(outputExpression, selection, scanOption)
print "# ... Done."
