{
// const char *filenameData = "Nov4ReReco.dat";
const char *filenameMC   = "DYToMuMu_powheg_Fall10.dat";
const char *filenameData = "Dec22ReReco.dat";
// const char *filenameMC   = "DYToMuMu_Winter10_Powheg.dat";
/// Read data set
TTree tdata("tdata", "real data");
TTree tmc("tmc", "MC");
  const char * leafVariables =
    /*  1. run                      */ "run/I:"
    /*  2. lumi                     */ "lumi:"
    /*  3. event                    */ "event:"
    /*  3. isEB                     */ "isEB:"
    /*  4. phoPt[g]                 */ "pt/F:"
    /*  5. muPt[mnear]              */ "muNearPt:"
    /*  6. muPt[mfar]               */ "muFarPt:"
    /*  7. phoEta[g]                */ "eta:"
    /*  8. muEta[mnear]             */ "muNearEta:"
    /*  9. muEta[mfar]              */ "muFarEta:"
    /* 10. phoPhi[g]                */ "phi:"
    /* 11. muPhi[mnear]             */ "muNearPhi:"
    /* 12. muPhi[mfar]              */ "muFarPhi:"
    /* 13. phoR9                    */ "r9:"
    /* 14. mass[mm]                 */ "m2:"
    /* 15. mmgMass                  */ "m3:"
    /* 16. mmgDeltaRNear            */ "dr:"
    /* 17. kRatio(mmgMass,mass[mm]) */ "ik";
tdata.ReadFile(filenameData, leafVariables);
tmc  .ReadFile(filenameMC  , leafVariables);


}
