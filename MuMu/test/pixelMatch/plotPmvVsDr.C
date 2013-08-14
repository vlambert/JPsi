// void plotPmvVsDr()
{
  TFile *_file0 = new TFile("pixelMatchHistos_Nov4ReReco_Fall10_v1.root");

  h_drNear_EB_zfsr = (TH1F*) _file0->Get("h_drNear_EB_zfsr");
  h_drNear_EB_data38x = (TH1F*) _file0->Get("h_drNear_EB_data38x");
  h_drNear_EB_pass_zfsr = (TH1F*) _file0->Get("h_drNear_EB_pass_zfsr");
  h_drNear_EB_pass_data38x = (TH1F*) _file0->Get("h_drNear_EB_pass_data38x");


  TGraphAsymmErrors *gr = new TGraphAsymmErrors();
  gr->BayesDivide(h_drNear_EB_pass_zfsr, h_drNear_EB_zfsr);
  gr->GetXaxis()->SetTitle("min #DeltaR(#mu,#gamma)");
  gr->GetYaxis()->SetTitle("Pixel Match Veto Efficiency");
  gr->SetTitle("POWHEG+Pythia Z#rightarrow#mu#mu Fall10 MC, FSR events");
  gr->Draw("ap");
  TGraphAsymmErrors *gr_mc = gr;

  new TCanvas();
  gr = new TGraphAsymmErrors();
  gr->BayesDivide(h_drNear_EB_pass_data38x, h_drNear_EB_data38x);
  gr->GetXaxis()->SetTitle("min #DeltaR(#mu,#gamma)");
  gr->GetYaxis()->SetTitle("Pixel Match Veto Efficiency");
  gr->SetTitle("2010 Data, L = 36.1 pb^{-1}");
  gr->Draw("ap");
  TGraphAsymmErrors *gr_data = gr;

  TH1F *hpass0 = h_drNear_EB_pass_zfsr;
  TH1F *htot0  = h_drNear_EB_zfsr;
  double xbins[] = {0., 0.01, 0.02, 0.05, 0.1, 0.2, 1.};
  hpass = new TH1F("hpass_mc", "hpass", sizeof(xbins)/sizeof(double)-1, xbins);
  htot  = new TH1F("htot_mc", "htot", sizeof(xbins)/sizeof(double)-1, xbins);

  for (int bin = 1; bin <= hpass0->GetNbinsX(); ++bin) {
    hpass->Fill(hpass0->GetBinCenter(bin), hpass0->GetBinContent(bin));
    htot ->Fill(htot0 ->GetBinCenter(bin), htot0 ->GetBinContent(bin));
  }

  new TCanvas();
  gr = new TGraphAsymmErrors();
  gr->BayesDivide(hpass, htot);
  gr->GetXaxis()->SetTitle("min #DeltaR(#mu,#gamma)");
  gr->GetYaxis()->SetTitle("Pixel Match Veto Efficiency");
  gr->SetTitle("POWHEG+Pythia Z#rightarrow#mu#mu Fall10 MC, FSR events");
  gr->Draw("ap");

  nbins = sizeof(xbins)/sizeof(double);
  int last_bin = nbins-2;
  printf("MC: %.1f + %.1f - %.1f %%\n",
         100. * gr->GetY()[last_bin],
         100. * gr->GetErrorYhigh(last_bin),
         100. * gr->GetErrorYlow(last_bin)
         );

  TGraphAsymmErrors *gr_mc_varbins = gr;

  hpass0 = h_drNear_EB_pass_data38x;
  htot0  = h_drNear_EB_data38x;
  double xbins[] = {0., 0.01, 0.02, 0.05, 0.1, 0.2, 1.};
  hpass = new TH1F("hpass_data", "hpass", sizeof(xbins)/sizeof(double)-1, xbins);
  htot  = new TH1F("htot_data", "htot", sizeof(xbins)/sizeof(double)-1, xbins);

  for (int bin = 1; bin <= hpass0->GetNbinsX(); ++bin) {
    hpass->Fill(hpass0->GetBinCenter(bin), hpass0->GetBinContent(bin));
    htot ->Fill(htot0 ->GetBinCenter(bin), htot0 ->GetBinContent(bin));
  }

  new TCanvas();
  gr = new TGraphAsymmErrors();
  gr->BayesDivide(hpass, htot);
  gr->GetXaxis()->SetTitle("min #DeltaR(#mu,#gamma)");
  gr->GetYaxis()->SetTitle("Pixel Match Veto Efficiency");
  gr->SetTitle("2010 Data, L = 36.1 pb^{-1}");
  gr->Draw("ap");

  nbins = sizeof(xbins)/sizeof(double);
  last_bin = nbins-2;
  printf("data: %.1f + %.1f - %.1f %%\n",
         100. * gr->GetY()[last_bin],
         100. * gr->GetErrorYhigh(last_bin),
         100. * gr->GetErrorYlow(last_bin)
         );

  TGraphAsymmErrors *gr_data_varbins = gr;

}