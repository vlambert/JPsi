import ROOT
ROOT.gSystem.Load('libJPsiMuMu')
ROOT.gROOT.ProcessLine('#include "JPsi/MuMu/interface/DataDrivenBinning.h"')
ROOT.gROOT.ProcessLine('typedef vector<double> VDouble')
DataDrivenBinning = ROOT.cit.DataDrivenBinning
VDouble = ROOT.VDouble
