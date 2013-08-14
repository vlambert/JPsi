## Configuration
import sys
import os
import ROOT
from makeFsrHistos import templateSel
from makeFsrHistos import bchain

inputDir = "/raid1/veverka/zgamma/DimuonTrees_v3b"

inputFileNames = ["MuMuGammaTree_Data7TeV_FNAL_upto148864_JSON.root"]

selection = templateSel["all"] + "& isBaselineCand[mm] & orderByVProb[mm]==0 & (mmgMass > 87) & (mmgMass < 95) & phoPt[g] > 5"
outputFileName = "phoSigmaIetaIeta_Zmumu_22ipb.txt"


#inputFileNames = """
#MuMuGammaTree_Zmumu_Spring10.root
#""".split()

#selection = templateSel["fake"]
#outputFileName = "phoSigmaIetaIeta_Zmumu_Spring10_fake.txt"

outputExpression = "phoPt[g]:phoEta[g]:phoSigmaIetaIeta[g]"
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
  chain.Add(os.path.join(inputDir, f))

chain.SetAlias("mm", "mmgDimuon")
chain.SetAlias("g", "mmgPhoton")

print "Going trhough %d input entries ..." % chain.GetEntries()

# Preselection
# chain.Draw(">>elist", "isVbtfBaselineCand[mm]")
# chain.SetEventList(ROOT.gDirectory.Get("elist"))

chain.Draw(outputExpression, selection, "goff")
outputSize = chain.GetSelectedRows()

print "Writing to %d entries `%s'" % (outputSize, outputFileName)
outputFile = open(outputFileName, "w")
ascii = "\n".join(["%.4g\t% .4g\t%.4g" %
                   (chain.GetV1()[i], chain.GetV2()[i], chain.GetV3()[i],)
                   for i in range(outputSize)
                   ])
outputFile.write("# " + outputExpression.replace(":", "\t") + "\n")
outputFile.write(ascii + "\n")
outputFile.close()
print "... Done."
