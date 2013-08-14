'''
Test whether it is possible in RooFit ot have a 2D PDF where one of observables
has a range dependent on the other observable. It turns out that yes but
care has to be taken with 2D plots.

Jan Veverka, Caltech, 18 January 2012
'''

import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle

w = ROOT.RooWorkspace('w', 'w')

##------------------------------------------------------------------------------
def plotxy(pdf, xyexpr = 'x:y'):
    h_pdf = pdf.createHistogram(xyexpr)
    h_pdf.SetLineColor(ROOT.kBlue)
    xname, yname = xyexpr.split(':')
    for xbin in range(h_pdf.GetNbinsX() + 1):
        for ybin in range(h_pdf.GetNbinsY() + 1):
            xval = h_pdf.GetXaxis().GetBinCenter(xbin)
            yval = h_pdf.GetYaxis().GetBinCenter(ybin)
            w.var(xname).setVal(xval)
            w.var(yname).setVal(yval)
            if xval < w.var(xname).getMin() or w.var(xname).getMax() < xval:
                h_pdf.SetBinContent(h_pdf.GetBin(xbin, ybin), 0)
            if yval < w.var(yname).getMin() or w.var(yname).getMax() < yval:
                h_pdf.SetBinContent(h_pdf.GetBin(xbin, ybin), 0)            
    canvases.next(h_pdf.GetName())
    h_pdf.Draw('surf')
    canvases.next(h_pdf.GetName() + '_cont1')
    h_pdf.Draw('cont1')

## Rectangualar ranges ---------------------------------------------------------
gx = w.factory('Gaussian::gx(x[-5,5],mx[0],sx[0.5])')
gy = w.factory('Gaussian::gy(y[-5,5],my[0],sy[3])')
fprod = w.factory('PROD::fprod(gx, gy)')
plotxy(fprod)

## Dependent ranges -5 < x < y -------------------------------------------------
lo = w.factory('lo[-5]')
w.var('y').setVal(5)
w.var('x').setRange(w.factory('lo[-5]'), w.var('y'))
fprod.SetName('fprod2')
plotxy(fprod)

canvases.update()



