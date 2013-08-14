from ROOT import *

t = TTree("t", "t")
t.ReadFile("trigger.dat",
           "run/I:lumi:event:" +\
           "phoPt/F:muPtN:muPtF:" +\
           "phoEta:muEtaN:muEtaF:" +\
           "phoPhi:muPhiN:muPhiF:" +\
           "mmMass:mmMassVanilla:" +\
           "mmgMass:mmgMassVanilla:" +\
           "mmgDeltaRNear:" +\
           "kRatio:kRatioVanilla:" +\
           "HLT_Mu9/I:HLT_Mu11:HLT_Mu15_v1:" +\
           "muHltMu9MatchN:muHltMu11MatchN:muHltMu15v1MatchN:" +\
           "muHltMu9MatchF:muHltMu11MatchF:muHltMu15v1MatchF")

triggerSel = \
    "(133874 <= run & run <= 147195 & muPtF > 20 & muHltMu9MatchF   ) |"+\
    "(133874 <= run & run <= 147195 & muPtN > 20 & muHltMu9MatchN   ) |"+\
    "(147196 <= run & run <= 148821 & muPtF > 20 & muHltMu11MatchF  ) |"+\
    "(147196 <= run & run <= 148821 & muPtN > 20 & muHltMu11MatchN  ) |"+\
    "(148822 <= run & run <= 149442 & muPtF > 20 & muHltMu15v1MatchF) |"+\
    "(148822 <= run & run <= 149442 & muPtN > 20 & muHltMu15v1MatchN)"

if __name__ == "__main__": import user