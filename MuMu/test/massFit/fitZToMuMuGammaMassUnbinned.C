/** \macro fitJPsi2SMassUnbinned.C
 *
 * $Id: fitZToMuMuGammaMassUnbinned.C,v 1.6 2011/06/22 19:14:35 veverka Exp $
 *
 *
 * Macro implementing unbinned Maximum-likelihood fit of
 * the Z->mmg lineshape
 *
 * Software developed for the CMS Detector at LHC
 *
 *  \author J. Veverka - Caltech, Pasadena, USA
 *  Inspired by
 *    E. Schneider - Caltech, Pasadena, USA
 *    S. Ganzhur   - CEA/DAPNIA/SPP, Saclay
 *    Y. Yang      - Caltech, Pasadena, USA
 *
 */
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

#include "tdrstyle.C"

#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif

using namespace RooFit;

double NormalizedIntegral(RooAbsPdf & function, RooRealVar & integrationVar, double lowerLimit, double upperLimit){

  integrationVar.setRange("integralRange",lowerLimit,upperLimit);
  RooAbsReal* integral = function.createIntegral(integrationVar,NormSet(integrationVar),Range("integralRange"));


  double normlizedIntegralValue = integral->getVal();

  //  cout<<normlizedIntegralValue<<endl;


  return normlizedIntegralValue;


}

RooAddPdf fitZToMuMuGammaMassUnbinned(
  const char *filename = "ZMuMuGammaMass_36.1ipb_EE.txt",
//   const char *filename = "ZMuMuGammaMass_2.9ipb_EB.txt",
//   const char *filename = "ZMuMuGammaMass_2.9ipb_EE.txt",
//   const char *filename = "ZMuMuGammaMass_Zmumu_Spring10_EB.txt",
//   const char *filename = "DimuonMass_data_Nov4ReReco.txt",

  const char* plotOpt = "NEU",
  const int nbins = 60)
{
  gROOT->ProcessLine(".L tdrstyle.C");
  setTDRStyle();
  gStyle->SetPadRightMargin(0.05);

  double minMass = 60;
  double maxMass = 120;
  RooRealVar  mass("mass","m(#mu#mu#gamma)", minMass, maxMass,"GeV/c^{2}");

  // Read data set

  RooDataSet *data = RooDataSet::read(filename,RooArgSet(mass));
//   RooDataSet *dataB = RooDataSet::read(filenameB,RooArgSet(mass));

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
  model.fitTo(*data,FitOptions("mh"),Optimize(0),Timer(1));
//   signal->fitTo(*data,FitOptions("mh"),Optimize(0),Timer(1));

  t.Print() ;

  TCanvas *c = new TCanvas("c","Unbinned Invariant Mass Fit", 0,0,800,600);
// Plot the fit results
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

  return model;

}

