{
file0 = new TFile("ootpu_500_50bins_EE.root");

new TCanvas();
hR9_PUEarly0_Norm->Draw("hist");
hR9_PUEarly0_Norm->GetXaxis()->SetRangeUser(0.91,0.98);
hR9_PUEarly10_Norm->Draw("same");

new TCanvas();
hR9_PUInTime0_Norm->Draw("hist");
hR9_PUInTime0_Norm->GetXaxis()->SetRangeUser(0.91,0.98);
hR9_PUInTime10_Norm->Draw("same");

new TCanvas();
hR9_PULate0_Norm->Draw("hist");
hR9_PULate0_Norm->GetXaxis()->SetRangeUser(0.91,0.98);
hR9_PULate10_Norm->Draw("same");
}