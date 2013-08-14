from ROOT import *
#  {
#     gROOT->Reset();
#     gStyle->SetOptTitle(0);
gStyle.SetOptTitle(0)

#     TCanvas c1("c2pad","c2pad",900,700);
c1 = TCanvas('c2pad', 'c2pad', 900, 700)

#     gStyle->SetPadBorderMode(0);
#     gStyle->SetOptStat(0);
#     gStyle->SetPadTickX(1);
#     gStyle->SetPadTickY(1);
gStyle.SetPadBorderMode(0)
gStyle.SetOptStat(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)

#     TH2F h2("h2", "h2", 10, 0, 1, 10, 0, 1);
h2 = TH2F('h2', 'h2', 10, 0, 1, 10, 0, 1)

#     Int_t i;
#     for(i = 0; i < 10000; ++i) {
#        h2.Fill(gRandom->Exp(0.5), gRandom->Gaus(0.5, 0.2));
#     }
for i in range(10000):
    h2.Fill(gRandom.Exp(0.5), gRandom.Gaus(0.5, 0.2))

#     h1 = h2.ProjectionX("h1");
h1 = h2.ProjectionX('h1')

#     h1->SetNdivisions(505, "Y");
h1.SetNdivisions(505, 'Y')

#     TPad top_pad("top_pad", "top_pad",0,0.2, 1.0, 1.0);
#     top_pad.Draw();
#     top_pad.cd();
#     top_pad.SetBottomMargin(0);
#     h2->GetYaxis()->SetLabelFont(63);
#     h2->GetYaxis()->SetLabelSize(20);
#     h2.Draw();
top_pad = TPad('top_pad', 'top_pad', 0, 0.2, 1.0, 1.0)
top_pad.Draw()
top_pad.cd()
top_pad.SetBottomMargin(0)
h2.GetYaxis().SetLabelFont(63)
h2.GetYaxis().SetLabelSize(20)
h2.Draw()

#     c1.cd();
#     TPad bottom_pad("bottom_pad", "bottom_pad", 0, 0., 1.0, 0.2);
#     bottom_pad.Draw();
#     bottom_pad.cd();
#     bottom_pad->SetTopMargin(0);
#     h1->GetYaxis()->SetLabelFont(63);
#     h1->GetYaxis()->SetLabelSize(20);
#     h1->Draw();
c1.cd()
bottom_pad = TPad('bottom_pad', 'bottom_pad', 0, 0., 1.0, 0.2)
bottom_pad.Draw()
bottom_pad.cd()
bottom_pad.SetTopMargin(0)
h1.GetYaxis().SetLabelFont(63)
h1.GetYaxis().SetLabelSize(20)
h1.Draw()

c1.Update()

#  }
