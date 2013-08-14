'''
Plot the results of the stre fit range systematics.
    Usage: python -i <filename>
'''

import JPsi.MuMu.common.canvases as canvases
from JPsi.MuMu.escale.fitResultPlotter import FitResultPlotter
from JPsi.MuMu.common.binedges import BinEdges
from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *
from JPsi.MuMu.escale.lyondata import data_2011_09_23_confID155805 as lyon
from JPsi.MuMu.scaleFitter import subdet_r9_categories

gStyle.SetPadTopMargin(0.1)
canvases.wwidth = 400
canvases.wheight = 400
canvases.yperiod = 10

path = '/Users/veverka/Work/CMSSW_4_2_3_FWLITE/src/JPsi/MuMu/test/escale/11-11-09'
path = '/Users/veverka/Work/Talks/11-11-09'

plotters = []
hists = []
graphs = []

## Configuration for plots vs Pt
binedges = list(BinEdges([10, 12, 15, 20, 25, 30, 100]))
bincenters = [0.5*(lo + hi)
              for lo, hi in BinEdges([10, 12, 15, 20, 25, 30, 50])]
binhalfwidths = [0.5*(hi - lo)
                 for lo, hi in BinEdges([10, 12, 15, 20, 25, 30, 50])]
n = len(binedges)

cats = list(subdet_r9_categories)

def var_vs_pt(name):
    """Returns functions that take a workspaces ws and return
    x, y, ex, ey where y and ey correspond to workspace
    variable of a given name and x and ex are pt bins."""
    return (
        lambda ws, i = iter(bincenters): i.next(),    # x
        lambda ws: ws.var(name).getVal(),             # y
        lambda ws, i = iter(binhalfwidths): i.next(), # ex
        lambda ws: ws.var(name).getError(),           # ey
    )

categories = [c.name for c in cats]

workspaces = ['ws1'] * n
snapshot = 'sFit_strue_mc_Nominal{f}_mmMass80_{c}_PhoEt{l}-{h}_bifurGauss'
plotter = FitResultPlotter(None, None)
for etar9 in cats:
    frp = FitResultPlotter(
        sources = 'dummy',
        getters = var_vs_pt('#Deltas'),
        xtitle = 'E_{T}^{#gamma} (GeV)',
        ytitle = 's_{gen} = E^{#gamma}_{reco}/E^{#gamma}_{gen} - 1 (%)',
        )
    for fitrange, title in zip(['FitRange' + x for x in '65 68 71'.split()],
                               '-3% Nominal +3%'.split()):
        filenames = [os.path.join(path, 'strue_%s.root' % fitrange)] * n
        snapshots = [snapshot.format(f=fitrange, c=etar9.name, l=lo, h=hi)
                     for lo, hi in binedges]
        frp.sources = zip(filenames, workspaces, snapshots)
        frp.getters = var_vs_pt('#Deltas')
        frp.title = title
        frp.getdata()
        frp.makegraph()

    canvases.next('strue_FitRangeSystematics' + etar9.name)
    frp.plotall(title=etar9.title)
    plotters.append(frp)

    graph = frp.graphs[0].Clone('g_' + etar9.name)
    for i in range(graph.GetN()):
        x = graph.GetX()[i]
        ylo = min([g.GetY()[i] for g in frp.graphs])
        yhi = max([g.GetY()[i] for g in frp.graphs])
        graph.SetPoint(i, x, 0.5 * (yhi - ylo))
        graph.SetPointError(i, graph.GetEX()[i], 0)

    plotter.graphs.append(graph)
    plotter.titles.append(etar9.title)

canvases.next('strue_FitRangeSystematics')
plotter.xtitle = 'E_{T}^{#gamma} (GeV)'
plotter.ytitle = 'Uncertainty on True Scale (%)' 
plotter.plotall(title = 'Fit Range Systematics')
plotters.append(plotter)


