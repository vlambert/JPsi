import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *

gROOT.LoadMacro('energyCorrection.cc+')

canvases = []
tree = esChains.getChains('v4')['z']

canvases.append(TCanvas())
tree.Draw("corrE(scRawE+preshowerE,scEta,scPhiWidth/scEtaWidth)/scE", "phoIsEB")

canvases.append(TCanvas())
tree.Draw("corrE(scRawE+preshowerE,scEta,scPhiWidth/scEtaWidth)/scE", "!phoIsEB")

canvases.append(TCanvas())
tree.Draw("newCorrE(scRawE+preshowerE,scEta,scPhiWidth/scEtaWidth)/phoGenE>>new_eb",
          "phoIsEB & phoR9 < 0.94 & phoGenE > 9")
tree.Draw("corrE(scRawE+preshowerE,scEta,scPhiWidth/scEtaWidth)/phoGenE>>old_eb",
          "phoIsEB & phoR9 < 0.94 & phoGenE > 9", "same")

canvases.append(TCanvas())
tree.Draw("newCorrE(scRawE+preshowerE,scEta,scPhiWidth/scEtaWidth)/phoGenE>>new_ee",
          "!phoIsEB & phoR9 < 0.95 & phoGenE > 9")
tree.Draw("corrE(scRawE+preshowerE,scEta,scPhiWidth/scEtaWidth)/phoGenE>>old_ee",
          "!phoIsEB & phoR9 < 0.95 & phoGenE > 9", "same")

canvases.append(TCanvas())
tree.Draw("newCorrE(scRawE+preshowerE,scEta,scPhiWidth/scEtaWidth)/phoGenE>>new_eb",
          "phoIsEB & phoGenE > 9")

canvases.append(TCanvas())
tree.Draw("newCorrE(scRawE+preshowerE,scEta,scPhiWidth/scEtaWidth)/scE", "!phoIsEB")

if __name__ == "__main__": import user
