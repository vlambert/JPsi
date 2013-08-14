#!/usr/bin/env python -i
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases
from JPsi.MuMu.escale.fitResultPlotter import FitResultPlotter
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf

# filename = 'massmorph_scalescan_EB_highR9_phoPt20-25.root'
# filename = 'massmorph_resscan_EB_highR9_phoPt12-15.root'
filename = 'massmorph_scalescan_EB_highR9_phoPt10-12.root'
wsname = 'w'

file1 = ROOT.TFile(filename)
w = file1.Get(wsname)
ismear = 20

phoERes = w.var('phoERes')
phoRes = w.var('phoRes')
phoScale = w.var('phoScale')
sdata = w.data('sdata_%d' % ismear)

canvases.next('massmorph_%d' % ismear)
plot = phoERes.frame(roo.Range(-30, 30))
sdata.plotOn(plot)
phoEResPdf = w.pdf('phoEResPdf_%d_shape_transform' % ismear)
phoEResPdfShape = w.pdf('phoEResPdf_%d_shape' % ismear)
phoEResPdfShape.plotOn(plot)
w.loadSnapshot('smear_%d' % ismear)
phoEResPdf.plotOn(plot, roo.LineColor(ROOT.kRed), roo.LineStyle(ROOT.kDashed))
plot.Draw()
canvases.update()
