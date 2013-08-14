'''
Photon Energy Scale (PhoES) and Photon Energy Resolution (PHOSPHOR) Fit model 5.

Model Z+jets background with a parametrized KEYS pdf trained on MC.
Model other backgrounds with an exponential.

Jan Veverka, Caltech, 31 January 2012.
'''
   
##- Boilerplate imports --------------------------------------------------------
import math
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf
from JPsi.MuMu.common.parametrizedndkeyspdf import ParametrizedNDKeysPdf
from JPsi.MuMu.escale.logphoereskeyspdf import LogPhoeresKeysPdf
from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator
from JPsi.MuMu.escale.phosphormodel5 import PhosphorModel5

##-- Configuration -------------------------------------------------------------
## Selection
# name = 'EB_highR9_pt15to20'
name = 'EB_lowR9_pt12to15'

strain = 'nominal'
rtrain = 'nominal'

sfit = 'nominal'
rfit = 'nominal'

fit_data_fraction = 0.25
reduce_data = False

sw = ROOT.TStopwatch()
times = []

##------------------------------------------------------------------------------
def parse_name_to_cuts():
    'Parse the name and apply the relevant cuts.'
    global cuts
    cuts = ['mmMass + mmgMass < 190']
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
def parse_name_to_title():
    'Parse the name and translate it into a title.'
    global title
    global latex_labels
    global latex_title
    tokens = []
    latex_labels = []
    if 'EB' in name:
        tokens.append('Barrel')
        latex_labels.append('Barrel')
        if 'highR9' in name:
            tokens.append('R9 > 0.94')
            latex_labels.append('R_{9}^{#gamma} > 0.94')
        elif 'lowR9' in name:
            tokens.append('R9 < 0.94')
            latex_labels.append('R_{9}^{#gamma} < 0.94')
    elif 'EE' in name:
        tokens.append('Endcaps')
        latex_labels.append('Endcaps')
        if 'highR9' in name:
            tokens.append('R9 > 0.95')
            latex_labels.append('R_{9}^{#gamma} > 0.95')
        elif 'lowR9' in name:
            tokens.append('R9 < 0.95')
            latex_labels.append('R_{9}^{#gamma} < 0.95')

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
                tokens.append('pt %s-%s GeV' % (lo, hi))
                latex_labels.append(
                    'E_{T}^{#gamma} #in [%s, %s] GeV' % (lo, hi)
                    )
    title = ', '.join(tokens)
    latex_title = ', '.join(latex_labels)
## End of parse_name_to_title().

##------------------------------------------------------------------------------
def init():
    'Initialize workspace and common variables and functions.'
    global plots, outputfile
    plots = []
    parse_name_to_title()
    parse_name_to_cuts()
    outputfile = 'phosphor5_model_and_fit_' + name + '.root'
    
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
    global phoScale, phoRes, phoScaleTrue, phoResTrue
    phoScale = w.factory('phoScale[0,-50,50]')
    phoRes = w.factory('phoRes[3,0.1,20.1]')
    phoScaleTrue = w.factory('phoScaleTrue[0,-50,50]')
    phoResTrue = w.factory('phoResTrue[1.5,0.01,50]')

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

    global xfunc
    xfunc = w.factory('''FormulaVar::xfunc(
        "0.5 * (1 - mmMass^2 / mmgMass^2)",
        {mmMass, mmgMass}
        )''')

    global xmean
    xmean = w.factory('xmean[0.1, 0, 1]')

    global mmgMassPeak, mmgMassWidth
    mmgMassPeak = w.factory('mmgMassPeak[91.2, 0, 200]')
    mmgMassWidth = w.factory('mmgMassWidth[5, 0.1, 200]')
    
## End of init().


