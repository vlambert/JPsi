'''
Phton Energy Scale and Photon Energy Resolution (PHOESPHOER) Fit model 1.
Strategy to build a 2D model for the mmMass and mmgMass as functions
of PhoES and PhoER.

Key formula:
mmgMass^2 = mmMass^2 + (mmgMassPhoEGen^2 - mmMass^2) * phoE/phoEGen (1)

Assumption:
phoE/phoEGen is uncorrelated with both mmMass and mmgMass

Strategy:
1. Build a 2D KEYS PDF of X = mmMass and
   T1 = log(mmgMassPhoEGen^2 - mmMass^2) fXT1(x, t1).

2. Build a 1D KEYS PDF of T2 = log(phoE/phoEGen) depending on
   s = phoScale and r = phoRes fT2(t2|s,r). Note that
   phoERes = 100 * (phoE/phoEGen - 1).
   Thus a substitution
   phoERes = 100 * (1 + exp(t2))
   in the phoEResPdf(phoERes|s,r) can be used.

3. Use FFT to convolve fXT1 and fT2 in T1 and T2 to get a 2D PDF
   of X and T = T1 + T2 fXT(x,t|s,r):
   fXT(x,t|s,r) = fXT1(x,t) * fT2(t|s,r)
   Note that X is an additional observable while s and t are parameters.
   It is important to cache the convolution in t *and* x for efficient
   likelihood calculation.

4. Substitute for T using the key formula T -> T3 = log(mmgMass^2 - mmMass^2)
   to obtain a density in X and Y = mmgMass fXY(x,y|s,r).
   fXY(x,y|s,r) = fXT(x,t3(x,y)|s,r).

Culprit:
T3 is only well defined for y > x.  Need to make the range of x depend on y.
Is this possible in RooFit?
This is solved by a identity function bound from above (texpbound).

Culprit 2:
t1 and t2 are correlated which introduces bias, especially in the resolution
which is undermeasured.
Possible solutions:
(a) make bins in photon E instead of Et.  This reduces the correlation and
(hopefully) the bias somewhat.
(b) Remove convolution and build the model fXY(x, y| s) that only dependce
on the photon Energy scale. Scan through a range of resolutions to fit
for it.

Culprit 3:
An overly simplified version 

Jan Veverka, Caltech, 18 January 2012.
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
from JPsi.MuMu.escale.logphoereskeyspdf import LogPhoeresKeysPdf
from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator

##-- Configuration -------------------------------------------------------------
## Selection
name = 'EB_highR9_pt20-25'
outputfile = 'out_phosphor1' + name + '_test.root'
cuts = ['mmMass + mmgMass < 190',
        'isFSR',
        'phoGenE > 0',
        #'60 < mmMass & mmMass < 70', 
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
    if '_e' in name:
        ## Split the name into tokens.
        for tok in name.split('_'):
            ## Get the token with the pt
            if 'e' == tok[0]:
                lo, hi = tok.replace('e', '').split('-')
                cuts.append('%s <= phoPt * cosh(phoEta)' % lo)
                cuts.append('phoPt * cosh(phoEta) < %s' % hi)
## End of parse_name_to_cuts().

##------------------------------------------------------------------------------
def init():
    'Initialize workspace and common variables and functions.'
    global plots
    plots = []
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
    global phoScale, phoRes, t
    phoScale = w.factory('phoScale[0,-50,50]')
    phoRes = w.factory('phoRes[1.5,0.01,50]')
    t = w.factory('t[7,1,20]')

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
                       ['m_{#mu#mu#gamma}',
                        'm_{#mu#mu#gamma} with E_{gen}^{#gamma}',
                        'm_{#mu^{+}#mu^{-}}',
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
def get_derived_data():
    ## Get x, t1 data
    global data
    global xt1data
    t1func = w.factory(
        '''expr::t1func("log(mmgMassPhoGenE^2 - mmMass^2)",
                        {mmgMassPhoGenE, mmMass})'''
        )
    t1func.SetName('t')
    data.addColumn(t1func)
    xt1data = data.reduce(ROOT.RooArgSet(mmMass, t))
    t1func.SetName('t1func')
    data = data.reduce(ROOT.RooArgSet(mmgMass, mmMass, phoERes, mmgMassPhoGenE))
    xmin = ROOT.Double(0)
    xmax = ROOT.Double(0)
    xt1data.getRange(mmMass, xmin, xmax, 0.05)
    global mmMass_range
    mmMass_range = (float(xmin), float(xmax))
    xt1data.getRange(t, xmin, xmax, 0.05)
    global t1range
    t1range = (float(xmin), float(xmax))

    ## Get t2 data
    global t2data
    t.setRange(-2, 2)
    t2func = w.factory(
        'expr::t2func("log(0.01 * phoERes + 1)", {phoERes})'
        )
    t2func.SetName('t')
    data.addColumn(t2func)
    t2func.SetName('t2func')
    t2data = data.reduce(ROOT.RooArgSet(t))
    data = data.reduce(ROOT.RooArgSet(mmgMass, mmMass, phoERes, mmgMassPhoGenE))
    t2data.getRange(t, xmin, xmax, 0.05)
    global t2range
    t2range = (float(xmin), float(xmax))

    ## Get x, t data
    global xtdata
    t.setRange(*t1range)
    tfunc = w.factory('''expr::tfunc("log(mmgMass^2 - mmMass^2)",
                                     {mmgMass, mmMass})''')
    tfunc.SetName('t')
    data.addColumn(tfunc)
    tfunc.SetName('tfunc')
    xtdata = data.reduce(ROOT.RooArgSet(mmMass, t))
    data = data.reduce(ROOT.RooArgSet(mmgMass, mmMass, phoERes, mmgMassPhoGenE))
## End of get_derived_data().

##------------------------------------------------------------------------------
def plot_xt1_proj_x():
    ## Plot fXT1(x, t1) projected on x axis
    canvases.next('xt1_proj_x')
    plot = mmMass.frame()
    xt1data.plotOn(plot)
    xt1pdf.plotOn(plot)
    plot.Draw()
    plots.append(plot)
## End of plot_xt1_proj_x().

##------------------------------------------------------------------------------
def plot_xt1_proj_t1():
    ## Plot fXT1(x, t1) projected on t1 axis
    canvases.next('xt1_proj_t1')
    t.setRange(*t1range)
    t.SetTitle('log(m_{#mu#mu#gamma,E_{gen}^{#gamma}}^{2} - m_{#mu#mu}^{2})')
    plot = t.frame()
    xt1data.plotOn(plot)
    xt1pdf.plotOn(plot)
    plot.Draw()
    plots.append(plot)
## End of plot_xt1_proj_t1().

##------------------------------------------------------------------------------
def plot_xt1():
    ## Plot fXT1(x, t1) with training data.
    c1 = canvases.next('xt1')
    c1.SetWindowSize(800, 400)
    c1.Divide(2,1)
    c1.cd(1).SetGrid()
    t.setRange(*t1range)
    t.SetTitle('log(m_{#mu#mu#gamma,E_{gen}^{#gamma}}^{2} - m_{#mu#mu}^{2})')
    hxt1d = xt1data.createHistogram(mmMass, t, 100, 100, '', 'hxt1')
    hxt1d.SetTitle('Data')
    hxt1d.GetXaxis().SetTitle(mmMass.GetTitle() + ' (GeV)')
    hxt1d.GetYaxis().SetTitle(t.GetTitle())
    hxt1d.GetXaxis().SetTitleOffset(1.3)
    hxt1d.GetXaxis().SetRangeUser(*mmMass_range)
    hxt1d.GetYaxis().SetRangeUser(*t1range)
    hxt1d.Draw('cont0')
    plots.append(hxt1d)

    c1.cd(2).SetGrid()
    hxt1f = xt1pdf.createHistogram('hxt1f', mmMass, roo.YVar(t))
    hxt1f.SetTitle('PDF')
    hxt1f.GetXaxis().SetTitleOffset(1.3)
    hxt1f.Draw("cont0")
    plots.append(hxt1f)
## End of plot_xt1().

##------------------------------------------------------------------------------
def plot_t2():
    ## Plot fT2(t2|s,r) fitted to training data.
    canvases.next('t2pdf').SetGrid()
    t.setRange(*t2range)
    t.setVal(0)
    t.SetTitle('log(E_{reco}^{#gamma}/E_{gen}^{#gamma})')
    phoScale.setVal(t2pdf.s0val)
    phoRes.setVal(t2pdf.r0val)
    t2pdf.fitTo(t2data, roo.Range(ROOT.TMath.Log(0.5), ROOT.TMath.Log(1.5)),
                roo.NumCPU(8), roo.SumW2Error(True))
    myrange = (math.log(1 + 0.01 * (t2pdf.s0val - 5*t2pdf.r0val)),
               math.log(1 + 0.01 * (t2pdf.s0val + 5*t2pdf.r0val)))
    plot = t.frame(roo.Range(*myrange))
    t2data.plotOn(plot)
    t2pdf.plotOn(plot)
    plot.Draw()
    Latex([
        's_{shape}: %.3f %%' % t2pdf.s0val,
        's_{fit}: %.3f #pm %.3f %%' % (phoScale.getVal(), phoScale.getError()),
        's_{fit} - s_{shape}: %.4f #pm %.4f %%' % (
            phoScale.getVal() - t2pdf.s0val,
            phoScale.getError()
            ),
        'r_{shape}: %.3f %%' % t2pdf.r0val,
        'r_{fit}: %.3f #pm %.3f %%' % (phoRes.getVal(), phoRes.getError()),
        'r_{fit}/r_{shape}: %.4f #pm %.4f' % (
            phoRes.getVal() / t2pdf.r0val,
            phoRes.getError() / t2pdf.r0val),
        ], position=(0.2, 0.75)).draw()
    plots.append(plot)
## End of plot_t2()

##------------------------------------------------------------------------------
def check_timer(label = ''):
    sw.Stop()
    print label, 'CPU time:', sw.CpuTime(), 's, real time:', sw.RealTime(), 's'
    sw.Reset()
    sw.Start()

##------------------------------------------------------------------------------
def plot_xy_proj_y():
    'Plot fXY(x,y|s,r) projected on mmgMass.'
    c1 = canvases.next('xy_proj_y').SetGrid()
    plot = mmgMass.frame(roo.Range(75, 105))
    # plot = mmgMass.frame()
    data.plotOn(plot)
    xypdf.plotOn(plot)
    plot.Draw()
## End of plot_xy_proj_y().

##------------------------------------------------------------------------------
def plot_xy_proj_x():
    'Plot fXY(x,y|s,r) projected on mmMass.'
    c1 = canvases.next('xy_proj_x').SetGrid()
    # plot = mmMass.frame(roo.Range(40, 90))
    plot = mmMass.frame()
    data.plotOn(plot)
    xypdf.plotOn(plot)
    plot.Draw()
## End of plot_xy_proj_x()

##------------------------------------------------------------------------------
def plot_xy():
    'Plot fXY(x,y|s,r) 2D plot with data.'
    c1 = canvases.next('xy')
    if c1:
        c1.SetWindowSize(800, 400)
        c1.Divide(2,1)
        c1.cd(1).SetGrid()
    hd = data.createHistogram(mmMass, mmgMass, 50, 50, '', 'hxyd')
    hd.SetTitle('Data')
    hd.GetXaxis().SetTitle(mmMass.GetTitle() + ' (GeV)')
    hd.GetYaxis().SetTitle(mmgMass.GetTitle() + ' (GeV)')
    # hd.GetXaxis().SetTitleOffset(1.3)
    hd.GetXaxis().SetRangeUser(40, 80)
    hd.GetYaxis().SetRangeUser(75, 105)
    hd.Draw('cont0')

    if c1:
        c1.cd(2).SetGrid()
    hf = xypdf.createHistogram('hxyf', mmMass, roo.Binning(100, 40, 80),
                               roo.YVar(mmgMass, roo.Binning(100, 75, 105)))
    hf.SetTitle('PDF')
    # hf.GetXaxis().SetTitleOffset(1.3)
    hf.Draw("cont0")
## End of plot_xy().

##------------------------------------------------------------------------------
def plot_xy_slice_y():    
    'Plot fXY(x,y|s,r) slice at mmMass = [55, 60, 65, 70, 75] GeV.'
    c1 = canvases.next('xy_slice_y').SetGrid()
    plot = mmgMass.frame()
    for mval, color in zip(
        [45, 50, 55, 60, 65, 70, 75, 80],
        'Red Yellow Orange Spring Green Magenta Blue Black'.split()
        ):
        mmMass.setVal(mval)
        xypdf.plotOn(plot, roo.LineColor(getattr(ROOT, 'k' + color)))

    plot.Draw()
## End of plot_xy_slice_y().

##------------------------------------------------------------------------------
def plot_xy_slice_x():
    'Plot fXY(x,y|s,r) slice at mmgMass values.'
    c1 = canvases.next('xy_slice_x').SetGrid()
    plot = mmMass.frame()
    for mval, color in zip(
        [70, 75, 80, 85, 90, 95, 100, 105],
        'Red Yellow Orange Spring Green Magenta Blue Black'.split()
        ):
        mmgMass.setVal(mval)
        xypdf.plotOn(plot, roo.LineColor(getattr(ROOT, 'k' + color)))

    plot.Draw()
## End of plot_xy_slice_x()

##------------------------------------------------------------------------------
def set_xbinning():
    ## ## This seems to be messing up the normalization.
    ## xbins = [51.5, 55.5, 58.5, 60.5, 62.5, 64.0, 65.5, 67.5, 70.0, 74.5]
    ## xbinning = ROOT.RooBinning(mmMass.getMin(), mmMass.getMax(), 'cache')
    ## for x in xbins:
    ##     xbinning.addBoundary(x)
    ## xbinning.Print()
    ## mmMass.setBinning(xbinning, 'cache')
    pass
## End of set_xbinning().
    
##------------------------------------------------------------------------------
def set_phores_caching():
    xbins = [0.5, 2]
    xbinning = ROOT.RooBinning(phoRes.getMin(), phoRes.getMax(), 'cache')
    for x in xbins:
        xbinning.addBoundary(x)
    xbinning.Print()
    phoRes.setBinning(xbinning, 'cache')
    cacheset = ROOT.RooArgSet(phoRes)
    cacheset.add(xypdf.cacheObservables())
    xypdf.setCacheObservables(cacheset)
## End of set_phores_caching().
    
##------------------------------------------------------------------------------
def build_models():
    ## Build the model fXT1(x, t1) for mmMass vs
    ## log(mmgMassPhoGenE^2 - mmMass^2)
    global xt1pdf
    t.setRange(*t1range)
    xt1pdf = ROOT.RooNDKeysPdf('xt1pdf', 'xt1pdf', ROOT.RooArgList(mmMass, t),
                               xt1data, "a", 1.)
    xt1pdf.setNormValueCaching(2)
    ## Trigger filling the normalization cache.
    xt1pdf.getVal(ROOT.RooArgSet(mmMass, t))

    ## Build the model fT2(t2|s,r) for log(Ereco/Egen) ft2(t2|r,s)
    global t2pdf
    t.setRange(*t2range)
    t.setVal(0)
    t2pdf = LogPhoeresKeysPdf('t2pdf', 't2pdf', phoERes, t, phoScale,
                              phoRes, data, rho=1.0)

    ## Build the model for fXY(x,y|s,r) = fXT1(t) * fT2(t|s,r), t = t(x,y)
    global eptbound, tcfunc, xypdf
    trange = (4, 10)
    buffrac = 0.2
    exptbound = w.factory(
        '''cexpr::exptbound(
            "({M}*{M} - {m}*{m} <= {exptmin}) * {exptmin} +
             ({exptmin} < {M}*{M} - {m}*{m}) * ({M}*{M} - {m}*{m})",
             {{{M}, {m}}})'''.format(
            ## exptmin = math.exp(t1range[0] + t2range[0]),
            exptmin = math.exp(trange[0] - buffrac * (trange[1] - trange[0])),
            m='mmMass', M='mmgMass'
            )
        )
    tcfunc = w.factory('''cexpr::tcfunc("log(exptbound)", {exptbound})''')
    t.setRange(*trange)
    mmMass.setRange(*mmMass_range)
    t.setBins(2000, "cache")
    mmMass.setBins(20, "cache")
    xypdf = ROOT.RooFFTConvPdf('xypdf', 'xypdf', tcfunc, t, xt1pdf, t2pdf)
    xypdf.setBufferFraction(0.2)
    xypdf.setCacheObservables(ROOT.RooArgSet(mmMass, t))
    xypdf.setNormValueCaching(2)
## End of build_models().

##------------------------------------------------------------------------------
sw = ROOT.TStopwatch()
sw.Start()

## (a) xt1pdf norm val chaching
## (b) cache=1000*40, rho=3, 296s
## (c) cache=100*10, rho=1.5, 2.2s
## (d) cache=100*20, rho=1.5, 36s
## (e) cache=100*50, rho=1.5, 74s 
## (f) cache=100*100, rho=1.5, 136s
## (g) cache=100*200, rho=1.5, 260s
## (h) cache=200*10, rho=1.5, 19.7s
## (i) cache=500*10, rho=1.5, 22.5s
## (j) cache=1000*10, rho=1.5, 24.7s
## (l) cache=2000*10, rho=1.5, 18.2s
## (m) cache=5000*10, rho=1.5, 183s
## (k) cache=10000*10, rho=1.5, 72.2s
## (n) cache=200*50, rho=1.5, 16.3s
## (o) cache=500*50, rho=1.5, 323s
## (p) cache=1000*50, rho=1.5, 334s
## (q) cache=2000*50, rho=1.5, 100s
## (r) cache=2000*100, rho=1.5, 198s
## (s) cache=2000*200, rho=1.5, 397s
## (t) cache=2000*50, rho=1.5, no 9., 89s
## (u) cache=2000*50, rho=1.5, no 9., 10., 77s 
## (v) cache=2000*50, rho=1.0/1.5, 80s
## (w) cache=2000*50, rho=1.0, 79s
## (x) cache=2000*50, rho=1.0, cexpr, 79s
## (y) cache=2000*20, rho=1.0, cexpr, 32s
## (z) cache=2000*10, rho=1.0, cexpr, 32s
## (A) cache=2000*10, rho=1.0, cexpr, xbinning, 28s
## (B) cache=2000*20, rho=1.0, cexpr, 33s + 3:59:03h (fit)
  ## NO.   NAME      VALUE            ERROR       STEP SIZE       VALUE   
  ##  1  phoRes       4.28004e-01   3.72722e-01   4.53126e-02  -1.38766e+00
  ##  2  phoScale    -9.24848e-01   3.37972e-01   3.85105e-05  -1.84980e-02
## (C) cache=2000*10, rho=1.0, cexpr, batch mode, 17s
## (D) cache=2000*20, rho=1.0, cexpr, batch mode, 32s
## (E) cache=2000, rho=1.0, cexpr, batch mode, 154s
## (F) cache=1000, rho=1.0, cexpr, batch mode, 630s

import socket
print 'Phosphor Model 1 running on', socket.gethostname()

## 1. real time (s): 0.0 s
init()
check_timer(1)

## 2. real time (s): 5.2 s
get_data()
check_timer(2)

## 3. real time (s): 0.1 s
get_derived_data()
check_timer(3)

## 4. real time (s): 20.4, 21.2 (a), 34.3 (b), 14.4 (v), 14.4 (w), 17.4 (x)
##                   16.8 (C)
build_models()
check_timer(4)

## ## 5. real time (s): 44.6, 44.2 (a)
## plot_xt1_proj_x()
## check_timer(5)

## ## 6. real time (s): 32.6, 32.6 (a)
## plot_xt1_proj_t1()
## check_timer(6)

## ## 7. real time (s): 6.1, 6.0(a)
## plot_xt1()
## check_timer(7)

## 8. real time (s): 0.4
plot_t2()
check_timer(8)

canvases.update()

## set_xbinning()
t.setRange(*t1range)
t.setVal(0.5 * (t1range[0] + t1range[1]))

sw2 = ROOT.TStopwatch()
sw2.Start()

## 9. real time (s): 74 (q), 52 (v), 21 (y)
plot_xy_proj_y()
check_timer(9)

## 10. real time (s): 13 (q), 73 (t), 5.5 (y)
plot_xy_proj_x()
check_timer(10)

## 11. real time (s): 13 (q), 75 (u), 5.5 (y)
plot_xy()
check_timer(11)

## 12. real time (s): 1 (q)
plot_xy_slice_y()
check_timer(12)

## 13. real time (s): 1 (q)
plot_xy_slice_x()
check_timer(13)

sw2.Stop()
print 'CPU time:', sw2.CpuTime(), 's, real time:', sw2.RealTime(), 's'
 
canvases.update()

## Plot fXT(t|s,r) fitted to data
## real time (h): 3:59:03

# data_small = data.reduce(roo.EventRange(0, data.numEntries()/10))
data_small = data.reduce(roo.EventRange(0, data.numEntries()))
data_small.Print()
xypdf.fitTo(data_small, roo.NumCPU(8), roo.Verbose(True), roo.Timer(True),
            roo.SumW2Error(True),
            #roo.Minos(ROOT.RooArgSet(phoRes))
            )
## xyfit.Print('v')
## w.Import(xyfit)

## Store interesting things in the workspace
if t.getBinning('cache'):
    binning = t.getBinning('cache')
else:
    binning = t.getBinning()

binning.SetName(t.GetName() + '_binning')
w.Import(binning, binning.GetName())
    
if mmMass.getBinning('cache'):         
    binning = mmMass.getBinning('cache')
else:
    binning = mmMass.getBinning()

binning.SetName(mmMass.GetName() + '_binning')
w.Import(binning, binning.GetName())
       
## canvases.next('tpdf').SetGrid()
## t.setRange(5, 10)
## t.SetTitle('log(m_{#mu#mu#gamma}^{2} - m_{#mu#mu}^{2})')
## xypdf.fitTo(tdata, roo.Range(5.5, 9.5))
## plot = t.frame(roo.Range(6, 9))
## tdata.plotOn(plot)
## tpdf.plotOn(plot)
## tpdf.paramOn(plot)
## plot.Draw()

## real time (s): 267.3, 296.5(b), 2.2(c)


canvases.update()

for c in canvases.canvases:
    if c:
        w.Import(c)

w.writeToFile(outputfile)

if __name__ == '__main__':
    # main()
    import user
