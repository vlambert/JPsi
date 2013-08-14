from makeFsrHistos import *
gROOT.LoadMacro("resolutionErrors.C")
# selAll  = lyonSel["all"] + "& 87 < mmgMass & mmgMass < 95"
# selFake = lyonSel["fake"] + "& 87 < mmgMass & mmgMass < 95"
selAll  = newSel["all"] #+ "& 87 < mmgMass & mmgMass < 95"
selFake = newSel["fake"] #+ "& 87 < mmgMass & mmgMass < 95"
chainMC.Draw(">>myList" ,selAll)
chainMC.SetEventList( gDirectory.Get("myList") )
# chainMC.Draw("mmgMass", selAll, "", 10000)
p1 = "muPt[mu1], muEta[mu1], muPhi[mu1]"
p2 = "muPt[mu2], muEta[mu2], muPhi[mu2]"
pg = "phoPt[g], phoEta[g], phoPhi[g]"
pmm = "pt[mm], eta[mm], phi[mm], mass[mm]"
p12g = "%s, %s, %s" % (p1, p2, pg)
pmmg = "%s, %s" % (pmm, pg)

# chainMC.Draw("scaledMmgMass(0, %s)" % p123 ,selAll, "", 5000)
chainMC.Draw("scaledDimuonPhotonMass(0, %s)>>(300,60,120)" % pmmg ,selAll, "", 5000)
