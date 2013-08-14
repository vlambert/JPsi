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

outputFileName = "DimuonMass_2.9ipb.txt"

# inputFileNames = """
# MuMuGammaTree_Zmumu_Spring10.root
# """.split()

# outputFileName = "DimuonMass_Zmumu_Spring10.txt"

def makeSelection(cuts):
  return " & ".join("(%s)" % cut for cut in cuts)

selection = makeSelection([
  "isVbtfBaselineCand",
  "muPt[dau1] > 20",
  "muPt[dau2] > 20",
  "orderByVProb == 0",
  ])

outputExpression = "mass"
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
