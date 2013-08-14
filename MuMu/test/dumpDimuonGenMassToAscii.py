import sys
import os

print "Switching to batch mode ..."
sys.argv.append( '-b' )

import ROOT
from makeFsrHistos import templateSel
from makeFsrHistos import bfiles, bchain

## Configuration
chain = bchain["z"]


chain.SetAlias("pt1", "muGenPt[dau1]")
chain.SetAlias("pt2", "muGenPt[dau2]")
chain.SetAlias("eta1", "muGenEta[dau1]")
chain.SetAlias("eta2", "muGenEta[dau2]")
chain.SetAlias("phi1", "muGenPhi[dau1]")
chain.SetAlias("phi2", "muGenPhi[dau2]")

genMass = "twoBodyMass(pt1,eta1,phi1,0.106,pt2,eta2,phi2,0.106)"

selection = "isBaselineCand & orderByVProb==0 & abs(%s-90)<70" % genMass
outputFileName = "dimuonGenMass_Zmumu-powheg-Summer10.txt"

outputExpression = genMass

ROOT.gROOT.LoadMacro("resolutionErrors.C+")

print "Dumping `%s'" % outputExpression
print "  from `%s' " % "', `".join(bfiles["z"])
print "  to `%s'"    % outputFileName
print "  for `%s'"   % selection

print "Going trhough %d input entries ..." % chain.GetEntries()

chain.Draw(outputExpression, selection, "goff")
outputSize = chain.GetSelectedRows()

print "Writing to %d entries `%s'" % (outputSize, outputFileName)
outputFile = open(outputFileName, "w")
ascii = "\n".join(["%.6g" %
                   (chain.GetV1()[i],)
                   for i in range(outputSize)
                   ])
outputFile.write("# " + outputExpression.replace(":", "\t") + "\n")
outputFile.write(ascii + "\n")
outputFile.close()
print "... Done."
