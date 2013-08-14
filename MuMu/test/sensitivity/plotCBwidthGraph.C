{
    TGraphErrors gre("cbWidth2.dat");
    gre.Draw("ap");
    gre.GetXaxis().SetTitle("E(#gamma) scale [%]");
    gre.GetYaxis().SetTitle("#sigma_{CB} [GeV/c^{2}]");
}