################################################################################
## Plot the p-values for 68% range (BASELINE)
name = 'FitRange68'
title = 'Baseline Fit Range'
filenames = [os.path.join(path, 'strue_%s.root' % name)] * n
workspaces = ['ws1'] * n
snapshot = 'chi2_strue_mc_Nominal%s_mmMass80_%s_PhoEt%d-%d_bifurGauss'

frp = FitResultPlotter(
    sources = zip(filenames, workspaces,
                  [snapshot % (name, 'EB_highR9', lo, hi)
                   for lo, hi in binedges]),
    getters =  var_vs_pt('chi2Prob'),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 'p-value',
    title = 'Barrel, R_{9}^{#gamma} < 0.94',
    )

for icat in cats:
    frp.sources = zip(filenames, workspaces,
                      [snapshot % (name, icat.name, lo, hi)
                       for lo, hi in binedges])
    frp.getters = var_vs_pt('chi2Prob')
    frp.title = ', '.join(icat.labels)
    frp.getdata()
    frp.makegraph()

canvases.next('strue_pvalues_vs_phoEt_%s' % name)
frp.plotall(title = title)
plotters.append(frp)

## Make the distribution of the p-values
hist = frp.histogramall(
    name = 'h_strue_pvalues_%s' % name,
    title = '%s;p-value;Fits' % title,
    nbins = 5, xlow = 0, xhigh = 1
    )
canvases.next('strue_pvalues_distro_%s' % name)
hist.Draw('e0')
hists.append(hist)
canvases.canvases[-1].Update()



################################################################################
## Plot the p-values for 71% range
name = 'FitRange71'
title = '+3% Fit Range'
filenames = [os.path.join(path, 'strue_%s.root' % name)] * n
workspaces = ['ws1'] * n
snapshot = 'chi2_strue_mc_Nominal%s_mmMass80_%s_PhoEt%d-%d_bifurGauss'

frp = FitResultPlotter(
    sources = zip(filenames, workspaces,
                  [snapshot % (name, 'EB_highR9', lo, hi)
                   for lo, hi in binedges]),
    getters =  var_vs_pt('chi2Prob'),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 'p-value',
    title = 'Barrel, R_{9}^{#gamma} < 0.94',
    )

for icat in cats:
    frp.sources = zip(filenames, workspaces,
                      [snapshot % (name, icat.name, lo, hi)
                       for lo, hi in binedges])
    frp.getters = var_vs_pt('chi2Prob')
    frp.title = ', '.join(icat.labels)
    frp.getdata()
    frp.makegraph()

canvases.next('strue_pvalues_vs_phoEt_%s' % name)
frp.plotall(title = title)
plotters.append(frp)

## Make the distribution of the p-values
hist = frp.histogramall(
    name = 'h_strue_pvalues_%s' % name,
    title = '%s;p-value;Fits' % title,
    nbins = 5, xlow = 0, xhigh = 1
    )
canvases.next('strue_pvalues_distro_%s' % name)
hist.Draw('e0')
hists.append(hist)
canvases.canvases[-1].Update()


################################################################################
## Plot the p-values for 73% range
name = 'FitRange73'
filenames = [os.path.join(path, 'strue_%s.root' % name)] * n
workspaces = ['ws1'] * n
snapshot = 'chi2_strue_mc_Nominal%s_mmMass80_%s_PhoEt%d-%d_bifurGauss'

frp = FitResultPlotter(
    sources = zip(filenames, workspaces,
                  [snapshot % (name, 'EB_highR9', lo, hi)
                   for lo, hi in binedges]),
    getters =  var_vs_pt('chi2Prob'),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 'p-value',
    title = 'Barrel, R_{9}^{#gamma} < 0.94',
    )

for icat in cats:
    frp.sources = zip(filenames, workspaces,
                      [snapshot % (name, icat.name, lo, hi)
                       for lo, hi in binedges])
    frp.getters = var_vs_pt('chi2Prob')
    frp.title = ', '.join(icat.labels)
    frp.getdata()
    frp.makegraph()

canvases.next('strue_pvalues_vs_phoEt_%s' % name)
frp.plotall(title = '+5% Fit Range Data Coverage')
plotters.append(frp)

