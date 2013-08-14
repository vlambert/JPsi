'''
1. Build a gaussian model g(x|m,s)
2. Generate unbinned data from g 1 and 2 with (s,m) = (s1,m1) and (m2,s2)
3. Use data 1 to build Keys PDF k1(x|s1,m1)
4. Use k to build HistPDF with _transformed_ x variable t = (x-m)/s
   h1((x-hm)/hs|m1,s1)
5. Fit h1 to data2 to simulate a "measurement" of m2, s2.
'''

## Usual boiler plate
import copy
import sys
## Switch to ROOT's batch mode
#sys.argv.append("-b")
import JPsi.MuMu.common.roofit as roofit
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases

from math import log
from math import sqrt
from ROOT import gSystem
from ROOT import gROOT
from ROOT import kBlack
from ROOT import kRed
from ROOT import kDashed
from ROOT import RooArgSet as ArgSet
from ROOT import RooArgList as ArgList
from ROOT import RooBinning as Binning
from ROOT import RooDataHist as DataHist
from ROOT import RooDataSet as DataSet
from ROOT import RooFFTConvPdf as FFTConvPdf
from ROOT import RooHistPdf as HistPdf
from ROOT import RooKeysPdf as KeysPdf
from ROOT import RooRealVar as RealVar
from ROOT import RooWorkspace as Workspace
from ROOT import TCanvas

from JPsi.MuMu.common.roofit import AutoPrecision
from JPsi.MuMu.common.roofit import EventRange
from JPsi.MuMu.common.roofit import Format
from JPsi.MuMu.common.roofit import Import
from JPsi.MuMu.common.roofit import Layout
from JPsi.MuMu.common.roofit import LineColor
from JPsi.MuMu.common.roofit import LineStyle
from JPsi.MuMu.common.roofit import NumCPU
from JPsi.MuMu.common.roofit import Range
from JPsi.MuMu.common.roofit import RenameAllVariables
from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.datadrivenbinning import DataDrivenBinning

gSystem.Load('libJPsiMuMu')
gROOT.LoadMacro("tools.C+")

try:
    setattr(Workspace, "Import", getattr(Workspace, "import"))
except NameError:
    ## Try again :-)
    setattr(Workspace, "Import", getattr(Workspace, "import"))
    
w = Workspace('w', 'w')

## 1. Build a gaussian model g(x|m,s)
g = w.factory('Gaussian::g(x[-10,10],gm[0,-3,3],gs[1,0.1,3])')
x = w.var('x')

## 2. Generate unbinned data from g 1 and 2 with (s,m) = (s1,m1) and (m2,s2)
data1 = g.generate(ArgSet(x), 10000)

w.var('gm').setVal(-3.)
w.var('gs').setVal(2)
data2 = g.generate(ArgSet(x), 10000)

w.var('gm').setVal(0.)
w.var('gs').setVal(1.)

## 3. Use data 1 to build Keys PDF k1(x|s1,m1)
k = KeysPdf('k', 'k', x, data1, KeysPdf.NoMirror, 2)

## 4. Use k to build HistPDF with _transformed_ x variable t = (x-m)/s
##    h1((x-hm)/hs|m1,s1)
t = w.factory('FormulaVar::t("(x - hm) / hs", {x, hm[0,-5,5], hs[1,0.1,3]})')
hist = k.createHistogram('x', 10000)
dh = DataHist('dh', 'dh', ArgList(x), hist)
h = HistPdf('h', 'h', ArgList(t), ArgList(x), dh, 2)

## 5. Plot results
f1 = x.frame()
f1.SetTitle('Training Data')
data1.plotOn(f1)
g.plotOn(f1)
k.plotOn(f1, LineColor(kRed), LineStyle(kDashed))
h.plotOn(f1, LineColor(kBlack), LineStyle(kDashed))
canvases.next('Training_Data')
f1.Draw()

## 6. Fit h1 to data2 to simulate a "measurement" of m2, s2.
h.fitTo(data2)

f2 = x.frame()
f2.SetTitle('Test Data')
data2.plotOn(f2)
h.plotOn(f2)
h.paramOn(f2)
canvases.next('Test_Data')
f2.Draw()

for c in canvases.canvases:
    c.Update()

if __name__ == '__main__':
    import user
