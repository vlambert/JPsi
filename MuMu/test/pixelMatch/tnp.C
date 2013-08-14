#include <iostream>
#include "RooAbsPdf.h"
#include "RooAddPdf.h"
#include "RooArgList.h"
#include "RooBreitWigner.h"
#include "RooCBShape.h"
#include "RooDataSet.h"
#include "RooExponential.h"
#include "RooFFTConvPdf.h"
#include "RooGaussian.h"
#include "RooPlot.h"
#include "RooRealVar.h"
#include "RooWorkspace.h"

#include "TCanvas.h"
#include "TROOT.h"
#include "TStopwatch.h"
#include "TStyle.h"
#include "TTree.h"
#include "TLatex.h"

// #include "tdrstyle.C"

#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif

using namespace RooFit;
using namespace std;
RooWorkspace ws1("ws1", "ws1");

double oplus(double x, double y) {
  return TMath::Sqrt(x*x + y*y);
}

void calcEff(double p, double ep, double f, double ef, double &eff, double &eeff) {
   eff = p / (p+f);
   eeff = eff * (1-eff) * oplus(ep/p, ef/f);
   cout << eff << " +/- " << eeff << endl;
}

RooDataSet * getData(
       const RooRealVar &mmgMass,
       const char *filename = "pixelMatch_data_Nov4ReReco.dat",
       const char *cut = "minDEta > 0.04 ||  minDPhi > 0.25"
     )
{

  // Read data set
  TTree tree("tree", "fit data");
  tree.ReadFile(filename,
         "Row/I:"
         "Instance:"
         "nVertices:"
         "mmgMass/F:"
         "phoPt:"
         "phoEta:"
         "minDEta:"
         "minDeltaR:"
         "phoHasPixelMatch/I:"
         "phoPdgId:"
         "phoMomPdgId:"
         "phoMomStatus:"
         "isFSR:"
         "isISR:"
         "minDPhi/F"
         "minDTheta"
       );

  RooRealVar nVertices("nVertices", "nVertices", 0, 99);
  RooRealVar minDEta("minDEta", "minDEta", 0, 99);
  RooRealVar minDPhi("minDPhi", "minDPhi", 0, 99);
  RooRealVar phoEta("phoEta", "#eta^{#gamma}", -3, 3);
  RooRealVar phoPt("phoPt", "p_{T}^{#gamma}", 0, 7e3);
  RooRealVar minDeltaR("minDeltaR", "minDeltaR", 0, 99);
  RooRealVar phoHasPixelMatch("phoHasPixelMatch", "phoHasPixelMatch", -1, 2);
  RooCategory isFSR("isFSR", "isFSR");
  isFSR.defineType("true", 1);
  isFSR.defineType("false", 0);


  RooArgSet vars = RooArgSet(
                     nVertices,
                     mmgMass,
                     minDEta,
                     minDPhi,
                     phoEta,
                     phoPt,
                     minDeltaR,
                     phoHasPixelMatch,
                     isFSR
                   );

  RooDataSet *data = new RooDataSet("data",
                                    "pho pixel match data",
                                    &tree,
                                    vars,
                                    cut);

  std::cout << "Selected events: " << data->sumEntries() << cout::endl;

  return data;
}  // end get data


