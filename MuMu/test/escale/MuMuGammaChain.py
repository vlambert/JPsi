from basicRoot import *
import os

bfiles = {}
bfiles["data38x"] = """
  MuMuGammaTree_combined_Sep17ReRecov2_StremExpressv3_json_135821-144114_Sept17ReReco_FNAL.root
  MuMuGammaTree_combined_Sep17ReRecov2_StremExpressv3_json_146240-149392_PromptRecov2_FNAL.root
  """.split()
#   ["MuMuGammaTree_Data7TeV_FNAL_upto148864_JSON.root"]

bfiles["z"] = """
    MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_1-1.root
    MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_2-3.root
    MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_4-8.root
    MuMuGammaTree_Zmumu_M20_CTEQ66-powheg_9-18.root
    """.split()
bfiles["zg"] = ["MuMuGammaTree_Zgamma.root"]

bpath = "/home/veverka/Work/zgamma/sihih"

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

if __name__ == "__main__": import user

