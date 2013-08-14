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
import ROOT
import JPsi.MuMu.common.roofit as roofit
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.tools

from math import log
from math import sqrt

from ROOT import gStyle
from ROOT import gSystem
from ROOT import gROOT
from ROOT import kBlack
from ROOT import kBlue
from ROOT import kRed
from ROOT import kDashed

from ROOT import RooArgList
from ROOT import RooArgSet
from ROOT import RooBinning
from ROOT import RooCustomizer
from ROOT import RooDataHist
from ROOT import RooDataSet
from ROOT import RooFFTConvPdf
from ROOT import RooFormulaVar
from ROOT import RooHistPdf
from ROOT import RooKeysPdf
from ROOT import RooMinuit
from ROOT import RooRealVar
from ROOT import RooNDKeysPdf
from ROOT import RooWorkspace

from ROOT import TCanvas
from ROOT import TGraphErrors
from ROOT import TH1F

from JPsi.MuMu.common.latex import Latex

from JPsi.MuMu.common.roofit import AutoPrecision
from JPsi.MuMu.common.roofit import EventRange
from JPsi.MuMu.common.roofit import Format
from JPsi.MuMu.common.roofit import Import
from JPsi.MuMu.common.roofit import Layout
from JPsi.MuMu.common.roofit import LineColor
from JPsi.MuMu.common.roofit import LineStyle
from JPsi.MuMu.common.roofit import Minos
from JPsi.MuMu.common.roofit import NumCPU
from JPsi.MuMu.common.roofit import Range
from JPsi.MuMu.common.roofit import RenameAllVariables
from JPsi.MuMu.common.roofit import ShiftToZero
from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.datadrivenbinning import DataDrivenBinning
from JPsi.MuMu.tools import effSigma

gSystem.Load('libJPsiMuMu')
# gROOT.LoadMacro('tools.C+')
gStyle.SetPadTopMargin(0.1)

setattr(RooWorkspace, "Import", getattr(RooWorkspace, "import"))

## Here starts the meat.

nentries = -1

## Pairs of photon scale and extra smearing.
sTest = [-2, 0.5]
rTest = [1, 0.5]
phoPtRange = (15,20)

chains = getChains('v11')
mcTree = chains['z']
dataTree = chains['data']

w = RooWorkspace('w')

massShift = 90 + 1.03506

## Define variables
mmgMass = w.factory('mmgMass[40, 180]')
mmgMassShifted = w.factory('mmgMassShifted[-50, 90]')
mmgGenMass = w.factory('mmgGenMass[0, 300]')
mmgMassPhoGenE = w.factory('mmgMassPhoGenE[0, 300]')
mmgMassShiftedPhoGenE = w.factory('mmgMassShiftedPhoGenE[-90, 210]')
mmgMassPhoSmear = w.factory('mmgMassPhoSmear[-30,30]')
mmgMassPhoSmear.SetTitle('mmgMass - mmgMassPhoGenE')
phoERes = w.factory('phoERes[-0.3,3]')
mmMass = w.factory('mmMass[10, 180]')
weight = w.factory('weight[1]')
phoScale = w.factory('phoScale[0,-50,50]')
weight.SetTitle('pileup.weight')

## Shift mmg mass to peak at zero so that the mass spectrum can be treated
## as the detector resolution in the FFT convolution.
mmgMassShifted.SetTitle('mmgMass - %g' % float(massShift))
mmgMassShiftedPhoGenE.SetTitle('mmgMassPhoGenE - %g' % float(massShift))

## print '## Photon scaling fraction, dlog(m_uuy)/dlog(E_y)'
## Photon scaling fraction, dlog(m_uuy)/dlog(E_y)
phoF = w.factory('phoF[0.15 * 91.2, 0, 100]')
phoFFunc = w.factory('''FormulaVar::phoFFunc(
    "mmgMass * (0.5 - 0.5 * mmMass^2 / mmgMass^2)",
    {mmMass, mmgMass}
    )''')

