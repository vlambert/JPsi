'''
Get the PDF for the photon Et of FSR and ISR.
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
from ROOT import kBlack
from ROOT import kBlue
from ROOT import kRed
from ROOT import kDashed

from ROOT import RooArgList
from ROOT import RooArgSet
from ROOT import RooBinning
from ROOT import RooDataHist
from ROOT import RooDataSet
from ROOT import RooExponential
from ROOT import RooFFTConvPdf
from ROOT import RooFormulaVar
from ROOT import RooHistPdf
from ROOT import RooKeysPdf
from ROOT import RooMinuit
from ROOT import RooRealVar
from ROOT import RooWorkspace

from ROOT import TCanvas
from ROOT import TGraphErrors
from ROOT import TH1F

from JPsi.MuMu.common.roofit import AutoPrecision
from JPsi.MuMu.common.roofit import Components
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

gSystem.Load('libJPsiMuMu')
gROOT.LoadMacro("tools.C+")
gStyle.SetPadTopMargin(0.1)

setattr(RooWorkspace, "Import", getattr(RooWorkspace, "import"))

## Here starts the meat.

nentries = 50000

## Pairs of photon scale and extra smearing.
phoPtRange = (5,100)

chains = getChains('v11')
mcTree = chains['z']

w = RooWorkspace('w')

massShift = 90 + 1.03506

## Define variables
phoPt = w.factory('phoPt[0,100]')
mmgMass = w.factory('mmgMass[50,130]')
mmgGeom = w.factory('mmgGeom[0,10]')
mmgGeom.SetTitle('(mmgMass^2 - mmMass^2)/mmMass/phoPt')
weight = w.factory('weight[1]')
weight.SetTitle('pileup.weight')

cuts = ['%f < phoPt & phoPt < %f' % phoPtRange,
        'phoIsEB',
        'phoR9 < 0.94',
        'mmMass + mmgMass < 190',
        'isFSR',
        ]

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
                   variables=[phoPt, mmgMass, mmgGeom],
                   weight=weight,
                   cuts = (cuts[:] + ['%f < phoPt & phoPt < %f' % phoPtRange]))


phoPtPdf1 = w.factory('''SUM::phoPtPdf1(
    fg[0.25,0,1] * Gaussian::g1(phoPt, m1[10,-100,100], s1[12,5,100]),
    Exponential::e1(phoPt, tau1[-0.2,-10,10])
    )''')

## phoPtPdf2 = w.factory('''SUM::phoPtPdf2(
##     fg[0.25,0,1] * Gaussian::g2(phoPt, m2[10,-100,100], s2[12,5,100]),
##     fe21[0.9,0.1] * Exponential::e21(phoPt, tau21[-0.2,-10,10]),
##     Exponential::e22(phoPt, tau22[-0.1,-10,10])
##     )''')

w.Print()

e1 = w.pdf('e1')

## Make plots
plots = []

## ## Plot exponential only
## plot = phoPt.frame()
## plots.append(plot)
## data.plotOn(plot)
## e1.fitTo(data, Range(5,50))
## e1.plotOn(plot)
## e1.paramOn(plot)
## canvases.next('exponential').SetLogy()
## plot.Draw()

## Plot expo + gaus
canvases.next('EplusG').SetLogy()
plot = phoPt.frame()
plots.append(plot)
data.plotOn(plot)
phoPtPdf1.fitTo(data,Range(5,50))
phoPtPdf1.plotOn(plot,Range(0,80))
phoPtPdf1.plotOn(plot, Components('e1'), LineStyle(kDashed))
phoPtPdf1.plotOn(plot, Components('g1'), LineStyle(kDashed))
phoPtPdf1.paramOn(plot)
plot.Draw()

## ## Plot 2*expo + gaus
## canvases.next('2EplusG').SetLogy()
## plot = phoPt.frame()
## plots.append(plot)
## data.plotOn(plot)
## phoPtPdf2.fitTo(data,Range(5,80))
## phoPtPdf2.plotOn(plot)
## phoPtPdf2.plotOn(plot, Components('e21'), LineStyle(kDashed))
## phoPtPdf2.plotOn(plot, Components('e22'), LineStyle(kDashed))
## phoPtPdf2.plotOn(plot, Components('g2'), LineStyle(kDashed))
## phoPtPdf2.paramOn(plot)
## plot.Draw()

#rdata = data.reduce('mmgMass < 90')

for c in canvases.canvases:
    c.Update()
    
if __name__ == "__main__":
    import user

