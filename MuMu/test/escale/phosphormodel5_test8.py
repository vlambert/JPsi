'''
Photon Energy Scale (PhoES) and Photon Energy Resolution (PHOSPHOR) Fit model 5.

Test the use custom RooFit PDF class to speed up the calculation of the numerical
integration.  The normalization integral is calculated for 

Jan Veverka, Caltech, 8 February 2012.
'''

import ROOT
import JPsi.MuMu.common.roofit as roo
import FWLite.Tools.canvases as canvases
import FWLite.Tools.cmsstyle as cmsstyle
from FWLite.Tools.latex import Latex
ROOT.gSystem.Load('libJPsiMuMu')

# name = 'EB_pt12to15'
# name = 'EB_pt15to20'
# name = 'EE_pt12to15'
name = 'EE_pt15to20'

times = []

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
def check_timer(label = ''):
    sw.Stop()
    ct, rt = sw.CpuTime(), sw.RealTime()
    print '+++', label, 'CPU time:', ct, 's, real time: %.2f' % rt, 's'
    sw.Reset()
    sw.Start()
    times.append((label, ct, rt))
    return ct, rt
## End of check_timer()

ROOT.RooAbsReal.defaultIntegratorConfig().setEpsRel(1e-8)
ROOT.RooAbsReal.defaultIntegratorConfig().setEpsAbs(1e-8)

## Read the model from a file
ifilename = 'phosphor5_model_and_fit_%s.root' % name
ifile = ROOT.TFile.Open(ifilename)
w = ifile.Get('w')
# model = w.pdf(name + '_pm5')
signal = w.pdf(name + '_signal_model')
zj_pdf = w.pdf(name + '_zj_pdf')
## TODO: build model = S+B, fit it to S only and S+B and compare with previous.
signal2 = ROOT.RooHistPdf(signal, 'signal2')
mass = w.var('mmgMass')
phos = w.var('phoScale')
phor = w.var('phoRes')
dhist = w.data(signal.GetName() + '_phor_dhist')
msubs = w.function(signal.GetName() + '_msubs_4')


nset = ROOT.RooArgSet(mass)
mass.setRange(60, 120)
print 'signal norm:', signal.getNorm(nset)
print 'signal2 norm:', signal2.getNorm(nset)

range_name = ROOT.TNamed('fit', 'fit')
## norm = signal.getNormObj(ROOT.RooArgSet(mass), ROOT.RooArgSet(), range_name)
## norm2 = signal2.getNormObj(ROOT.RooArgSet(mass), ROOT.RooArgSet(), range_name)
norm = signal.createIntegral(ROOT.RooArgSet(mass), 'fit')
norm2 = signal2.createIntegral(ROOT.RooArgSet(mass), 'fit')

sw = ROOT.TStopwatch()

fitres = w.obj(name + '_fitres3_hesse')

phosbins = ROOT.RooBinning(20, -20, 20, 'normcache')
phorbins = ROOT.RooBinning(20, 0., 25, 'normcache')
phos.setBinning(phosbins, 'normcache')
phor.setBinning(phorbins, 'normcache')

print '+++ Calculating norm cache ...'
sw.Start()
nh2f = norm2.createHistogram('nh2f', phos, roo.Binning('normcache'), 
                             roo.YVar(phor, roo.Binning('normcache')),
                             roo.Scaling(False))
check_timer('Norm cache ...')
nhist = ROOT.RooDataHist('nhist', 'nhist', ROOT.RooArgList(phos, phor), nh2f)
nfunc = ROOT.RooHistFunc('nfunc', 'nfunc', ROOT.RooArgSet(phos, phor), nhist, 2)

print '+++ Creating RooPhosphorPdf ...'
signal3 = ROOT.RooPhosphorPdf('signal3', 'signal3', mass, msubs, phos, phor,
                              dhist, 2)
norm3 = signal3.createIntegral(ROOT.RooArgSet(mass), 'fit')
check_timer('RooPhosphorPdf ctor and normaliztion integral')
signal3.getVal(ROOT.RooArgSet(mass))
nfunc3 = signal3.getNormCache()['signal3_Int[mmgMass|(60,120)]']

