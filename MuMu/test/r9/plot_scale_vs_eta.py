import os
import ROOT

ROOT.gROOT.LoadMacro(os.path.join(os.environ['CMSSW_BASE'],
                                  'src/JPsi/MuMu/test/CMSStyle.C'))
ROOT.CMSstyle()

labels = """
Flat p_{T} gun
low R_{9}^{#gamma}
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

cuts = [
    "r9 < 0.94",
    "isEB",
    "!isEBEtaGap",
    "!isEBPhiGap",
    "!isEBEEGap",
    "0.02 < abs(scEta)",
    "abs(scEta) < 1.44"
]

## Remove the eta cracks
for boundaries in [(0.42, 0.46), (0.77, 0.81), (1.13, 1.16)]:
    cuts.append("(abs(scEta) < %f | %f < abs(scEta))" % boundaries) 

for i, t in enumerate(trees):
    t.SetAlias('recoE', 'pt*cosh(eta)')
    t.Draw("recoE/genE:abs(scEta)>>h%d(15,0,1.5)" % i,
           " & ".join(cuts),
           "profile")

histos = [ROOT.gDirectory.Get("h%d" % i) for i in range(len(trees))]

for h in histos:
    h.Sumw2()
    #h.Scale(200./h.Integral(1,100))
    h.GetYaxis().SetRangeUser(0.95, 1.05)
    h.GetXaxis().SetTitle('#eta_{SC}')
    h.GetYaxis().SetTitle('E_{reco}/E_{gen}')
    h.SetTitle('')
    h.SetStats(0)

histos[0].SetLineColor(ROOT.kRed);
histos[1].SetLineColor(ROOT.kBlack);
histos[2].SetLineColor(ROOT.kBlue);

histos[0].Draw();
histos[1].Draw("same");
histos[0].Draw("same");
histos[2].Draw("same");

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
latex.SetTextFont( 10*(latex.GetTextFont()/10) + 3)
latex.SetTextSize(18)

## Add labels
while '' in labels:
    labels.remove('')
    
for i, label in enumerate(labels):
    latex.DrawLatex(0.25, 0.3 - i * 0.055, label)