## print '## List the cuts with looser window on mmgMass to allow for scale changes'
## List the cuts with looser window on mmgMass to allow for scale changes
fTest = [1. + s/100. for s in sTest]
lo = 'scaledMmgMass3(%f, mmgMass, mmMass)' %  min(fTest + [0])
hi = 'scaledMmgMass3(%f, mmgMass, mmMass)' %  max(fTest + [0])
cuts = ['%f < %s & %s < %f' % (mmgMass.getMin(), hi, lo, mmgMass.getMax()),
        '%f < mmMass & mmMass < %f' % (mmMass.getMin(), mmMass.getMax()),
        #'%f < m1gMass & m1gMass < %f' % (m1gMass.getMin(), m1gMass.getMax()),
        #'%f < m2gMass & m2gMass < %f' % (m2gMass.getMin(), m2gMass.getMax()),
        '15 < phoPt & phoPt < 20',
        'phoIsEB',
        'phoR9 < 0.94',
        'mmMass + mmgMass < 190',
        #'1 <= abs(phoIEtaX) & abs(phoIEtaX) <= 25',
        #'isFSR',
        ]

## print '## Add a loose cut on photon pt'
## Add a loose cut on photon pt
lo = phoPtRange[0] * min(fTest)
hi = phoPtRange[1] * max(fTest)
cuts.append('%f <= phoPt & phoPt < %f' % (lo, hi))

## print '## Add an optional cut on number of entries'
## Add an optional cut on number of entries
if nentries > 0:
    cuts.append('Entry$ < %d' % nentries)

## Create a preselected tree
tree = mcTree.CopyTree('&'.join(cuts))

## Have to copy aliases by hand
for a in mcTree.GetListOfAliases():
    tree.SetAlias(a.GetName(), a.GetTitle())

## print '## Get the nominal dataset'
## Get the nominal dataset
data = dataset.get(tree=tree,
                   variables=[mmgMass, mmgMassShifted, mmMass, mmgMassPhoGenE,
                              mmgMassShiftedPhoGenE, phoERes, mmgMassPhoSmear],
                   weight=weight,
                   cuts = (cuts[:] + ['%f < phoPt & phoPt < %f' % phoPtRange]))

## Create a preselected tree for real data
tree = dataTree.CopyTree('&'.join(cuts))

## Have to copy aliases by hand
for a in dataTree.GetListOfAliases():
    tree.SetAlias(a.GetName(), a.GetTitle())

## Get the nominal dataset
weight.SetTitle('1')
realdata = dataset.get(tree=tree,
                   variables=[mmgMass, mmgMassShifted, mmMass],
                   weight=weight,
                   cuts = (cuts[:] + ['%f < phoPt & phoPt < %f' % phoPtRange]))


## print '## Get the photon scale sensitivity factor'
## Get the photon scale sensitivity factor
phoFFunc.SetName('phoF')
data.addColumn(phoFFunc)
phoFFunc.SetName('phoFFunc')
phoF.setVal(18.13)
#phoF.setVal(data.mean(phoF))
phoF.setConstant()

reducedData = {}
for x in ('mmgMass mmgMassShifted phoERes mmgMassPhoGenE'.split() +
          'mmgMassShiftedPhoGenE mmgMassPhoSmear'.split()):
    reducedData[x] = data.reduce(RooArgSet(w.var(x)))    
    ## print '## Rename reduced data to mmgMass'
    if x != 'mmgMass':
        ## Rename reduced data to mmgMass
        formula = RooFormulaVar('mmgMass', 'rename ' + x, x,
                                RooArgList(w.var(x)))
        reducedData[x].addColumn(formula)
    if x != 'mmgMassShifted':
        ## Rename it also to mmgMassShifted
        formula = RooFormulaVar('mmgMassShifted', 'rename ' + x, x,
                                RooArgList(w.var(x)))
        reducedData[x].addColumn(formula)
    ## Drop the column with the original data
    # reducedData[x] = reducedData[x].reduce(RooArgSet(mmgMass, mmgMassShifted))
    reducedData[x].SetName(x + 'Data')
    ## Import the data in the workspace
    w.Import(reducedData[x])

