/** \macro fitJPsi2SMassUnbinned.C
 *
 * $Id: ikFit.C,v 1.2 2011/03/29 00:34:50 veverka Exp $
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

#include <stdio>
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

void fit(
  const char* cut = "abs(eta) < 1.5",
  const char* label = "|#eta^{#gamma}| < 1.5",
//   const char *filename = "ikRatio-CaltechSelection_mm80_34ipb.txt",
  const char *filename = "Dec22ReReco.dat",
  const char* plotOpt = "NEU",
  const int nbins = 20
)
{
  double minik = 0.;
  double maxik = 2.;
  double minikfit = 0.;
  double maxikfit = 2.;
  RooRealVar  ik("ik","E^{#gamma}_{ECAL}/E^{#gamma}_{muons}", minik, maxik);
  RooRealVar  eta("eta","eta^{#gamma}", -3, 3);
  RooRealVar  r9("r9","R_{9}^{#gamma}", -3, 3);
  RooRealVar  m3("m3","m(#mu#mu#gamma)", 0, 999);

  // Read data set

  TTree tree("tree", "fit data");
  const char * leafVariables =
    /*  1. run                      */ "run/I:"
    /*  2. lumi                     */ "lumi:"
    /*  3. event                    */ "event:"
    /*  4. isEB                     */ "isEB:"
    /*  5. phoPt[g]                 */ "pt/F:"
    /*  6. muPt[mnear]              */ "muNearPt:"
    /*  7. muPt[mfar]               */ "muFarPt:"
    /*  8. phoEta[g]                */ "eta:"
    /*  9. muEta[mnear]             */ "muNearEta:"
    /* 10. muEta[mfar]              */ "muFarEta:"
    /* 11. phoPhi[g]                */ "phi:"
    /* 12. muPhi[mnear]             */ "muNearPhi:"
    /* 13. muPhi[mfar]              */ "muFarPhi:"
    /* 14. phoR9                    */ "r9:"
    /* 15. mass[mm]                 */ "m2:"
    /* 16. mmgMass                  */ "m3:"
    /* 17. mmgDeltaRNear            */ "dr:"
    /* 18. kRatio(mmgMass,mass[mm]) */ "ik";

  tree.ReadFile(filename, leafVariables);
  RooDataSet *data = new RooDataSet("data",
                                    "pho scale data",
                                    &tree,
                                    RooArgSet(ik, eta, r9, m3),
                                    cut);

  std::cout << "Selected events: " << data->sumEntries() << cout::endl;
//   RooDataSet *dataB = RooDataSet::read(filenameB,RooArgSet(mass));

// Build p.d.f.

////////////////////////////////////////////////
//             Parameters                     //
////////////////////////////////////////////////

//  Signal p.d.f. parameters
//  Parameters for a Gaussian
  RooRealVar  mean ("#mu", "1/k mean", 1, 0, 2);
  RooRealVar  sigma("#sigma","1/k sigma", 0.1, 0.001, 1.0);


////////////////////////////////////////////////
//               P.D.F.s                      //
////////////////////////////////////////////////

// Signal p.d.f.
  RooGaussian    model("model", "A  Gaussian Lineshape", ik, mean, sigma);

  TStopwatch t ;
  t.Start() ;
  model.fitTo(*data,FitOptions("mh"),Optimize(0),Timer(1),Range(minikfit,maxikfit));

  t.Print() ;

//   TCanvas *c = new TCanvas("c","Unbinned Invariant Mass Fit", 0,0,800,600);
// Plot the fit results
  RooPlot* plot = ik.frame(Range(minik,maxik),Bins(nbins));

// Plot 1
//   dataB->plotOn(plot, MarkerColor(kRed), LineColor(kRed));
  data->plotOn(plot);
//   model.plotOn(plot);
  model.plotOn(plot);
  //model.paramOn(plot, Format(plotOpt, AutoPrecision(1)), Parameters(RooArgSet(nsig, nbkg, m0, sigma)));
  model.paramOn(plot,
                Format(plotOpt, AutoPrecision(2) ),
                Parameters(RooArgSet(mean, sigma)),
                Layout(.6, 0.9, 0.9),
                ShowConstants(kTRUE) );

//   model.plotOn(plot, Components("signal"), LineStyle(kDashed), LineColor(kRed));
//   model.plotOn(plot, Components("bg"), LineStyle(kDashed), LineColor(kRed));


  plot->Draw();

  TLatex *   tex = new TLatex(0.2,0.875,"CMS preliminary");
  tex->SetNDC();
  tex->SetTextFont(42);
  tex->SetLineWidth(2);
  tex->Draw();
/*  tex->DrawLatex(0.2, 0.8, "Z #rightarrow #mu#mu Powheg");
  tex->DrawLatex(0.2, 0.725, "Summer10 MC");*/
  tex->DrawLatex(0.2, 0.8, "7 TeV Data");
  tex->DrawLatex(0.2, 0.725, "L = 34 pb^{-1}");
  tex->DrawLatex(0.2, 0.65, label );
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

//   return model;

}

void ikFit()
{
  gROOT->ProcessLine(".L tdrstyle.C");
  setTDRStyle();
  gStyle->SetPadRightMargin(0.05);

  TCanvas *c1 = new TCanvas("c1", "c1", 0, 0, 800, 600);
  fit("abs(eta) < 1.5 & abs(m3-91.2)<4", "|#eta^{#gamma}| < 1.5");
  TCanvas *c2 = new TCanvas("c2", "c2", 20, 20, 800, 600);
  fit("abs(eta) > 1.5 & abs(m3-91.2)<4", "|#eta^{#gamma}| > 1.5");
  TCanvas *c3 = new TCanvas("c3", "c3", 40, 40, 800, 600);
  fit("abs(eta) < 1.5 & abs(m3-91.2)<4 & r9 > 0.94", "|#eta^{#gamma}| < 1.5, r_{9}^{#gamma} > 0.94");
  TCanvas *c4 = new TCanvas("c4", "c4", 50, 50, 800, 600);
  fit("abs(eta) > 1.5 & abs(m3-91.2)<4 & r9 > 0.95", "|#eta^{#gamma}| > 1.5, r_{9}^{#gamma} > 0.95");
}

