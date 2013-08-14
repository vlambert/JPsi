import os
import ROOT

### Black Magic to Make RooFit work on MacOS X --------------------------------
import sys
if sys.platform == 'darwin':
    try:
        import libRooFit
    except ImportError:
        pass

#------------------------------------------------------------------------------

## Common ROOT objects
## Globals
from ROOT import gDirectory, gROOT, gStyle, gSystem, gPad

## Classes
from ROOT import TChain, TCanvas, TH1F, THStack, TLegend, TF1, TMath, \
                 TTree, Form, TFile, TGraph, TGraphErrors, TGraphAsymmErrors, \
                 TLatex
## Colors
from ROOT import kBlue, kViolet, kMagenta, kPink, kRed, kOrange, kYellow
from ROOT import kSpring, kGreen, kTeal, kCyan, kAzure, kWhite, kBlack, kGray
## Bools
from ROOT import kTRUE, kFALSE

#------------------------------------------------------------------------------
## Common RooFit objects
from ROOT import RooRealVar, RooArgSet, RooArgList, RooDataSet, RooCategory, \
                 RooWorkspace, RooAbsData

from array import array

## Workaround the python's `import' keyword
setattr( RooWorkspace, 'Import', getattr(RooWorkspace, 'import') )

#------------------------------------------------------------------------------
## Set the CMS Style
gROOT.LoadMacro( os.path.join( os.environ['CMSSW_BASE'],
                               'src/JPsi/MuMu/test/CMSStyle.C' ) )
ROOT.CMSstyle()