## Define the translated mass
## mmgMassFunc = w.factory('''FormulaVar::mmgMassFunc(
##     "mmgMass - phoF*phoScale/100.",
##     {mmgMass, phoF, phoScale}
##     )''')

## print '## Get the nominal model for translation, use rho=2'
## Get the nominal model for translation, use rho=2
model = w.factory('KeysPdf::model(mmgMass, mmgMassData, NoMirror, 1.5)')

## Get the empirical PDF's for unsmeared mass and photon resolution
theory = w.factory('''KeysPdf::theory(mmgMassShifted, mmgMassShiftedPhoGenEData,
                                      NoMirror, 1.3)''')
## theory2 = RooNDKeysPdf('theory2', 'theory2', RooArgList(mmgMassShifted),
##                        reducedData['mmgMassShiftedPhoGenE'], 'a', 1.3)

## Increase the phoERes range by 20 % margin to ensure zero density outside
## of the data range.
phoEResRange = phoERes.getMax() - phoERes.getMin()
phoERes.setRange(phoERes.getMin() - 0.1 * phoEResRange,
                 phoERes.getMax() + 0.1 * phoEResRange)
phoEResShape = w.factory('KeysPdf::phoEResShape(phoERes, phoEResData, NoMirror, 1.5)')
#phoERes.setRange(-10,10)
phoEResShape2 = w.factory('KeysNDPdf::phoEResShape2(phoERes, phoEResData, NoMirror, 2)')

w.Print()

## Find the mode of the photon eneregy resolution function.
## This is equal to the photon energy scale in MC.
phoEResShapeNegative = w.factory('''FormulaVar::phoEResShapeNegative::(
    "-phoEResShape", {phoEResShape}
    )''')

## Find the minimum of - phoEResShape = maximum of phoEResShape
minuit = RooMinuit(phoEResShapeNegative)
minuit.migrad()
phoEScaleMC = phoERes.getVal()

## Turn the photon resolution function into a mass smearing while introducing
## location and scale parameters.  Do this by turning it into a RooHistPdf.
## Start a hack to make sure that the photon resolution shape is 0
## outside of the training range.
phoEResHist = phoEResShape.createHistogram('phoERes', 10000)
bw = phoEResHist.GetBinWidth(1)
nbins = phoEResHist.GetNbinsX()
phoEResHistExtended = TH1F('phoEResHistExtended', 'phoEResHistExtended',
                           int(1.2 * nbins),
                           phoERes.getMin() - 0.1 * nbins * bw,
                           phoERes.getMax() + 0.1 * nbins * bw)
for b in range(1, phoEResHist.GetNbinsX() + 1):
    bcenter = phoEResHist.GetBinCenter(b)
    newb = phoEResHistExtended.FindBin(bcenter)
    bcontent =  phoEResHist.GetBinContent(b)
    phoEResHistExtended.SetBinContent(newb, 1e5 * bcontent)
deltaMass = (mmgMass.getMax() - mmgMass.getMin()) / phoF.getVal()
phoERes.setRange(-0.5 * deltaMass, 0.5 * deltaMass)
phoEResDataHist = RooDataHist('phoEResDataHist', 'phoEResDataHist',
                              RooArgList(phoERes), phoEResHistExtended)
# phoERes.setRange(-0.5 * deltaMass, 0.5 * deltaMass)
## Define the mass smearing mean and widht as functions of photon
## energy scale and resolution
phoMean = w.factory('''FormulaVar::phoMean("phoF * phoScale / 100.",
                                           {phoF, phoScale})''')
#phoEResMC = ROOT.effSigma(phoEResHistExtended) * 100
phoEResMC = effSigma(phoEResHistExtended) * 100
phoWidth = w.factory('''FormulaVar::phoWidth(
    "phoF * phoRes / {effSigma}",
    {{phoF, phoRes[{effSigma},0.1,1000]}}
    )'''.format(effSigma = phoEResMC))
w.var('phoScale').setUnit('%')
w.var('phoRes').setUnit('%')

