# from ROOT import *
nBins = 50
minMass = 2.

maxMass = 4.5

sourcePath = "/tmp/veverka/"
sourceFiles = ["minimumBias", "mu"]

sourceFiles = [sourcePath + f + "Ntuples.root" for f in sourceFiles]
import ROOT
chain = ROOT.TChain("Events")
for f in sourceFiles:
  chain.Add(f)

chain.Draw('ggssJPsiMass>>hggmmMass(%d,%g,%g)' % (nBins, minMass, maxMass), 'ggssJPsiCharge == -2', "goff")
chain.Draw('ggssJPsiMass>>hggppMass(%d,%g,%g)' % (nBins, minMass, maxMass), 'ggssJPsiCharge ==  2', "goff")
chain.Draw('ggosJPsiMass>>hggpmMass(%d,%g,%g)' % (nBins, minMass, maxMass), 'ggosJPsiCharge ==  0', "goff")
chain.Draw('gtssJPsiMass>>hgtmmMass(%d,%g,%g)' % (nBins, minMass, maxMass), 'gtssJPsiCharge == -2', "goff")
chain.Draw('gtssJPsiMass>>hgtppMass(%d,%g,%g)' % (nBins, minMass, maxMass), 'gtssJPsiCharge ==  2', "goff")
chain.Draw('gtosJPsiMass>>hgtpmMass(%d,%g,%g)' % (nBins, minMass, maxMass), 'gtosJPsiCharge ==  0', "goff")
chain.Draw('ttssJPsiMass>>httmmMass(%d,%g,%g)' % (nBins, minMass, maxMass), 'ttssJPsiCharge == -2', "goff")
chain.Draw('ttssJPsiMass>>httppMass(%d,%g,%g)' % (nBins, minMass, maxMass), 'ttssJPsiCharge ==  2', "goff")
chain.Draw('ttosJPsiMass>>httpmMass(%d,%g,%g)' % (nBins, minMass, maxMass), 'ttosJPsiCharge ==  0', "goff")


hppMass = ROOT.gDirectory.Get("hggppMass").Clone("hppMass")
hppMass.Add(ROOT.gDirectory.Get("hgtppMass") )
hppMass.Add(ROOT.gDirectory.Get("httppMass") )
hppMass.Sumw2()
hppMass.Scale(2.)

hmmMass = ROOT.gDirectory.Get("hggmmMass").Clone("hmmMass")
hmmMass.Add(ROOT.gDirectory.Get("hgtmmMass") )
hmmMass.Add(ROOT.gDirectory.Get("httmmMass") )
hmmMass.Sumw2()
hmmMass.Scale(2.)

hpmMass = ROOT.gDirectory.Get("hggpmMass").Clone("hpmMass")
hpmMass.Add(ROOT.gDirectory.Get("hgtpmMass") )
hpmMass.Add(ROOT.gDirectory.Get("httpmMass") )

hpmMass.SetTitle("CMS Preliminary, L = 19 nb^{-1}, #sqrt{s} = 7 TeV")
hpmMass.GetXaxis().SetTitle("dimuon mass [GeV/c^{2}]")
hpmMass.GetYaxis().SetTitle("events per bin")
hpmMass.SetMarkerStyle(20)
hpmMass.Draw("ep")

hppMass.SetLineColor(ROOT.kRed)
hppMass.SetFillColor(ROOT.kRed)
hppMass.SetFillStyle(3001)
hppMass.Draw("e same")
hppMass.Draw("hist same")


hmmMass.SetLineColor(ROOT.kBlue)
hmmMass.SetFillColor(ROOT.kBlue)
hmmMass.SetFillStyle(3004)
hmmMass.Draw("e same")
hmmMass.Draw("hist same")

hpmMass.Draw("ep same")

legend = ROOT.TLegend(0.65,0.55,0.85,0.75)
legend.AddEntry(hpmMass, "#mu^{+}#mu^{-}")
legend.AddEntry(hppMass, "#mu^{+}#mu^{+} #times 2")
legend.AddEntry(hmmMass, "#mu^{-}#mu^{-} #times 2")
legend.SetLineColor(ROOT.kWhite)
legend.SetFillColor(ROOT.kWhite)
legend.Draw()

if __name__ == "__main__": import user