data = w.data('data')
zj_mc = w.data(name + '_zj_mc')
fitdata = data.reduce(ROOT.RooArgSet(mass))
fitdata.append(zj_mc.reduce(ROOT.RooArgSet(mass)))
nll = signal3.createNLL(fitdata, roo.Range('fit'),
                        roo.NumCPU(8),
                        ## roo.SumW2Error(True),
    )

signalf = w.var(name + '_signal_f')
model3 = ROOT.RooAddPdf('model3', 'model3', signal3, zj_pdf, signalf)

##------------------------------------------------------------------------------
plot = mass.frame(roo.Range(75, 105))
phor.setVal(fitres.floatParsFinal().find(phor.GetName()).getVal())
for x, color in zip([-10, -5, 0, 10, 20],
                    'Red Orange Green Blue Black'.split()):
    phos.setVal(x)
    kcolor = getattr(ROOT, 'k' + color)
    signal.plotOn(plot, roo.LineColor(kcolor))
canvases.next('scan_phos').SetGrid()
plot.Draw()

##------------------------------------------------------------------------------
plot = mass.frame(roo.Range(75, 105))
phos.setVal(fitres.floatParsFinal().find(phos.GetName()).getVal())
for x, color in zip([0, 2, 5, 10, 15], 'Red Orange Green Blue Black'.split()):
    phor.setVal(x)
    kcolor = getattr(ROOT, 'k' + color)
    signal.plotOn(plot, roo.LineColor(kcolor))

canvases.next('scan_phor').SetGrid()
plot.Draw()

##------------------------------------------------------------------------------
## Recover the values from the results of the fit.
phos.setVal(fitres.floatParsFinal().find(phos.GetName()).getVal())
phor.setVal(fitres.floatParsFinal().find(phor.GetName()).getVal())
plot = phos.frame(roo.Range(-5, 15))
print 'Calculating norm vs scale ...'
sw.Start()
# norm.plotOn(plot)
# norm2.plotOn(plot, roo.LineColor(ROOT.kRed), roo.LineStyle(ROOT.kDashed))
# norm3.plotOn(plot, roo.LineColor(ROOT.kGreen), roo.LineStyle(ROOT.kDotted))
check_timer('Norm vs scale')
nfunc.plotOn(plot, roo.LineColor(ROOT.kRed), roo.LineStyle(ROOT.kDashed))
nfunc3.plotOn(plot, roo.LineColor(ROOT.kBlack), roo.LineStyle(ROOT.kDotted))
canvases.next('norm_vs_scale').SetGrid()
plot.GetYaxis().SetRangeUser(0.99, 1.00)
plot.Draw()

##------------------------------------------------------------------------------
## Recover the values from the results of the fit.
phos.setVal(fitres.floatParsFinal().find(phos.GetName()).getVal())
phor.setVal(fitres.floatParsFinal().find(phor.GetName()).getVal())
plot = phor.frame(roo.Range(0.1, 20.1))
print 'Calculating norm vs res ...'
sw.Reset()
sw.Start()
# norm.plotOn(plot)
# norm2.plotOn(plot, roo.LineColor(ROOT.kRed), roo.LineStyle(ROOT.kDashed))
# norm3.plotOn(plot, roo.LineColor(ROOT.kGreen), roo.LineStyle(ROOT.kDotted))
check_timer('Norm vs res')
nfunc.plotOn(plot, roo.LineColor(ROOT.kRed), roo.LineStyle(ROOT.kDashed))
nfunc3.plotOn(plot, roo.LineColor(ROOT.kBlack), roo.LineStyle(ROOT.kDotted))
canvases.next('norm_vs_res').SetGrid()
plot.GetYaxis().SetRangeUser(0.99, 1.00)
plot.Draw()

canvases.update()

print 'Let us crash:', norm3.getVal()
check_timer('Norm cache calculation')

##------------------------------------------------------------------------------
## Fit the S+B Monte Carlo.
sw.Reset()
sw.Start()
phos.setVal(fitres.floatParsInit().find(phos.GetName()).getVal())
phor.setVal(fitres.floatParsInit().find(phor.GetName()).getVal())
fitres3 = model3.fitTo(fitdata, roo.Range('fit'), roo.Timer(), roo.NumCPU(8),
                       roo.SumW2Error(True), roo.Verbose(), roo.Minos())