##------------------------------------------------------------------------------
def get_data(chains = getChains('v11')):
    'Get the nominal data that is used for smearing.'
    ## The TFormula expression defining the data is given in the titles.
    weight.SetTitle('pileup.weight')
    phoERes.SetTitle('100 * phoERes')
    mmgMassPhoGenE.SetTitle('threeBodyMass(mu1Pt, mu1Eta, mu1Phi, 0.106, '
                            '              mu2Pt, mu2Eta, mu2Phi, 0.106, '
                            '              phoGenE * phoPt / phoE, '
                            '                     phoEta, phoPhi, 0)')
    ## Create a preselected tree
    tree = {}
    tree['z'] = chains['z'].CopyTree('&'.join(cuts))
    # dtree = chains['data'].
    ## Have to copy aliases by hand
    for a in chains['z'].GetListOfAliases():
        tree['z'].SetAlias(a.GetName(), a.GetTitle())

    ## Get the nominal dataset
    global data
    data = {}
    data['fsr'] = dataset.get(tree=tree['z'], weight=weight,
                              cuts=cuts + ['isFSR'],
                              variables=[mmgMass, mmMass, phoERes,
                                         mmgMassPhoGenE])

    data['zj'] = dataset.get(tree=tree['z'], weight=weight,
                             cuts=cuts + ['!isFSR'],
                             variables=[mmgMass, mmMass])

    ## Set units and nice titles
    for x, t, u in zip([mmgMass, mmgMassPhoGenE, mmMass, phoERes, phoScale,
                        phoRes],
                       ['m_{#mu#mu#gamma}',
                        'm_{#mu#mu#gamma} with E_{gen}^{#gamma}',
                        'm_{#mu^{+}#mu^{-}}',
                        'E_{reco}^{#gamma}/E_{gen}^{#gamma} - 1',
                        'E^{#gamma} Scale', 'E^{#gamma} Resolution'],
                       'GeV GeV GeV % % %'.split()):
        x.SetTitle(t)
        x.setUnit(u)
    ##-- Get Smeared Data ------------------------------------------------------
    global calibrator
    calibrator = MonteCarloCalibrator(data['fsr'], 1)
## End of get_data.

##------------------------------------------------------------------------------
def get_confint(x, cl=5):
    if x.hasAsymError():
        if x.getErrorHi() <= 0.:
            ehi = x.getError()
        else:
            ehi = x.getErrorHi()
        if x.getErrorLo() >= 0.:
            elo = -x.getError()
        else:
            elo = x.getErrorLo()
        return (max(x.getVal() + cl * elo, x.getMin()),
                min(x.getVal() + cl * ehi, x.getMax()))
    else:
        return (max(x.getVal() - cl * x.getError(), x.getMin()),
                min(x.getVal() + cl * x.getError(), x.getMax()))
## End of get_confint().

##------------------------------------------------------------------------------
def check_timer(label = ''):
    sw.Stop()
    ct, rt = sw.CpuTime(), sw.RealTime()
    print '+++', label, 'CPU time:', ct, 's, real time: %.2f' % rt, 's'
    sw.Reset()
    sw.Start()
    times.append((label, ct, rt))
    return ct, rt
## End of check_timer()

##------------------------------------------------------------------------------
def outro():
    'Closing stuff'
    canvases.update()
    canvases.make_plots(['png', 'eps'])

    for c in canvases.canvases:
        if c:
            w.Import(c, 'c_' + c.GetName())
    w.writeToFile(outputfile)
## End of outro().

