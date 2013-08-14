import ROOT
import JPsi.MuMu.common.roofit
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.binedges import BinEdges
from JPsi.MuMu.scaleFitter import subdet_r9_categories

ROOT.gSystem.Load('libJPsiMuMu')

filename = 'strue_InitialValueFitSystematics10.root'
rootfile = ROOT.TFile.Open(filename)
w = rootfile.Get('ws1')
deltas = w.var('#Deltas')
binedges = list(BinEdges([10, 12, 15, 20, 25, 30, 100]))


iname = 'param_init_data_strue_mc_NominalFitRange68_mmMass80_{er}_PhoEt{l}-{h}_bifurGauss'
fname = 'param_fitted_data_strue_mc_NominalFitRange68_mmMass80_{er}_PhoEt{l}-{h}_bifurGauss'
DeltasRMS = w.factory('#DeltasRMS[0,20]')
DeltasRMS.setBins(5)
DeltasRMS.SetTitle("RMS of #Deltas")
DeltasRMS.setUnit('%')
irmsdata = ROOT.RooDataSet('irmsdata', 'irmsdata', ROOT.RooArgSet(DeltasRMS))
frmsdata = ROOT.RooDataSet('frmsdata', 'frmsdata', ROOT.RooArgSet(DeltasRMS))
fdatamod = frmsdata
for etar9 in list(subdet_r9_categories):
    for lo, hi in binedges:
        idata = w.data(iname.format(er=etar9.name, l=lo, h=hi))
        fdata = w.data(fname.format(er=etar9.name, l=lo, h=hi))
        ## Remove one bad fit by hand
        if etar9.name == 'EB_highR9' and lo == 10:
            fdata = fdata.reduce(ROOT.RooFit.EventRange(0,8))
            fdatamod = fdata
        irmsdata.add(ROOT.RooArgSet(idata.rmsVar(deltas)))
        frmsdata.add(ROOT.RooArgSet(fdata.rmsVar(deltas)))
        
        # print etar9.name, lo, fdata.rmsVar(deltas).getVal()

canvases.next('initValSyst_strue_initRms')
iplot = DeltasRMS.frame(ROOT.RooFit.AutoRange(irmsdata))
iplot.SetTitle('Initial Values')
irmsdata.plotOn(iplot)
iplot.Draw()

canvases.next('initValSyst_strue_fittedRms')
fplot = DeltasRMS.frame(ROOT.RooFit.AutoRange(frmsdata))
fplot.SetTitle('Fitted Values')
frmsdata.plotOn(fplot)
fplot.Draw()
