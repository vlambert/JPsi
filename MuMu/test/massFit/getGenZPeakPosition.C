void getGenZPeakPosition() {

  using namespace RooFit;

  RooRealVar  mass("mass","m(#mu#mu#gamma)", 40, 150,"GeV/c^{2}");
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


  TCanvas *c = new TCanvas("c","Unbinned Invariant Mass Fit", 0,0,800,600);
// Plot the fit results
  RooPlot* plot = mass.frame(); //Range(minMass,maxMass),Bins(nbins));

// Plot 1
  model.plotOn(plot);
  model.paramOn(plot,
                Format("NEU", AutoPrecision(2) ),
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

}