from ROOT import *

class Var(RooRealVar):
    """store histogram data related to a variable,
    title holds the selection."""
    def __init__(self, name, title, minValue, maxValue, unit, numBins=0):
        RooRealVar.__init__(self, name, title, minValue, maxValue, unit)
        if numBins > 0:
            self.setBins(numBins)

histos = {}
## Dictionary defining histograms in the format
## key = histogram id relating it to definition of cuts
## value.name = variable name used to build the histogram name
## value.title = TTree::Draw expression defining what is drawn
## value.{min,max}Value = x-axis range
## value.unit = variable unit used for axis titles
## value.numBins = number of histogram bins
histos["mass"] = Var("mass", "mass", 30, 130, "GeV", 100)
histos["mmgMass"  ] = Var("mmgMass"  , "mmgMass", 60, 120, "GeV", 60)
histos["mmgMassEB"] = Var("mmgMassEB", "mmgMass", 60, 120, "GeV", 60)
histos["mmgMassEE"] = Var("mmgMassEE", "mmgMass", 60, 120, "GeV", 60)
histos["ebSihih"] = Var("ebSihih", "phoSigmaIetaIeta[g]", 0., 0.03, "", 30)
histos["eeSihih"] = Var("eeSihih", "phoSigmaIetaIeta[g]", 0., 0.1, "", 20)
histos["ubebSihih"] = Var("ubebSihih", "phoSigmaIetaIeta[g]", 0., 0.03, "", 30)
histos["eeSihihVsDR"] = Var("eeSihihVsDR", "phoSigmaIetaIeta[g]:mmgDeltaRNear", 0., 3., "", 150)
histos["phoPt"  ] = Var("phoPt"  , "phoPt[g]", 0, 100, "GeV", 100)
histos["phoPtEB"] = Var("phoPtEB", "phoPt[g]", 0, 100, "GeV", 100)
histos["phoPtEE"] = Var("phoPtEE", "phoPt[g]", 0, 100, "GeV", 100)
histos["phoEta"  ] = Var("phoEta"  , "phoEta[g]", -3, 3, "", 60)
histos["phoE"  ] = Var("phoE"  , "phoPt[g]*TMath::CosH(phoEta[g])", 0, 100, "GeV", 100)
histos["phoEEB"] = Var("phoEEB", "phoPt[g]*TMath::CosH(phoEta[g])", 0, 100, "GeV", 100)
histos["phoEEE"] = Var("phoEEE", "phoPt[g]*TMath::CosH(phoEta[g])", 0, 100, "GeV", 100)
histos["kRatio"] = Var("kRatio", "kRatio(mmgMass, mass[mm])", 0, 2, "", 40)
histos["kRatio2"] = Var("kRatio2", "kRatio(mmgMass, mass[mm])", 0, 2, "", 200)
histos["inverseK"] = Var("inverseK", "1./kRatio(mmgMass, mass[mm])", 0, 2, "", 40)
histos["inverseK2"] = Var("inverseK2", "1./kRatio(mmgMass, mass[mm])", 0, 2, "", 200)
histos["minusLogK"] = Var("minusLogK", "-log(kRatio(mmgMass, mass[mm]))", -1, 1, "", 40)
histos["minusLogKEB"] = Var("minusLogKEB", "-log(kRatio(mmgMass, mass[mm]))", -1, 1, "", 40)
histos["minusLogKEE"] = Var("minusLogKEE", "-log(kRatio(mmgMass, mass[mm]))", -1, 1, "", 40)
histos["minusLogKEBR9"] = Var("minusLogKEBR9", "-log(kRatio(mmgMass, mass[mm]))", -1, 1, "", 40)
histos["minusLogKEER9"] = Var("minusLogKEER9", "-log(kRatio(mmgMass, mass[mm]))", -1, 1, "", 40)
histos["minusLogK2"] = Var("minusLogK2", "-log(kRatio(mmgMass, mass[mm]))", -1, 1, "", 200)

mu1P4 =  "muPt[mu1] muEta[mu1] muPhi[mu1] 0.105658".split()
mu2P4 =  "muPt[mu2] muEta[mu2] muPhi[mu2] 0.105658".split()
phoP4 = "phoPt[g]  phoEta[g]  phoPhi[g]   0".split()

