## Configuration
import os
import sys

print "Switching to batch mode ..."
sys.argv.append( '-b' )

import ROOT
import MuMuGammaChain
## Configuration

dataset = "tt"
chains = MuMuGammaChain.getChains(MuMuGammaChain.cfiles,
                                  MuMuGammaChain.cpath
                                  )
chain = chains[dataset]

outputFileName = "DimuonMass_%s_Nov4ReReco.txt" % dataset

# inputFileNames = """
# MuMuGammaTree_Zmumu_Spring10.root
# """.split()

# outputFileName = "DimuonMass_Zmumu_Spring10.txt"

def makeSelection(cuts):
  return " & ".join("(%s)" % cut for cut in cuts)

lyonCuts = [
    "muIsGlobalMuon[dau1]",
    "muIsGlobalMuon[dau2]",
    "muIsTrackerMuon[dau1]",
    "muIsTrackerMuon[dau2]",
    "muSiHits[dau1] > 10",
    "muSiHits[dau2] > 10",
    "muGlobalNormalizedChi2[dau1] < 10",
    "muGlobalNormalizedChi2[dau2] < 10",
    "abs(muEta[dau1]) < 2.4",
    "abs(muEta[dau2]) < 2.4",
    "muTrackIso[dau1] < 3",
    "muTrackIso[dau2] < 3",
    "min(abs(muEta[dau1]),muEta[dau2]) < 2.1",
    "charge == 0",
    "min(muPt[dau1], muPt[dau2]) > 10",
    "max(muPt[dau1], muPt[dau2]) > 30",
    "min(muEcalIso[dau1], muEcalIso[dau2]) <= 1.0",
    "min(muHcalIso[dau1], muHcalIso[dau2]) <= 1.0",
    "40 <= mass && mass <= 120", ## originally [40,80]
    ]

selection = makeSelection(lyonCuts)

outputExpression = "mass"
print "Dumping `%s'" % outputExpression
print "  from `%s' " % "', `".join(MuMuGammaChain.bfiles[dataset])
print "  to `%s'"    % outputFileName
print "  for `%s'"   % selection

print "Switching to batch mode ..."
sys.argv.append( '-b' )

print "Going trhough %d input entries ..." % chain.GetEntries()

# Preselection
#chain.Draw(">>elist", "isVbtfBaselineCand[mm]")
#chain.SetEventList(ROOT.gDirectory.Get("elist"))

chain.Draw(outputExpression, selection, "goff")
output = chain.GetV1()
outputSize = chain.GetSelectedRows()

print "Writing to %d entries `%s'" % (outputSize, outputFileName)
outputFile = open(outputFileName, "w")
weight = MuMuGammaChain.cweight[dataset]
ascii = "\n".join(["%f %f" % (output[i], weight) for i in range(outputSize)])
outputFile.write(ascii + "\n")
outputFile.close()
print "... Done."