RooAddPdf fitBWxCBPlusExp(
  const RooRealVar & mass,
  const RooDataSet * data,
  TVirtualPad *c=0,
  const char *suffix = "",
  float cbBiasVal  = -1,
  float cbSigmaVal = -1,
  float cbCutVal   = -1,
  float cbPowerVal = -1,
  float expRateVal =  99,
  const char* plotOpt = "NEU",
  const int nbins = 60)
{

// Build p.d.f.

////////////////////////////////////////////////
//             Parameters                     //
////////////////////////////////////////////////

//  Signal p.d.f. parameters
//  Parameters for a Gaussian and a Crystal Ball Lineshape
  RooRealVar  cbBias ("#Deltam_{CB}", "CB Bias", 0.05, -2, 2,"GeV/c^{2}");
  RooRealVar  cbSigma("#sigma_{CB}","CB Width", 1.38, 0.01, 10.0,"GeV/c^{2}");
  RooRealVar  cbCut  ("a_{CB}","CB Cut", 1.5, 0.1, 2.0);
  RooRealVar  cbPower("n_{CB}","CB Power", 1.3, 0.1, 20.0);

//   cbSigma.setConstant(kTRUE);
//   cbCut.setConstant(kTRUE);
//   cbPower.setConstant(kTRUE);

//  Parameters for Breit-Wigner
  RooRealVar bwMean("m_{Z}","BW Mean", 91.1876, "GeV/c^{2}");
  RooRealVar bwWidth("#Gamma_{Z}", "BW Width", 2.4952, "GeV/c^{2}");

  // Keep Breit-Wigner parameters fixed to the PDG values
//   bwMean.setConstant(kTRUE);
//   bwWidth.setConstant(kTRUE);


//  Background p.d.f. parameters
// Parameters for exponential
  RooRealVar expRate("#lambda_{exp}", "Exponential Rate", -0.119, -10, 1);

//   expRate.setConstant(kTRUE);



// fraction of signal
//  RooRealVar  frac("frac", "Signal Fraction", 0.1,0.,0.3.);
/*  RooRealVar  nsig("N_{S}", "#signal events", 9000, 0.,10000.);
  RooRealVar  nbkg("N_{B}", "#background events", 1000,2,10000.);*/
  RooRealVar  nsig("N_{S}", "#signal events", 29300, 0.1, 100000.);
  RooRealVar  nbkg("N_{B}", "#background events", 0, 0., 10000.);

//   nbkg.setConstant(kTRUE);

  if (cbBiasVal > 0) {
    cbBias.setVal(cbBiasVal);
    cbBias.setConstant();
  }

  if (cbSigmaVal > 0) {
    cbSigma.setVal(cbSigmaVal);
    cbSigma.setConstant();
  }

  if (cbCutVal > 0) {
    cbCut.setVal(cbCutVal);
    cbCut.setConstant();
  }

  if (cbPowerVal > 0) {
    cbPower.setVal(cbPowerVal);
    cbPower.setConstant();
  }

  if (expRateVal < 1) {
    expRate.setVal(expRateVal);
    expRate.setConstant();
  }


////////////////////////////////////////////////
//               P.D.F.s                      //
////////////////////////////////////////////////

// Di-photon mass signal p.d.f.
  RooBreitWigner bw("bw", "bw", mass, bwMean, bwWidth);
//   RooGaussian    signal("signal", "A  Gaussian Lineshape", mass, m0, sigma);
  RooCBShape     cball("cball", "A  Crystal Ball Lineshape", mass, cbBias, cbSigma, cbCut, cbPower);

  mass.setBins(100000, "fft");
  RooFFTConvPdf BWxCB("BWxCB","bw (X) crystall ball", mass, bw, cball);


// Di-photon mass background  p.d.f.
  RooExponential bg("bg","bkgd exp", mass, expRate);

// Di-photon mass model p.d.f.
  RooAddPdf      model("model", "signal + background mass model", RooArgList(BWxCB, bg), RooArgList(nsig, nbkg));


  TStopwatch t ;
  t.Start() ;
  model.fitTo(*data,FitOptions("mh"),Optimize(0),Timer(1),Extended());
//   signal->fitTo(*data,FitOptions("mh"),Optimize(0),Timer(1));

  t.Print() ;

  if (!c)
    TCanvas *c = new TCanvas("c","Unbinned Invariant Mass Fit", 0,0,800,600);
// Plot the fit results
  Double_t minMass = 60, maxMass = 120;
  RooPlot* plot = mass.frame(Range(minMass,maxMass),Bins(nbins));

// Plot 1
//   dataB->plotOn(plot, MarkerColor(kRed), LineColor(kRed));
  data->plotOn(plot);
//   model.plotOn(plot);
  model.plotOn(plot);
  //model.paramOn(plot, Format(plotOpt, AutoPrecision(1)), Parameters(RooArgSet(nsig, nbkg, m0, sigma)));
  model.paramOn(plot,
                Format(plotOpt, AutoPrecision(2) ),
                Parameters(RooArgSet(cbBias,
                                     cbSigma,
                                     cbCut,
                                     cbPower,
                                     bwMean,
                                     bwWidth,
                                     expRate,
                                     nsig,
                                     nbkg)),
                Layout(.67, 0.97, 0.97),
                ShowConstants(kTRUE) );

//   model.plotOn(plot, Components("signal"), LineStyle(kDashed), LineColor(kRed));
  model.plotOn(plot, Components("bg"), LineStyle(kDashed), LineColor(kRed));


  plot->Draw();

//   TLatex *   tex = new TLatex(0.2,0.8,"CMS preliminary");
//   tex->SetNDC();
//   tex->SetTextFont(42);
//   tex->SetLineWidth(2);
//   tex->Draw();
//   tex->DrawLatex(0.2, 0.725, "7 TeV Data, L = 258 pb^{-1}");
//
//   float fsig_peak = NormalizedIntegral(model,
//                       mass,
//                       cbBias.getVal() - 2.5*cbSigma.getVal(),
//                       cbBias.getVal() + 2.5*cbSigma.getVal()
//                     );

//   float fbkg_peak = NormalizedIntegral(bg,
//                       mass,
//                       m0.getVal() - 2.5*sigma.getVal(),
//                       m0.getVal() + 2.5*sigma.getVal()
//                     );

/*  double nsigVal = fsig_peak * nsig.getVal();
  double nsigErr = fsig_peak * nsig.getError();
  double nsigErrRel = nsigErr / nsigVal;*/
//   double nbkgVal = fbkg_peak * nbkg.getVal();
//   double nbkgErr = fbkg_peak * nbkg.getError();
//   double nbkgErrRel = nbkgErr / nbkgVal;

//   cout << "nsig " << nsigVal << " +/- " << nsigErr << endl;
//   cout << "S/B_{#pm2.5#sigma} " << nsigVal/nbkgVal << " +/- "
//     << (nsigVal/nbkgVal)*sqrt(nsigErrRel*nsigErrRel + nbkgErrRel*nbkgErrRel)
//     << endl;

//   tex->DrawLatex(0.2, 0.6, Form("N_{S} = %.0f#pm%.0f", nsigVal, nsigErr) );
//   tex->DrawLatex(0.2, 0.525, Form("S/B_{#pm2.5#sigma} = %.1f", nsigVal/nbkgVal) );
//   tex->DrawLatex(0.2, 0.45, Form("#frac{S}{#sqrt{B}}_{#pm2.5#sigma} = %.1f", nsigVal/sqrt(nbkgVal)));

//   leg = new TLegend(0.65,0.6,0.9,0.75);
//   leg->SetFillColor(kWhite);
//   leg->SetLineColor(kWhite);
//   leg->SetShadowColor(kWhite);
//   leg->SetTextFont(42);

//   TLegendEntry * ldata  = leg->AddEntry(data, "Opposite Sign");
//   TLegendEntry * ldataB = leg->AddEntry(dataB, "Same Sign");
//   ldata->SetMarkerStyle(20);
//   ldataB->SetMarkerStyle(20);
//   ldataB->SetMarkerColor(kRed);

//   leg->Draw();

  if (strlen(suffix) > 0) {
    const char *name = nsig.GetName();
    ws1.import(nsig, RenameVariable(name, Form("%s_%s", name, suffix) ) );
    const char *name = nbkg.GetName();
    ws1.import(nbkg, RenameVariable(name, Form("%s_%s", name, suffix) ) );
  } else {
    ws1.import(nsig);
    ws1.import(nbkg);
  }

  return model;

}


