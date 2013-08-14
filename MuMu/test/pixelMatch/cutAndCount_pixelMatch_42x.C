{
gROOT->LoadMacro("../resolutionErrors.C");

// const char *filenameData = "pixelMatch_data_Nov4ReReco_v4.dat";
// const char *filenameMC   = "pixelMatch_Powheg_Fall10_v4.dat";

// const char *path = "/raid2/veverka/pmvTrees/";
const char *path = "/Users/veverka/Work/Data/pmvTrees/";

/**
    'data' : [ 'pmvTree_V9_Run2010B-ZMu-Apr21ReReco-v1.root',
              'pmvTree_V9_ZMu-May10ReReco-42X-v3.root',
              'pmvTree_V9_PromptReco-v4_FNAL_42X-v3.root', ],
    'z'    : [ 'pmvTree_V9_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
    'qcd'  : [ 'pmvTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V6.root' ],
    'w'    : [ 'pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V6.root' ],
    'tt'   : [ 'pmvTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V6.root' ],
*/

// const char *filenameData = "pmvTree_V9_ZMu-May10ReReco_plus_PromptReco-v4-42X-v3.root";
// const char *filenameMC   = "pmvTree_V9_DYToMuMu_pythia6_v2_RECO-42X-v4.root";
// const char *filenameQCD  = "pmvTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V6.root";
// const char *filenameW    = "pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V6.root";
// const char *filenameTT   = "pmvTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V6.root";

// 2011A+B
// const char *filenameData = "pmvTree_V15_05Jul2011ReReco_05Aug2011_03Oct2011-v1_PromptReco-v1B_RECO.root";
// 2011A
// const char *filenameData = "pmvTree_V15_05Jul2011ReReco_05Aug2011_03Oct2011-v1_RECO.root";
// 2011B
const char *filenameData = "pmvTree_V15_DoubleMu_Run2011B-PromptReco-v1_condor_Dimuon_RECO-42X-v9.root";


// const char *filenameMC = "pmvTree_V15_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_Summer11-PU_S4_START42_V11-v1_glidein_Dimuon_RECO-42X-v9.root";
// const char *filenameMC = "pmvTree_V16_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_Summer11-PU_S4_START42_V11-v1_glidein_Dimuon_RECO-42X-v9.root";
 const char *filenameMC = "pmvTree_V17_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_Summer11-PU_S4_START42_V11-v1_glidein_Dimuon_RECO-42X-v9.root";


const char *filenameQCD  = "pmvTree_V15_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Summer11-PU_S4_START42_V11-v1_condor_Dimuon_RECO-42X-v9.root";
const char *filenameW    = "pmvTree_V15_WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_Summer11-PU_S4_START42_V11-v1_condor_Dimuon_RECO-42X-v9.root";
const char *filenameTT   = "pmvTree_V15_TTJets_TuneZ2_7TeV-madgraph-tauola_Summer11-PU_S4_START42_V11-v2_condor_Dimuon_RECO-42X-v9.root";







enum mcSample {z=0, qcd, w, tt};

// Weights of V15 AOD ntuples for 4.603 / fb 
// double weight[] = {
//   0.2578237765992,  // Z
//   15.5412157722089, // QCD
//   0.20516095989489, // tt
//   1.77177343641992 // W
// };

// Weights of V15 RECO ntuples for 4.603 / fb 
double weight[] = {
  0.2578237765992 / (105./129.),  // Z
  15.5412157722089 / 0.2522, // QCD
  1.77177343641992 / 0.0113, // W
  0.20516095989489, // tt
};

TFile dataFile(Form("%s%s", path, filenameData));
TFile mcFile(Form("%s%s", path, filenameMC));
TFile qcdFile(Form("%s%s", path, filenameQCD));
TFile wFile(Form("%s%s", path, filenameW));
TFile ttFile(Form("%s%s", path, filenameTT));

/// Read data set
TTree * tdata  = (TTree*) dataFile.Get("pmvTree/pmv");
TTree * tmc    = (TTree*) mcFile.Get("pmvTree/pmv");
TTree * tqcd   = (TTree*) qcdFile.Get("pmvTree/pmv");
TTree * tw   = (TTree*) wFile.Get("pmvTree/pmv");
TTree * ttt   = (TTree*) ttFile.Get("pmvTree/pmv");

TCut drCut("minDeltaR < 1");
// TCut phoTIsoCut("phoTrackIsoCorr < 2 + 0.001 * phoPt");
// TCut phoEIsoCut("phoEcalIso < 4.2+0.006*phoPt");
// TCut phoHIsoCut("phoHcalIso < 2.2+0.0025*phoPt");
// TCut ebSihihCut("minDTheta<0.05|phoSigmaIetaIeta<0.013");
 TCut ebCut("abs(phoEta) < 1.5");
 TCut eeCut("abs(phoEta) > 1.5");
 TCut signalCut("isFSR");
 TCut backgroundCut("!isFSR");
 TCut mWindowCut("abs(mmgMass-90) < 15");
 TCut ubCut("(minDEta > 0.04 | minDPhi > 0.2)");
 // TCut vetoCut("phoDeltaRToTrack > 1");
 // TCut vetoCut("phoDeltaRToTrack > 0.062"); //eb low R9
 TCut vetoCut("!phoHasPixelMatch");
 TCut nVtx1to2("nVertices<=2");
 TCut phoPt5to10("5 <= phoPt & phoPt < 10");
 TCut phoPt10to20("10 <= phoPt & phoPt < 20");
 TCut phoPt20up("20 <= phoPt");
 // TCut ebLowR9("0.36 < phoR9 && phoR9 <= 0.94");
 // TCut eeLowR9("0.32 < phoR9 && phoR9 <= 0.94");
 TCut ebLowR9("phoR9 <= 0.94");
 TCut eeLowR9("phoR9 <= 0.95");
 TCut ebLowR9MC("0.36 < phoR9 && phoR9 <= 0.94");
 TCut eeLowR9MC("0.32 < phoR9 && phoR9 <= 0.94");
 // TCut ebLowR9("phoR9 <= 0.94");
 // TCut eeLowR9("phoR9 <= 0.95");
 TCut highR9("0.94 < phoR9");
 TCut ebHighR9("0.94 < phoR9");
 // TCut eeHighR9("0.94 < phoR9");
 TCut eeHighR9("0.95 < phoR9");
 TCut run2011A("id.run < 175860");
 TCut run2011B("id.run >= 175860");


 // These cuts are for the pixel match veto
 TCut ebSelection("phoIsEB & abs(mmgMass-90)<15 & (minDEta > 0.04 | minDPhi > 0.3) && scEt > 10 && phoHoE < 0.5");
 TCut eeSelection("!phoIsEB & abs(mmgMass-90)<15 & (minDEta > 0.08 | minDPhi > 0.3) && scEt > 10 && phoHoE < 0.5");

 // These near muon veto cuts are for the "delta R to nearest track" electron veto
 // TCut ebSelection("phoIsEB & abs(mmgMass-90)<15 & (minDEta > 0.04 | minDPhi > 0.1) && scEt > 10 && phoHoE < 0.5");
 // TCut eeSelection("!phoIsEB & abs(mmgMass-90)<15 & (minDEta > 0.04 | minDPhi > 0.2) && scEt > 10 && phoHoE < 0.5");

 //*****************************************************************************
 // TCut selection = ebSelection && ebHighR9;
 // TCut selection = ebSelection && ebLowR9;
 // TCut selection = eeSelection && eeHighR9;
 TCut selection = eeSelection && eeLowR9;
 //*****************************************************************************

// gStyle->SetPadLeftMargin(1.3);
TCanvas * c1 = new TCanvas("c1", "c1", 20, 20, 800, 400);
c1->Divide(2,1);
c1->cd(1);

// Automatically calculate the sum of squares of weights
// since we deal with weighed histograms.
TH1::SetDefaultSumw2();

// Scale all MC such that z has event weight 1 to maintain it's statistical error

cmsDriver.py MCDBtoEDM \
--conditions START42_V14B::All \
-s NONE \
--eventcontent RAWSIM \
--datatier GEN \
--filein mcdb:2380

// Calculate efficiency
double eff = ps / (ps + fs);
double eff_mc = ps_mc / (ps_mc + fs_mc);

// Efficiency error
if (fs < 1.e-5) {
    fs = 1.;
}
double eeff = eff*(1-eff)*Oplus(eps/ps, efs/fs);
double eeff_mc = eff_mc*(1-eff_mc)*Oplus(eps_mc/ps_mc, efs_mc/fs_mc);

cout << "== Normal approx. errors == " << endl;
cout << "veto efficiency in MC: " << eff_mc << " +/- " << eeff_mc << endl;
cout << "veto efficiency in data: " << eff << " +/- " << eeff << endl;

/// CL 1-sigma/68% Bayesian with Beta(1,1) prior with mode of posterior
/// to define the interval

TH1F h_pass("h_pass", "number of passing signal probes", 2, 0, 2);
TH1F h_total("h_total", "number of all signal probes", 2, 0, 2);

h_pass .GetXaxis()->SetBinLabel(1, "data");
h_total.GetXaxis()->SetBinLabel(1, "data");
h_pass .GetXaxis()->SetBinLabel(2, "MC");
h_total.GetXaxis()->SetBinLabel(2, "MC");

h_pass.Fill("data", ps);
h_pass.Fill("MC"  , ps_mc);
h_total.Fill("data", ps + fs);
h_total.Fill("MC"  , ps_mc + fs_mc);

TEfficiency g_eff("eff", "data;sample;#epsilon_{PMV}", 2, 0.5, 2.5);

// Hack to fill the efficiency for data
for ( int i = 0; i < (int) ps + fs; ++i ) {
  if ( i < (int) fs ) {
    g_eff.Fill(/*fail*/ 0, /*data*/ 1);
  } else {
    g_eff.Fill(/*pass*/ 1, /*data*/ 1);
  }
}

// Hack to fill the efficiency for MC
for ( int i = 0; i < (int) ps_mc + fs_mc; ++i ) {
  if ( i < (int) fs_mc ) {
    g_eff.Fill(/*fail*/ 0, /*MC*/ 2);
  } else {
    g_eff.Fill(/*pass*/ 1, /*MC*/ 2);
  }
}

// // Hack to draw the efficiency
// g_eff.GetXaxis()->SetBinLabel(1, "data");
// g_eff.GetXaxis()->SetBinLabel(2, "MC");
// g_eff.BayesDivide(&h_pass, &h_total);

// Add systematic error on data in quadrature
// Assume systematic errors = 100% background
double eeff_syst = eff*(1-eff)*Oplus(pb/ps, fb/fs);

cout << "Veto: " << vetoCut.GetTitle() << endl;
cout << "== Clopper-Pearson errors == " << endl;
cout << "Veto efficiencies: Data (%) | MC (%) | data/MC" << endl;
cout << "Selection: " << selection.GetTitle() << endl;


/// Data
printf ( "%.2f + %.2f - %.2f (stat.) +/- %.2f (syst.) | ",
         100 * g_eff.GetEfficiency(1),
         100 * g_eff.GetEfficiencyErrorUp(1),
         100 * g_eff.GetEfficiencyErrorLow(1),
         100 * eeff_syst );

/// MC
printf ( "%.2f + %.2f - %.2f (stat.) | ",
         100 * g_eff.GetEfficiency(2),
         100 * g_eff.GetEfficiencyErrorUp(2),
         100 * g_eff.GetEfficiencyErrorLow(2) );


/// data / MC

printf ( "%.4f + %.4f - %.4f\n",
         g_eff.GetEfficiency(1) / g_eff.GetEfficiency(2),
         Oplus( g_eff.GetEfficiencyErrorUp(1),
                g_eff.GetEfficiencyErrorUp(2),
                eeff_syst ),
         Oplus( g_eff.GetEfficiencyErrorLow(1),
                g_eff.GetEfficiencyErrorLow(2),
                eeff_syst ) );

/// Latex
/// Data
printf ( "%.2f$^{+%.2f}_{-%.2f} \\pm %.2f$ & ",
         100 * g_eff.GetEfficiency(1),
         100 * g_eff.GetEfficiencyErrorUp(1),
         100 * g_eff.GetEfficiencyErrorLow(1), 
	 100 * eeff_syst);
/// MC
printf ( "%.2f$^{+%.2f}_{-%.2f}$ & ",
         100 * g_eff.GetEfficiency(2),
         100 * g_eff.GetEfficiencyErrorUp(2),
         100 * g_eff.GetEfficiencyErrorLow(2) );
/// data / MC
printf ( "%.4f$^{+%.4f}_{-%.4f}$ \\\\\n",
         g_eff.GetEfficiency(1) / g_eff.GetEfficiency(2),
         Oplus( g_eff.GetEfficiencyErrorUp(1),
                g_eff.GetEfficiencyErrorUp(2),
                eeff_syst ),
         Oplus( g_eff.GetEfficiencyErrorLow(1),
                g_eff.GetEfficiencyErrorLow(2),
                eeff_syst ) );

// Draw passing probes TODO: ADD W and ttbar

// This is black magic
 if (hpb_qcd) {
   hp_mc->Add(hpb_qcd);
   hpb_mc->Add(hpb_qcd);
 }

 double scaleFactorBase = (p + f) / (hp_mc->Integral(1,30) + hf_mc->Integral(1,15));
 double scaleFactor = scaleFactorBase; //* hp->GetBinWidth(1) / hp_mc->GetBinWidth(1);
hp_mc->Scale(scaleFactor);
hpb_mc->Scale(scaleFactor);
hpb_qcd->Scale(scaleFactor);

hp_mc->SetLineColor(kAzure - 9);
hp_mc->SetFillColor(kAzure - 9);
hpb_mc->SetLineColor(kSpring + 5);
hpb_mc->SetFillColor(kSpring + 5);
hpb_qcd->SetLineColor(kYellow - 7); // kOrange-2, kRed-3
hpb_qcd->SetFillColor(kYellow - 7);

hp_mc->SetTitle("Passing Probes");
hp_mc->GetXaxis()->SetTitle("m(#mu#mu#gamma) (GeV)");
hp_mc->GetYaxis()->SetTitle("Entries / 1 GeV");
hp_mc->GetYaxis()->SetTitleOffset(1.7);


hp_mc->SetStats(0);
hpb_mc->SetStats(0);
hpb_qcd->SetStats(0);

hp->SetMarkerStyle(20);

double ymax = TMath::Max(
    hp->GetMaximum() + TMath::Sqrt(hp->GetMaximum()),
    hp_mc->GetMaximum()
);

hp_mc->GetYaxis()->SetRangeUser(0, 1.1*ymax);


TPad * pad1 = (TPad*) c1->cd(1);
pad1->SetLeftMargin(0.15);
hp_mc->Draw("hist");
hpb_mc->Draw("hist same");
hpb_qcd->Draw("hist same");
hp->Draw("e0same");
c1->cd(1)->RedrawAxis();


// Draw failing probes
// double scaleFactor = hf->Integral() / hf_mc->Integral();
 scaleFactor = scaleFactorBase; // * hf->GetBinWidth(1) / hf_mc->GetBinWidth(1);
hf_mc->Scale(scaleFactor);
hfb_mc->Scale(scaleFactor);

hf_mc->SetLineColor(kAzure - 9);
hf_mc->SetFillColor(kAzure - 9);
hfb_mc->SetLineColor(kSpring + 5);
hfb_mc->SetFillColor(kSpring + 5);

hf_mc->SetTitle("Failing Probes");
hf_mc->GetXaxis()->SetTitle("m(#mu#mu#gamma) (GeV)");
hf_mc->GetYaxis()->SetTitle("Entries / 5 GeV");
hf_mc->GetYaxis()->SetTitleOffset(1.2);


hf_mc->SetStats(0);
hfb_mc->SetStats(0);

hf->SetMarkerStyle(20);

double ymax = TMath::Max(
    hf->GetMaximum() + TMath::Sqrt(hf->GetMaximum()),
    hf_mc->GetMaximum()
);

hf_mc->GetYaxis()->SetRangeUser(0, 1.1*ymax);

c1->cd(2);
hf_mc->Draw("hist");
hfb_mc->Draw("hist same");
hf->Draw("e0same");
c1->cd(2)->RedrawAxis();

TCanvas *c2 = new TCanvas("c2", "c2", 40, 40 ,400, 400);
c2->SetRightMargin(0.02);
c2->SetLeftMargin(0.12);
g_eff.Draw();
// c2->Modified();
c2->Update();
TGraphAsymmErrors *gr1 = g_eff.GetPaintedGraph();
gr1->GetXaxis()->SetBinLabel( gr1->GetXaxis()->FindBin(1), "data" );
gr1->GetXaxis()->SetBinLabel( gr1->GetXaxis()->FindBin(2), "MC" );
TH2F *frame = new TH2F("frame","",2,0.5,2.5,1,0.7,1);
frame->SetStats(0);
frame->GetYaxis()->SetTitleOffset(1.5);
frame->GetYaxis()->SetTitle("Efficiency");
frame->GetXaxis()->SetLabelSize(0.08);
frame->GetXaxis()->SetBinLabel(1,"data");
frame->GetXaxis()->SetBinLabel(2,"MC");
frame->Draw();
g_eff.GetPaintedGraph()->Draw("p");

c1->Print("m3_x.eps");
c1->Print("m3_x.png");
// c2->Print("eff_x.eps");
// c2->Print("eff_x.png");
}
