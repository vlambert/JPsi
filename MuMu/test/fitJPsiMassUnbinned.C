/** \macro fitJPsiMassUnbinned.C
 *
 * $Id: fitJPsiMassUnbinned.C,v 1.4 2010/07/25 16:53:31 veverka Exp $
 *
 *
 * Macro implementing unbinned Maximum-likelihood fit of
 * the pi0->gg lineshape modified for the J/psi->mu+mu-
 *
 * Software developed for the CMS Detector at LHC
 *
 *
 *  \author S. Ganzhur - CEA/DAPNIA/SPP, Saclay
 *  \author Y. Yang    - Caltech, Pasadena, USA
 *  \author J. Veverka - Caltech, Pasadena, USA
 *
 */


using namespace RooFit;

double NormalizedIntegral(RooAbsPdf & function, RooRealVar & integrationVar, double lowerLimit, double upperLimit){

  integrationVar.setRange("integralRange",lowerLimit,upperLimit);
  RooAbsReal* integral = function.createIntegral(integrationVar,NormSet(integrationVar),Range("integralRange"));


  double normlizedIntegralValue = integral->getVal();

  //  cout<<normlizedIntegralValue<<endl;


  return normlizedIntegralValue;


}

fitJPsiMassUnbinned(const char *filename = "JPsiMassOS_186nb.txt",
  const char* plotOpt = "NEU",
  const int nbins = 50,
  const char* filenameB = "JPsiMassSS_186nb.txt")
{

  gROOT->ProcessLine(".L tdrstyle.C");
  setTDRStyle();
  gStyle->SetPadRightMargin(0.05);

  RooRealVar  mass("mass","M^{#mu#mu}", 2.6, 3.5,"GeV/c^{2}");

  // Read data set

  RooDataSet *data = RooDataSet::read(filename,RooArgSet(mass));
  RooDataSet *dataB = RooDataSet::read(filenameB,RooArgSet(mass));

// Build p.d.f.

////////////////////////////////////////////////
//             Parameters                     //
////////////////////////////////////////////////

//  Signal p.d.f. parameters
//  Parameters for a Gaussian and a Crystal Ball Lineshape
  RooRealVar  m0   ("m_{0}", "Bias", 3.1, 2.9, 3.3,"GeV/c^{2}");
  RooRealVar  sigma("#sigma","Width", 0.04,0.01,0.1,"GeV/c^{2}");
  RooRealVar  cut  ("#alpha","Cut", 0.6,0.6,2.0);
  RooRealVar  power("power","Power", 10.0, 0.5, 20.0);


//  Background p.d.f. parameters
//  Parameters for a polynomial lineshape
  RooRealVar  c0("c_{0}", "c0", 0., -10, 10);
  RooRealVar  c1("c_{1}", "c1", 0., -100, 0);
  RooRealVar  c2("c_{2}", "c2", 0., -100, 100);
//  c0.setConstant();

// fraction of signal
//  RooRealVar  frac("frac", "Signal Fraction", 0.1,0.,0.3.);
  RooRealVar  nsig("N_{S}", "#signal events", 9000, 0.,10000.);
  RooRealVar  nbkg("N_{B}", "#background events", 1000,2,10000.);



////////////////////////////////////////////////
//               P.D.F.s                      //
////////////////////////////////////////////////

// Di-photon mass signal p.d.f.
  RooGaussian    signal("signal", "A  Gaussian Lineshape", mass, m0, sigma);
  // RooCBShape     signal("signal", "A  Crystal Ball Lineshape", mass, m0,sigma, cut, power);

// Di-photon mass background  p.d.f.
  RooPolynomial bg("bg", "Backgroung Distribution", mass, RooArgList(c0,c1));

// Di-photon mass model p.d.f.
//  RooAddPdf      model("model", "Di-photon mass model", signal, bg, frac);
  RooAddPdf      model("model", "Di-photon mass model", RooArgList(signal, bg), RooArgList(nsig, nbkg));


  TStopwatch t ;
  t.Start() ;
  model->fitTo(*data,FitOptions("mh"),Optimize(0),Timer(1));

  t.Print() ;

  c = new TCanvas("c","J/psi->mu mu Distributions", 0,0,800,600);
// Plot the fit results
  RooPlot* plot = mass.frame(Range(2.6,3.5),Bins(nbins));

// Plot 1
  dataB->plotOn(plot, MarkerColor(kRed));
  data->plotOn(plot);
  model.plotOn(plot);
  //model.paramOn(plot, Format(plotOpt, AutoPrecision(1)), Parameters(RooArgSet(nsig, nbkg, m0, sigma)));
  model.paramOn(plot, Format(plotOpt, AutoPrecision(1)), Parameters(RooArgSet(m0, sigma)));

  /// model.plotOn(plot, Components("signal"), LineStyle(kDashed), LineColor(kRed));

  model.plotOn(plot, Components("bg"), LineStyle(kDashed), LineColor(kRed));


  plot->Draw();

  TLatex *   tex = new TLatex(0.2,0.8,"CMS preliminary");
  tex->SetTextFont(42);
  tex->SetNDC();
  tex->SetLineWidth(2);
  tex->Draw();
  tex->DrawLatex(0.2, 0.725, "#sqrt{s} = 7 TeV");
  tex->DrawLatex(0.2, 0.650, "L = 186 nb^{-1}");

  float fsig_peak = NormalizedIntegral(signal,
                      mass,
                      m0.getVal() - 2.5*sigma.getVal(),
                      m0.getVal() + 2.5*sigma.getVal()
                    );

  float fbkg_peak = NormalizedIntegral(bg,
                      mass,
                      m0.getVal() - 2.5*sigma.getVal(),
                      m0.getVal() + 2.5*sigma.getVal()
                    );

  double nsigVal = fsig_peak * nsig.getVal();
  double nsigErr = fsig_peak * nsig.getError();
  double nsigErrRel = nsigErr / nsigVal;
  double nbkgVal = fbkg_peak * nbkg.getVal();
  double nbkgErr = fbkg_peak * nbkg.getError();
  double nbkgErrRel = nbkgErr / nbkgVal;

  cout << "nsig " << nsigVal << " +/- " << nsigErr << endl;
  cout << "S/B_{#pm2.5#sigma} " << nsigVal/nbkgVal << " +/- "
    << (nsigVal/nbkgVal)*sqrt(nsigErrRel*nsigErrRel + nbkgErrRel*nbkgErrRel)
    << endl;

  tex->DrawLatex(0.2, 0.5, Form("N_{S} = %.0f#pm%.0f", nsigVal, nsigErr) );
  tex->DrawLatex(0.2, 0.425, Form("S/B_{#pm2.5#sigma} = %.1f", nsigVal/nbkgVal) );

  leg = new TLegend(0.65,0.6,0.9,0.75);
  leg->SetFillColor(kWhite);
  leg->SetLineColor(kWhite);
  leg->SetShadowColor(kWhite);
  leg->SetTextFont(42);

  TLegendEntry * ldata  = leg->AddEntry(data, "Opposite Sign");
  TLegendEntry * ldataB = leg->AddEntry(dataB, "Same Sign");
  ldata->SetMarkerStyle(20);
  ldataB->SetMarkerStyle(20);
  ldataB->SetMarkerColor(kRed);

  leg->Draw();

}

