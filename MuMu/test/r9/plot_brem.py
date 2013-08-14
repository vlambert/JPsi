import os
import ROOT
import JPsi.MuMu.common.r9Chains as chains
import JPsi.MuMu.common.cmsstyle as cmsstyle

labels = """
Endcaps
Flat p_{T} gun
E^{#gamma}_{T} #in [10, 100] GeV
""".split('\n')

trees = [chains.getChains('v1')[i] for i in 'g93p01 g94cms g94p02'.split()]

for i, t in enumerate(trees):
    t.SetAlias('brem', 'scPhiWidth/scEtaWidth')
    t.Draw("brem>>h%d(30,0,15)" % i,
           "r9 < 0.94 & 1.16 < abs(eta) & abs(eta) < 1.44")

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
latex.SetTextFont( 10*(latex.GetTextFont()/10) + 3)
latex.SetTextSize(18)

## Add labels
while '' in labels:
    labels.remove('')

for i, label in enumerate(labels):
    latex.DrawLatex(0.25, 0.6 - i * 0.055, label)

