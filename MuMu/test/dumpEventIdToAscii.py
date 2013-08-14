## Configuration
import sys
import os

print "Switching to batch mode ..."
sys.argv.append( '-b' )

import ROOT
import MuMuGammaChain

from makeFsrHistos import templateSel

chain = MuMuGammaChain.chain["data38x"]
selection = "isVbtfBaselineCand & orderByVProb==0 & run <= 144114 & abs(mass-90)<30"
outputFileName = "eventId_data38x_uptoRun144114.txt"

# selection = templateSel["all"] + "& (mmgMass > 87) & (mmgMass < 95) & phoPt[g] > 10"
#inputFileNames = """
#MuMuGammaTree_Zmumu_Spring10.root
#""".split()

#selection = templateSel["fake"]
#outputFileName = "phoSigmaIetaIeta_Zmumu_Spring10_fake.txt"

outputExpression = "run:lumi:event"
outputFormat = "%6.0f\t%6.0f\t%12.0f"
print "Dumping `%s'" % outputExpression
print "  from `%s' " % "', `".join([
    os.path.basename(t.GetTitle()) for t in chain.GetListOfFiles()])
print "  to `%s'"    % outputFileName
print "  for `%s'"   % selection


print "Going trhough %d input entries ..." % chain.GetEntries()

chain.Draw(outputExpression, selection, "goff")
outputSize = chain.GetSelectedRows()

print "Writing to %d entries `%s'" % (outputSize, outputFileName)
outputFile = open(outputFileName, "w")
ascii = "\n".join([outputFormat %
                   (chain.GetV1()[i], chain.GetV2()[i], chain.GetV3()[i],)
                   for i in range(outputSize)
                   ])
outputFile.write("# " + outputExpression.replace(":", "\t") + "\n")
outputFile.write(ascii + "\n")
outputFile.close()
print "... Done."
