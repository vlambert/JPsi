import sys
import os
import re

print "Switching to batch mode ..."
sys.argv.append( '-b' )

import ROOT
import JPsi.MuMu.common.pmvTrees as pmvTrees

## Configuration
# sample = "data39x"
sample, version = 'z', 'v12'
# sample, version = 'data2011', 'v9'
# sample = "zg"
# sample = "qcd"

ROOT.gROOT.LoadMacro("resolutionErrors.C++")
ROOT.gROOT.LoadMacro("res/tools.C++")

chain = pmvTrees.getChains(version)[sample]

## Apply run-based energy scale correction to MC
## Store the pileup weight for MC, dummy weight for real data
if sample == 'data2011':
    outputVars = """
        mmMass
        scaledMmgMass3(corrByRun(id.run,scEta,phoR9),mmgMass,mmMass)
        phoPt*corrByRun(id.run,scEta,phoR9)
        scEta
        phoR9
        1
        """.split()
else:
    outputVars = """
        mmMass
        mmgMass
        phoPt
        scEta
        phoR9
        pileup.weight
        """.split()

outputExpression = ":".join(outputVars)

scanOption = (len(outputVars) - 1) * ":"

def makeSelection(cuts):
  return " & ".join("(%s)" % cut for cut in cuts)

selectionCuts = []

selection = makeSelection(selectionCuts)

print "# Dumping `%s'" % outputExpression
print "#   from `%s' " % "', `".join( [ t.GetTitle() for
                                        t in chain.GetListOfFiles() ] )
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
