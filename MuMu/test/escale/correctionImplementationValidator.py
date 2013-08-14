import os
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *

CMSSW_BASE = os.environ['CMSSW_BASE']

## Add JPsi/MuMu/interface to the include path
gROOT.ProcessLine( '.include %s' % os.path.join( CMSSW_BASE, 'src' ) )

## Load the cluster correction functions
gROOT.LoadMacro( os.path.join( CMSSW_BASE,
                               'src/JPsi/MuMu/src/clusterCorrection.cc+' ) )

chains = esChains.getChains('v7')

_tree = chains['z']

_tree.SetAlias( 'phoE', 'phoPt * cosh(phoEta)' )
_tree.SetAlias( 'brem', 'scPhiWidth / scEtaWidth' )
_tree.SetAlias( 'rawE', 'scRawE + preshowerE' )
_tree.SetAlias( 'corrE',
                'phoCrackCorr * corrE(rawE, scEta, brem)' )


#------------------------------------------------------------------------------
class Selection:
    "Store selection data."
    def __init__ (self, name, title, cut):
        self.name = name
        self.title = title
        self.cut = cut
# <-- Selection

#------------------------------------------------------------------------------
class Variable:
    "Store variable data."
    def __init__ (self, name, title, unit, expression, ytitle='', binning=''):
        self.name = name
        self.title = title
        self.unit = unit
        self.expression = expression
        self.ytitle = ytitle
        self.binning = binning
# <-- Variable

_selections = {
    'eb' : Selection('EB', 'Barrel', 'phoIsEB & phoR9 < 0.94' ),
    'ee' : Selection('EE', 'Endcaps', '!phoIsEB & phoR9 < 0.95' )
}

_variables = [
    Variable( 'EcorrOverReco', 'E_{corr} / E_{reco}', '', 'corrE / phoE' ),
    Variable( 'EcorrOverRecoVsEta', 'super cluster |#eta|', '',
              'corrE / phoE : scEta', 'E_{corr} / E_{reco}' ),
]

_hists = {}
_canvases = []

for x in _variables:
    for label, sel in _selections.items():
        _canvases.append( TCanvas() )
        name = '%s_%s' % (x.name, sel.name)
        expr = '%s >> h_%s%s' % (x.expression, name, x.binning)
        _tree.Draw(expr, sel.cut)
        _hists[name] = gDirectory.Get( 'h_' + name )
        _hists[name].SetTitle( sel.title )
        unit = ''
        if x.unit != '':
            unit = '(%s)' % unit
        _hists[name].GetXaxis().SetTitle( x.title + ' ' + unit )
#         _hists[name].Draw()

