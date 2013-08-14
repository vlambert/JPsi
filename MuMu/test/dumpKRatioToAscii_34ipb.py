import sys
import os

print "Switching to batch mode ..."
sys.argv.append( '-b' )

import ROOT
import MuMuGammaChain
# from makeFsrHistos import templateSel
# from makeFsrHistos import bfiles, bchain

## Configuration
chains = MuMuGammaChain.getChains(MuMuGammaChain.bfiles,
                                  MuMuGammaChain.bpath
                                  )
#chain = chains["data38x"]
chain = chains["z"]

#chain = ROOT.TChain("MuMuGammaTree/mmg")
# chain.Add("MuMuGammaTree_Zmumu_M20_CTEQ66-powheg.root")

#chain.Add("MuMuGammaTree_135821-144114_Sept17ReReco_FNAL.root")
#chain.Add("MuMuGammaTree_146240-149392_PromptRecov2_FNAL.root")

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

outputFileName = "ikRatio_LyonSelection_Zmumu-powheg-Summer10.txt"

outputExpression = "1./kRatio(mmgMass, mass[mm]):phoPt[g]:phoEta[g]:phoR9[g]"

def makeSelection(cuts):
  return " & ".join("(%s)" % cut for cut in cuts)

photonId = makeSelection([
    "phoPt[g] > 10",  ## was 10
    "phoEcalIso[g] < 4.2 + 0.006 * phoPt[g]",
    "phoHcalIso[g] < 2.2 + 0.0025 * phoPt[g]",
    "phoTrackIso[g] < 2.0 + 0.001 * phoPt[g]",
    "phoHadronicOverEm[g] < 0.05",
    "((abs(phoEta[g]) > 1.5 & phoSigmaIetaIeta[g] < 0.03) || (phoSigmaIetaIeta[g] < 0.013))",
    "!phoHasPixelSeed"
    ])

selection = makeSelection([
    "isBaselineCand[mm]",
    "orderByVProb[mm] == 0",
    "mass[mm] > 40",
    "mass[mm] < 80", ## originally 85
    "abs(mmgMass-zMassPdg()) < 4",
    "nPhotons > 0",
#     "mmgPhoton == 0", # require the hardest photon in the events
    "abs(phoScEta[g]) < 2.5",
    "abs(phoScEta[g]) < 1.4442 || abs(phoScEta[g]) > 1.566",
    "5 < phoPt[g]", ## originally 5
    "phoSeedRecoFlag[g] != 2",       # DATA ONLY! EcalRecHit::kOutOfTime = 2
    "phoSeedSeverityLevel[g] != 4",  # DATA ONLY! EcalSeverityLevelAlgo::kWeird = 4
    "phoSeedSeverityLevel[g] != 5",  # DATA ONLY! EcalSeverityLevelAlgo::kBad = 5
    "phoSeedSwissCross[g] < 0.95",   # extra spike cleaning check
    "mmgDeltaRNear < 0.5 || (%s)" % photonId,
    ])


lyonCuts = [
    "abs(phoScEta[g]) < 2.5",
    "abs(phoEta[g]) < 1.4442 || abs(phoEta[g]) > 1.566",
    "phoSeedRecoFlag[g] != 2",       # DATA ONLY! EcalRecHit::kOutOfTime = 2
    "phoSeedSeverityLevel[g] != 4",  # DATA ONLY! EcalSeverityLevelAlgo::kWeird = 4
    "phoSeedSeverityLevel[g] != 5",  # DATA ONLY! EcalSeverityLevelAlgo::kBad = 5
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


lyonCuts[lyonCuts.index("phoPt[g] > 10")] = "phoPt[g] > 5"
selection = makeSelection(lyonCuts)

## To reproduce Lyons selection do
##+   selection + "& phoPt[g]>10 & mmgDeltaRNear<0.8 & muPt[mmgMuonFar]>30

ROOT.gROOT.LoadMacro("resolutionErrors.C+")

print "Dumping `%s'" % outputExpression
print "  from `%s' " % "', `".join(MuMuGammaChain.bfiles["data38x"])
print "  to `%s'"    % outputFileName
print "  for `%s'"   % selection

print "Going trhough %d input entries ..." % chain.GetEntries()

chain.Draw(outputExpression, selection, "goff")
outputSize = chain.GetSelectedRows()

print "Writing to %d entries `%s'" % (outputSize, outputFileName)
outputFile = open(outputFileName, "w")
ascii = "\n".join(["%.6g\t%.6g\t%.6g\t%.6g" %
                   (chain.GetV1()[i], chain.GetV2()[i], chain.GetV3()[i], chain.GetV4()[i] )
                   for i in range(outputSize)
                   ])
outputFile.write("# " + outputExpression.replace(":", "\t") + "\n")
outputFile.write(ascii + "\n")
outputFile.close()
print "... Done."