##------------------------------------------------------------------------------
def main():
    global data

    sw.Start()
    
    init()
    get_data()

    if reduce_data:
        reduced_entries = int((1 - fit_data_fraction) * data['fsr'].numEntries())
        data['fsr'] = data['fsr'].reduce(roo.EventRange(0, int(reduced_entries)))

    check_timer('1. init and get_data (%d entries)' % data['fsr'].numEntries())
    
    ## phor_reference_targets = ROOT.RooBinning

    mmgMass.setBins(1000, 'cache')
    phoRes.setBins(50, 'cache')
    # phoScale.setBins(40, 'cache')
    # phortargets =  [0.5 + 0.5 * i for i in range(16)]
    phortargets = [0.5, 1, 2, 3, 4, 5, 7, 10]
    # phortargets = [0.5, calibrator.r0.getVal(), 10]
    # phortargets.append(calibrator.r0.getVal())
    phortargets.sort()

    ROOT.RooAbsReal.defaultIntegratorConfig().setEpsAbs(1e-09)
    ROOT.RooAbsReal.defaultIntegratorConfig().setEpsRel(1e-09)

    ## Build the signal PDF
    global signal_model
    signal_model = PhosphorModel5(name + '_signal_model',
                                  name + '_signal_model',
                                  mmgMass, phoScale, phoRes,
                                  data['fsr'], w, 'nominal', phortargets,
                                  rho=2)
    w.Import(signal_model)

    ## Build the Z+jets background PDF.
    data['zj'].SetName(name + '_zj_mc')
    w.Import(data['zj'])

    global zj_pdf
    zj_pdf = ROOT.RooKeysPdf(name + '_zj_pdf', name + '_zj_pdf', mmgMass,
                             data['zj'], ROOT.RooKeysPdf.NoMirror, 1.5)
    w.Import(zj_pdf)
    
    ## Build the PDF for other backgrounds.
    global bkg_pdf
    bkg_pdf = w.factory(
        '''Exponential::{name}_bkg_pdf(mmgMass, {name}_bkg_c[-1,-10,10])
        '''.format(name=name)
        )

    ## Build the composite model PDF
    global pm
    pm = w.factory(
        ## '''SUM::{name}_pm5({name}_signal_N[1000,0,1e6] * {name}_signal_model,
        ##                    {name}_zj_N    [10,0,1e6]   * {name}_zj_pdf,
        ##                    {name}_bkg_N   [10,0,1e6]   * {name}_bkg_pdf)
        ## '''.format(name=name)
        '''SUM::{name}_pm5({name}_signal_N[1000,0,1e6] * {name}_signal_model,
                           {name}_zj_N[50,0,1e6] * {name}_zj_pdf)
        '''.format(name=name)
        )

    check_timer('2. PhosphorModel5 build')

    ## ROOT.RooAbsReal.defaultIntegratorConfig().setEpsAbs(1e-07)
    ## ROOT.RooAbsReal.defaultIntegratorConfig().setEpsRel(1e-07)

    global fitdata
    fitdata = calibrator.get_smeared_data(sfit, rfit, name + '_fitdata',
                                          name + '_fitdata', True)
    fitdata.reduce(ROOT.RooArgSet(mmgMass, mmMass))
    fitdata.append(data['zj'])
    fitdata.SetName(name + '_fitdata')
    data['fit'] = fitdata
    ## RooAdaptiveGaussKronrodIntegrater1D
    #mmgMass.setRange(40, 140)
    ## ROOT.RooAbsReal.defaultIntegratorConfig().method1D().setLabel(
    ##     "RooAdaptiveGaussKronrodIntegrator1D"
    ##     )

    ## msubs_lo = w.factory('EDIT::msubs_lo(pm5_msubs_0, mmgMass=mmgMassLo[40])')
    ## msubs_hi = w.factory('EDIT::msubs_hi(pm5_msubs_0, mmgMass=mmgMassHi[140])')
    # mmgMass.setRange('fit', msubs_lo, msubs_hi)
    mmgMass.setRange('fit', 60, 120)

    ## pm.setNormValueCaching(1)
    ## pm.getVal(ROOT.RooArgSet(mmgMass))
    ## rfitdata = fitdata.reduce('60 < mmgMass & mmgMass < 120')

    if reduce_data == True:
        fitdata = fitdata.reduce(roo.Range(reduced_entries,
                                           fitdata.numEntries()))
    check_timer('3. get fit data (%d entries)' % fitdata.numEntries())

    nll = pm.createNLL(fitdata, roo.Range('fit'))
    minuit = ROOT.RooMinuit(nll)
    minuit.setProfile()
    minuit.setVerbose()

    phoScale.setError(1)
    phoRes.setError(1)

    ## Initial HESSE
    status = minuit.hesse()
    fitres = minuit.save(name + '_fitres1_inithesse')
    w.Import(fitres, fitres.GetName())
    check_timer('4. initial hesse (status: %d)' % status)

    ## Minimization
    minuit.setStrategy(2)
    status = minuit.migrad()
    fitres = minuit.save(name + '_fitres2_migrad')
    w.Import(fitres, fitres.GetName())
    check_timer('5. migrad (status: %d)' % status)
    
    ## Parabolic errors
    status = minuit.hesse()
    fitres = minuit.save(name + '_fitres3_hesse')
    w.Import(fitres, fitres.GetName())
    check_timer('6. hesse (status: %d)' % status)
    
    ## Minos errors
    ## status = minuit.minos()
    ## fitres = minuit.save(name + '_fitres4_minos')
    ## w.Import(fitres, fitres.GetName())
    ## check_timer('7. minos (status: %d)' % status)
   
    ## fres = pm.fitTo(fitdata,
    ##                 roo.Range('fit'),
    ##                 roo.Strategy(2),
    ##                 roo.InitialHesse(True),
    ##                 roo.Minos(),
    ##                 roo.Verbose(True),
    ##                 roo.NumCPU(8), roo.Save(), roo.Timer())

    signal_model._phorhist.GetXaxis().SetRangeUser(75, 105)
    signal_model._phorhist.GetYaxis().SetRangeUser(0, 10)
    signal_model._phorhist.GetXaxis().SetTitle('%s (%s)' % (mmgMass.GetTitle(),
                                                  mmgMass.getUnit()))
    signal_model._phorhist.GetYaxis().SetTitle('E^{#gamma} Resolution (%)')
    signal_model._phorhist.GetZaxis().SetTitle('Probability Density (1/GeV/%)')
    signal_model._phorhist.SetTitle(latex_title)
    signal_model._phorhist.GetXaxis().SetTitleOffset(1.5)
    signal_model._phorhist.GetYaxis().SetTitleOffset(1.5)
    signal_model._phorhist.GetZaxis().SetTitleOffset(1.5)
    signal_model._phorhist.SetStats(False)
    canvases.next(name + '_phorhist')
    signal_model._phorhist.Draw('surf1')

    global graph
    graph = signal_model.make_mctrue_graph()
    graph.GetXaxis().SetTitle('E^{#gamma} resolution (%)')
    graph.GetYaxis().SetTitle('m_{#mu^{+}#mu^{-}#gamma} effective #sigma (GeV)')
    graph.SetTitle(latex_title)
    canvases.next(name + '_mwidth_vs_phor')
    graph.Draw('ap')

    mmgMass.setRange('plot', 70, 110)
    mmgMass.setBins(80)
    plot = mmgMass.frame(roo.Range('plot'))
    plot.SetTitle(latex_title)
    fitdata.plotOn(plot)
    pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'))
    pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'),
              roo.Components('*zj*'), roo.LineStyle(ROOT.kDashed))     
    canvases.next(name + '_fit')
    plot.Draw()
    Latex([
        'E^{#gamma} Scale',
        '  MC Truth: %.2f #pm %.2f %%' % (calibrator.s.getVal(),
                                          calibrator.s.getError()),
        '  #mu#mu#gamma Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f} %%' % (
            phoScale.getVal(), phoScale.getError(), phoScale.getErrorHi(),
            phoScale.getErrorLo()
            ),
        '',
        'E^{#gamma} resolution',
        '  MC Truth: %.2f #pm %.2f %%' % (calibrator.r.getVal(),
                                          calibrator.r.getError()),
        '  #mu#mu#gamma Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f} %%' % (
            phoRes.getVal(), phoRes.getError(), phoRes.getErrorHi(),
            phoRes.getErrorLo()
            ),
        '',
        'N_{S} (events)',
        '  MC Truth: %.0f' % fitdata.sumEntries(),
        '  #mu#mu#gamma Fit: %.0f #pm %.0f' % (
            w.var(name + '_signal_N').getVal(),
            w.var(name + '_signal_N').getError()
            )
        ],
        position=(0.2, 0.8)
        ).draw()

    check_timer('8. fast plots')

    pm.fitTo(data['fsr'], roo.Verbose(), roo.Save(), roo.SumW2Error(True),
             roo.Range(60, 120), roo.NumCPU(8))
    mmgMass.setRange('plot', 70, 110)
    mmgMass.setBins(80)
    plot = mmgMass.frame(roo.Range('plot'))
    plot.SetTitle(latex_title)
    fitdata.plotOn(plot)
    pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'))
    pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'),
              roo.Components('*zj*'), roo.LineStyle(ROOT.kDashed))
    canvases.next(name + '_fit_singal_only')
    plot.Draw()
    Latex(
        [
            'E^{#gamma} Scale',
            '  MC Truth: %.2f #pm %.2f %%' % (calibrator.s.getVal(),
                                            calibrator.s.getError()),
            '  #mu#mu#gamma Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f} %%' % (
                phoScale.getVal(), phoScale.getError(), phoScale.getErrorHi(),
                phoScale.getErrorLo()
                ),
            '',
            'E^{#gamma} resolution',
            '  MC Truth: %.2f #pm %.2f %%' % (calibrator.r.getVal(),
                                            calibrator.r.getError()),
            '  #mu#mu#gamma Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f} %%' % (
                phoRes.getVal(), phoRes.getError(), phoRes.getErrorHi(),
                phoRes.getErrorLo()
                ),
            '',
            ## 'N_{S} (events)',
            ## '  MC Truth: %.0f' % fitdata.sumEntries(),
            ## '  #mu#mu#gamma Fit: %.0f #pm %.0f' % (
            ##     w.var(name + '_signal_f').getVal() * fitdata.sumEntries(),
            ##     w.var(name + '_signal_f').getError() * fitdata.sumEntries()
            ##     )
            'N_{S} (events)',
            '  MC Truth: %.1f' % fitdata.sumEntries(),
            '  #mu#mu#gamma Fit: %.1f #pm %.1f' % (
                w.var(name + '_signal_N').getVal(),
                w.var(name + '_signal_N').getError()
                )
            ],
        position=(0.2, 0.8)
        ).draw()

    ## canvases.next(name + '_nll_vs_phos').SetGrid()
    ## plot = pm.w.var('phoScale').frame(roo.Range(*get_confint(phoScale)))
    ## plot.SetTitle(latex_title)
    ## nll.plotOn(plot, roo.ShiftToZero())
    ## # plot.GetYaxis().SetRangeUser(0, 10)
    ## plot.Draw()
    ## check_timer('9. nll vs phos')

    ## canvases.next(name + 'norm')
    ## norm = pm.getNormObj(ROOT.RooArgSet(), ROOT.RooArgSet(mmgMass))
    ## plot = phoScale.frame(roo.Range(*get_confint(phoScale)))
    ## norm.plotOn(plot)
    ## plot.GetYaxis().SetRangeUser(0.9995, 1.0005)
    ## plot.Draw()
    ## check_timer('10. norm vs phos')

    ## canvases.next(name + '_nll_vs_phor').SetGrid()
    ## plot = pm.w.var('phoRes').frame(roo.Range(*get_confint(phoRes)))
    ## nll.plotOn(plot, roo.ShiftToZero())
    ## # plot.GetYaxis().SetRangeUser(0, 10)
    ## plot.Draw()

    ## canvases.next(name + '_nll_vs_phor_zoom').SetGrid()
    ## plot = pm.w.var('phoRes').frame(roo.Range(*get_confint(phoRes,1.5)))
    ## nll.plotOn(plot, roo.ShiftToZero())
    ## # plot.GetYaxis().SetRangeUser(0, 10)
    ## plot.Draw()
    ## check_timer('11. nll vs phor')

    ## canvases.next(name + '_nll2d').SetGrid()
    ## h2nll = nll.createHistogram(
    ##     'h2nll', phoScale, roo.Binning(40, *get_confint(phoScale, 2)),
    ##     roo.YVar(phoRes, roo.Binning(40, *get_confint(phoRes, 2)))
    ##     )
    ## h2nll.SetStats(False)
    ## h2nll.Draw('colz')
    ## check_timer('12. 2d nll')

    ## Get real data
    dchain = getChains('v12')['data']
    weight.SetTitle('1')
    mmgMass.SetTitle('mmgMass')
    mmMass.SetTitle('mmMass')
    dataset.variables = []
    dataset.cuts = []
    data['real'] = dataset.get(tree=dchain, cuts=cuts[:],
                               variables=[mmgMass, mmMass],
                               weight=weight)
    mmgMass.SetTitle('m_{#mu#mu#gamma}')

    ## Fit it!
    fres_realdata = pm.fitTo(data['real'], roo.Range(60, 120),
                             roo.NumCPU(8), roo.Save(), roo.Timer(),
                             roo.Verbose())

    ## Make a plot
    plot = mmgMass.frame(roo.Range('plot'))
    data['real'].plotOn(plot)
    pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'))
    pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'),
              roo.Components('*zj*'), roo.LineStyle(ROOT.kDashed))
    pm.paramOn(plot)
    canvases.next(name + '_real_data')
    plot.Draw()

    outro()
    check_timer('13. outro')
    
## End of main().

##------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
    import user

