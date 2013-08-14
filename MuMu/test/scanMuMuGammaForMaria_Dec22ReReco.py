import sys
import os
import re

print "Switching to batch mode ..."
sys.argv.append( '-b' )

import ROOT
import JPsi.MuMu.common.MuMuGammaChains as mmgChains


## Configuration
# sample = "data39x"
#sample = "z"
sample = "zg"
# sample = "qcd"


ROOT.gROOT.LoadMacro("resolutionErrors.C+")

#myFiles = mmgChains.efiles
#myPath  = mmgChains.epath

myFiles = mmgChains.cfiles
myPath  = mmgChains.cpath

chains = mmgChains.getChains( myFiles, myPath )

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
    "phoGenMatchPdgId[0]==22 && " +\
        "abs(phoGenMatchMomPdgId[0])==13"
)

# ISR MC truth
chain.SetAlias(
    "isISR",
    "phoGenMatchPdgId[0]==22 && " +\
        "phoGenMatchMomPdgId[0]==22 && "+\
        "phoGenMatchMomStatus[0]==3"
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
    muPt[0]
    muEta[0]
    muPhi[0]
    muEcalIso[0]
    muHcalIso[0]
    phoPt[0]
    phoEta[0]
    phoPhi[0]
    isFSR
    isISR
    phoEcalIso
    phoHcalIso
    phoTrackIso
    phoTrackIso-muPt[mnear]*(phoTrackIso>=muPt[mnear]&mmgDeltaRNear<0.4)
    phoSigmaIetaIeta
    phoHadronicOverEm
    phoHasPixelSeed
    twoBodyMass(muPt[0],muEta[0],muPhi[0],0.1057,phoPt[0],phoEta[0],phoPhi[0],0)
    """.split()

outputExpression = ":".join(outputVars)

# scanOption = "col=6d:4d:10ld:6.3f:6.3f:6.3f:7.4f:7.4f:7.4f:7.4f:7.4f:7.4f:6.3f:6.3f:6.3f:6.4f:6.4f:2d:2d:2d:2d:2d:2d:2d:2d:2d"
# scanOption = "col=6d:4d:10ld:::::::::::::::::2d:2d:2d:2d:2d:2d:2d:2d:2d"
# scanOption = "col=6d:4d:10ld::::::::::::::"
scanOption = (len(outputVars) - 1) * ":"

def makeSelection(cuts):
  return " & ".join("(%s)" % cut for cut in cuts)

muCuts = [
    "muPt > 20",
    "muIsGlobalMuon[0]",
    "muStripHits[0] + muPixelHits[0] >= 10",
    "muPt[0] > 10.",
    "abs(muEta[0]) < 2.4",
    "abs(muDxyBS[0]) < 0.2",
    "muGlobalNormalizedChi2[0] < 10.",
    "muPixelHits[0] > 0",
    "muStations[0] > 1",
    "muMuonHits[0] > 0",
    "muIsTrackerMuon[0]",
]

phoCuts = [
    "phoPt > 20",
    "abs(phoScEta[0]) < 2.5",
    "abs(phoScEta[0]) < 1.4442 || abs(phoScEta[0]) > 1.566",
]

photonCleaningCuts = [
    "phoSeedRecoFlag[0] != 2",       # EcalRecHit::kOutOfTime = 2
    "phoSeedSeverityLevel[0] != 4",  # EcalSeverityLevelAlgo::kWeird = 4
    "phoSeedSeverityLevel[0] != 5",  # EcalSeverityLevelAlgo::kBad = 5
    "phoSeedSwissCross[0] < 0.95",   # extra spike cleaning check
]

## Apply photon cleaning to data only
if sample != "data39x":
    photonCleaningCuts = []

# selection = makeSelection(lyonCuts)
selectionCuts = muCuts + phoCuts + photonCleaningCuts
selection = makeSelection(selectionCuts)

print "# Dumping `%s'" % outputExpression
print "#   from `%s' " % "', `".join( myFiles )
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
