{
//=========Macro generated from canvas: c1/c1
//=========  (Tue Jun  7 10:40:47 2011) by ROOT version5.22/00d
   TCanvas *c1 = new TCanvas("c1", "c1",24,41,800,400);
   c1->Range(0,0,1,1);
   c1->SetFillColor(0);
   c1->SetBorderMode(0);
   c1->SetBorderSize(2);
   c1->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: c1_1
   TPad *c1_1 = new TPad("c1_1", "c1_1",0.01,0.01,0.49,0.99);
   c1_1->Draw();
   c1_1->cd();
   c1_1->Range(71.25,-11.93937,108.75,107.4543);
   c1_1->SetFillColor(0);
   c1_1->SetBorderMode(0);
   c1_1->SetBorderSize(2);
   c1_1->SetFrameBorderMode(0);
   c1_1->SetFrameBorderMode(0);
   
   TH1 *hp_mc = new TH1F("hp_mc","R_{9} > 0.94",15,75,105);
   hp_mc->SetBinContent(1,2.390599);
   hp_mc->SetBinContent(2,0.9971244);
   hp_mc->SetBinContent(3,1.303846);
   hp_mc->SetBinContent(4,3.469844);
   hp_mc->SetBinContent(5,3.40258);
   hp_mc->SetBinContent(6,14.50341);
   hp_mc->SetBinContent(7,28.63037);
   hp_mc->SetBinContent(8,75.38523);
   hp_mc->SetBinContent(9,74.79257);
   hp_mc->SetBinContent(10,31.55992);
   hp_mc->SetBinContent(11,13.9126);
   hp_mc->SetBinContent(12,4.147945);
   hp_mc->SetBinContent(13,3.443571);
   hp_mc->SetBinContent(14,2.534017);
   hp_mc->SetBinContent(15,1.526363);
   hp_mc->SetMinimum(0);
   hp_mc->SetMaximum(95.51494);
   hp_mc->SetEntries(1116);
   hp_mc->SetStats(0);

   Int_t ci;   // for color index setting
   ci = TColor::GetColor("#99ccff");
   hp_mc->SetFillColor(ci);

   ci = TColor::GetColor("#99ccff");
   hp_mc->SetLineColor(ci);
   hp_mc->GetXaxis()->SetTitle("m(#mu#mu#gamma) (GeV)");
   hp_mc->GetYaxis()->SetTitle("Entries / 1 GeV");
   hp_mc->Draw("");
   
   TH1 *hpb_mc = new TH1F("hpb_mc","mmgMass {pileup.weightOOT * 0.153557 * (((phoIsEB & abs(mmgMass-90)<15 & phoPt > 20 && scEt > 10 && phoHoE < 0.5)&&(phoR9 > 0.94))&&(!isFSR))}",15,75,105);
   hpb_mc->SetBinContent(8,0.4589717);
   hpb_mc->SetBinContent(12,0.234945);
   hpb_mc->SetBinContent(13,0.3174091);
   hpb_mc->SetEntries(3);
   hpb_mc->SetStats(0);

   ci = TColor::GetColor("#99cc33");
   hpb_mc->SetFillColor(ci);

   ci = TColor::GetColor("#99cc33");
   hpb_mc->SetLineColor(ci);
   hpb_mc->Draw("same");
   
   TH1 *hpb_qcd = new TH1F("hpb_qcd","mmgMass {pileup.weightOOT * 0.278842 * ((phoIsEB & abs(mmgMass-90)<15 & phoPt > 20 && scEt > 10 && phoHoE < 0.5)&&(phoR9 > 0.94))}",15,75,105);
   hpb_qcd->SetStats(0);

   ci = TColor::GetColor("#ffff66");
   hpb_qcd->SetFillColor(ci);

   ci = TColor::GetColor("#ffff66");
   hpb_qcd->SetLineColor(ci);
   hpb_qcd->Draw("same");
   
   TH1 *hp = new TH1F("hp","mmgMass {(phoIsEB & abs(mmgMass-90)<15 & phoPt > 20 && scEt > 10 && phoHoE < 0.5)&&(phoR9 > 0.94)}",15,75,105);
   hp->SetBinContent(1,1);
   hp->SetBinContent(2,1);
   hp->SetBinContent(3,1);
   hp->SetBinContent(4,2);
   hp->SetBinContent(5,8);
   hp->SetBinContent(6,17);
   hp->SetBinContent(7,30);
   hp->SetBinContent(8,65);
   hp->SetBinContent(9,78);
   hp->SetBinContent(10,38);
   hp->SetBinContent(11,8);
   hp->SetBinContent(12,10);
   hp->SetBinContent(13,1);
   hp->SetBinContent(14,1);
   hp->SetBinContent(15,1);
   hp->SetEntries(262);
   hp->SetMarkerStyle(20);
   hp->Draw("e0same");
   
   TH1 *hp_mc = new TH1F("hp_mc","R_{9} > 0.94",15,75,105);
   hp_mc->SetBinContent(1,2.390599);
   hp_mc->SetBinContent(2,0.9971244);
   hp_mc->SetBinContent(3,1.303846);
   hp_mc->SetBinContent(4,3.469844);
   hp_mc->SetBinContent(5,3.40258);
   hp_mc->SetBinContent(6,14.50341);
   hp_mc->SetBinContent(7,28.63037);
   hp_mc->SetBinContent(8,75.38523);
   hp_mc->SetBinContent(9,74.79257);
   hp_mc->SetBinContent(10,31.55992);
   hp_mc->SetBinContent(11,13.9126);
   hp_mc->SetBinContent(12,4.147945);
   hp_mc->SetBinContent(13,3.443571);
   hp_mc->SetBinContent(14,2.534017);
   hp_mc->SetBinContent(15,1.526363);
   hp_mc->SetMinimum(0);
   hp_mc->SetMaximum(95.51494);
   hp_mc->SetEntries(1116);
   hp_mc->SetDirectory(0);
   hp_mc->SetStats(0);

   ci = TColor::GetColor("#99ccff");
   hp_mc->SetFillColor(ci);

   ci = TColor::GetColor("#99ccff");
   hp_mc->SetLineColor(ci);
   hp_mc->GetXaxis()->SetTitle("m(#mu#mu#gamma) (GeV)");
   hp_mc->GetYaxis()->SetTitle("Entries / 1 GeV");
   hp_mc->Draw("sameaxis");
   
   TPaveText *pt = new TPaveText(0.01,0.9357505,0.2184422,0.995,"blNDC");
   pt->SetName("title");
   pt->SetBorderSize(1);
   TText *text = pt->AddText("R_{9} > 0.94");
   pt->Draw();
   c1_1->Modified();
   c1->cd();
  
// ------------>Primitives in pad: c1_2
   c1_2 = new TPad("c1_2", "c1_2",0.51,0.01,0.99,0.99);
   c1_2->Draw();
   c1_2->cd();
   c1_2->Range(71.25,-12.58972,108.75,113.3075);
   c1_2->SetFillColor(0);
   c1_2->SetBorderMode(0);
   c1_2->SetBorderSize(2);
   c1_2->SetFrameBorderMode(0);
   c1_2->SetFrameBorderMode(0);
   
   TH1 *hf_mc = new TH1F("hf_mc","R_{9} < 0.94",15,75,105);
   hf_mc->SetBinContent(1,2.227835);
   hf_mc->SetBinContent(2,1.461737);
   hf_mc->SetBinContent(3,2.343367);
   hf_mc->SetBinContent(4,3.823656);
   hf_mc->SetBinContent(5,7.485086);
   hf_mc->SetBinContent(6,12.33043);
   hf_mc->SetBinContent(7,27.29893);
   hf_mc->SetBinContent(8,59.5336);
   hf_mc->SetBinContent(9,91.56161);
   hf_mc->SetBinContent(10,45.08149);
   hf_mc->SetBinContent(11,21.85184);
   hf_mc->SetBinContent(12,7.575786);
   hf_mc->SetBinContent(13,2.608295);
   hf_mc->SetBinContent(14,2.238171);
   hf_mc->SetBinContent(15,2.578175);
   hf_mc->SetMinimum(0);
   hf_mc->SetMaximum(100.7178);
   hf_mc->SetEntries(1364);
   hf_mc->SetStats(0);

   ci = TColor::GetColor("#99ccff");
   hf_mc->SetFillColor(ci);

   ci = TColor::GetColor("#99ccff");
   hf_mc->SetLineColor(ci);
   hf_mc->GetXaxis()->SetTitle("m(#mu#mu#gamma) (GeV)");
   hf_mc->GetYaxis()->SetTitle("Entries / 5 GeV");
   hf_mc->Draw("");
   
   TH1 *hfb_mc = new TH1F("hfb_mc","mmgMass {pileup.weightOOT * 0.153557 * (((phoIsEB & abs(mmgMass-90)<15 & phoPt > 20 && scEt > 10 && phoHoE < 0.5)&&(!(phoR9 > 0.94)))&&(!isFSR))}",15,75,105);
   hfb_mc->SetBinContent(8,0.7849345);
   hfb_mc->SetBinContent(9,0.7789978);
   hfb_mc->SetBinContent(12,0.05842461);
   hfb_mc->SetBinContent(13,0.07675707);
   hfb_mc->SetBinContent(14,0.08758801);
   hfb_mc->SetBinContent(15,0.6225014);
   hfb_mc->SetEntries(11);
   hfb_mc->SetStats(0);

   ci = TColor::GetColor("#99cc33");
   hfb_mc->SetFillColor(ci);

   ci = TColor::GetColor("#99cc33");
   hfb_mc->SetLineColor(ci);
   hfb_mc->Draw("same");
   
   TH1 *hf = new TH1F("hf","mmgMass {(phoIsEB & abs(mmgMass-90)<15 & phoPt > 20 && scEt > 10 && phoHoE < 0.5)&&(!(phoR9 > 0.94))}",15,75,105);
   hf->SetBinContent(1,1);
   hf->SetBinContent(2,3);
   hf->SetBinContent(3,3);
   hf->SetBinContent(4,4);
   hf->SetBinContent(5,10);
   hf->SetBinContent(6,15);
   hf->SetBinContent(7,28);
   hf->SetBinContent(8,60);
   hf->SetBinContent(9,74);
   hf->SetBinContent(10,53);
   hf->SetBinContent(11,24);
   hf->SetBinContent(12,2);
   hf->SetBinContent(13,5);
   hf->SetBinContent(14,3);
   hf->SetBinContent(15,5);
   hf->SetEntries(290);
   hf->SetMarkerStyle(20);
   hf->Draw("e0same");
   
   TH1 *hf_mc = new TH1F("hf_mc","R_{9} < 0.94",15,75,105);
   hf_mc->SetBinContent(1,2.227835);
   hf_mc->SetBinContent(2,1.461737);
   hf_mc->SetBinContent(3,2.343367);
   hf_mc->SetBinContent(4,3.823656);
   hf_mc->SetBinContent(5,7.485086);
   hf_mc->SetBinContent(6,12.33043);
   hf_mc->SetBinContent(7,27.29893);
   hf_mc->SetBinContent(8,59.5336);
   hf_mc->SetBinContent(9,91.56161);
   hf_mc->SetBinContent(10,45.08149);
   hf_mc->SetBinContent(11,21.85184);
   hf_mc->SetBinContent(12,7.575786);
   hf_mc->SetBinContent(13,2.608295);
   hf_mc->SetBinContent(14,2.238171);
   hf_mc->SetBinContent(15,2.578175);
   hf_mc->SetMinimum(0);
   hf_mc->SetMaximum(100.7178);
   hf_mc->SetEntries(1364);
   hf_mc->SetDirectory(0);
   hf_mc->SetStats(0);

   ci = TColor::GetColor("#99ccff");
   hf_mc->SetFillColor(ci);

   ci = TColor::GetColor("#99ccff");
   hf_mc->SetLineColor(ci);
   hf_mc->GetXaxis()->SetTitle("m(#mu#mu#gamma) (GeV)");
   hf_mc->GetYaxis()->SetTitle("Entries / 5 GeV");
   hf_mc->Draw("sameaxis");
   
   pt = new TPaveText(0.01,0.9357505,0.2184422,0.995,"blNDC");
   pt->SetName("title");
   pt->SetBorderSize(1);
   text = pt->AddText("R_{9} < 0.94");
   pt->Draw();
   c1_2->Modified();
   c1->cd();
   c1->Modified();
   c1->cd();
   c1->SetSelected(c1);
}
