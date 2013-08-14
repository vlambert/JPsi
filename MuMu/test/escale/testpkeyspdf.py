'''
Given a selection and data for Zmmg events, build a parametrized KEYS PDF
for the photon resolution shape (Ereco/Etrue - 1) * 100 (in %).  The
shape of the PDF is taken from the RooKeysPdf trained on the simulated
data.  The parametrization introduces dependence on the location
and scale x -> (x-m)/s.  Here, the location and scale parameters are named
m and s.  They are named phoScale and phoRes in the code and they
bear the meaning of the mode and effective sigma of the shape.
The test checks that the PDF shifts and scales correctly as a function
of m and s.
'''
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.cmsstyle as cmsstyle

from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf

##------------------------------------------------------------------------------
## Here starts the meat.

## Selection
cuts = ['phoIsEB',
        'phoR9 > 0.94',
        '20 < phoPt & phoPt < 25',
        'mmMass + mmgMass < 190',
        'isFSR',
        'phoGenE > 0',
        ]
cutlabels = [
    'Barrel',
    'R_{9} > 0.94',
    'E_{T}^{#gamma} #in [20, 25] GeV',
    'm_{#mu#mu} + m_{#mu#mu#gamma} < 190 GeV',
    'FSR'
    ]

## Create the default workspace
w = ROOT.RooWorkspace('w')

## Define data variables 
mmgMass = w.factory('mmgMass[40, 140]')
mmMass = w.factory('mmMass[10, 140]')
phoERes = w.factory('phoERes[-70, 100]')
weight = w.factory('weight[1]')

## The TFormula expression defining the data is given in the titles.
weight.SetTitle('pileup.weight')
phoERes.SetTitle('100 * phoERes')

## Create a preselected tree
zchain = getChains('v11')['z']
tree = zchain.CopyTree('&'.join(cuts))
## Have to copy aliases by hand
for a in zchain.GetListOfAliases():
    tree.SetAlias(a.GetName(), a.GetTitle())

## Get the nominal dataset
data = dataset.get(tree=tree, weight=weight, cuts=cuts,
                   variables=[mmgMass, mmMass, phoERes,])

## Give the titles the original meaning
phoERes.SetTitle('E_{reco}^{#gamma}/E_{gen}^{#gamma} - 1')
phoERes.setUnit('%')

##------------------------------------------------------------------------------
## Build model
phoScale = w.factory('phoScale[0,-50,50]')
phoRes = w.factory('phoRes[5,0.01,50]')
range_save = (phoERes.getMin(), phoERes.getMax())
## Enlarge the range of the observable to get vanishing tails.
phoERes.setRange(-90, 150)
phoEResPdf = ParametrizedKeysPdf('phoEResPdf', 'phoEResPdf',
                                 phoERes, phoScale, phoRes, data,
                                 ROOT.RooKeysPdf.NoMirror, 1.5)
phoERes.setRange(*range_save)

##------------------------------------------------------------------------------
## Plot the phoEResPdf for various values of the scale
canvases.next('ShapeScaleScan').SetGrid()
phoRes.setVal(1)
plot = phoERes.frame(roo.Range(-10, 10))
latexlabels = []
for i, color in enumerate('Red Yellow Green Blue Black'.split()):
    scale = -4 + 2*i
    phoScale.setVal(scale)
    phoEResPdf.plotOn(plot, roo.LineColor(getattr(ROOT, 'k' + color)))
    label = Latex(['s: %d %%' % scale,],
                  position=(0.8, 0.75 - (i+1) * 0.055))
    label.SetTextColor(getattr(ROOT, 'k' + color))
    latexlabels.append(label)

plot.SetTitle('Scale Parametrization Closure')
plot.GetYaxis().SetTitle('a. u.')
plot.Draw()
Latex(cutlabels, position=(0.2, 0.75)).draw()
Latex(['r: 1 %',], position=(0.8, 0.75)).draw()
for l in latexlabels:
    l.draw()

##------------------------------------------------------------------------------
## Plot the phoEResPdf for various values of the effective sigma
canvases.next('ShapeWidthScan').SetGrid()
plot = phoERes.frame(roo.Range(-13, 10))
phoScale.setVal(0)
latexlabels = []
for i, color in enumerate('Red Yellow Green Blue Black'.split()):
    res = 1./(1. + 0.25*(2-i))
    color = getattr(ROOT, 'k' + color)
    phoRes.setVal(res)
    phoEResPdf.plotOn(plot, roo.LineColor(color))
    label = Latex(['r: %.2g %%' % res,],
                  position=(0.75, 0.75 - (i+1) * 0.055))
    label.SetTextColor(color)
    latexlabels.append(label)

