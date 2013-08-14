## Configuration
import sys
import ROOT

inputFileNames = """
MuMuGammaTree_132440-135802_MinimumBias_Commissioning10-SD_Mu-Jun14thSkim_v1.root
MuMuGammaTree_135803-137436_Mu_Run2010A-Jun14thReReco_v1.root
MuMuGammaTree_137437-139558_Mu_Run2010A-PromptReco-v4b.root
MuMuGammaTree_139559-140159_Mu_Run2010A-Jul16thReReco-v1.root
MuMuGammaTree_140160-144114_Mu_Run2010A-PromptReco-v4.root
""".split()

outputFileName = "ZMuMuGammaMass_2.9ipb_EE.txt"

# inputFileNames = """
# MuMuGammaTree_Zmumu_Spring10.root
# """.split()
#
# outputFileName = "ZMuMuGammaMass_Zmumu_Spring10_EB.txt"

def makeSelection(cuts):
  return " & ".join("(%s)" % cut for cut in cuts)

photonId = makeSelection([
  "phoPt[g] > 10",
  "phoEcalIso[g] < 4.2 + 0.004 * phoPt[g]",
  "phoHcalIso[g] < 2.2 + 0.001 * phoPt[g]",
  "phoTrackIso[g] < 2.0 + 0.001 * phoPt[g]",
  "phoHadronicOverEm[g] < 0.05",
  "((abs(phoEta[g]) > 1.5 & phoSigmaIetaIeta[g] < 0.026) || (phoSigmaIetaIeta[g] < 0.013))",
  ])

selection = makeSelection([
#   "phoSeedRecoFlag[g] != 2",       # DATA ONLY! EcalRecHit::kOutOfTime = 2
#   "phoSeedSeverityLevel[g] != 4",  # DATA ONLY! EcalSeverityLevelAlgo::kWeird = 4
#   "phoSeedSeverityLevel[g] != 5",  # DATA ONLY! EcalSeverityLevelAlgo::kBad = 5
  "abs(phoEta[g]) > 1.5",  # EB or EE
  "nPhotons > 0",
  "abs(phoScEta[g]) < 2.5",
  "abs(phoEta[g]) < 1.4442 || abs(phoEta[g]) > 1.566",
  "mass[mm] > 40",
  "mass[mm] < 85",
  "mmgMass > 60",
  "mmgMass < 120",
  "phoPt[g] > 5",
  "mmgDeltaRNear < 0.5 || (%s)" % photonId,
  ])

outputExpression = "mmgMass"
print "Dumping `%s'" % outputExpression
print "  from `%s' " % "', `".join(inputFileNames)
print "  to `%s'"    % outputFileName
print "  for `%s'"   % selection

print "Switching to batch mode ..."
sys.argv.append( '-b' )

print "Loading ROOT ..."
chain = ROOT.TChain("MuMuGammaTree/mmg")
for f in inputFileNames:
  print "Reading `%s'" % f
  chain.Add(f)

chain.SetAlias("mm", "mmgDimuon")
chain.SetAlias("g", "mmgPhoton")

print "Going trhough %d input entries ..." % chain.GetEntries()

# Preselection
chain.Draw(">>elist", "isVbtfBaselineCand[mm]")
chain.SetEventList(ROOT.gDirectory.Get("elist"))

chain.Draw(outputExpression, selection, "goff")
output = chain.GetV1()
outputSize = chain.GetSelectedRows()

print "Writing to %d entries `%s'" % (outputSize, outputFileName)
outputFile = open(outputFileName, "w")
ascii = "\n".join(["%f" % output[i] for i in range(outputSize)])
outputFile.write(ascii + "\n")
outputFile.close()
print "... Done."
