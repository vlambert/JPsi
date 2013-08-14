"""
Makes the custom ROOT class DummyRootClass visible to PyROOT.
  Usage:
  from JPsi.MuMu.common.dummyrootclass import DummyRootClass
  drc = DummyRootClass()
"""

import ROOT

## The order of the following two lines matters!
ROOT.gSystem.Load('libJPsiMuMu')
ROOT.gROOT.ProcessLine('#include "JPsi/MuMu/interface/DummyRootClass.h"')

DummyRootClass = ROOT.cit.DummyRootClass