## Shift the mass range to be symmetric around zero
## mmgMassRangeMean = 0.5 * (mmgMass.getMin() + mmgMass.getMax())
## mmgMass.setRange(mmgMass.getMin() - mmgMassRangeMean,
##                  mmgMass.getMax() - mmgMassRangeMean)
phoEResFuncOfMMGMassShifted = w.factory(
    '''FormulaVar::phoEResFuncOfMMGMassShifted(
        "(mmgMassShifted - phoMean)/phoWidth + ({mcscale})",
        {{mmgMassShifted, phoMean, phoWidth}}
        )'''.format(mcscale = phoEScaleMC))

#phoEResFuncOfMMGMass = w.factory('FormulaVar::phoEResFuncOfMMGMass2("mmgMass ", {mmgMass})')

## Plug in the mass smering mean and width into the smearing shape
phoSmear = RooHistPdf('phoSmear', 'phoSmear',
                      RooArgList(phoEResFuncOfMMGMassShifted),
                      RooArgList(phoERes), phoEResDataHist, 2)
## TODO: use RooCustomizer to transform phoEResShape
## Define the transform such that the phoEResShape is always evaluated
## inside of it's boundaries.
cust = RooCustomizer(phoEResShape, "transformed")
cust.replaceArg(phoERes, phoEResFuncOfMMGMassShifted)
phoSmear2 = cust.build()

w.Import(phoSmear)

## Apply photon smearing to the theory
mmgMassShifted.setRange(-30, 30)
mmgMassShifted.setBins(10000, 'fft')
theoryXphoSmear = w.factory('FCONV::theoryXphoSmear(mmgMassShifted, phoSmear, theory)')
## mmgMassPhoGenEFunc = w.factory('FormulaVar::mmgMassPhoGenEFunc("mmgMass", {mmgMass})')
## theoryXphoSmear = RooFFTConvPdf('theoryXphoSmear', 'theoryXphoSmear',
##                                 mmgMassPhoGenEFunc, mmgMassPhoGenE, theory, phoSmear)

## Fit Smeared theory to data
#theoryXphoSmear.fitTo(mmgData, Range(70,110))

## Make labels
labels = []
if 'phoIsEB' in cuts:
    labels.append('Barrel')
else:
    labels.append('Endcaps')
    
labels = ['E_{T}^{#gamma} #in [%g,%g] GeV' % phoPtRange]

for c in cuts:
    if 'phoR9' in c:
        labels.append(c.replace('phoR9', 'R_{9}'))
        break

# labels.append('Moduel 1')

labels.append('True Resolution (#sigma_{eff}): %.3g %%' % phoEResMC)
labels.append('True Scale: %.3g %%' % (100*phoEScaleMC))
labels.append('<EdM/dE>: %.3g GeV' % phoF.getVal())

llabels = Latex(labels, (0.21, 0.83))

## Make plots
plots = []

phoRes = w.var('phoRes')
phoRes.SetTitle('#sigma_{eff}(E_{#gamma})')
phoScale.SetTitle('E_{#gamma} Scale')
## for x in [phoRes, phoScale]:
##     x.SetTitle(x.GetName())

## Theory for unsmeared photon
canvases.next('theory')#.SetLogy()
mmgMassShiftedTitle = mmgMassShifted.GetTitle().replace('mmgMass', 'm(#mu#mu#gamma)')
mmgMassShifted.setUnit('GeV')
mmgMassShifted.SetTitle(mmgMassShiftedTitle.replace('m(#mu#mu#gamma)', 'm(#mu#mu + gen #gamma)'))
plot = mmgMassShifted.frame(Range(60-90,120-90)) #Range(-5,5)) #Range(0, 500))
mmgMassShifted.SetTitle(mmgMassShiftedTitle)
plot.SetTitle('"Theory:" #mu#mu#gamma Inv. Mass Modeling with Gen. Level Photon Energy')
reducedData['mmgMassShiftedPhoGenE'].plotOn(plot)
theory.plotOn(plot)
# theory2.plotOn(plot, LineColor(kRed), LineStyle(kDashed))
plot.Draw()
plots.append(plot)

