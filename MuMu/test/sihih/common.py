import sys
import MuMuGammaChain
import ROOT

## Define the TChains
chains = MuMuGammaChain.getChains(MuMuGammaChain.cfiles,
                                  MuMuGammaChain.cpath
                                  )

## Aliases
for ch in chains.values():
    ch.SetAlias("g", "mmgPhoton")
    ch.SetAlias("mu1", "dau1[mmgDimuon]")
    ch.SetAlias("mu2", "dau2[mmgDimuon]")
    ch.SetAlias("mm", "mmgDimuon")

## Handy shortcut(s)
flush = sys.stdout.flush

## Tools
ROOT.gROOT.LoadMacro("resolutionErrors.C+")

def makeSelection(cuts):
    "Make an and of list of string cuts"
    return " & ".join("(%s)" % cut for cut in cuts)

def makeHistos(chains, var, sel, ignoreDatasets = [], option = ""):
    """Takes a dictionary of TChains, a RooRealVar and string selection
    and for each TChain makes a histogram of the variable in the current
    directory for the selection.  The title of the var defines the
    plotted expression.  The histogram names are given by the keys of the
    TChains and the name of the var.  Binning is taken from the var."""
    print "\nMaking %s histos ...\n  " % var.GetName(),; flush()
    binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())
    for label, (dataset, cuts) in sel.items():
        if dataset in ignoreDatasets: continue
        print label,; flush()
        ch = chains[dataset]
        ## variable title holds the expression for TTree::Draw
        hname = "h_%s_%s" % (var.GetName(), label)
        expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
        # print 'ch.Draw("%s", "%s", "goff %s")' % (expr, makeSelection(cuts), option)
        ch.Draw(expr, makeSelection(cuts), "goff" + option)

