// void plotPmvVsDr()
{
  TFile *_file0 = new TFile("pixelMatchHistos_Nov4ReReco_Fall10_v2.root");

  h_dPhi_EB_zfsr = (TH1F*) _file0->Get("h_dPhi_EB_zfsr");
  h_dPhi_EB_data38x = (TH1F*) _file0->Get("h_dPhi_EB_data38x");
  h_dPhi_EB_pass_zfsr = (TH1F*) _file0->Get("h_dPhi_EB_pass_zfsr");
  h_dPhi_EB_pass_data38x = (TH1F*) _file0->Get("h_dPhi_EB_pass_data38x");


  TGraphAsymmErrors *gr = new TGraphAsymmErrors();
  gr->BayesDivide(h_dPhi_EB_pass_zfsr, h_dPhi_EB_zfsr);
  gr->GetXaxis()->SetTitle("#Delta#phi(#mu_{near},#gamma)");
  gr->GetYaxis()->SetTitle("Pixel Match Veto Efficiency");
  gr->SetTitle("POWHEG+Pythia Z#rightarrow#mu#mu Fall10 MC, FSR events");
  gr->Draw("ap");
  TGraphAsymmErrors *gr_mc = gr;

  new TCanvas();
  gr = new TGraphAsymmErrors();
  gr->BayesDivide(h_dPhi_EB_pass_data38x, h_dPhi_EB_data38x);
  gr->GetXaxis()->SetTitle("#Delta#phi(#mu_{near},#gamma)");
  gr->GetYaxis()->SetTitle("Pixel Match Veto Efficiency");
  gr->SetTitle("2010 Data, L = 36.1 pb^{-1}");
  gr->Draw("ap");
  TGraphAsymmErrors *gr_data = gr;

  TH1F *hpass0 = h_dPhi_EB_pass_zfsr;
  TH1F *htot0  = h_dPhi_EB_zfsr;
  double xbins[] = {0., 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04,
                    0.045, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                    0.12, 0.14, 0.16, 0.18, 0.2,
                    0.22, 0.24, 0.26, 0.28, 0.3,
                    0.35, 0.45, 0.5, 1.};
  int nbins = sizeof(xbins) / sizeof(double) - 1;

  hpass = new TH1F("hpass_mc", "hpass", nbins, xbins);
  htot  = new TH1F("htot_mc", "htot", nbins, xbins);

  for (int bin = 1; bin <= hpass0->GetNbinsX(); ++bin) {
    hpass->Fill(hpass0->GetBinCenter(bin), hpass0->GetBinContent(bin));
    htot ->Fill(htot0 ->GetBinCenter(bin), htot0 ->GetBinContent(bin));
  }

  new TCanvas();
  gr = new TGraphAsymmErrors();
  gr->BayesDivide(hpass, htot);
  gr->GetXaxis()->SetTitle("#Delta#phi(#mu_{near},#gamma)");
  gr->GetYaxis()->SetTitle("Pixel Match Veto Efficiency");
  gr->SetTitle("POWHEG+Pythia Z#rightarrow#mu#mu Fall10 MC, FSR events");
  gr->Draw("ap");

  int last_point = gr->GetN() - 1; // counting from 0

  printf("MC: %.1f + %.1f - %.1f %%\n",
         100. * gr->GetY()[last_point],
         100. * gr->GetErrorYhigh(last_point),
         100. * gr->GetErrorYlow(last_point)
         );

  TGraphAsymmErrors *gr_mc_varbins = gr;

  hpass0 = h_dPhi_EB_pass_data38x;
  htot0  = h_dPhi_EB_data38x;

  hpass = new TH1F("hpass_data", "hpass", nbins, xbins);
  htot  = new TH1F("htot_data", "htot", nbins, xbins);

  for (int bin = 1; bin <= hpass0->GetNbinsX(); ++bin) {
    hpass->Fill(hpass0->GetBinCenter(bin), hpass0->GetBinContent(bin));
    htot ->Fill(htot0 ->GetBinCenter(bin), htot0 ->GetBinContent(bin));
  }

  new TCanvas();
  gr = new TGraphAsymmErrors();
  gr->BayesDivide(hpass, htot);
  gr->GetXaxis()->SetTitle("#Delta#phi(#mu_{near},#gamma)");
  gr->GetYaxis()->SetTitle("Pixel Match Veto Efficiency");
  gr->SetTitle("2010 Data, L = 36.1 pb^{-1}");
  gr->Draw("ap");

  int last_point = gr->GetN() - 1; // counting from 0

  printf("data: %.1f + %.1f - %.1f %%\n",
         100. * gr->GetY()[last_point],
         100. * gr->GetErrorYhigh(last_point),
         100. * gr->GetErrorYlow(last_point)
         );

  TGraphAsymmErrors *gr_data_varbins = gr;

}