mass.setRange('plot', 70, 110)
mass.setBins(80)
plot = mass.frame(roo.Range('plot'))
parse_name_to_title()
plot.SetTitle(latex_title)
fitdata.plotOn(plot)
model3.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'))
model3.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'),
              roo.Components('*zj*'), roo.LineStyle(ROOT.kDashed))     
canvases.next(name + '_fast_fit').SetGrid()
plot.Draw()
labels_titles = ['E^{#gamma} Scale', 'E^{#gamma} resolution', 'Signal purity']
val_with_errors = lambda x, s=1: (s*x.getVal(), s*x.getError(),
                                  s*x.getErrorHi(), s*x.getErrorLo())
labels_slow_fit, labels_fast_fit = [], []
for x, s in zip([phos, phor, signalf], [1, 1, 100]):
    labels_fast_fit.append(
        '  Fast Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f} %%' % val_with_errors(x, s)
        )
phos.setVal(fitres.floatParsFinal().find(phos.GetName()).getVal())
phor.setVal(fitres.floatParsFinal().find(phor.GetName()).getVal())
signalf.setVal(fitres.floatParsFinal().find(signalf.GetName()).getVal())
for x, s in zip([phos, phor, signalf], [1, 1, 100]):
    labels_slow_fit.append(
        '  Slow Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f} %%' % val_with_errors(x, s)
        )

latex_labels = []

for (t, s, f) in zip(labels_titles, labels_slow_fit, labels_fast_fit):
    latex_labels.extend([t, s, f, ''])
    
Latex(latex_labels, position=(0.2, 0.8)).draw()

##------------------------------------------------------------------------------
## Fit the S only Monte Carlo.
sw.Reset()
sw.Start()
phos.setVal(fitres.floatParsInit().find(phos.GetName()).getVal())
phor.setVal(fitres.floatParsInit().find(phor.GetName()).getVal())
fitres3 = model3.fitTo(data, roo.Range('fit'), roo.Timer(), roo.NumCPU(8),
                       roo.SumW2Error(True), roo.Verbose(), roo.Minos())

mass.setRange('plot', 70, 110)
mass.setBins(80)
plot = mass.frame(roo.Range('plot'))
parse_name_to_title()
plot.SetTitle(latex_title)
fitdata.plotOn(plot)
model3.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'))
model3.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'),
              roo.Components('*zj*'), roo.LineStyle(ROOT.kDashed))     
canvases.next(name + '_fast_fit').SetGrid()
plot.Draw()
labels_titles = ['E^{#gamma} Scale', 'E^{#gamma} resolution', 'Signal purity']
val_with_errors = lambda x, s=1: (s*x.getVal(), s*x.getError(),
                                  s*x.getErrorHi(), s*x.getErrorLo())
labels_slow_fit, labels_fast_fit = [], []
for x, s in zip([phos, phor, signalf], [1, 1, 100]):
    labels_fast_fit.append(
        '  Fast Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f} %%' % val_with_errors(x, s)
        )
phos.setVal(fitres.floatParsFinal().find(phos.GetName()).getVal())
phor.setVal(fitres.floatParsFinal().find(phor.GetName()).getVal())
signalf.setVal(fitres.floatParsFinal().find(signalf.GetName()).getVal())
for x, s in zip([phos, phor, signalf], [1, 1, 100]):
    labels_slow_fit.append(
        '  Slow Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f} %%' % val_with_errors(x, s)
        )

latex_labels = []

for (t, s, f) in zip(labels_titles, labels_slow_fit, labels_fast_fit):
    latex_labels.extend([t, s, f, ''])
    
Latex(latex_labels, position=(0.2, 0.8)).draw()

##------------------------------------------------------------------------------
plot = phos.frame(roo.Range(0,1))
nll.plotOn(plot, roo.ShiftToZero())
canvases.next('nll_vs_phos').SetGrid()
plot.Draw()
check_timer('Plotting NLL(phos).')


##------------------------------------------------------------------------------
plot = phor.frame(roo.Range(4,7))
nll.plotOn(plot, roo.ShiftToZero())
canvases.next('nll_vs_phor').SetGrid()
plot.Draw()
check_timer('Plotting NLL(phor)')

##------------------------------------------------------------------------------
for cname in 'phorhist mwidth_vs_phor fit fit_singal_only real_data'.split():
    w.obj('_'.join(['c', name, cname])).Draw()

canvases.update()

##------------------------------------------------------------------------------
if __name__ == '__main__':
    import user