## Make the distribution of the p-values
hist = frp.histogramall(
    name = 'h_strue_pvalues_%s' % name,
    title = '+5% Fit Range Coverage;p-value;Fits',
    nbins = 5, xlow = 0, xhigh = 1
    )
canvases.next('strue_pvalues_distro_%s' % name)
hist.Draw('e0')
hists.append(hist)
canvases.canvases[-1].Update()


################################################################################
## Plot the p-values for 65% range
name = 'FitRange65'
filenames = [os.path.join(path, 'strue_%s.root' % name)] * n
workspaces = ['ws1'] * n
snapshot = 'chi2_strue_mc_Nominal%s_mmMass80_%s_PhoEt%d-%d_bifurGauss'

frp = FitResultPlotter(
    sources = zip(filenames, workspaces,
                  [snapshot % (name, 'EB_highR9', lo, hi)
                   for lo, hi in binedges]),
    getters =  var_vs_pt('chi2Prob'),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 'p-value',
    title = 'Barrel, R_{9}^{#gamma} < 0.94',
    )

for icat in cats:
    frp.sources = zip(filenames, workspaces,
                      [snapshot % (name, icat.name, lo, hi)
                       for lo, hi in binedges])
    frp.getters = var_vs_pt('chi2Prob')
    frp.title = ', '.join(icat.labels)
    frp.getdata()
    frp.makegraph()

canvases.next('strue_pvalues_vs_phoEt_%s' % name)
frp.plotall(title = '-3% Fit Range Coverage')
plotters.append(frp)

## Make the distribution of the p-values
hist = frp.histogramall(
    name = 'h_strue_pvalues_%s' % name,
    title = '-3% Fit Range Coverage;p-value;Fits',
    nbins = 5, xlow = 0, xhigh = 1
    )
canvases.next('strue_pvalues_distro_%s' % name)
hist.Draw('e0')
hists.append(hist)
canvases.canvases[-1].Update()


################################################################################
## Plot the p-values for 100% range
name = 'FitRange100'
filenames = [os.path.join(path, 'strue_%s.root' % name)] * n
workspaces = ['ws1'] * n
snapshot = 'chi2_strue_mc_Nominal%s_mmMass80_%s_PhoEt%d-%d_bifurGauss'

frp = FitResultPlotter(
    sources = zip(filenames, workspaces,
                  [snapshot % (name, 'EB_highR9', lo, hi)
                   for lo, hi in binedges]),
    getters =  var_vs_pt('chi2Prob'),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 'p-value',
    title = 'Barrel, R_{9}^{#gamma} < 0.94',
    )

for icat in cats:
    frp.sources = zip(filenames, workspaces,
                      [snapshot % (name, icat.name, lo, hi)
                       for lo, hi in binedges])
    frp.getters = var_vs_pt('chi2Prob')
    frp.title = ', '.join(icat.labels)
    frp.getdata()
    frp.makegraph()

canvases.next('strue_pvalues_vs_phoEt_%s' % name).SetLogy()
frp.plotall(title = '100% Fit Range Coverage', logy = True)
plotters.append(frp)

## Make the distribution of the p-values
hist = frp.histogramall(
    name = 'h_strue_pvalues_%s' % name,
    title = '100% Fit Range Coverage;p-value;Fits',
    nbins = 5, xlow = 0, xhigh = 1
    )
canvases.next('strue_pvalues_distro_%s' % name)
hist.Draw('e0')
hists.append(hist)
canvases.canvases[-1].Update()


################################################################################
## Plot the p-values for 34% range
name = 'FitRange34'
filenames = [os.path.join(path, 'strue_%s.root' % name)] * n
workspaces = ['ws1'] * n
snapshot = 'chi2_strue_mc_Nominal%s_mmMass80_%s_PhoEt%d-%d_bifurGauss'

frp = FitResultPlotter(
    sources = zip(filenames, workspaces,
                  [snapshot % (name, 'EB_highR9', lo, hi)
                   for lo, hi in binedges]),
    getters =  var_vs_pt('chi2Prob'),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 'p-value',
    title = 'Barrel, R_{9}^{#gamma} < 0.94',
    )