mu1GenP4 =  "muGenPt[mu1] muGenEta[mu1] muGenPhi[mu1] 0.105658".split()
mu2GenP4 =  "muGenPt[mu2] muGenEta[mu2] muGenPhi[mu2] 0.105658".split()
phoGenP4 = "phoGenPt[g]  phoGenEta[g]  phoGenPhi[g]   0".split()

mmMassGen   = "twoBodyMass(%s,%s,%s,%s,%s,%s,%s,%s)" % tuple(mu1GenP4 + mu2GenP4)
mmMassReco  = "twoBodyMass(%s,%s,%s,%s,%s,%s,%s,%s)" % tuple(mu1P4 + mu2P4)
mmMassVReco = "mass[mm]"

mmgMassGen   = "threeBodyMass(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % \
               tuple(mu1GenP4 + mu2GenP4 + phoGenP4)
mmgMassReco  = "threeBodyMass(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % \
               tuple(mu1P4 + mu2P4 + phoP4)
mmgMassVReco = "mmgMass"

kGen   = "kRatio(%s, %s)" % (mmgMassGen  , mmMassGen  )
kReco  = "kRatio(%s, %s)" % (mmgMassReco , mmMassReco )
kVReco = "kRatio(%s, %s)" % (mmgMassVReco, mmMassVReco)


histos["ikReco"     ] = Var("ikReco"  , "1./kRatio(mmgMassVanilla, massVanilla[mm])" , 0, 2, "", 200)
histos["ikRecoEB"   ] = Var("ikRecoEB", "1./kRatio(mmgMassVanilla, massVanilla[mm])" , 0, 2, "", 200)
histos["ikRecoEE"   ] = Var("ikRecoEE", "1./kRatio(mmgMassVanilla, massVanilla[mm])" , 0, 2, "", 200)
histos["ikVReco"    ] = Var("ikVReco"  , "1./kRatio(mmgMass, mass[mm])" , 0, 2, "", 200)
histos["ikVRecoEB"  ] = Var("ikVRecoEB", "1./kRatio(mmgMass, mass[mm])" , 0, 2, "", 200)
histos["ikVRecoEE"  ] = Var("ikVRecoEE", "1./kRatio(mmgMass, mass[mm])" , 0, 2, "", 200)
histos["ikVVReco"   ] = Var("ikVVReco"  , "1./kRatio(mmgMassVCorr, massVCorr[mm])" , 0, 2, "", 200)
histos["ikVVRecoEB" ] = Var("ikVVRecoEB", "1./kRatio(mmgMassVCorr, massVCorr[mm])" , 0, 2, "", 200)
histos["ikVVRecoEE" ] = Var("ikVVRecoEE", "1./kRatio(mmgMassVCorr, massVCorr[mm])" , 0, 2, "", 200)

histos["ikRecoOverGen"  ] = Var("ikRecoOverGen"  , "kRatio(mmgMassGen, massGen[mm]) / kRatio(mmgMassVanilla, massVanilla[mm])", 0, 2, "", 200)
histos["ikVRecoOverGen" ] = Var("ikVRecoOverGen" , "kRatio(mmgMassGen, massGen[mm]) / kRatio(mmgMass       , mass       [mm])", 0, 2, "", 200)
histos["ikVVRecoOverGen"] = Var("ikVVRecoOverGen", "kRatio(mmgMassGen, massGen[mm]) / kRatio(mmgMassVCorr  , mass       [mm])", 0, 2, "", 200)

histos["mmMassRecoOverGen" ] = Var("mmMassRecoOverGen" , "massVanilla[mm]/massGen[mm]", 0.8, 1.2, "", 200)
histos["mmMassVRecoOverGen"] = Var("mmMassVRecoOverGen" , "mass[mm]/massGen[mm]", 0.8, 1.2, "", 200)
histos["mmgMassRecoOverGen" ] = Var("mmgMassRecoOverGen" , "mmgMassVanilla[mm]/mmgMassGen[mm]", 0.8, 1.2, "", 200)
histos["mmgMassVRecoOverGen"] = Var("mmgMassVRecoOverGen" , "mmgMass[mm]/mmgMassGen[mm]", 0.8, 1.2, "", 200)
histos["mmgMassVVRecoOverGen"] = Var("mmgMassVVRecoOverGen" , "mmgMassVCorr[mm]/mmgMassGen[mm]", 0.8, 1.2, "", 200)

