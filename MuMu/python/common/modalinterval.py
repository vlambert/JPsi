import ROOT
ROOT.gSystem.Load('libJPsiMuMu')
ROOT.gROOT.ProcessLine('#include "JPsi/MuMu/interface/ModalInterval.h"')
ROOT.gROOT.ProcessLine('typedef vector<double> VDouble')
ModalInterval = ROOT.cit.ModalInterval
VDouble = ROOT.VDouble