for icat in cats:
    frp.sources = zip(filenames, workspaces,
                      [snapshot % (name, icat.name, lo, hi)
                       for lo, hi in binedges])
    frp.getters = var_vs_pt('chi2Prob')
    frp.title = ', '.join(icat.labels)
    frp.getdata()
    frp.makegraph()

canvases.next('strue_pvalues_vs_phoEt_%s' % name)
frp.plotall(title = '-34% Fit Range Coverage')
plotters.append(frp)

## Make the distribution of the p-values
hist = frp.histogramall(
    name = 'h_strue_pvalues_%s' % name,
    title = '-34% Fit Range Coverage;p-value;Fits',
    nbins = 5, xlow = 0, xhigh = 1
    )
canvases.next('strue_pvalues_distro_%s' % name)
hist.Draw('e0')
hists.append(hist)
canvases.canvases[-1].Update()


################################################################################
## Plot the p-values for (-50, 0)% range
name = 'FitRangeNegative'
title = '-50 .. 0 % Fit Range'
filenames = [os.path.join(path, 'strue_%s.root' % name)] * n
workspaces = ['ws1'] * n
snapshot = 'chi2_strue_mc_%s_mmMass80_%s_PhoEt%d-%d_bifurGauss'

frp = FitResultPlotter(
    sources = zip(filenames, workspaces,
                  [snapshot % (name, 'EB_highR9', lo, hi)
                   for lo, hi in binedges]),
    getters =  var_vs_pt('chi2Prob'),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 'p-value',
    title = 'Barrel, R_{9}^{#gamma} < 0.94',
    )

for icat in cats:
    frp.sources = zip(filenames, workspaces,
                      [snapshot % (name, icat.name, lo, hi)
                       for lo, hi in binedges])
    frp.getters = var_vs_pt('chi2Prob')
    frp.title = ', '.join(icat.labels)
    frp.getdata()
    frp.makegraph()

canvases.next('strue_pvalues_vs_phoEt_%s' % name)
frp.plotall(title = title)
plotters.append(frp)

## Make the distribution of the p-values
hist = frp.histogramall(
    name = 'h_strue_pvalues_%s' % name,
    title = '%s;p-value;Fits' % title,
    nbins = 5, xlow = 0, xhigh = 1
    )
canvases.next('strue_pvalues_distro_%s' % name)
hist.Draw('e0')
hists.append(hist)
canvases.canvases[-1].Update()


################################################################################
## Plot the p-values for (0, 50)% range
name = 'FitRangePositive'
title = '0 .. 50 % Fit Range'
filenames = [os.path.join(path, 'strue_%s.root' % name)] * n
workspaces = ['ws1'] * n
snapshot = 'chi2_strue_mc_%s_mmMass80_%s_PhoEt%d-%d_bifurGauss'

frp = FitResultPlotter(
    sources = zip(filenames, workspaces,
                  [snapshot % (name, 'EB_highR9', lo, hi)
                   for lo, hi in binedges]),
    getters =  var_vs_pt('chi2Prob'),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 'p-value',
    title = 'Barrel, R_{9}^{#gamma} < 0.94',
    )

for icat in cats:
    frp.sources = zip(filenames, workspaces,
                      [snapshot % (name, icat.name, lo, hi)
                       for lo, hi in binedges])
    frp.getters = var_vs_pt('chi2Prob')
    frp.title = ', '.join(icat.labels)
    frp.getdata()
    frp.makegraph()

canvases.next('strue_pvalues_vs_phoEt_%s' % name)
frp.plotall(title = title)
plotters.append(frp)

## Make the distribution of the p-values
hist = frp.histogramall(
    name = 'h_strue_pvalues_%s' % name,
    title = '%s;p-value;Fits' % title,
    nbins = 5, xlow = 0, xhigh = 1
    )
canvases.next('strue_pvalues_distro_%s' % name)
hist.Draw('e0')
hists.append(hist)
canvases.canvases[-1].Update()



if __name__ == '__main__':
    import user
