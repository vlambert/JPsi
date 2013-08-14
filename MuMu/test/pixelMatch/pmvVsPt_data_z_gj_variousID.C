{
//=========Macro generated from canvas: c1_n6/c1_n6
//=========  (Wed Jun  1 15:27:34 2011) by ROOT version5.22/00d
   TCanvas *c1_n6 = new TCanvas("c1_n6", "c1_n6",4,21,600,600);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   c1_n6->SetHighLightColor(2);
   c1_n6->Range(-22.17721,0.8103659,116.4304,1.115244);
   c1_n6->SetFillColor(0);
   c1_n6->SetBorderMode(0);
   c1_n6->SetBorderSize(2);
   c1_n6->SetGridx();
   c1_n6->SetGridy();
   c1_n6->SetTickx(1);
   c1_n6->SetTicky(1);
   c1_n6->SetLeftMargin(0.16);
   c1_n6->SetRightMargin(0.05);
   c1_n6->SetTopMargin(0.05);
   c1_n6->SetBottomMargin(0.13);
   c1_n6->SetFrameFillStyle(0);
   c1_n6->SetFrameBorderMode(0);
   c1_n6->SetFrameFillStyle(0);
   c1_n6->SetFrameBorderMode(0);
   
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(8);
   grae->SetName("");
   grae->SetTitle("");
   grae->SetFillColor(1);

   Int_t ci;   // for color index setting
   ci = TColor::GetColor("#99ccff");
   grae->SetLineColor(ci);

   ci = TColor::GetColor("#99ccff");
   grae->SetMarkerColor(ci);
   grae->SetMarkerStyle(21);
   grae->SetPoint(0,6.25,0.9650399);
   grae->SetPointError(0,1.25,1.25,0.00123023,0.001203028);
   grae->SetPoint(1,8.75,0.9775244);
   grae->SetPointError(1,1.25,1.25,0.001110355,0.001075736);
   grae->SetPoint(2,12.5,0.9779006);
   grae->SetPointError(2,2.5,2.5,0.0009368141,0.000911632);
   grae->SetPoint(3,17.5,0.9768352);
   grae->SetPointError(3,2.5,2.5,0.001226468,0.001185606);
   grae->SetPoint(4,22.5,0.9737546);
   grae->SetPointError(4,2.5,2.5,0.001655924,0.001590803);
   grae->SetPoint(5,27.5,0.9708705);
   grae->SetPointError(5,2.5,2.5,0.002237446,0.002131542);
   grae->SetPoint(6,40,0.9666012);
   grae->SetPointError(6,10,10,0.002582259,0.002459818);
   grae->SetPoint(7,75,0.9565217);
   grae->SetPointError(7,25,25,0.01113438,0.009570357);
   
   TH1 *Graph1 = new TH1F("Graph1","",100,0,109.5);
   Graph1->SetMinimum(0.85);
   Graph1->SetMaximum(1.1);
   Graph1->SetDirectory(0);
   Graph1->SetStats(0);
   Graph1->SetLineStyle(0);
   Graph1->SetMarkerStyle(20);
   Graph1->GetXaxis()->SetTitle("p_{T}^{#gamma}");
   Graph1->GetXaxis()->SetLabelFont(42);
   Graph1->GetXaxis()->SetLabelOffset(0.007);
   Graph1->GetXaxis()->SetLabelSize(0.05);
   Graph1->GetXaxis()->SetTitleSize(0.06);
   Graph1->GetXaxis()->SetTitleOffset(0.9);
   Graph1->GetXaxis()->SetTitleFont(42);
   Graph1->GetYaxis()->SetTitle("Pixel Match Veto Efficiency");
   Graph1->GetYaxis()->SetLabelFont(42);
   Graph1->GetYaxis()->SetLabelOffset(0.007);
   Graph1->GetYaxis()->SetLabelSize(0.05);
   Graph1->GetYaxis()->SetTitleSize(0.06);
   Graph1->GetYaxis()->SetTitleOffset(1.25);
   Graph1->GetYaxis()->SetTitleFont(42);
   Graph1->GetZaxis()->SetLabelFont(42);
   Graph1->GetZaxis()->SetLabelOffset(0.007);
   Graph1->GetZaxis()->SetLabelSize(0.05);
   Graph1->GetZaxis()->SetTitleSize(0.06);
   Graph1->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph1);
   
   grae->Draw("ap");
   
   grae = new TGraphAsymmErrors(9);
   grae->SetName("");
   grae->SetTitle("");
   grae->SetFillColor(1);

   ci = TColor::GetColor("#99cc33");
   grae->SetLineColor(ci);

   ci = TColor::GetColor("#99cc33");
   grae->SetMarkerColor(ci);
   grae->SetMarkerStyle(22);
   grae->SetPoint(0,22.5,0.9725678);
   grae->SetPointError(0,2.5,2.5,0.002115356,0.00201468);
   grae->SetPoint(1,27.5,0.9685404);
   grae->SetPointError(1,2.5,2.5,0.00273032,0.002585534);
   grae->SetPoint(2,32.5,0.9681916);
   grae->SetPointError(2,2.5,2.5,0.003434131,0.003210526);
   grae->SetPoint(3,37.5,0.9700234);
   grae->SetPointError(3,2.5,2.5,0.003844125,0.00354981);
   grae->SetPoint(4,42.5,0.9659746);
   grae->SetPointError(4,2.5,2.5,0.004540999,0.004181756);
   grae->SetPoint(5,47.5,0.9654867);
   grae->SetPointError(5,2.5,2.5,0.005718452,0.005167407);
   grae->SetPoint(6,55,0.968386);
   grae->SetPointError(6,5,5,0.005319872,0.004798493);
   grae->SetPoint(7,65,0.9759036);
   grae->SetPointError(7,5,5,0.007564913,0.006278358);
   grae->SetPoint(8,85,0.9560117);
   grae->SetPointError(8,15,15,0.01204743,0.01025542);
   
   TH1 *Graph2 = new TH1F("Graph2","",100,12,108);
   Graph2->SetMinimum(0.9401425);
   Graph2->SetMaximum(0.9860037);
   Graph2->SetDirectory(0);
   Graph2->SetStats(0);
   Graph2->SetLineStyle(0);
   Graph2->SetMarkerStyle(20);
   Graph2->GetXaxis()->SetTitle("p_{T}^{#gamma}");
   Graph2->GetXaxis()->SetLabelFont(42);
   Graph2->GetXaxis()->SetLabelOffset(0.007);
   Graph2->GetXaxis()->SetLabelSize(0.05);
   Graph2->GetXaxis()->SetTitleSize(0.06);
   Graph2->GetXaxis()->SetTitleOffset(0.9);
   Graph2->GetXaxis()->SetTitleFont(42);
   Graph2->GetYaxis()->SetTitle("Pixel Match Veto Efficiency");
   Graph2->GetYaxis()->SetLabelFont(42);
   Graph2->GetYaxis()->SetLabelOffset(0.007);
   Graph2->GetYaxis()->SetLabelSize(0.05);
   Graph2->GetYaxis()->SetTitleSize(0.06);
   Graph2->GetYaxis()->SetTitleOffset(1.25);
   Graph2->GetYaxis()->SetTitleFont(42);
   Graph2->GetZaxis()->SetLabelFont(42);
   Graph2->GetZaxis()->SetLabelOffset(0.007);
   Graph2->GetZaxis()->SetLabelSize(0.05);
   Graph2->GetZaxis()->SetTitleSize(0.06);
   Graph2->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph2);
   
   grae->Draw("p");
   
   grae = new TGraphAsymmErrors(9);
   grae->SetName("");
   grae->SetTitle("");
   grae->SetFillColor(1);

   ci = TColor::GetColor("#ffcc33");
   grae->SetLineColor(ci);

   ci = TColor::GetColor("#ffcc33");
   grae->SetMarkerColor(ci);
   grae->SetMarkerStyle(23);
   grae->SetPoint(0,22.5,0.972866);
   grae->SetPointError(0,2.5,2.5,0.002292388,0.002173354);
   grae->SetPoint(1,27.5,0.9696477);
   grae->SetPointError(1,2.5,2.5,0.002912787,0.002742736);
   grae->SetPoint(2,32.5,0.9673336);
   grae->SetPointError(2,2.5,2.5,0.003724927,0.003469905);
   grae->SetPoint(3,37.5,0.9691745);
   grae->SetPointError(3,2.5,2.5,0.004121907,0.003794174);
   grae->SetPoint(4,42.5,0.967433);
   grae->SetPointError(4,2.5,2.5,0.00469385,0.004294714);
   grae->SetPoint(5,47.5,0.9613095);
   grae->SetPointError(5,2.5,2.5,0.006393643,0.005781595);
   grae->SetPoint(6,55,0.9705069);
   grae->SetPointError(6,5,5,0.00544137,0.004860824);
   grae->SetPoint(7,65,0.9733333);
   grae->SetPointError(7,5,5,0.008355383,0.006939965);
   grae->SetPoint(8,85,0.955836);
   grae->SetPointError(8,15,15,0.01255431,0.01062691);
   
   TH1 *Graph3 = new TH1F("Graph3","",100,12,108);
   Graph3->SetMinimum(0.9395825);
   Graph3->SetMaximum(0.9839725);
   Graph3->SetDirectory(0);
   Graph3->SetStats(0);
   Graph3->SetLineStyle(0);
   Graph3->SetMarkerStyle(20);
   Graph3->GetXaxis()->SetTitle("p_{T}^{#gamma}");
   Graph3->GetXaxis()->SetLabelFont(42);
   Graph3->GetXaxis()->SetLabelOffset(0.007);
   Graph3->GetXaxis()->SetLabelSize(0.05);
   Graph3->GetXaxis()->SetTitleSize(0.06);
   Graph3->GetXaxis()->SetTitleOffset(0.9);
   Graph3->GetXaxis()->SetTitleFont(42);
   Graph3->GetYaxis()->SetTitle("Pixel Match Veto Efficiency");
   Graph3->GetYaxis()->SetLabelFont(42);
   Graph3->GetYaxis()->SetLabelOffset(0.007);
   Graph3->GetYaxis()->SetLabelSize(0.05);
   Graph3->GetYaxis()->SetTitleSize(0.06);
   Graph3->GetYaxis()->SetTitleOffset(1.25);
   Graph3->GetYaxis()->SetTitleFont(42);
   Graph3->GetZaxis()->SetLabelFont(42);
   Graph3->GetZaxis()->SetLabelOffset(0.007);
   Graph3->GetZaxis()->SetLabelSize(0.05);
   Graph3->GetZaxis()->SetTitleSize(0.06);
   Graph3->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph3);
   
   grae->Draw("p");
   
   grae = new TGraphAsymmErrors(9);
   grae->SetName("");
   grae->SetTitle("");
   grae->SetFillColor(1);

   ci = TColor::GetColor("#cc3333");
   grae->SetLineColor(ci);

   ci = TColor::GetColor("#cc3333");
   grae->SetMarkerColor(ci);
   grae->SetMarkerStyle(24);
   grae->SetPoint(0,22.5,0.9741774);
   grae->SetPointError(0,2.5,2.5,0.002357654,0.00222572);
   grae->SetPoint(1,27.5,0.9706573);
   grae->SetPointError(1,2.5,2.5,0.002987114,0.002802575);
   grae->SetPoint(2,32.5,0.967462);
   grae->SetPointError(2,2.5,2.5,0.003836774,0.003565726);
   grae->SetPoint(3,37.5,0.9694275);
   grae->SetPointError(3,2.5,2.5,0.004241166,0.003892254);
   grae->SetPoint(4,42.5,0.9667332);
   grae->SetPointError(4,2.5,2.5,0.004842511,0.004427268);
   grae->SetPoint(5,47.5,0.9609053);
   grae->SetPointError(5,2.5,2.5,0.006547565,0.00591339);
   grae->SetPoint(6,55,0.9695817);
   grae->SetPointError(6,5,5,0.005608715,0.005011174);
   grae->SetPoint(7,65,0.97254);
   grae->SetPointError(7,5,5,0.008598711,0.007143846);
   grae->SetPoint(8,85,0.9546926);
   grae->SetPointError(8,15,15,0.01286829,0.0108963);
   
   TH1 *Graph4 = new TH1F("Graph4","",100,12,108);
   Graph4->SetMinimum(0.9380383);
   Graph4->SetMaximum(0.9834699);
   Graph4->SetDirectory(0);
   Graph4->SetStats(0);
   Graph4->SetLineStyle(0);
   Graph4->SetMarkerStyle(20);
   Graph4->GetXaxis()->SetTitle("p_{T}^{#gamma}");
   Graph4->GetXaxis()->SetLabelFont(42);
   Graph4->GetXaxis()->SetLabelOffset(0.007);
   Graph4->GetXaxis()->SetLabelSize(0.05);
   Graph4->GetXaxis()->SetTitleSize(0.06);
   Graph4->GetXaxis()->SetTitleOffset(0.9);
   Graph4->GetXaxis()->SetTitleFont(42);
   Graph4->GetYaxis()->SetTitle("Pixel Match Veto Efficiency");
   Graph4->GetYaxis()->SetLabelFont(42);
   Graph4->GetYaxis()->SetLabelOffset(0.007);
   Graph4->GetYaxis()->SetLabelSize(0.05);
   Graph4->GetYaxis()->SetTitleSize(0.06);
   Graph4->GetYaxis()->SetTitleOffset(1.25);
   Graph4->GetYaxis()->SetTitleFont(42);
   Graph4->GetZaxis()->SetLabelFont(42);
   Graph4->GetZaxis()->SetLabelOffset(0.007);
   Graph4->GetZaxis()->SetLabelSize(0.05);
   Graph4->GetZaxis()->SetTitleSize(0.06);
   Graph4->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph4);
   
   grae->Draw("p");
   
   grae = new TGraphAsymmErrors(3);
   grae->SetName("");
   grae->SetTitle("Dec22ReReco, L = 35.9 pb^{-1}");
   grae->SetFillColor(1);
   grae->SetMarkerStyle(20);
   grae->SetPoint(0,7.5,0.9818182);
   grae->SetPointError(0,2.5,2.5,0.01640221,0.01022284);
   grae->SetPoint(1,15,0.9493671);
   grae->SetPointError(1,5,5,0.02879342,0.02112124);
   grae->SetPoint(2,35,0.9803922);
   grae->SetPointError(2,15,15,0.02806694,0.01416086);
   
   TH1 *Graph5 = new TH1F("Graph5","Dec22ReReco, L = 35.9 pb^{-1}",100,0.5,54.5);
   Graph5->SetMinimum(0.9131757);
   Graph5->SetMaximum(1.001951);
   Graph5->SetDirectory(0);
   Graph5->SetStats(0);
   Graph5->SetLineStyle(0);
   Graph5->SetMarkerStyle(20);
   Graph5->GetXaxis()->SetTitle("p_{T}^{#gamma}");
   Graph5->GetXaxis()->SetLabelFont(42);
   Graph5->GetXaxis()->SetLabelOffset(0.007);
   Graph5->GetXaxis()->SetLabelSize(0.05);
   Graph5->GetXaxis()->SetTitleSize(0.06);
   Graph5->GetXaxis()->SetTitleOffset(0.9);
   Graph5->GetXaxis()->SetTitleFont(42);
   Graph5->GetYaxis()->SetTitle("Pixel Match Veto Efficiency");
   Graph5->GetYaxis()->SetLabelFont(42);
   Graph5->GetYaxis()->SetLabelOffset(0.007);
   Graph5->GetYaxis()->SetLabelSize(0.05);
   Graph5->GetYaxis()->SetTitleSize(0.06);
   Graph5->GetYaxis()->SetTitleOffset(1.25);
   Graph5->GetYaxis()->SetTitleFont(42);
   Graph5->GetZaxis()->SetLabelFont(42);
   Graph5->GetZaxis()->SetLabelOffset(0.007);
   Graph5->GetZaxis()->SetLabelSize(0.05);
   Graph5->GetZaxis()->SetTitleSize(0.06);
   Graph5->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph5);
   
   grae->Draw("p");
   
   TLegend *leg = new TLegend(0.55,0.6,0.9,0.9,NULL,"brNDC");
   leg->SetBorderSize(0);
   leg->SetTextFont(62);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(1);
   leg->SetFillColor(0);
   leg->SetFillStyle(1001);
   TLegendEntry *entry=leg->AddEntry("","Data","pl");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(20);
   entry->SetMarkerSize(1);
   entry=leg->AddEntry("","Z#rightarrow#mu#mu#gamma","pl");

   ci = TColor::GetColor("#99ccff");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);

   ci = TColor::GetColor("#99ccff");
   entry->SetMarkerColor(ci);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry=leg->AddEntry("","#gamma+j no #gamma ID","pl");

   ci = TColor::GetColor("#99cc33");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);

   ci = TColor::GetColor("#99cc33");
   entry->SetMarkerColor(ci);
   entry->SetMarkerStyle(22);
   entry->SetMarkerSize(1);
   entry=leg->AddEntry("","#gamma+j partial #gamma ID","pl");

   ci = TColor::GetColor("#ffcc33");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);

   ci = TColor::GetColor("#ffcc33");
   entry->SetMarkerColor(ci);
   entry->SetMarkerStyle(23);
   entry->SetMarkerSize(1);
   entry=leg->AddEntry("","#gamma+j full #gamma ID","pl");

   ci = TColor::GetColor("#cc3333");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);

   ci = TColor::GetColor("#cc3333");
   entry->SetMarkerColor(ci);
   entry->SetMarkerStyle(24);
   entry->SetMarkerSize(1);
   leg->Draw();
   c1_n6->Modified();
   c1_n6->cd();
   c1_n6->SetSelected(c1_n6);
}