phoScale.setVal(-4)
for res, color in zip([1./(1. + 0.25*(2-i)) for i in range(5)],
                        [ROOT.kRed, ROOT.kYellow, ROOT.kGreen,
                         ROOT.kBlue, ROOT.kBlack]):
    phoRes.setVal(res)
    phoEResPdf.plotOn(plot, roo.LineColor(color))

phoScale.setVal(2)
for res, color in zip([1./(1. + 0.25*(2-i)) for i in range(5)],
                        [ROOT.kRed, ROOT.kYellow, ROOT.kGreen,
                         ROOT.kBlue, ROOT.kBlack]):
    phoRes.setVal(res)
    phoEResPdf.plotOn(plot, roo.LineColor(color))

plot.SetTitle('Resolution Parametrization Closure')
plot.GetYaxis().SetTitle('a. u.')
plot.Draw()
Latex(cutlabels, position=(0.2, 0.75)).draw()
Latex(['s: -4, 0, 2 %',], position=(0.75, 0.75)).draw()
for l in latexlabels:
    l.draw()

##------------------------------------------------------------------------------
## Extract the MC truth scale and resolution from MC
phoEResPdf.fitTo(data, roo.PrintLevel(-1), roo.SumW2Error(False))
phoScaleRef = phoScale.getVal()
phoResRef = phoScale.getVal()

## mmgMassPhoSmearE = w.factory('mmgMassPhoSmearE[40, 140]')
## phoEResSmear = w.factory('phoEResSmear[-80, 110]')

##------------------------------------------------------------------------------
## Plot the nominal MC data overlayed with the pdf shape and fit
canvases.next('nominal_fit')
phoERes.setUnit("%")
plot = phoERes.frame(roo.Range(-7.5, 7.5))
plot.SetTitle("MC overlayed with PDF shape (blue) and it's parametrized fit"
              "(dashed red)")
data.plotOn(plot)
phoEResPdf.shape.plotOn(plot)
phoEResPdf.plotOn(plot, roo.LineColor(ROOT.kRed), roo.LineStyle(ROOT.kDashed))
plot.Draw()
Latex([
    's_{shape}: %.3f %%' % phoEResPdf.shapemode,
    's_{fit}: %.3f #pm %.3f %%' % (phoScale.getVal(), phoScale.getError()),
    's_{fit} - s_{shape}: %.4f #pm %.4f' % (
        phoScale.getVal() - phoEResPdf.shapemode,
        phoScale.getError()
        ),
    'r_{shape}: %.3f %%' % phoEResPdf.shapewidth,
    'r_{fit}: %.3f #pm %.3f %%' % (phoRes.getVal(), phoRes.getError()),
    'r_{fit}/r_{shape}: %.4f #pm %.4f' % (
        phoRes.getVal() / phoEResPdf.shapewidth,
        phoRes.getError() / phoEResPdf.shapewidth),
    ], position=(0.2, 0.75)).draw()

##------------------------------------------------------------------------------
## Plot the nominal MC data overlayed with a CB fit

cb = w.factory('''CBShape::cb(phoERes, mcb[0,-50, 50], scb[3, 0.1, 20],
                              acb[1.5, -10, 10], ncb[1.5, 0.2, 10])''')

cb.fitTo(data, roo.Range(-40, 20))

c1 = canvases.next('nominal_data_log')
c1.SetLogy()
c1.SetGrid()
phoERes.setUnit("%")
plot = phoERes.frame(roo.Range(-40, 20), roo.SumW2Error(True))
plot.SetTitle(', '.join(cutlabels[:3]))
data.plotOn(plot)
cb.plotOn(plot)
plot.GetYaxis().SetRangeUser(0.01, 1e4)
plot.Draw()

canvases.next('nominal_data_zoom').SetGrid()
phoERes.setUnit("%")
plot = phoERes.frame(roo.Range(-7.5, 7.5))
plot.SetTitle(', '.join(cutlabels[:3]))
data.plotOn(plot)
cb.plotOn(plot)
plot.Draw()


##------------------------------------------------------------------------------
## Footer stuff
canvases.update()
if __name__ == "__main__":
    import user

