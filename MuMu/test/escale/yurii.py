from ROOT import *

mcTree = TTree("mcTree", "MC tree")
dataTree = TTree("dataTree", "tree with real data")

mcTree.ReadFile("yuriisMethod-Powheg_Fall10.txt", "m2/F:m3:pt:eta")
dataTree.ReadFile("yuriisMethod-data_Nov4ReReco.txt", "m2/F:m3:pt:eta")

dataTree.Draw(">>presel", "pt > 10 & abs(m3 - 91.2) < 4", "entrylist")
dataTree.SetEntryList(gDirectory.Get("presel"))

gROOT.LoadMacro("tools.C+")

## To swith between EB and EE efficiently
def applySelection(selection):
    for t in [mcTree, dataTree]:
        #t.SetEntryList(0)
        lname = "elist_" + t.GetName()
        t.Draw(">>" + lname, selection, "entrylist")
        elist = gDirectory.Get(lname)
        t.SetEntryList(gDirectory.Get(lname))


def plotDataVsPdf():
    hmc = gDirectory.Get("hmc")
    hdata = gDirectory.Get("hdata")
    if not hmc or not hdata:
        raise RuntimeError, "Didn't find a histogram"
    hmc.Scale(hdata.GetEntries() * hdata.GetBinWidth(1))
    for h in [hdata, hmc]:
        h.GetXaxis().SetTitle("E_{ECAL}^{#gamma} / E_{muons}^{#gamma}")
        h.GetYaxis().SetTitle("Events / %g" % hdata.GetBinWidth(2))
    hdata.SetMarkerStyle(20)
    hdata.Draw("e0")
    hmc.Draw("same")
    hdata.Draw("e0 same")

def nll(scale):
    "Calculate the negative log likelihood of data with PDF from MC"
    ## Convert the scale in % in a scaling factor
    sfactor = 1. + scale/100.
    ## Add the scale dependant selection
    selection = "%f * pt > 10 &" % sfactor + \
                "abs(scaledMmgMass(%f, m3, m2) - 91.2) < 4" % sfactor
    mcTree.Draw("%f * inverseK(m3, m2) >> hmc(100,0,2)" % sfactor, selection, "goff")
    hmc = gDirectory.Get("hmc")
    ## Normalize area to 1
    hmc.Scale( 1./hmc.Integral() / hmc.GetBinWidth(1) )
    ## Fit with Gauss; use the fit to get an estimate for the tails where there is no data
    hmc.Fit("gaus", "Q0")
    fit = hmc.GetFunction("gaus")
    ## Get the real data
    dataTree.Draw("inverseK(m3, m2) >> hdata(20,0,2)", "", "goff")
    ## Sum the negative log likelihood over all the data
    sum = 0.
    for i in range( dataTree.GetSelectedRows() ):
        ik = dataTree.GetV1()[i]
        likelihood = hmc.Interpolate(ik)
        ## Make sure we have a positive likelihood value
        if likelihood <= 0.:
            likelihood = fit.Eval(ik)
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