## Photon Resolution
canvases.next('phoERes').SetLogy()
phoERes.SetTitle('E^{#gamma}_{reco}/E^{#gamma}_{gen} - 1')
phoERes.setRange(-0.9,3.2)
plot = phoERes.frame()
plot.SetTitle('Photon Resolution Modeling Zoom Out')
reducedData['phoERes'].plotOn(plot)
phoEResShape.plotOn(plot)
plot.Draw()
plot.GetYaxis().SetRangeUser(1e-3, 1e4)
llabels.position = (0.6, 0.83)
llabels.draw()
plots.append(plot)

## Photon Resolution Zoom In
canvases.next('phoEResZoom')
plot = phoERes.frame(Range(-0.25 + phoEScaleMC, 0.33 + phoEScaleMC))
plot.SetTitle('Photon Resolution Modeling Zoom In')
reducedData['phoERes'].plotOn(plot)
phoEResShape.plotOn(plot)
plot.Draw()
llabels.draw()
llabels.position = (0.21, 0.83)
plots.append(plot)

## ## Photon Resolution Zoom Out
## canvases.next('phoEResZoomOut')
## plot = phoERes.frame(Range(-1,1))
## reducedData['phoERes'].plotOn(plot)
## phoEResShape.plotOn(plot)
## phoEResShape2.plotOn(plot, LineColor(kRed))
## plot.Draw()
## llabels.draw()
## plots.append(plot)

## Mass smearing due to photon resolution
canvases.next('mmgMassPhoSmear')#.SetLogy()
mmgMassShifted.SetTitle('m(#mu#mu + reco #gamma) - m(#mu#mu + gen #gamma)')
plot = mmgMassShifted.frame(Range(-5,5)) #Range(-5,5)) #Range(0, 500))
mmgMassShifted.SetTitle(mmgMassShiftedTitle)
plot.SetTitle('"Resolution:" Modeling of Mass Smearing Due to Photon Energy Resolution')
reducedData['mmgMassPhoSmear'].plotOn(plot)
phoSmear.fitTo(reducedData['mmgMassPhoSmear'], Range(-5, 5), NumCPU(3))
phoSmear.plotOn(plot)
phoSmear.paramOn(plot)
phoSmear2.fitTo(reducedData['mmgMassPhoSmear'], Range(-5, 5), NumCPU(3))
phoSmear2.plotOn(plot, LineColor(kRed), LineStyle(kDashed))
plot.Draw()
llabels.draw()
plots.append(plot)

## Plot theory, smearing and smeared theory
plot = mmgMassShifted.frame(Range(-5, 5))
plot.SetTitle('Model = Theory * Resolution')
phoScale.setVal(0)
phoRes.setVal(phoEResMC)
theory.plotOn(plot)
phoSmear.plotOn(plot, LineColor(kRed))
theoryXphoSmear.plotOn(plot, LineColor(kBlack))
c1 = canvases.next('convolution')
c1.SetGridx()
c1.SetGridy()
plot.Draw()
llabels.draw()

## Data and model
theoryXphoSmear.fitTo(reducedData['mmgMassShifted'],
                      Range(62-massShift, 118-massShift),
                      #Minos(),
                      NumCPU(3))
canvases.next('model')
plot = mmgMassShifted.frame(Range(58-massShift, 122-massShift))
plot.SetTitle('"Model = Theory * Resolution:" Reco. Mass Modeling as a Convolution')
reducedData['mmgMassShifted'].plotOn(plot)
theoryXphoSmear.plotOn(plot)
theoryXphoSmear.paramOn(plot)
plot.Draw()
llabels.draw()
phoEResMCFit = phoRes.getVal()
phoEScaleMCFit = phoScale.getVal()

## Real data and model
theoryXphoSmear.fitTo(realdata,
                      Range(62-massShift, 118-massShift),
                      # Minos(),
                      NumCPU(3))
