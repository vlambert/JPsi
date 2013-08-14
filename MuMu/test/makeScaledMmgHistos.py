from makeFsrHistos import *
from ROOT import TFile
file = TFile("scaledMmgHistos.root", "recreate")
gROOT.LoadMacro("resolutionErrors.C")
# selAll  = lyonSel["all"] + "& 87 < mmgMass & mmgMass < 95"
# selFake = lyonSel["fake"] + "& 87 < mmgMass & mmgMass < 95"
selAll  = newSel["all"] + "& g==0"   # Leading photon only
selFake = newSel["fake"] + "& g==0"  # Leading photon only
chainMC.Draw(">>myList" ,selAll, "")
chainMC.SetEventList( gDirectory.Get("myList") )
# chainMC.Draw("mmgMass", selAll, "", 10000)
p1 = "muPt[mu1], muEta[mu1], muPhi[mu1]"
p2 = "muPt[mu2], muEta[mu2], muPhi[mu2]"
pg = "phoPt[g], phoEta[g], phoPhi[g]"
pmm = "pt[mm], eta[mm], phi[mm], mass[mm]"
p12g = "%s, %s, %s" % (p1, p2, pg)
pmmg = "%s, %s" % (pmm, pg)

percents = range(-25, 26)
binning = "(60,60,120)"
histos = []


# chainMC.Draw("scaledMmgMass(0, %s)" % p123 ,selAll, "", 5000)
for i in range(len(percents)):
    scale = float (percents[i]) / 100.
    if percents[i] < 0:
        name = "scaledMmgMass_m%02d" % -percents[i]
    else:
        name = "scaledMmgMass_%02d" % percents[i]
    expr = "scaledDimuonPhotonMass(%f, %s)>>%s%s" % (scale, pmmg, name, binning)
    print "Making", name, ":", expr, "..."
    print
    chainMC.Draw(expr ,selAll, "goff")
    histos.append( gDirectory.Get(name) )

file.Write()