fitGaussPlusPoly(
  const RooRealVar & mass,
  const RooDataSet * data,
  TVirtualPad *c=0,
  int floatGaussMean=1,
  const char* plotOpt = "NEU",
  const int nbins = 60)
)
{
  // signal
  RooRealVar mean("mean","mean of gaussian",91.19,80,100) ;
  RooRealVar sigma("sigma","width of gaussian",3,2.5, 10) ;
  RooGaussian gauss("gauss","gaussian PDF",mass,mean,sigma) ;

  if (!floatGaussMean) mean.setConstant();

  // Construct background pdf
  RooRealVar a0("a0","a0",-0.1,-1,1) ;
  RooRealVar a1("a1","a1",0.004,-1,1) ;
  RooChebychev bg("bg","bg",mass, RooArgSet(a0)) ;

  // Construct composite pdf
  RooRealVar  nsig("N_{S}", "#signal events", 29300, 0.1, 100000.);
  RooRealVar  nbkg("N_{B}", "#background events", 0, 0., 10000.);

  RooAddPdf   model("model",
                    "signal + background mass model",
                    RooArgList(gauss, bg),
                    RooArgList(nsig, nbkg)
              );


  TStopwatch t ;
  t.Start() ;
  model.fitTo(*data,FitOptions("mh"),Optimize(0),Timer(1));
//   signal->fitTo(*data,FitOptions("mh"),Optimize(0),Timer(1));

  t.Print() ;

  if (!c) {
    TCanvas *c = new TCanvas("c","Unbinned Invariant Mass Fit", 0,0,800,600);
  }
// Plot the fit results
  Double_t minMass = 60, maxMass = 120;
  RooPlot* plot = mass.frame(Range(minMass,maxMass),Bins(nbins));

// Plot 1
//   dataB->plotOn(plot, MarkerColor(kRed), LineColor(kRed));
  data->plotOn(plot);
//   model.plotOn(plot);
  model.plotOn(plot);
  //model.paramOn(plot, Format(plotOpt, AutoPrecision(1)), Parameters(RooArgSet(nsig, nbkg, m0, sigma)));
  model.paramOn(plot,
                Format(plotOpt, AutoPrecision(2) ),
                Parameters(RooArgSet(mean, sigma, a0, a1,
                                     nsig,
                                     nbkg)),
                Layout(.67, 0.97, 0.97),
                ShowConstants(kTRUE) );

//   model.plotOn(plot, Components("signal"), LineStyle(kDashed), LineColor(kRed));
  model.plotOn(plot, Components("bg"), LineStyle(kDashed), LineColor(kRed));


  plot->Draw();
}


