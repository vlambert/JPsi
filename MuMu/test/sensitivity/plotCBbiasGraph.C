{
    TGraphErrors gre("cbBias2.dat");
    gre.Draw("ap");
    gre.GetXaxis().SetTitle("E(#gamma) scale [%]");
    gre.GetYaxis().SetTitle("#Deltam_{CB} [GeV/c^{2}]");
}