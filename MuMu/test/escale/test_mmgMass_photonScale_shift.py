'''
Build f(m|s) for the mmg invariant mass of a given scale. Test if it is well
approximated by f(m|s) ~ f(m - x*m*s|0) where x is the photon energy sensitivy
factor x = (d log m) / (d log E) where m is the mumugamma invariant mass and
E is the photon energy
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
## sTest = [-20, -10, -5, -2, -1, -0.5, 0, 0.5, 1, 2, 5, 10, 20]
sTest = [-5, -2, -1, -0.5, 0, 0.5, 1, 2, 5]
phoPtRange = (12,15)

chains = getChains('v11')
mcTree = chains['z']

w = RooWorkspace('w')

## Define variables 
mmgMass = w.factory('mmgMass[40, 140]')
mmMass = w.factory('mmMass[10, 140]')
weight = w.factory('weight[1]')
phoScale = w.factory('phoScale[0,-50,50]')
weight.SetTitle('pileup.weight')

## Photon scaling fraction, dlog(m_uuy)/dlog(E_y)
fPho = w.factory('fPho[0.15*91.2,0,100]')
fPhoFunc = w.factory('''FormulaVar::fPhoFunc(
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
        'phoR9 < 0.94',
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

## Get the nominal dataset
data = dataset.get(tree=tree, variable=mmgMass, weight=weight,
                   cuts = (cuts[:] + ['%f < phoPt & phoPt < %f' % phoPtRange]))
mmData = dataset.get(variable=mmMass,
                      cuts = (cuts[:] + ['%f < phoPt & phoPt < %f' % phoPtRange]))
data.merge(mmData)

## Get the photon scale sensitivity factor
fPhoFunc.SetName('fPho')
data.addColumn(fPhoFunc)
fPhoFunc.SetName('fPhoFunc')
fPho.setVal(data.mean(fPho))
fPho.setConstant()

mmgData = data.reduce(RooArgSet(mmgMass))

## Put the nominal data in the workspace
mmgData.SetName('mmgData')
# w.Import(mmgData)

## Define the translated mass
mmgMassFunc = w.factory('''FormulaVar::mmgMassFunc(
    "((mmgMass - mmgMode) / mmgScale + mmgMode)  - fPho*phoScale/100.",
    {mmgMass, mmgMode[91.2,70,110], mmgScale[1.,0.1,5], fPho, phoScale}
    )''')
mmgMode = w.var('mmgMode')
mmgScale = w.var('mmgScale')

## Get the nominal model for translation, use rho=2
model = RooKeysPdf('model', 'model', mmgMass, mmgData, RooKeysPdf.NoMirror, 2)

## Sample nominal model to binned data, no Poisson fluctuation
modelHist = model.createHistogram('mmgMass', 10000)
modelDH = RooDataHist('modelDH', 'modelDH', RooArgList(mmgMass), modelHist)

## Use the sampled model to build a transformed model, interpolation order=2
tmodel = RooHistPdf('tmodel', 'tmodel', RooArgList(mmgMassFunc),
                    RooArgList(mmgMass), modelDH, 2)


## Find the mode of the tmodel.
mmgMode.setVal(modelHist.GetBinCenter(modelHist.GetMaximumBin()))
mmgMode.setConstant(True)
fPho.setConstant(True)

## Fit the photon scale
phoScale.setConstant(False)
mmgScale.setConstant(True)

## Make plots
canvases.next('nominal')
mmgFrame = mmgMass.frame(Range(60,120))
mmgData.plotOn(mmgFrame)
phoScale.setVal(0)
model.plotOn(mmgFrame)
tmodel.plotOn(mmgFrame, LineStyle(kDashed), LineColor(kRed))
mmgFrame.Draw()

## Get the test datasets and models
dataCollection = []
models = []
sFitted = []
sFittedErr = []
for i, (fac, s) in enumerate(zip(fTest, sTest)):
    mmgMass.SetTitle('scaledMmgMass3(%f, mmgMass, mmMass)' % fac)
    phoPtRangeMod = (phoPtRange[0] * fac, phoPtRange[1] * fac)
    cutsMod = cuts[:] + ['%f < phoPt & phoPt < %f' % phoPtRangeMod]
    data = dataset.get(variable=mmgMass, cuts=cutsMod)
    ## Import the data in the workspace
    data.SetName('data%d' % i)
    w.Import(data)
    ## Also build the PDF's
    ## m = w.factory('KeysPdf::model%d(mmgMass, data%d, NoMirror, 2)' % (i, i))
    dataCollection.append(data)
    ## models.append(m)

    ## fit the transformed model to the test data
    tmodel.fitTo(data)
    sFitted.append(phoScale.getVal())
    sFittedErr.append(phoScale.getError())

    ## Display data overlaid with fitted and extrapolated models
    canvases.next('test%d' % i)
    frame = mmgMass.frame(Range(60,120))
    frame.SetTitle('')
    frame.GetXaxis().SetTitle(
        'm_{#mu#mu#gamma} (GeV), E^{#gamma} scaled by %g%%' % s
        )
    data.plotOn(frame)
    # m.plotOn(frame)
    tmodel.plotOn(frame, LineStyle(kDashed), LineColor(kRed))
    tmodel.paramOn(frame)
    frame.Draw()
    canvases.canvases[-1].Update()

## Plot fitted vs true
graphs = []    
graph = TGraphErrors(len(sTest))
for i, (x, y, ey) in enumerate(zip(sTest, sFitted, sFittedErr)):
    graph.SetPoint(i, x, y)
    graph.SetPointError(i, 0, ey)

canvases.next('Injected_vs_Fitted')
graph.SetTitle('Tranform Closure Test')
graph.Draw('ap')
graph.GetYaxis().SetTitle('Fitted Scale (%)')
graph.GetXaxis().SetTitle('Injected Scale (%)')
graph.Fit('pol1', '', '', -6, 6)


graphs.append(graph)

graph = TGraphErrors(len(sTest))
for i, (x, y, ey) in enumerate(zip(sTest, sFitted, sFittedErr)):
    graph.SetPoint(i, x, y - x)
    graph.SetPointError(i, 0, ey)

canvases.next('Injected_vs_Fitted_Bias')
graph.SetTitle('Tranform Closure Test')
graph.Draw('ap')
graph.GetYaxis().SetTitle('Fitted Scale Bias (%)')
graph.GetXaxis().SetTitle('Injected Scale (%)')
graph.Fit('pol2', '', '', -6, 6)

graphs.append(graph)

print 'report:'
fPho.Print()
phoScale.Print()
mmgMode.Print()
mmgScale.Print()

for c in canvases.canvases:
    c.Update()
    
if __name__ == "__main__":
    import user