void tnp()
{
  gROOT->ProcessLine(".L tdrstyle.C");
  setTDRStyle();
  gStyle->SetPadRightMargin(0.05);

  const char *selection =
    "(minDEta > 0.04 | minDPhi > 0.5) &"
    "minDeltaR < 1 &"
//     "20 <= phoPt &"
    "10 <= phoPt & phoPt < 20 &"
//     "5 <= phoPt & phoPt < 10 &"
    "abs(phoEta) < 1.5";

   RooRealVar mmgMass("mmgMass","m_{#mu#mu#gamma}", 60, 120, "GeV");
   RooDataSet *mcDataPass = getData(
                        mmgMass,
                        "pixelMatch_Powheg_Fall10_v2.dat",
                        Form("%s & phoHasPixelMatch < 0.5", selection)
                      );

   RooDataSet *mcDataFail = getData(
                        mmgMass,
                        "pixelMatch_Powheg_Fall10_v2.dat",
                        Form("%s & phoHasPixelMatch > 0.5", selection)
                      );
   RooDataSet *realDataPass = getData(
                        mmgMass,
                        "pixelMatch_data_Nov4ReReco_v2.dat",
                        Form("%s & phoHasPixelMatch < 0.5", selection)
                      );
   RooDataSet *realDataFail = getData(
                        mmgMass,
                        "pixelMatch_data_Nov4ReReco_v2.dat",
                        Form("%s & phoHasPixelMatch > 0.5", selection)
                      );

   TCanvas *c1 = new TCanvas("c","Unbinned Invariant Mass Fit", 0,0,1200,900);
   c1->Divide(2,2);
   fitBWxCBPlusExp (mmgMass, realDataPass, c1->cd(1), "dataPass",
     -1, // cbBias
     -1, // cbSigma
     1.75, // cbCut
     -1, // cbPower
     99 // expRate
   );
//    fitGaussPlusPoly(mmgMass, realDataFail, c1->cd(2), ");
   fitBWxCBPlusExp(mmgMass, realDataFail, c1->cd(2), "dataFail",
     -1, // cbBias
     2.44678, // cbSigma
     2.0, // cbCut
     9.24028e-01, // cbPower
     -5.32862e-03 // expRate
   );
   fitBWxCBPlusExp (mmgMass, mcDataPass  , c1->cd(3), "mcPass" );
//    fitGaussPlusPoly(mmgMass, mcDataFail  , c1->cd(4) );
   fitBWxCBPlusExp(mmgMass, mcDataFail  , c1->cd(4), "mcFail",
     -1, // cbBias
     2.45, // cbSigma
     2.0, // cbCut
     9.24028e-01, // cbPower
     -5.32862e-03 // expRate
   );

   ws1.Print();

   // passing probes in MC
   double p_mc  = ws1.var("N_{S}_mcPass")->getVal();
   double ep_mc = ws1.var("N_{S}_mcPass")->getError();

   // failing probes in MC
   double f_mc  = ws1.var("N_{S}_mcFail")->getVal();
   double ef_mc = ws1.var("N_{S}_mcFail")->getError();

   // passing probes in data
   double p_data  = ws1.var("N_{S}_dataPass")->getVal();
   double ep_data = ws1.var("N_{S}_dataPass")->getError();

   // failing probes in data
   double f_data  = ws1.var("N_{S}_dataFail")->getVal();
   double ef_data = ws1.var("N_{S}_dataFail")->getError();

   double eff, eeff;

   cout << "MC   eff: ";
   calcEff(p_mc, ep_mc, f_mc, ef_mc, eff, eeff);
   cout << endl;

   cout << "data eff: ";
   calcEff(p_data, ep_data, f_data, ef_data, eff, eeff);
   cout << endl;
}