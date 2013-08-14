'''Loads cluster correction functions corrE and newCorrE to ROOT'''
import os
import ROOT

## Helper variable
_CMSSW_BASE = os.environ['CMSSW_BASE']

## Add JPsi/MuMu/{src,interface} to the include path
ROOT.gROOT.ProcessLine('.include %s' % os.path.join(_CMSSW_BASE, 'interface'))
ROOT.gROOT.ProcessLine('.include %s' % os.path.join(_CMSSW_BASE, 'src'))

## Load compiled cluster correction functions
ROOT.gROOT.LoadMacro(
    os.path.join( _CMSSW_BASE,
                 'src/JPsi/MuMu/src/clusterCorrection.cc+' )
)

## Import the cluster correction functions
from ROOT import corrE, newCorrE
