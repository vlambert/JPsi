'''
Model for the density of the mu-mu-gamma (MMG) invarinat mass.  It is based on
simulation which is smoothed by KEYS kernel estimator.  Dependence on photon
energy scale (PhoS) and resolution (PhoR) is introduced by smearing the
simulation event by event.  The smearing changes the photon reconstructed energy
Ereco.  It is defined by a linear transformation of the detector response
Ereco/Egen. The transformation keeps the shape of Ereco/Egen but changes the
position and width of its peak to target scale and resolution expressed in %.
They are defined as the mode and effective sigma of the distribution
100 * (Ereco/Egen - 1)
The factor of 100 accounts for the "%" units.  The shape of the MMG mass
inbetween the grid points is interpolated using the moment morphing.

Motivation: Another conventional way of smearing the simulation is by adding
a random Gaussian variable.  Unlike such noise injection, the linear
transformation has the welcome properties of
    1. Being deterministing; there are no random numbers involved in the
    smearing process,
    2. Simulating non-Gaussian shapes,
    3. Being able to model better (smaller) resolution than the nominal
    simulation.

Another conventional way of obtaining the mass density for a given scale and
resolution target is smearing the simulation each time.  Unlike such brute
force approach, the moment morphing interpolation is:
    1. computationally very fast; after the initial calculation of the grid,
    2. robust; it is less prone to numerical noise coasing multiple local
    minima during the minimum log-likelihood fitting.
'''

##- Boilerplate imports --------------------------------------------------------

import array
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.rangesafekeyspdf import RangeSafeKeysPdf
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf
from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator

##-- Configuration -------------------------------------------------------------
## Target photon scale and resolution in %
## scaletargets = [-10, -5, 0, 5, 10]
## resolutiontargets = [0.5, 1, 2, 4, 6, 8, 10]
scaletargets = [-5, 0, 5]
resolutiontargets = [0.5, 1, 2, 4, 6, 8, 10]

stest = 'nominal'
rtest = 3
## name = 'EB_highR9_pt12to15'
name = 'EB_highR9_pt20-25'

## Selection
cuts = ['mmMass + mmgMass < 190',
        'isFSR',
        'phoGenE > 0',
        ]

##------------------------------------------------------------------------------
def parse_name_to_cuts():
    'Parse the name and apply the relevant cuts.'
    if 'EB' in name:
        cuts.append('phoIsEB')
        if 'highR9' in name:
            cuts.append('phoR9 > 0.94')
        elif 'lowR9' in name:
            cuts.append('phoR9 < 0.94')
    elif 'EE' in name:
        cuts.append('!phoIsEB')
        if 'highR9' in name:
            cuts.append('phoR9 > 0.95')
        elif 'lowR9' in name:
            cuts.append('phoR9 < 0.95')

    if 'pt' in name:
        ## Split the name into tokens.
        for tok in name.split('_'):
            ## Get the token with the pt
            if 'pt' in tok:
                if '-' in tok:
                    separator = '-'
                elif 'to' in tok:
                    separator = 'to'
                else:
                    raise RuntimeError, 'Error parsing %s in %s!' % (tok, name)
                lo, hi = tok.replace('pt', '').split(separator)
                cuts.append('%s <= phoPt & phoPt < %s' % (lo, hi))
## End of parse_name_to_cuts().

##------------------------------------------------------------------------------
def init():
    'Initialize workspace and common variables and functions.'
    parse_name_to_cuts()
    ## Create the default workspace
    global w
    w = ROOT.RooWorkspace('w')

    ## Define data observables. 
    global mmgMass, mmMass, phoERes, weight
    mmgMass = w.factory('mmgMass[40, 140]')
    mmMass = w.factory('mmMass[10, 140]')
    phoERes = w.factory('phoERes[-70, 100]')
    weight = w.factory('weight[1]')

    ## Define model parameters.
    global phoScale, phoRes
    phoScale = w.factory('phoScale[0,-50,50]')
    phoRes = w.factory('phoRes[3,0.01,50]')

    ## Set units.
    for x, u in zip([phoScale, phoRes],
                    '% %'.split()):
        x.setUnit(u)

    ## Prep for storing fit results in the workspace.
    global phoScaleTarget, phoResTarget, params
    phoScaleTarget = w.factory('phoScaleTarget[0,-50,50]')
    phoResTarget = w.factory('phoResTarget[5,0.01,50]')
    params = ROOT.RooArgSet(phoScaleTarget, phoResTarget)
    w.defineSet('params', params)
