import os
import ROOT

# path = "/home/veverka/Work/data/pmv/"
path = "/raid2/veverka/PMVTrees_v1/"

filenames = {
#     "Data": "pmvTree_Mu_Run2010AB-Dec22ReReco_v1_json_V3.root",
#     "Z"   : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v2_V3.root",
    "Data": "pmvTree_ZMu-May10ReReco_V4.root",
    "Z"   : "pmvTree_zSpring11_V4.root",
    "QCD" : "pmvTree_QCD_Pt-20_MuEnrichedPt-15_Winter10_V3.root",
    "W"   : "pmvTree_WJetsToLNu_TuneZ2_7TeV-madgraph_Winter10_V3.root",
    "TT"  : "pmvTree_TTJets_TuneZ2-madgraph-Winter10_V3.root",
    }

weights = { "Data": 1.,
            "Z"   : 0.030541912803076, # z
#             "Z"   : 0.00225451955683,  # z2
            "QCD" : 0.10306919044126,
            "W"   : 0.074139194512438,
            "TT"  : 0.005083191122289, }

files, trees, rawEvents, events = {}, {}, {}, {}
mcTotal = 0.
mcTotalRaw = 0
for tag, fname in filenames.items():
    files[tag] = ROOT.TFile( os.path.join( path, fname ) )
    trees[tag] = files[tag].Get("pmvTree/pmv")
    if tag == "Z":
        rawEvents["ZS"] = trees["Z"].Draw( ">>foo", "abs(mmgMass-90)<15 & isFSR", "goff" )
        rawEvents["ZB"] = trees["Z"].Draw( ">>foo", "abs(mmgMass-90)<15 &!isFSR", "goff" )
        events["ZS"] = rawEvents["ZS"] * weights["Z"]
        events["ZB"] = rawEvents["ZB"] * weights["Z"]
        mcTotal += events["ZS"] + events["ZB"]
        mcTotalRaw += rawEvents["ZS"] + rawEvents["ZB"]
    else:
        rawEvents[tag] = trees[tag].Draw( ">>foo", "abs(mmgMass-90)<15", "goff" )
        events[tag] = rawEvents[tag] * weights[tag]
        if tag != "Data":
            mcTotal += events[tag]
            mcTotalRaw += rawEvents[tag]

fractions = {}
fractionsTotal = 0.
for tag, nevents in events.items():
    if tag == "Data":
        fractions[tag] = 1.
    else:
        fractions[tag] = nevents / mcTotal
        fractionsTotal += fractions[tag]

for tag in ["Data", "ZS", "ZB", "QCD", "W", "TT"]:
    print "%10s & %7d & %6.2f & %6.2f \\\\" % \
          (tag, rawEvents[tag], events[tag], 100 * fractions[tag])

print "%10s & %7d & %6.2f & %6.2g \\\\" % \
      ("Total MC", mcTotalRaw, mcTotal, 100 * fractionsTotal)
