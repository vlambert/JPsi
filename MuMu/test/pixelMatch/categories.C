{
  gROOT->LoadMacro("tnp.C");
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
   RooPlot *mplot = mmgMass.frame();
   mcDataPass->plotOn(mplot);
   mcDataPass->plotOn(mplot, Cut("isFSR==isFSR::true"), LineColor(kBlue), MarkerColor(kBlue));
   mcDataPass->plotOn(mplot, Cut("isFSR==isFSR::true"), LineColor(kBlue), MarkerColor(kBlue));
}