'''
The true scale varies between (9.9, 14.4) % for EE, R9 < 0.94 (evt1of4, evt2of4).
'''
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases
import phosphormodel5_test9 as ph

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator

name = 'tsv_mc_EE_lowR9_pt10to12_v13'
plots = []
calibrators0, calibrators1 = [], []

for label in ['evt%dof4' % i for i in range(1,2)]:
    ph.name = name + '_' + label
    ph.define_globals()
    ph.define_workspace()
    ph.define_data_observables()
    ph.set_ranges_for_data_observables()
    ph.get_data(getChains(ph.model_tree_version))

    ph.phoERes.setRange('plot', -15, 35)
    
    plot = ph.phoERes.frame(roo.Range('plot'))
    plot.SetTitle('Fit ' + label)
    ph.data['fsr1'].plotOn(plot)
    ph.calibrator1.phoEResPdf.plotOn(plot)
    ph.calibrator1.phoEResPdf.paramOn(plot)
    canvases.next('fit_' + label).SetGrid()
    plot.Draw()
    plots.append(plot)

    plot = ph.phoERes.frame(roo.Range('plot'))
    plot.SetTitle('Train ' + label)
    ph.data['fsr0'].plotOn(plot)
    ph.calibrator0.phoEResPdf.plotOn(plot)
    ph.calibrator0.phoEResPdf.paramOn(plot)
    canvases.next('train_' + label).SetGrid()
    plot.Draw()
    plots.append(plot)
    
    plot = ph.phoERes.frame(roo.Range('plot'))
    plot.SetTitle('Train Model on Fit Data ' + label)
    ph.data['fsr1'].plotOn(plot)
    ph.calibrator0.phoEResPdf.fitTo(ph.data['fsr1'], 
                                    roo.Range(-50, 50),
                                    roo.Strategy(2))
    
    ph.calibrator0.phoEResPdf.plotOn(plot, 
                                     roo.Range('plot'), 
                                     roo.NormRange('plot'))
    ph.calibrator0.phoEResPdf.paramOn(plot)
    canvases.next('trainOnFit_' + label).SetGrid()
    plot.Draw()
    plots.append(plot)
    
    calibrators0.append(ph.calibrator0)
    calibrators1.append(ph.calibrator1)

canvases.update()

print '======', name
for cal0, cal1, i in zip(calibrators0, calibrators1, range(1,5)):
    print 'evt%dof4' % i
    cal0.s0.Print()
    cal0.s.Print()
    cal1.s.Print()
    cal0.r0.Print()
    cal0.r.Print()
    cal1.r.Print()
    