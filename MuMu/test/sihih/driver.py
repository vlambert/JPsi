import sys
import histos
import cuts
from ROOT import *
from common import *


filename = "sihihHistos_Nov4ReReco_38XMC.root"
histosToMake = "mass mmgMass".split()
# histosToMake = "mmgMassEB mmgMassEE phoPt phoPtEB phoPtEE phoE phoEEB phoEEE".split()

# histosToMake = """
#     ikReco
#     ikRecoEB
#     ikRecoEE
#     ikVReco
#     ikVRecoEB
#     ikVRecoEE
#     ikRecoOverGen
#     ikVRecoOverGen
#     ikVVRecoOverGen
#     mmMassRecoOverGen
#     mmMassVRecoOverGen
#     mmgMassRecoOverGen
#     mmgMassVRecoOverGen
#     mmgMassVVRecoOverGen
#     """.split()

#histosToMake = "mmMassRecoOverGen mmMassVRecoOverGen".split()
# profilesToMake = ["eeSihihVsDR"]
profilesToMake = []

## Preselection
#print "Applying preselection ...\n  ",
#for name, ch in chains.items():
    #print name,; flush()
    #lname = "eventList_%s" % name
    ##ch.Draw(">>%s" % lname, "isBaselineCand")
    #ch.Draw(">>%s" % lname, makeSelection(cuts.lyonCuts))
    #ch.SetEventList(gDirectory.Get(lname))

file = TFile(filename, "recreate")

###############################################################################
## Make histos

print "Starting loop over histos ..."
for x in histosToMake:
    makeHistos(chains, histos.histos[x], cuts.cuts[x], ignoreDatasets = [])

print "Starting loop over profiles ... "
for x in profilesToMake:
    makeHistos(chains, histos.histos[x], cuts.cuts[x], ["zmg", "data38x"], "profile")

print "Saving output to %s ... " % file.GetName()
file.Write()

print "Exitting with great success!"
