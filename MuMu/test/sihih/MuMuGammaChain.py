from basicRoot import *
import os

path = "/raid1/veverka/zgamma/DimuonTrees_v3"

#inputFiles = """
#MuMuGammaTree_MinimumBias_Commissioning10-SD_Mu-Jun14thSkim_v1_132440-137028.root
#MuMuGammaTree_Mu_Run2010A-Jun14thReReco_v1_135803-137436.root
#MuMuGammaTree_Mu_Run2010A-Jul16thReReco-v1_139559-140159.root
#MuMuGammaTree_Mu_Run2010A-PromptReco-v4_140160-140399.root
#MuMuGammaTree_Mu_Run2010A-PromptReco-v4_140400-141961.root
#MuMuGammaTree_Mu_Run2010A-PromptReco-v4_141962-142264_DCSTRONLY.root
#MuMuGammaTree_Mu_Run2010A-PromptReco-v4_137437-139558_v2.root
#""".split()

#inputFiles = """
#MuMuGammaTree_132440-135802_MinimumBias_Commissioning10-SD_Mu-Jun14thSkim_v1.root
#MuMuGammaTree_135803-137436_Mu_Run2010A-Jun14thReReco_v1.root
#MuMuGammaTree_137437-139558_Mu_Run2010A-PromptReco-v4b.root
#MuMuGammaTree_139559-140159_Mu_Run2010A-Jul16thReReco-v1.root
#MuMuGammaTree_140160-144114_Mu_Run2010A-PromptReco-v4.root
#MuMuGammaTree_PromptRecov2_json146729.root
#MuMuGammaTree_DCSTRONLY_146730-147284_PromptRecov2.root
#""".split()


# inputFiles = """
# MuMuGammaTree_Sept17ReReco.root
# MuMuGammaTree_PromptRecov2_json146729.root
# """.split()

files = {}
files["z"] = """
    MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_1-5.root
    MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_6-10.root
    MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_11-15.root
    MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_16-20.root
    MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_21-26.root
    """.split()

files["w"] = ["MuMuGammaTree_WJets-madgraph.root"]
files["tt"] = ["MuMuGammaTree_TTbarJets_Tauola-madgraph.root"]
files["qcd"] = ["MuMuGammaTree_InclusiveMu15.root"]

files["data36x"] = """
    MuMuGammaTree_132440-135802_MinimumBias_Commissioning10-SD_Mu-Jun14thSkim_v1.root
    MuMuGammaTree_135803-137436_Mu_Run2010A-Jun14thReReco_v1.root
    MuMuGammaTree_137437-139558_Mu_Run2010A-PromptReco-v4b.root
    MuMuGammaTree_139559-140159_Mu_Run2010A-Jul16thReReco-v1.root
    MuMuGammaTree_140160-144114_Mu_Run2010A-PromptReco-v4.root
    """.split()

files["data38x"] = """
    MuMuGammaTree_135821-144114_Sept17ReReco.root
    MuMuGammaTree_146240-147225_PromptRecov2_json148058.root
    MuMuGammaTree_147226-148002_PromptRecov2_json148058.root
    MuMuGammaTree_148003-148068_PromptRecov2_json148058.root
    """.split()

files["test"] = """
    MuMuGammaTree_146240-147225_PromptRecov2_json148058.root
    MuMuGammaTree_147226-148002_PromptRecov2_json148058.root
    MuMuGammaTree_148003-148068_PromptRecov2_json148058.root
    """.split()

bpath = "/raid1/veverka/zgamma/DimuonTrees_v3b"
bfiles = {}
bfiles["data38x"] = """
  MuMuGammaTree_combined_Sep17ReRecov2_StremExpressv3_json_135821-144114_Sept17ReReco_FNAL.root
  MuMuGammaTree_combined_Sep17ReRecov2_StremExpressv3_json_146240-149392_PromptRecov2_FNAL.root
  """.split()
#   ["MuMuGammaTree_Data7TeV_FNAL_upto148864_JSON.root"]

bfiles["z"] = ["MuMuGammaTree_Zmumu_M20_CTEQ66-powheg.root"]
    #MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_1-5.root
    #MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_6-10.root
    #MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_11-26.root
    #MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_27-29.root
    #MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_30-49.root
    #MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_50-69.root
    #MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_70-89.root
    #MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_90-101.root
    #""".split()
bfiles["zg"] = ["MuMuGammaTree_Zgamma.root"]
bfiles["zmg"] = ["MuMuGammaTree_ZJets-madgraph.root"]
bfiles["w"] = ["MuMuGammaTree_WJets-madgraph.root"]
bfiles["qcd"] = ["MuMuGammaTree_InclusiveMu15.root"]
bfiles["tt"] = ["MuMuGammaTree_TTbarJets_Tauola-madgraph.root"]

cpath = "/raid2/veverka/zgamma/DimuonTrees_v3c"
cfiles = {}
cfiles["data38x"] = ["MuMuGammaTree_Mu_Nov4ReRecoJSON.root"]
# cfiles["data38xNoJson"] = ["MuMuGammaTree_Mu.root"]
cfiles["z"] = ["MuMuGammaTree_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia.root"]
cfiles["zg"] = ["MuMuGammaTree_Zgamma_Summer10.root"]
#cfiles["zmg"] = [""]
cfiles["w"] = ["MuMuGammaTree_WJetsToLNu_TuneZ2_7TeV-madgraph-tauola.root"]
cfiles["qcd"] = ["MuMuGammaTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6.root"]
cfiles["tt"] = ["MuMuGammaTree_TTJets_TuneZ2_7TeV-madgraph-tauola.root"]


def getChains(files=bfiles, path=bpath):
    chains = {}
    for name, flist in files.items():
        chains[name] = TChain("MuMuGammaTree/mmg")
        for f in flist:
            print "Loading ", name, ":", f
            chains[name].Add( os.path.join(path, f) )
    return chains

# LO event weights for L = 30 pb-1
loWeight30 = {}
loWeight30["z"  ] = 2.77E-02
loWeight30["qcd"] = 4.67E-01
loWeight30["w"  ] = 7.37E-02
loWeight30["tt" ] = 1.95E-03

weight30 = {}
weight30["z"  ] = 2.83E-02
weight30["qcd"] = 4.67E-01
weight30["w"  ] = 9.19E-02
weight30["tt" ] = 3.38E-03

## NLO weight for c trees for 36.15/pb
cweight = {}
cweight["z"  ] = 2.55E-02
cweight["qcd"] = 1.04E-01
cweight["w"  ] = 5.89E-02
cweight["tt" ] = 3.75E-03
cweight["data38x"] = 1.

if __name__ == "__main__": import user