## End of init().


##------------------------------------------------------------------------------
def get_data(zchain = getChains('v11')['z']):
    'Get the nominal data that is used for smearing.'
    ## The TFormula expression defining the data is given in the titles.
    weight.SetTitle('pileup.weight')
    phoERes.SetTitle('100 * phoERes')

    ## Create a preselected tree
    tree = zchain.CopyTree('&'.join(cuts))
    ## Have to copy aliases by hand
    for a in zchain.GetListOfAliases():
        tree.SetAlias(a.GetName(), a.GetTitle())

    ## Get the nominal dataset
    global data
    data = dataset.get(tree=tree, weight=weight, cuts=cuts,
                       variables=[mmgMass, mmMass, phoERes,])

    ## Set units and nice titles
    for x, t, u in zip([mmgMass, mmMass, phoERes, phoRes, phoScale],
                       ['m_{#mu#mu#gamma}', 'm_{#mu#mu}',
                        'E_{reco}^{#gamma}/E_{gen}^{#gamma} - 1',
                        'photon energy resolution',
                        'photon energy scale',],
                       'GeV GeV %'.split()):
        x.SetTitle(t)
        x.setUnit(u)
    ##-- Get Smeared Data ------------------------------------------------------
    ## Enlarge the range of the observable to get vanishing tails.
    range_save = (phoERes.getMin(), phoERes.getMax())
    phoERes.setRange(-90, 150)
    global calibrator
    calibrator = MonteCarloCalibrator(data)
    phoERes.setRange(*range_save)
## End of get_data.

##------------------------------------------------------------------------------
def main():
    init()
    get_data()
## End of main().

##------------------------------------------------------------------------------
main()

## srefpoints = ROOT.RooArgList('phoScale_refgrid')
## sreflist = []
## ## Loop over target PhoS values.
## for bin, target in enumerate(scaletargets):
##     x = w.factory('phoScale_%d[%f]' % (bin, target))
##     x.setConstant()
##     srefpoints.add(x)
##     sreflist.append(x.GetName())
## ## End of loop over the target PhoS values.
## w.Import(srefpoints, srefpoints.GetName())

# rrefpoints = ROOT.RooArgList('phoRes_refgrid')
rreflist = []
## Loop over target PhoR values.
for bin, target in enumerate(resolutiontargets):
    x = w.factory('phoRes_%d[%f]' % (bin, target))
    x.setConstant()
    # rrefpoints.add(x)
    rreflist.append(x.GetName())
## End of loop over the target PhoR values.
# w.Import(rrefpoints, rrefpoints.GetName())


# spdflist = ROOT.RooArgList('mmgMassPdfs_sgrid')
# spdflist = []
varlist = ROOT.RooArgList(mmgMass)
## Loop over target PhoS values.
# for sbin, starget in enumerate(scaletargets):
    # rpdflist = ROOT.RooArgList('mmgMassPdfs_rgrid_s%d' % sbin)
rpdflist = []
    # savrange = (mmgMass.getMin(), mmgMass.getMax())
    ## Loop over the target PhoR values.
