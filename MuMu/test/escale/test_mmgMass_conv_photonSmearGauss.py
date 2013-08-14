'''
Build f(m|s,r) for the mmg invariant mass of a given scale and injected
extra resolution smearing s and r. Test if it is well
approximated by f(m|s,r) ~ f(m|0,0) * g(m|MZ*x*s,MZ*x*r) where x
is the photon energy sensitivy
factor x = (d log m) / (d log E) with m being the mumugamma invariant mass and
E the photon energy. MZ denotes the Z mass.
Could possibly extend to
f(m|0,0) * g(m|MZ*(1-x)*S,MZ*(1-x)*R) * g(m|MZ*x*s,MZ*x*r)
where S and R are the muon Scale and resolution.
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

from ROOT import gStyle
from ROOT import gSystem
from ROOT import gROOT
from ROOT import kRed
from ROOT import kDashed

from ROOT import RooArgList
from ROOT import RooArgSet
from ROOT import RooBinning
from ROOT import RooDataHist
from ROOT import RooDataSet
from ROOT import RooFFTConvPdf
from ROOT import RooHistPdf
from ROOT import RooKeysPdf
from ROOT import RooRealVar
from ROOT import RooWorkspace

from ROOT import TCanvas
from ROOT import TGraphErrors

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
gStyle.SetPadTopMargin(0.1)

setattr(RooWorkspace, "Import", getattr(RooWorkspace, "import"))

## Here starts the meat.

nentries = -1

## Pairs of photon scale and extra smearing.
sTest = [-2, 0.5]
rTest = [1, 0.5]
phoPtRange = (12,15)

chains = getChains('v11')
mcTree = chains['z']

w = RooWorkspace('w')

## Define variables 
mmgMass = w.factory('mmgMass[40, 180]')
mmgGenMass = w.factory('mmgGenMass[0, 300]')
mmgMassPhoGenE = w.factory('mmgMassPhoGenE[0, 300]')
phoERes = w.factory('phoERes[-1,10]')
mmMass = w.factory('mmMass[10, 180]')
weight = w.factory('weight[1]')
phoScale = w.factory('phoScale[0,-50,50]')
weight.SetTitle('pileup.weight')

## Photon scaling fraction, dlog(m_uuy)/dlog(E_y)
phoF = w.factory('phoF[0.15 * 91.2, 0, 100]')
phoFFunc = w.factory('''FormulaVar::phoFFunc(
    "mmgMass * (0.5 - 0.5 * mmMass^2 / mmgMass^2)",
    {mmMass, mmgMass}
    )''')

## List the cuts with looser window on mmgMass to allow for scale changes
fTest = [1. + s/100. for s in sTest]
lo = 'scaledMmgMass3(%f, mmgMass, mmMass)' %  min(fTest + [0])
hi = 'scaledMmgMass3(%f, mmgMass, mmMass)' %  max(fTest + [0])
cuts = ['%f < %s & %s < %f' % (mmgMass.getMin(), hi, lo, mmgMass.getMax()),
        '%f < mmMass & mmMass < %f' % (mmMass.getMin(), mmMass.getMax()),
        #'%f < m1gMass & m1gMass < %f' % (m1gMass.getMin(), m1gMass.getMax()),
        #'%f < m2gMass & m2gMass < %f' % (m2gMass.getMin(), m2gMass.getMax()),
        #'12 < phoPt & phoPt < 15',
        'phoIsEB',
        'phoR9 > 0.94',
        'mmMass + mmgMass < 190',
        #'isFSR',
        ]

## Add a loose cut on photon pt
lo = phoPtRange[0] * min(fTest)
hi = phoPtRange[1] * max(fTest)
cuts.append('%f <= phoPt & phoPt < %f' % (lo, hi))

## Add an optional cut on number of entries
if nentries > 0:
    cuts.append('Entry$ < %d' % nentries)

## Create a preselected tree
tree = mcTree.CopyTree('&'.join(cuts))

## Have to copy aliases by hand
for a in mcTree.GetListOfAliases():
    tree.SetAlias(a.GetName(), a.GetTitle())

## Get the nominal dataset
data = dataset.get(tree=tree,
                   variables=[mmgMass, mmMass, mmgMassPhoGenE, phoERes],
                   weight=weight,
                   cuts = (cuts[:] + ['%f < phoPt & phoPt < %f' % phoPtRange]))

## Get the photon scale sensitivity factor
phoFFunc.SetName('phoF')
data.addColumn(phoFFunc)
phoFFunc.SetName('phoFFunc')
phoF.setVal(data.mean(phoF))
phoF.setConstant()

mmgData = data.reduce(RooArgSet(mmgMass))
mmgMassPhoGenEData = data.reduce(RooArgSet(mmgMassPhoGenE))
rename_mmgMassPhoGenE_to_mmgMass = w.factory('''
    FormulaVar::rename_mmgMassPhoGenE_to_mmgMass("mmgMassPhoGenE",
                                                 {mmgMassPhoGenE})''')
rename_mmgMassPhoGenE_to_mmgMass.SetName('mmgMass')
mmgMassPhoGenEData.addColumn(rename_mmgMassPhoGenE_to_mmgMass)
rename_mmgMassPhoGenE_to_mmgMass.SetName('rename_mmgMassPhoGenE_to_mmgMass')

## Put the nominal data in the workspace
mmgData.SetName('mmgData')
mmgMassPhoGenEData.SetName('mmgMassPhoGenEData')
w.Import(mmgData)
w.Import(mmgMassPhoGenEData)

## Define the translated mass
mmgMassFunc = w.factory('''FormulaVar::mmgMassFunc(
    "mmgMass - phoF*phoScale/100.",
    {mmgMass, phoF, phoScale}
    )''')

## Get the nominal model for translation, use rho=2
model = w.factory('KeysPdf::model(mmgMass, mmgData, NoMirror, 2)')
theory = w.factory('KeysPdf::theory(mmgMass, mmgMassPhoGenEData, NoMirror, 2)')

## Define Gaussian photon smearing
phoMean = w.factory('''FormulaVar::phoMean("phoF * phoScale / 100",
                                           {phoF, phoScale})''')
phoWidth = w.factory('''FormulaVar::phoWidth("phoF * phoRes / 100",
                                             {phoF, phoRes[2,0.2,20]})''')
phoSmear = w.factory('Gaussian::phoSmear(mmgMass, phoMean, phoWidth)')
w.var('phoScale').setUnit('%')
w.var('phoRes').setUnit('%')

## Apply photon smearing to the theory
mmgMass.setBins(100000, 'fft')
theoryXphoSmear = w.factory('FCONV::theoryXphoSmear(mmgMass, theory, phoSmear)')
## mmgMassPhoGenEFunc = w.factory('FormulaVar::mmgMassPhoGenEFunc("mmgMass", {mmgMass})')
## theoryXphoSmear = RooFFTConvPdf('theoryXphoSmear', 'theoryXphoSmear',
##                                 mmgMassPhoGenEFunc, mmgMassPhoGenE, theory, phoSmear)

## Fit Smeared theory to data
theoryXphoSmear.fitTo(mmgData, Range(70,110))

## Make plots
canvases.next('nominal')
mmgFrame = mmgMass.frame(Range(80,100))
mmgData.plotOn(mmgFrame)
#phoScale.setVal(0)
model.plotOn(mmgFrame)
# theory.plotOn(mmgFrame, LineStyle(kDashed), LineColor(kRed))
theoryXphoSmear.plotOn(mmgFrame, LineStyle(kDashed), LineColor(kRed))
theoryXphoSmear.paramOn(mmgFrame)
## Shift the photon smearing to the Z mass and scale t
## phoSmearShifted = w.factory('Gaussian(mmgMass, pssMean[%f], pssWidth[%f])' %
##                             (91.2, 91.2 * w.var('phoRes').getVal() / 100.))
## phoSmearShifted.plotOn(mmgFrame, LineStyle(kDashed), LineColor(kRed))
mmgFrame.Draw()

for c in canvases.canvases:
    c.Update()
    
if __name__ == "__main__":
    import user