canvases.next('realdata')
plot = mmgMassShifted.frame(Range(58-massShift, 122-massShift))
plot.SetTitle('Fit Model to Real Data')
reducedData['mmgMassShifted'].plotOn(plot)
theoryXphoSmear.plotOn(plot)
theoryXphoSmear.paramOn(plot)
plot.Draw()
llabels.draw()
phoEResData = phoRes.getVal()
phoEScaleData = phoScale.getVal()

#plot.GetYaxis().SetRangeUser(1e-5, 1e2)

## Plot Likelihood vs scale
nll = theoryXphoSmear.createNLL(reducedData['mmgMassShifted'])
plot = phoScale.frame(
    Range(max(phoScale.getVal() - 5 * phoScale.getError(), phoScale.getMin()),
          min(phoScale.getVal() + 5 * phoScale.getError(), phoScale.getMax()))
    )
nll.plotOn(plot, ShiftToZero())
canvases.next('NLL_vs_phoScale')
plot.Draw()
llabels.position = (0.35, 0.83)
llabels.draw()

## Plot Likelihood vs resolution
#phoRes.SetTitle('Fitted Photon Resolution (#sigma_{eff})')
plot = phoRes.frame(
    Range(max(phoRes.getVal() - 5 * phoRes.getError(), phoRes.getMin()),
          min(phoRes.getVal() + 5 * phoRes.getError(), phoRes.getMax()))
    )
nll.plotOn(plot, ShiftToZero())
canvases.next('NLL_vs_phoRes')
plot.Draw()
llabels.draw()

## ## Plot Likelihood vs resolution
## phoRes = w.var('phoRes')
## plot = phoRes.frame(
##     Range(max(phoRes.getVal() - 5 * phoRes.getError(), phoRes.getMin()),
##           min(phoRes.getVal() + 5 * phoRes.getError(), phoRes.getMax()))
##     )
## nll.plotOn(plot, ShiftToZero())
## canvases.next('NLL_vs_phoRes')
## plot.Draw()
## llabels.draw()

## Plot Likelihood contours vs scale and resolution
canvases.next('NLL_Contours')
phoRes.setRange(
    max(min(phoRes.getVal(), phoEResMC) - 6 * phoRes.getError(), phoRes.getMin()),
    min(max(phoRes.getVal(), phoEResMC) + 6 * phoRes.getError(), phoRes.getMax())
    )

phoScale.setRange(
    max(min(phoScale.getVal(), 100*phoEScaleMC) - 10 * phoRes.getError(), phoRes.getMin()),
    min(max(phoScale.getVal(), 100*phoEScaleMC) + 10 * phoRes.getError(), phoRes.getMax())
    )

m = RooMinuit(nll)
m.migrad()
m.minos()
plot = m.contour(phoScale, phoRes, 1,2,3)
plot.SetTitle('NLL Countours')
plot.Draw()
mcTruth = ROOT.TMarker(100*phoEScaleMC, phoEResMC, 2)
mcTruth.DrawClone()
mcTruth.Draw()

## canvases.next('nominal')
## mmgFrame = mmgMass.frame(Range(80,100))
## mmgData.plotOn(mmgFrame)
## #phoScale.setVal(0)
## model.plotOn(mmgFrame)
## # theory.plotOn(mmgFrame, LineStyle(kDashed), LineColor(kRed))
## theoryXphoSmear.plotOn(mmgFrame, LineStyle(kDashed), LineColor(kRed))
## theoryXphoSmear.paramOn(mmgFrame)
## ## Shift the photon smearing to the Z mass and scale t
## ## phoSmearShifted = w.factory('Gaussian(mmgMass, pssMean[%f], pssWidth[%f])' %
## ##                             (91.2, 91.2 * w.var('phoRes').getVal() / 100.))
## ## phoSmearShifted.plotOn(mmgFrame, LineStyle(kDashed), LineColor(kRed))
## mmgFrame.Draw()

## Print report
print 'Source, scale, resolution'
print 'MC true', phoEScaleMC, phoEResMC
print 'MC fit', phoEScaleMCFit, phoEResMCFit
print 'data', phoEResData, phoEResData

for c in canvases.canvases:
    if c:
        c.Update()
    

if __name__ == "__main__":
    import user