starget = calibrator.s0.getVal()
sbin = 0
for rbin, rtarget in enumerate(resolutiontargets):
    bintag = 's%d_r%d' % (sbin, rbin)

    sdata = calibrator.get_smeared_data(starget, rtarget)
    dataname = '_'.join([sdata.GetName(), name, bintag])
    sdata.SetName(dataname)
    w.Import(sdata)

    pdfname = '_'.join(['mmgMassPdf', name, bintag])
    pdfname = pdfname.replace('-', 'to')
    ## KEYS PDF Dilemma: RooKeysPdf is deprecated,
    ## RooNDKeysPdf cannot be stored in a workspace,
    ## RooMomentMorph constructor works in workspace factory only
    ## pdf = ROOT.RooNDKeysPdf(pdfname, pdfname,
    ##                         ROOT.RooArgList(mmgMass), sdata, "a", 1.5)
    ## -> Stick to deprecated RooKeysPdf for now.
    ## mmgMass.setRange(40, 140)
    peak = w.factory('%s_mode[91.2, 60, 120]' % pdfname)
    width = w.factory('%s_effsigma[3, 0.1, 20]' % pdfname)
    pdf = ParametrizedKeysPdf(pdfname + '_pkeys', pdfname + '_pkyes',
                              mmgMass, peak, width, sdata,
                              ROOT.RooKeysPdf.NoMirror, 1.5)
    savrange = (mmgMass.getMin(), mmgMass.getMax())
    normrange = (40, 130)
    fitrange = (60, 120)
    mmgMass.setRange(*fitrange)
    peak.setVal(pdf.shapemode)
    width.setVal(pdf.shapewidth)
    pdf.fitTo(sdata, roo.Range(*fitrange), roo.Strategy(2))
    w.Import(pdf)
    ## peak.setConstant()
    ## width.setConstant()

    hist = pdf.createHistogram(pdfname + '_hist', mmgMass, roo.Binning(1000))
    dhist = ROOT.RooDataHist(pdfname + '_dhist', pdfname + '_hist',
                             ROOT.RooArgList(mmgMass), hist)
    w.Import(dhist)
    hpdf = w.factory('HistPdf::{name}({{mmgMass}}, {name}_dhist, 1)'.format(
        name=pdfname
        ))
    ## bdata = data.reduce(ROOT.RooArgSet(mmgMass))
    ## bdata = bdata.binnedClone(data.GetName() + '_binned', data.GetTitle())
    ## pdf = ROOT.RooHistPdf(pdfname, pdfname, ROOT.RooArgSet(mmgMass), bdata, 2)
    pdf.Print()
    # w.Import(pdf)
    rpdflist.append(pdfname)
    ## Store the target parameters in the workspaces
    phoScaleTarget.setVal(starget)
    phoResTarget.setVal(rtarget)
    w.saveSnapshot(pdfname, params, True)
## End of loop over the target PhoR values.
## mmgMass.setRange(50, 130)
pdfname = '_'.join(['mmgMassPdf', name, 's%d' % sbin])
pdf = w.factory('''MomentMorph::{pdf}(
                       phoRes, {{mmgMass}}, {{{pdflist}}}, {{{mreflist}}}
                       )'''.format(pdf=pdfname,
                                   pdflist=','.join(rpdflist),
                                   mreflist=','.join(rreflist)))
    ## pdf = ROOT.RooMomentMorph(pdfname, pdfname, phoRes, varlist, rpdflist,
    ##                           rrefpoints)
    ## spdflist.add(pdf)
    # spdflist.append(pdfname)
## End of loop over the target PhoS values.
# pdfname = 'mmgMassPdf_' + name
## pdf = ROOT.RooMomentMorph(pdfname, pdfname, phoScale, varlist, spdflist,
##                           srefpoints)
## pdf = w.factory('''MomentMorph::{pdf}(
##                        phoScale, {{mmgMass}}, {{{pdflist}}}, {{{mreflist}}}
##                        )'''.format(pdf=pdfname,
##                                    pdflist=','.join(spdflist),
##                                    mreflist=','.join(sreflist)))
## w.Import(pdf)

w.Print()

pdf.fitTo(data, roo.Range(60, 120), roo.Minos())

tdata = calibrator.get_smeared_data(stest, rtest)
tdata.SetName('tdata')
pdf.fitTo(tdata, roo.Range(60, 120), roo.Minos())
calibrator.phoEResPdf.fitTo(tdata, roo.Range(-50, 50))
canvases.next('test_fit')
plot = mmgMass.frame(roo.Range(70, 110))
tdata.plotOn(plot)
pdf.plotOn(plot)
plot.Draw()
Latex(
    [
        's_{true}: %.3f #pm %.3f %%' % (calibrator.s.getVal(),
                                        calibrator.s.getError()),
        ## 's_{fit}: %.3f #pm %.3f %%' % (phoScale.getVal(),
        ##                                phoScale.getError()),
        'r_{true}: %.3f #pm %.3f %%' % (calibrator.r.getVal(),
                                        calibrator.r.getError()),
        'r_{fit}: %.3f ^{+%.3f}_{%.3f} %%' % (phoRes.getVal(),
                                                 phoRes.getErrorHi(),
                                                 phoRes.getErrorLo()),
        ],
    position=(0.2, 0.8)
    ).draw()

canvases.next('test_nll').SetGrid()
nll = pdf.createNLL(tdata, roo.Range(60, 120))
rframe = phoRes.frame(roo.Range(phoRes.getVal() + 3*phoRes.getErrorLo(),
                                phoRes.getVal() + 3*phoRes.getErrorHi()))
nll.plotOn(rframe, roo.ShiftToZero())
rframe.Draw()

canvases.update()
if __name__ == '__main__':
    # main()
    import user
    
