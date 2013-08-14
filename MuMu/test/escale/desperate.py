##- Boilerplate imports --------------------------------------------------------

import array
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf
from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator

##-- Configuration -------------------------------------------------------------
## Selection
name = 'EB_highR9_pt20-25'
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
                lo, hi = tok.replace('pt', '').split('-')
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
    global mmgMass, mmMass, phoERes, mmgMassPhoGenE, weight
    mmgMass = w.factory('mmgMass[40, 140]')
    mmgMassPhoGenE = w.factory('mmgMassPhoGenE[0, 200]')
    mmMass = w.factory('mmMass[10, 140]')
    phoERes = w.factory('phoERes[-70, 100]')
    weight = w.factory('weight[1]')

    ## Define model parameters.
    global phoScale, phoRes
    phoScale = w.factory('phoScale[0,-50,50]')
    phoRes = w.factory('phoRes[3,0.01,50]')

    ## Set the binning for PDF normalization caching
    sbins = ROOT.RooUniformBinning(-10, 10, 2, 'cache')
    rboundaries = [0.5, 1, 2, 4, 6, 8, 10]
    rbins = ROOT.RooBinning(len(rboundaries) - 1, array.array('d', rboundaries),
                            'cache')
    phoScale.setBinning(sbins)
    phoRes.setBinning(rbins)

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
    mmgMassPhoGenE.SetTitle('threeBodyMass(mu1Pt, mu1Eta, mu1Phi, 0.106, '
                            '              mu2Pt, mu2Eta, mu2Phi, 0.106, '
                            '              phoGenE * phoPt / phoE, '
                            '                     phoEta, phoPhi, 0)')
    ## Create a preselected tree
    tree = zchain.CopyTree('&'.join(cuts))
    ## Have to copy aliases by hand
    for a in zchain.GetListOfAliases():
        tree.SetAlias(a.GetName(), a.GetTitle())

    ## Get the nominal dataset
    global data
    data = dataset.get(tree=tree, weight=weight, cuts=cuts,
                       variables=[mmgMass, mmMass, phoERes, mmgMassPhoGenE])

    ## Set units and nice titles
    for x, t, u in zip([mmgMass, mmgMassPhoGenE, mmMass, phoERes],
                       ['reconstructed m_{#mu#mu#gamma}',
                        'reconstructed m_{#mu#mu#gamma} with E_{gen}^{#gamma}',
                        'm_{#mu#mu}',
                        'E_{reco}^{#gamma}/E_{gen}^{#gamma} - 1', ],
                       'GeV GeV GeV %'.split()):
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
def plot_sanity_checks(data):
    pdfname = '_'.join(['bananaPdf', data.GetName()])
    pdf = ROOT.RooNDKeysPdf(pdfname, pdfname,
                            ROOT.RooArgList(mmMass, mmgMass), data, "a", 1.5)

    canvases.next(pdf.GetName() + '_mmgMassProj')
    plot = mmgMass.frame(roo.Range(60, 120))
    data.plotOn(plot)
    pdf.plotOn(plot)
    plot.Draw()

    canvases.next(pdf.GetName() + '_mmMassProj')
    plot = mmMass.frame(roo.Range(10, 120))
    data.plotOn(plot)
    pdf.plotOn(plot)
    plot.Draw()

    canvases.next(pdf.GetName()).SetGrid()
    h_pdf = pdf.createHistogram('h_' + pdf.GetName(), mmMass,
                                roo.Binning(40, 40, 80),
                                roo.YVar(mmgMass, roo.Binning(40, 70, 110)))
    h_pdf.Draw("cont1")

    canvases.next(data.GetName()).SetGrid()
    h_data = data.createHistogram(mmMass, mmgMass, 130, 100, '',
                                  'h_' + data.GetName())
    h_data.GetXaxis().SetRangeUser(40, 80)
    h_data.GetYaxis().SetRangeUser(70, 110)
    h_data.Draw("cont1")

    canvases.next('_'.join([pdf.GetName(), 'mmgMassSlices']))
    plot = mmgMass.frame(roo.Range(60, 120))
    for mmmassval, color in zip([55, 60, 65, 70],
                                'Red Orange Green Blue'.split()):
        mmMass.setVal(mmmassval)
        color = getattr(ROOT, 'k' + color)
        pdf.plotOn(plot, roo.LineColor(color))

    plot.Draw()
    canvases.update()
