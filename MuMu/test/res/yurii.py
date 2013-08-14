import ROOT
ROOT.gROOT.LoadMacro("tools.C+")
from ROOT import *

rand = TRandom3()

mcTree = TTree("mcTree", "MC tree")
dataTree = TTree("dataTree", "tree with real data")

mcTree.ReadFile( "yuriisMethod-DYToMuMu_powheg_Summer11_S4_full.dat",
                 "row/i:instance:m2/F:m3:pt:eta:r9:w" )
dataTree.ReadFile( "yuriisMethod-July17JSON_corrected.dat",
                   "row/i:instance:m2/F:m3:pt:eta:r9:w" )

# mcTree.ReadFile("yuriisMethod-DYToMuMu_Winter10_Powheg.dat", "m2/F:m3:pt:eta")
# dataTree.ReadFile("yuriisMethod-Dec22ReReco.dat", "m2/F:m3:pt:eta")
# mcTree.ReadFile("yuriisMethod-Powheg_Fall10.txt", "m2/F:m3:pt:eta")
# dataTree.ReadFile("yuriisMethod-data_Nov4ReReco.txt", "m2/F:m3:pt:eta")
# mcTree.ReadFile("Selected_MC_1.000_fromOlivier.txt", "m2/F:m3:pt:eta")
# dataTree.ReadFile("Selected_DATA_fromOlivier.txt", "m2/F:m3:pt:eta")

dataTree.Draw(">>presel", "pt > 10", "entrylist")
dataTree.SetEntryList(gDirectory.Get("presel"))

## Make the leaf variables
gROOT.ProcessLine("struct Leafs {Float_t m2, m3, pt, eta, r9, w;};")
mcLeafs = ROOT.Leafs()
dataLeafs = ROOT.Leafs()

hmc = TH1F()
hdata = TH1F()

## Link the leafs with the Branches
for leafs, tree in [(mcLeafs, mcTree), (dataLeafs, dataTree)]:
    for xname in "m2 m3 pt eta r9 w".split():
        tree.SetBranchAddress(xname, AddressOf(leafs, xname))

## To swith between EB and EE efficiently
def applySelection(selection):
    for t in [mcTree, dataTree]:
        t.SetEntryList(0)
        lname = "elist_" + t.GetName()
        t.Draw(">>" + lname, selection, "entrylist")
        elist = gDirectory.Get(lname)
        t.SetEntryList(gDirectory.Get(lname))

def nllik(scale, res):
    """Calculate the negative log likelihood of data with 1/k PDF from MC.
    Smear MC with extra gaussian of width res and uniformly shift by scale.
    both res and scale are in %.  Scale of 0% means no shift."""
    global hmc
    if hmc: hmc.Delete()
    hmc = TH1F("hmc", "hmc", 100, 0, 2)
    # Check if there is already pre-selection applied
    if mcTree.GetEntryList():
        nevents = mcTree.GetEntryList().GetN()
        getMcEntry = lambda i: mcTree.GetEntry(mcTree.GetEntryList().GetEntry(i))
    else:
        nevents = mcTree.GetEntries()
        getMcEntry = mcTree.GetEntry

    ## Loop over the MC to fill the histogram
    for i in range(nevents):
        sfactor = TMath.Exp(rand.Gaus(TMath.Log(1. + scale/100.), res/100.))
        getMcEntry(i)
        ## Apply cuts that depend on the photon scale
        if sfactor * mcLeafs.pt < 10: continue
        if abs(scaledMmgMass3(sfactor, mcLeafs.m3, mcLeafs.m2) - 91.2) > 4.:
            continue
        hmc.Fill(sfactor * inverseK(mcLeafs.m3, mcLeafs.m2))

    ## Normalize area to 1
    hmc.Scale( 1./hmc.Integral() / hmc.GetBinWidth(1) )

    ## Fit with Gauss; use the fit to get an estimate for the tails where there is no data
    hmc.Fit("gaus", "Q0")
    gaussFit = hmc.GetFunction("gaus")

    ## Get the real data
    dataTree.Draw("inverseK(m3, m2) >> hdata(20,0,2)",  "abs(m3 - 91.2) < 4", "goff")

    ## Sum the negative log likelihood over all the data
    sum = 0.
    for i in range( dataTree.GetSelectedRows() ):
        ik = dataTree.GetV1()[i]
        likelihood = hmc.Interpolate(ik)
        ## Make sure we have a positive likelihood value
        if likelihood <= 0.:
            likelihood = gaussFit.Eval(ik)
        sum -= log(likelihood)
    return sum

