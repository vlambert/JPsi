{
const char *filenameData = "pixelMatch_data_Nov4ReReco_v3.dat";
const char *filenameMC   = "pixelMatch_Powheg_Fall10_v3.dat";
/// Read data set
TTree tdata("tdata", "real data");
TTree tmc("tmc", "MC");
const char * leafVariables =
         /*  1. */ "Row/I:"
         /*  2. */ "Instance:"
         /*  3. */ "nVertices:"
         /*  4. */ "mmgMass/F:"
         /*  5. */ "mmMass:"
         /*  6. */ "minDEta:"
         /*  7. */ "minDeltaR:"
         /*  8. */ "muPtNear:"
         /*  9. */ "muPtFar:"
         /* 10. */ "muEcalIsoNear:"
         /* 11. */ "muEcalIsoFar:"
         /* 12. */ "muHcalIsoNear:"
         /* 13. */ "muHcalIsoFar:"
         /* 14. */ "phoPt:"
         /* 15. */ "phoEta:"
         /* 16. */ "phoHasPixelMatch/I:"
         /* 17. */ "phoPdgId:"
         /* 18. */ "phoMomPdgId:"
         /* 19. */ "phoMomStatus:"
         /* 20. */ "isFSR:"
         /* 21. */ "isISR:"
         /* 22. */ "phoEcalIso/F:"
         /* 23. */ "phoHcalIso:"
         /* 24. */ "phoTrackIso:"
         /* 25. */ "phoTrackIsoCorr:"
         /* 26. */ "phoSigmaIetaIeta:"
         /* 27. */ "phoHadronicOverEm:"
         /* 28. */ "minDPhi:"
         /* 29. */ "minDTheta";
tdata.ReadFile(filenameData, leafVariables);
tmc  .ReadFile(filenameMC  , leafVariables);


}
