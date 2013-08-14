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
from ROOT import kRed
from ROOT import kDashed
from ROOT import RooArgSet
from ROOT import RooBinning
from ROOT import RooDataSet
from ROOT import RooFFTConvPdf
from ROOT import RooKeysPdf
from ROOT import RooRealVar
from ROOT import RooWorkspace
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

setattr(RooWorkspace, "Import", getattr(RooWorkspace, "import"))

## Here starts the meat.

nentries = -1
sRange = (-10, 10)
phoPtRange = (12, 15)

chains = getChains('v11')
mcTree = chains['z']

w = RooWorkspace('w')

mmgMass = w.factory('mmgMass[40, 140]')
mmMass = w.factory('mmMass[10, 140]')
weight = w.factory('weight[1]')

weight.SetTitle('pileup.weight')

## List the cuts with looser window on mmgMass to allow for scale changes
fRange = fMin, fMax = 1. + sRange[0]/100., 1. + sRange[1]/100.
lo = 'scaledMmgMass3(%f, mmgMass, mmMass)' %  fMin
hi = 'scaledMmgMass3(%f, mmgMass, mmMass)' %  fMax
cuts = ['%f < %s & %s < %f' % (mmgMass.getMin(), lo, hi, mmgMass.getMax()),
        '%f < mmMass & mmMass < %f' % (mmMass.getMin(), mmMass.getMax()),
        #'%f < m1gMass & m1gMass < %f' % (m1gMass.getMin(), m1gMass.getMax()),
        #'%f < m2gMass & m2gMass < %f' % (m2gMass.getMin(), m2gMass.getMax()),
        #'12 < phoPt & phoPt < 15',
        'phoIsEB',
        'phoR9 < 0.94',
        'mmMass < 80',
        'isFSR']

## Add a loose cut on photon pt
lo = phoPtRange[0] * fRange[0]
hi = phoPtRange[1] * fRange[1]
cuts.append('%f <= phoPt & phoPt < %f' % (lo, hi))

## Add an optional cut on number of entries
if nentries > 0:
    cuts.append('Entry$ < %d' % nentries)

## Create a preselected tree
tree = mcTree.CopyTree('&'.join(cuts))

## Get the nominal dataset and those scaled up and down
mmgData = dataset.get(tree=tree, variable=mmgMass, weight=weight,
                      cuts = (cuts[:] + ['%f < phoPt & phoPt < %f' % phoPtRange]))

mmgMass.SetTitle('scaledMmgMass3(%f, mmgMass, mmMass)' % fMin)
phoPtRangeMod = (phoPtRange[0] * fMin, phoPtRange[1] * fMin)
cutsMod = cuts[:] + ['%f < phoPt & phoPt < %f' % phoPtRangeMod]
mmgDataMin = dataset.get(variable=mmgMass, cuts=cutsMod)

mmgMass.SetTitle('scaledMmgMass3(%f, mmgMass, mmMass)' % fMax)
phoPtRangeMod = (phoPtRange[0] * fMin, phoPtRange[1] * fMax)
cutsMod = cuts[:] + ['%f < phoPt & phoPt < %f' % phoPtRangeMod]
mmgDataMax = dataset.get(variable=mmgMass, cuts=cutsMod)

## Split the data in 2 independent halfs
n = mmgData.numEntries()

mmgData1 = mmgData.reduce(EventRange(0, int(n/2)))
mmgData2 = mmgData.reduce(EventRange(int(n/2) + 1, n))

mmgDataMin1 = mmgDataMin.reduce(EventRange(0, int(n/2)))
mmgDataMin2 = mmgDataMin.reduce(EventRange(int(n/2) + 1, n))

## Import both parts of data in the workspace
## for d, n in [(mmgData, 'mmgData'), (mmgHist, 'mmgHist')]:
for d, n in [(mmgData1, 'mmgData1'), (mmgData2, 'mmgData2'),
             (mmgDataMin1, 'mmgDataMin1'), (mmgDataMin2, 'mmgDataMin2')]:
    d.SetName(n)
    w.Import(d)

## Build the PDFs
mmgMassPdf1 = w.factory('KeysPdf::mmgMassPdf1(mmgMass, mmgData1, NoMirror, 2)')
#mmgMassPdf2 = w.factory('KeysPdf::mmgMassPdf2(mmgMass, mmgData2, NoMirror, 2)')
mmgMassPdfMin = w.factory('KeysPdf::mmgMassPdfMin(mmgMass, mmgDataMin1, NoMirror, 2)')

mmgFrame = mmgMass.frame(Range(60,120))
# mmgHist.plotOn(mmgFrame)
mmgData2.plotOn(mmgFrame)
mmgMassPdf1.plotOn(mmgFrame)
#mmgMassPdf2.plotOn(mmgFrame, LineColor(kRed), LineStyle(kDashed))
mmgMassPdfMin.plotOn(mmgFrame, LineStyle(kDashed))
canvases.next('mmgMass')
mmgFrame.Draw()


for c in canvases.canvases:
    c.Update()
    
if __name__ == "__main__":
    import user