def nllm3( scale, res, m3min=60, m3max=120, nbinsMC=30, 
           nbinsData=30, phoEtMin=10, phoEtMax=99999, nsmooth=0 ):
    """Calculate the negative log likelihood of data with m(uuy) PDF from MC.
    Smear MC with extra gaussian of width res and uniformly shift by scale.
    both res and scale are in %.  Scale of 0% means no shift."""
    global hmc
    global hdata
    if hmc: hmc.Delete()
    if gDirectory.Get("hmc"): gDirectory.Get("hmc").Delete()
#     hmc = TH1F("hmc", "hmc", nbinsMC, m3min, m3max)
    hmc = TH1F("hmc", "hmc", nbinsMC, 60, 120)
    # Check if there is already pre-selection applied
    if mcTree.GetEntryList():
        nevents = mcTree.GetEntryList().GetN()
        getMcEntry = lambda i: mcTree.GetEntry(mcTree.GetEntryList().GetEntry(i))
    else:
        nevents = mcTree.GetEntries()
        getMcEntry = mcTree.GetEntry

    ## Loop over the MC to fill the histogram
    for i in range(nevents):
        if res > 0:
            #sfactor = TMath.Exp(rand.Gaus(TMath.Log(1. + scale/100.), res/100.))
            sfactor = rand.Gaus(1. + scale/100., res/100.)
        else:
            sfactor = 1. + scale/100.
        getMcEntry(i)
        ## Apply cuts that depend on the photon scale
        if sfactor * mcLeafs.pt < phoEtMin or \
           sfactor * mcLeafs.pt > phoEtMax: continue
        sm3 = scaledMmgMass3(sfactor, mcLeafs.m3, mcLeafs.m2)
        #if abs(sm3 - 90.) > 30.:
#         if sm3 < m3min or m3max < sm3:
#             continue
        hmc.Fill(sm3, mcLeafs.w)

    ## Normalize area to 1
    hmc.Scale( 1./hmc.Integral() / hmc.GetBinWidth(1) )

    ## Smooth
    hmc.Smooth(nsmooth)

    ## Fit with Gauss; use the fit to get an estimate for the tails where there is no data
    hmc.Fit("gaus", "Q0")
    gaussFit = hmc.GetFunction("gaus")

    ## Get the real data
    if hdata: hdata.Delete()
    hdata = TH1F("hdata", "hdata", nbinsData, 60, 120)
    selExpr = "%f < m3 & m3 < %f & %f < pt & pt < %f" % (m3min, m3max, phoEtMin, phoEtMax)
    dataTree.Draw("m3 >> hdata", selExpr, "goff")

    ## Sum the negative log likelihood over all the data
    sum = 0.
    for i in range( dataTree.GetSelectedRows() ):
        x = dataTree.GetV1()[i]
        likelihood = hmc.Interpolate(x)
        ## Make sure we have a positive likelihood value
        if likelihood <= 0.:
            likelihood = gaussFit.Eval(x)
        sum -= log(likelihood)
    return sum

def chi2(scale, selection="", nbins = 20, xmin = 0., xmax = 2.):
    "Calculate the chi2 test of data and MC as a function of the scale"
    mcTree.Draw("(1. + %f/100.) * ik >> hmc(%d,%d,%d)" % (scale, nbins, xmin, xmax), selection, "goff")
    hmc = gDirectory.Get("hmc")
    ## Get the real data
    dataTree.Draw("ik>>hdata(%d,%d,%d)" % (nbins, xmin, xmax), selection, "goff")
    hdata = gDirectory.Get("hdata")
    ## Normalize MC to data
    hmc.Scale( hdata.Integral() / hmc.Integral() )
    return hmc.ChiTest(hdata)

if __name__ == "__main__": import user
