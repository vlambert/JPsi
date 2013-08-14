import ROOT

inFile = ROOT.TFile("histo_jpsi_full.root")

hss = inFile.Get("dimuonsGlbGlbSSHistos/massJpsi").Clone("hss")
hss.Add(inFile.Get("dimuonsGlbTrkSSHistos/massJpsi"))
hss.Add(inFile.Get("dimuonsTrkTrkSSHistos/massJpsi"))

hos = inFile.Get("dimuonsGlbGlbOSHistos/massJpsi").Clone("hos")
hos.Add(inFile.Get("dimuonsGlbTrkOSHistos/massJpsi"))
hos.Add(inFile.Get("dimuonsTrkTrkOSHistos/massJpsi"))

hos.SetLineColor(ROOT.kRed)
hss.SetLineColor(ROOT.kBlue)

hos.SetLineWidth(2)
hss.SetLineWidth(2)

hos.Rebin(40)
hss.Rebin(40)

hos.Draw()
hss.Draw("same")