## End of plot_sanity_checks().

##------------------------------------------------------------------------------
def test_substituting_for_mmgMassPhoGenE():
    pdfname = '_'.join(['pdf_mmMass_mmgMassPhoGenE', data.GetName()])
    pdf_mmMass_mmgMassPhoGenE = ROOT.RooNDKeysPdf(
        pdfname, pdfname, ROOT.RooArgList(mmMass, mmgMassPhoGenE), data, "a",
        1.5
        )
    ## Test substituting for mmgMassPhoGenE
    ## This formula is approximate for s = phoERes << 1
    ## 1/(1+s) - 1 ~ -s
    ## chachebins = ROOT.RooUniformBinning(-10, 10, 2, 'cache')
    ## phoERes.setBinning(chachebins)
    phoERes.setBins(3, 'cache')
    
    mmgMassFunc = w.factory('''expr::mmgMassFunc(
        "sqrt(mmgMass^2 - 0.01 * phoERes * (mmgMass^2 - mmMass^2))",
        {mmMass, mmgMass, phoERes}
            )'''
        )
    ## mmgMassFunc = w.factory('''cexpr::mmgMassFunc(
    ##     "sqrt(mmgMass*mmgMass - 0.01 * phoERes * (mmgMass*mmgMass - mmMass*mmMass))",
    ##     {mmMass, mmgMass, phoERes}
    ##         )'''
    ##     )

    cust = ROOT.RooCustomizer(pdf_mmMass_mmgMassPhoGenE, 'subs')
    cust.replaceArg(mmgMassPhoGenE, mmgMassFunc)
    pdf_mmMass_mmgMass = cust.build()
    pdf_mmMass_mmgMass.addOwnedComponents(ROOT.RooArgSet(mmgMassFunc))
    pdf_mmMass_mmgMass.SetName('pdf_mmMass_mmgMass')

    ## WARNING: The caching related lines below cause segmentation violation!
    ## pdf_mmMass_mmgMass.setNormValueCaching(2)

    ## print '-- Before chache --'
    ## w.Print()

    ## print '-- Calculating cache ... --'
    ## ## Trigger the cache calculation
    ## pdf_mmMass_mmgMass.getVal(ROOT.RooArgSet(mmMass, mmgMass))
    
    ## print '-- After chache --'
    ## w.Print()
    
    pdf = pdf_mmMass_mmgMassPhoGenE
    canvases.next(pdf.GetName()).SetGrid()
    h_pdf = pdf.createHistogram('h_' + pdf.GetName(),
                                mmMass,
                                roo.Binning(40, 40, 80),
                                roo.YVar(mmgMassPhoGenE,
                                         roo.Binning(40, 70, 110)))
    h_pdf.Draw("cont1")

    pdf = pdf_mmMass_mmgMass
    phoERes.setVal(0)
    canvases.next(pdf.GetName() + '_s0').SetGrid()
    h_pdf = pdf.createHistogram('h_' + pdf.GetName() + '_s0',
                                mmMass,
                                roo.Binning(40, 40, 80),
                                roo.YVar(mmgMass, roo.Binning(40, 70, 110)))
    h_pdf.Draw("cont1")

    phoERes.setVal(10)
    canvases.next(pdf.GetName() + '_s10').SetGrid()
    h_pdf = pdf.createHistogram('h_' + pdf.GetName() + '_s10',
                                mmMass,
                                roo.Binning(40, 40, 80),
                                roo.YVar(mmgMass, roo.Binning(40, 70, 110)))
    h_pdf.Draw("cont1")

    phoERes.setVal(-10)
    canvases.next(pdf.GetName() + '_sm10').SetGrid()
    h_pdf = pdf.createHistogram('h_' + pdf.GetName() + '_sm10',
                                mmMass,
                                roo.Binning(40, 40, 80),
                                roo.YVar(mmgMass, roo.Binning(40, 70, 110)))
    h_pdf.Draw("cont1")
