import os
import ROOT

ROOT.gROOT.LoadMacro(os.path.join(os.environ['CMSSW_BASE'],
                                  'src/JPsi/MuMu/test/CMSStyle.C'))
ROOT.CMSstyle()

labels = """
Endcaps
Flat p_{T} gun
E^{#gamma}_{T} #in [10, 100] GeV
""".split('\n')

path = ("/Users/veverka/Work/Data/r9Trees/SingleGammaFlatPt10To100_"
        "GEN_SIM_DIGI_L1_DIGI2RAW_HLT_RAW2DIGI_L1Reco_noPU_noOOTPU")

filenames = """
    r9Tree_V1_g93p01.root
    r9Tree_V1_g94cms.root
    r9Tree_V1_g94p02.root
    """.split()

files = [ROOT.TFile.Open(os.path.join(path, f)) for f in filenames]
trees = [f.Get("r9Tree/tree") for f in files]

for i, t in enumerate(trees):
    t.Draw("r9>>h%d(100,0.5,1.0)" % i,
           "0.3 < r9 & r9 < 1.1 & abs(eta) > 1.5")

histos = [ROOT.gDirectory.Get("h%d" % i) for i in range(len(trees))]

for h in histos:
    h.Sumw2()
    h.Scale(200./h.Integral(1,100))
    h.GetXaxis().SetTitle('photon R_{9}')
    h.GetYaxis().SetTitle('a.u.')
    h.SetTitle('')
    h.SetStats(0)

histos[0].SetLineColor(ROOT.kRed);
histos[1].SetLineColor(ROOT.kBlack);
histos[2].SetLineColor(ROOT.kBlue);

histos[0].Draw("e0");
histos[1].Draw("histsame");
histos[0].Draw("e0same");
histos[2].Draw("e0same");

legend = ROOT.TLegend(0.25, 0.85, 0.5, 0.7)
legend.SetFillColor(0)
legend.SetShadowColor(0)
legend.SetBorderSize(0)
legend.AddEntry(histos[0], "g93p01", "pl")
legend.AddEntry(histos[1], "Default", "pl")
legend.AddEntry(histos[2], "g94p02", "pl")
legend.Draw()

## Initialize latex label
latex = ROOT.TLatex()
latex.SetNDC()
## Font size in pixels
latex.SetTextFont(10*(latex.GetTextFont()/10) + 3)
latex.SetTextSize(18)

## Add labels
while '' in labels:
    labels.remove('')

for i, label in enumerate(labels):
    latex.DrawLatex(0.25, 0.6 - i * 0.055, label)

