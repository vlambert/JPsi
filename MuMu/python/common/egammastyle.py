'''Provides function cmsstyle that sets the ROOT CMS e/gamma Style.'''
import os
import sys
import ROOT

ROOT.gROOT.LoadMacro(os.path.join(os.environ['CMSSW_BASE'],
                                  'src/JPsi/MuMu/test/style-Egamma.C'))
setegammastyle = ROOT.setEgammaStyle
print "Setting ROOT's style to CMS E/Gamma Style..."
setegammastyle()
ROOT.gStyle.SetPalette(1)

## Check if roofit has been loaded.
if 'JPsi.MuMu.common.roofit' in sys.modules:
    ## Enlarge the size of the pad top margin.
    ROOT.gStyle.SetPadTopMargin(0.1)

