'''Provides function cmsstyle that sets the ROOT CMS Style.'''
import os
import sys
import ROOT

ROOT.gROOT.LoadMacro(os.path.join(os.environ['CMSSW_BASE'],
                                  'src/JPsi/MuMu/test/CMSStyle.C'))
cmsstyle = ROOT.CMSstyle
print "Setting ROOT's style to CMS Style..."
cmsstyle()
ROOT.gStyle.SetPalette(1)

## Check if roofit has been loaded.
if 'JPsi.MuMu.common.roofit' in sys.modules:
    ## Enlarge the size of the pad top margin.
    ROOT.gStyle.SetPadTopMargin(0.1)