## End of test_substituting_for_mmgMassPhoGenE().

##------------------------------------------------------------------------------
def main():
    sw = ROOT.TStopwatch()
    sw.Start()

    init()
    get_data()

    ## plot_sanity_checks(data)

    ## sdata = calibrator.get_smeared_data(-10, 1.5)
    ## sdata.SetName('sdata_sm10_r1p5')
    ## plot_sanity_checks(sdata)

    ## sdata = calibrator.get_smeared_data(10, 1.5)
    ## sdata.SetName('sdata_s10_r1p5')
    ## plot_sanity_checks(sdata)
    
    test_substituting_for_mmgMassPhoGenE()

    canvases.update()
    sw.Stop()
    print 'CPU time:', sw.CpuTime(), 's, real time:', sw.RealTime(), 's'
## End of main()    


##------------------------------------------------------------------------------
## sw = ROOT.TStopwatch()
## sw.Start()

## init()
## get_data()

## pdfname = '_'.join(['pdf_mmMass_mmgMassPhoGenE', data.GetName()])
## pdf_mmMass_mmgMassPhoGenE = ROOT.RooNDKeysPdf(
##     pdfname, pdfname, ROOT.RooArgList(mmMass, mmgMassPhoGenE), data, "a",
##     1.5
##     )
## ## Test substituting for mmgMassPhoGenE
## ## This formula is approximate for s = phoERes << 1
## ## 1/(1+s) - 1 ~ -s
## mmgMassFunc = w.factory('''expr::mmgMassFunc(
##     "sqrt(mmgMass^2 - 0.01 * phoERes * (mmgMass^2 - mmMass^2))",
##     {mmMass, mmgMass, phoERes}
##         )'''
##     )

## cust = ROOT.RooCustomizer(pdf_mmMass_mmgMassPhoGenE, 'subs')
## cust.replaceArg(mmgMassPhoGenE, mmgMassFunc)
## pdf_mmMass_mmgMass = cust.build()
## pdf_mmMass_mmgMass.SetName('pdf_mmMass_mmgMass')

## pdf_phoERes = ParametrizedKeysPdf('pdf_phoERes', 'pdf_phoERes', phoERes,
##                                   phoScale, phoRes, data,
##                                   ROOT.RooKeysPdf.NoMirror, 1.5)
## # w.Import(pdf_phoERes)

## pdf_mmMass_mmgMass_phoERes = ROOT.RooProdPdf(
##     'pdf_mmMass_mmgMass_phoERes', 'pdf_mmMass_mmgMass_phoERes',
##     ROOT.RooArgSet(pdf_phoERes),
##     roo.Conditional(ROOT.RooArgSet(pdf_mmMass_mmgMass),
##                     ROOT.RooArgSet(mmMass, mmgMass))
##     )

## ## Integrate out the photon resolution function.
## pdf_banana = pdf_mmMass_mmgMass_phoERes.createProjection(
##     ROOT.RooArgSet(phoERes)
##     )

## w.Import(pdf_banana, roo.RecycleConflictNodes())

## w.Print()

## canvases.next(pdf_mmMass_mmgMassPhoGenE.GetName() + '_mmgMassPhoGenEProj')
## plot = mmgMassPhoGenE.frame(roo.Range(60, 120))
## data.plotOn(plot)
## pdf_mmMass_mmgMassPhoGenE.plotOn(plot)
## plot.Draw()
## canvases.update()

## canvases.next(pdf_banana.GetName() + '_mmgMassProj')
## plot = mmgMass.frame(roo.Range(60, 120))
## data.plotOn(plot)
## pdf_banana.plotOn(plot)
## plot.Draw()

## sw = ROOT.TStopwatch()
## sw.Start()
 

if __name__ == '__main__':
    main()
    import user
