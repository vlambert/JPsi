{
gROOT->LoadMacro("../resolutionErrors.C");

// const char *filenameData = "pixelMatch_data_Nov4ReReco_v4.dat";
// const char *filenameMC   = "pixelMatch_Powheg_Fall10_v4.dat";
const char *filenameData = "pixelMatch_data_Dec22ReReco.dat";
const char *filenameMC   = "pixelMatch_Powheg_Winter10.dat";
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

TCut drCut("minDeltaR < 1");
TCut phoTIsoCut("phoTrackIsoCorr < 2 + 0.001 * phoPt");
TCut phoEIsoCut("phoEcalIso < 4.2+0.006*phoPt");
TCut phoHIsoCut("phoHcalIso < 2.2+0.0025*phoPt");
TCut ebSihihCut("minDTheta<0.05|phoSigmaIetaIeta<0.013");
TCut ebCut("abs(phoEta) < 1.5");
TCut eeCut("abs(phoEta) > 1.5");
TCut signalCut("isFSR");
TCut backgroundCut("!isFSR");
TCut mWindowCut("abs(mmgMass-90) < 15");
TCut ubCut("(minDEta > 0.04 | minDPhi > 0.5)");
TCut pmvCut("!phoHasPixelMatch");

TCut selectionBase = drCut &&
                     phoTIsoCut &&
                     phoEIsoCut &&
                     mWindowCut &&
                     ubCut;

TCut ebSelection = selectionBase && ebCut && ebSihihCut;
TCut eeSelection = selectionBase && eeCut;

TCut selection = ebSelection;
// TCut selection = eeSelection;

TCanvas * c1 = new TCanvas("c1", "c1", 20, 20, 800, 400);
c1->Divide(2,1);
c1->cd(1);


// Barrel MC, passing probes
double p_mc = tmc.Draw("mmgMass>>hp_mc", selection && pmvCut);
double pb_mc = tmc.Draw("mmgMass>>hpb_mc", selection && pmvCut && backgroundCut);
double ps_mc = p_mc - pb_mc;
double eps_mc = sqrt(ps_mc);

TH1F *hp_mc = (TH1F*) gDirectory->Get("hp_mc");
TH1F *hpb_mc = (TH1F*) gDirectory->Get("hpb_mc");

hp_mc->SetLineColor(kAzure - 9);
hp_mc->SetFillColor(kAzure - 9);
hpb_mc->SetLineColor(kSpring + 5);
hpb_mc->SetFillColor(kSpring + 5);

hp_mc->Draw();
hpb_mc->Draw("same");

c1->cd(2);

// Barrel MC, failing probes
double f_mc = tmc.Draw("mmgMass>>hf_mc", selection && !pmvCut);
double fb_mc = tmc.Draw("mmgMass>>hfb_mc", selection && !pmvCut && backgroundCut);
double fs_mc = f_mc - fb_mc;
double efs_mc = sqrt(fs_mc);

// Barrel data
double p = tdata.Draw("mmgMass", selection && pmvCut);
double f = tdata.Draw("mmgMass", selection && !pmvCut);

double ps = ps_mc * p / p_mc;
double fs = fs_mc * f / f_mc;

double pb = p - ps;
double fb = f - fs;

double eps = Oplus(sqrt(p), pb); // 100 % error on bg
double efs = Oplus(sqrt(f), fb); // 100 % error on bg

// Calculate efficiency
double eff = ps / (ps + fs);
double eff_mc = ps_mc / (ps_mc + fs_mc);

// Efficiency error
double eeff = eff*(1-eff)*Oplus(eps/ps, efs/fs);
double eeff_mc = eff_mc*(1-eff_mc)*Oplus(eps_mc/ps_mc, efs_mc/fs_mc);

cout << "MC PMV efficiency: " << eff_mc << " +/- " << eeff_mc << endl;
cout << "data PMV efficiency: " << eff << " +/- " << eeff << endl;


}
