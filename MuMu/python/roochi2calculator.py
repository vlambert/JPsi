import ROOT
ROOT.gSystem.Load('libJPsiMuMu')
ROOT.gROOT.ProcessLine('#include "JPsi/MuMu/interface/RooChi2Calculator.h"')
RooChi2Calculator = ROOT.cit.RooChi2Calculator

