'''
Plot mean and width of s vs pt for Baseline and Caltech MC and MC truth
    Usage: python -i frp_caltech_vs_lyon.py
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

filename = '/raid2/veverka/esFitResults/mc_sreco_strue_Baseline_V1.root'
filename = '/Users/veverka/Work/Talks/11-11-04/mc_sreco_strue_Baseline_V1.root'
filename1 = '/Users/veverka/Work/Talks/11-11-09/Baseline_mod1/mc_sreco_strue_Baseline_mod1.root'
filename3 = 'mc_sreco_strue_Baseline_mod3.root'
filename2 = 'mc_sreco_strue_Baseline_mod2.root'

plotters = []

## Configuration for plots vs Pt
binedges = list(BinEdges([10, 12, 15, 20, 25, 30, 100]))
bincenters = [0.5*(lo + hi)
              for lo, hi in BinEdges([10, 12, 15, 20, 25, 30, 50])]
binhalfwidths = [0.5*(hi - lo)
                 for lo, hi in BinEdges([10, 12, 15, 20, 25, 30, 50])]
n = len(binedges)
# binhalfwidths = [0] * n

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

categories = 'EB_lowR9 EB_highR9 EE_lowR9 EE_highR9'.split()
lyonmc = lyon['mc']

class Config():
    """Holds fitResultPlotter configuration data."""
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
## end of Config

cfgs = [
    ###########################################################################
    ## EB, R9 < 0.94, mmMass < 80 GeV, mmgMass in [87.2, 95.2]
    Config(
        ## Used to pick the right Lyon data and in canvas name
        name = 'EB_lowR9',
        ## Used in canvas title
        title = 'Barrel, R_{9} < 0.94, Baseline Selection, POWHEG S4',
        filenames1 = [filename1] * n,
        filenames2 = [filename2] * n,
        filenames3 = [filename3] * n,
        wsnames = ('ws1',) * n,
        sreco_snapshots1 = ['sFit_sreco_mc_cbShape_mmMass80_EB_lowR9_PhoEt%d-%d'
                            % (lo, hi) for lo, hi in binedges],
        sreco_snapshots2 = ['sFit_sreco_mc_cbShape_mmMass90_EB_lowR9_PhoEt%d-%d'
                            % (lo, hi) for lo, hi in binedges],
        sreco_snapshots3 = ['sFit_sreco_mc_cbShape_mmMass85_EB_lowR9_PhoEt%d-%d'
                            % (lo, hi) for lo, hi in binedges],
        ## MC truth scale
        strue_snapshots = ['sFit_strue_mc_bifurGauss_mmMass85_EB_lowR9_'
                           'PhoEt%d-%d' % (lo, hi) for lo, hi in binedges],
    ),
    ###########################################################################
    ## EB, R9 > 0.94, mmMass < 80 GeV, mmgMass in [87.2, 95.2]
    Config(
        ## Used to pick the right Lyon data and in canvas name
        name = 'EB_highR9',
        ## Used in canvas title
        title = 'Barrel, R_{9} > 0.94, Baseline Selection, POWHEG S4',
        filenames1 = [filename1] * n,
        filenames2 = [filename2] * n,
        filenames3 = [filename3] * n,
        wsnames = ('ws1',) * n,
        sreco_snapshots1 = ['sFit_sreco_mc_cbShape_mmMass80_EB_highR9_PhoEt%d-%d'
                           % (lo, hi) for lo, hi in binedges],
        sreco_snapshots2 = ['sFit_sreco_mc_cbShape_mmMass90_EB_highR9_PhoEt%d-%d'
                           % (lo, hi) for lo, hi in binedges],
        sreco_snapshots3 = ['sFit_sreco_mc_cbShape_mmMass85_EB_highR9_PhoEt%d-%d'
                           % (lo, hi) for lo, hi in binedges],
        ## MC truth scale
        strue_snapshots = ['sFit_strue_mc_bifurGauss_mmMass85_EB_highR9_'
                           'PhoEt%d-%d' % (lo, hi) for lo, hi in binedges],
    ),
    ###########################################################################
    ## EE, R9 < 0.95, mmMass < 80 GeV, mmgMass in [87.2, 95.2]
    Config(
        ## Used to pick the right Lyon data and in canvas name
        name = 'EE_lowR9',
        ## Used in canvas title
        title = 'Endcaps, R_{9} < 0.95, Baseline Selection, POWHEG S4',
        filenames1 = [filename1] * n,
        filenames2 = [filename2] * n,
        filenames3 = [filename3] * n,
        wsnames = ('ws1',) * n,
        sreco_snapshots1 = ['sFit_sreco_mc_cbShape_mmMass80_EE_lowR9_PhoEt%d-%d'
                           % (lo, hi) for lo, hi in binedges],
        sreco_snapshots2 = ['sFit_sreco_mc_cbShape_mmMass90_EE_lowR9_PhoEt%d-%d'
                           % (lo, hi) for lo, hi in binedges],
        sreco_snapshots3 = ['sFit_sreco_mc_cbShape_mmMass85_EE_lowR9_PhoEt%d-%d'
                           % (lo, hi) for lo, hi in binedges],
        ## MC truth scale
        strue_snapshots = ['sFit_strue_mc_bifurGauss_mmMass85_EE_lowR9_'
                           'PhoEt%d-%d' % (lo, hi) for lo, hi in binedges],
    ),
    ###########################################################################
    ## EE, R9 > 0.95, mmMass < 80 GeV, mmgMass in [87.2, 95.2]
    Config(
        ## Used to pick the right Lyon data and in canvas name
        name = 'EE_highR9',
        ## Used in canvas title
        title = 'Endcaps, R_{9} > 0.95, Baseline Selection, POWHEG S4',
        filenames1 = [filename1] * n,
        filenames2 = [filename2] * n,
        filenames3 = [filename3] * n,
        wsnames = ('ws1',) * n,
        sreco_snapshots1 = ['sFit_sreco_mc_cbShape_mmMass80_EE_highR9_PhoEt%d-%d'
                           % (lo, hi) for lo, hi in binedges],
        sreco_snapshots2 = ['sFit_sreco_mc_cbShape_mmMass90_EE_highR9_PhoEt%d-%d'
                           % (lo, hi) for lo, hi in binedges],
        sreco_snapshots3 = ['sFit_sreco_mc_cbShape_mmMass85_EE_highR9_PhoEt%d-%d'
                           % (lo, hi) for lo, hi in binedges],
        ## MC truth scale
        strue_snapshots = ['sFit_strue_mc_bifurGauss_mmMass85_EE_highR9_'
                           'PhoEt%d-%d' % (lo, hi) for lo, hi in binedges],
    ),
]


for cfg in cfgs[:]:
    #------------------------------------------------------------------------------
    ## Scale Comparison
    ## Baseline v2
    frp = FitResultPlotter(
        sources = zip(cfg.filenames1, cfg.wsnames, cfg.sreco_snapshots1),
        getters = var_vs_pt('#Deltas'),
        xtitle = 'E_{T}^{#gamma} (GeV)',
        ytitle = 's_{reco} = E^{#gamma}_{reco}/E^{kin}_{reco} - 1 (%)',
        title = 'Baseline v2',
        )
    frp.getdata()
    frp.makegraph()

    ## mmMass < 85 GeV
    frp.sources = zip(cfg.filenames3, cfg.wsnames, cfg.sreco_snapshots3)
    frp.getters = var_vs_pt('#Deltas')
    frp.title = 'm_{#mu#mu} < 85 GeV'
    frp.getdata()
    frp.makegraph()

    ## mmMass < 90 GeV
    frp.sources = zip(cfg.filenames2, cfg.wsnames, cfg.sreco_snapshots2)
    frp.getters = var_vs_pt('#Deltas')
    frp.title = 'm_{#mu#mu} < 90 GeV'
    frp.getdata()
    frp.makegraph()

    ## True
    frp.sources = zip(cfg.filenames3, cfg.wsnames, cfg.strue_snapshots)
    frp.getters = var_vs_pt('#Deltas')
    frp.title = 'MC Truth'
    frp.getdata()
    frp.makegraph()

    ## Compare Proposal 1, Baseline and MC truth scale
    canvases.next('s_' + cfg.name).SetGrid()
    frp.plotall(title = cfg.title,
                styles = [20, 25, 26, 22],
                colors = [kBlue, kRed, kGreen, kBlack])

    plotters.append(frp)

    #------------------------------------------------------------------------------
    ## S width Comparison
    ## Baseline
    ## frp = FitResultPlotter(
    ##     sources = zip(cfg.filenames, cfg.wsnames, cfg.sreco_snapshots),
    ##     getters = (
    ##         lambda ws, i = iter(bincenters): i.next(),    # x
    ##         lambda ws, i = iter(lyonmc[cfg.name]['sigma']): i.next(),    # y
    ##         lambda ws, i = iter(binhalfwidths): i.next(), # ex
    ##         lambda ws, i = iter(lyonmc[cfg.name]['esigma']): i.next(),   # ey
    ##         ),
    ##     xtitle = 'E_{T}^{#gamma} (GeV)',
    ##     ytitle = '#sigma(s_{reco}) (%)',
    ##     title = 'Baseline',
    ##     )
    ## frp.getdata()
    ## frp.makegraph()

    ## ## Proposal 1
    ## frp.getters = var_vs_pt('#sigma')
    ## frp.title = 'Proposal 1'
    ## frp.getdata()
    ## frp.makegraph()

    ## ## Compare Proposal 1 and Baseline s width
    ## canvases.next('sigma_' + cfg.name).SetGrid()
    ## frp.plotall(title = cfg.title,
    ##             styles = [20, 25])

    ## plotters.append(frp)
## end of loop over cfgs



################################################################################
## Plot the p-values of the MC true fits
filenames = [filename3] * n
workspaces = ['ws1'] * n
snapshot = 'chi2_strue_mc_bifurGauss_mmMass85_%s_PhoEt%d-%d_iter0'
cats = list(subdet_r9_categories)

frp = FitResultPlotter(
    sources = zip([filename2] * n,
                  ['ws1'] * n,
                  [snapshot % ('EB_highR9', lo, hi) for lo, hi in binedges]),
    getters =  var_vs_pt('chi2Prob'),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 'p-value',
    title = 'Barrel, R_{9}^{#gamma} < 0.94',
    )

for icat in cats:
    frp.sources = zip(filenames, workspaces,
                      [snapshot % (icat.name, lo, hi) for lo, hi in binedges])
    frp.getters = var_vs_pt('chi2Prob')
    frp.title = ', '.join(icat.labels)
    frp.getdata()
    frp.makegraph()

canvases.next('strue_pvalues_vs_phoEt_mmMass85')
frp.plotall(title = 'MC Truth Fits')
plotters.append(frp)

## Make the distribution of the p-values
hist = frp.histogramall(
    name = 'h_strue_pvalues',
    title = 's_{true} = E^{#gamma}_{reco}/E^{#gamma}_{gen};p-value;Fits',
    nbins = 5, xlow = 0, xhigh = 1
    )
canvases.next('strue_pvalues_distro_mmMass85')
hist.Draw('e0')
plotters.append(hist)

################################################################################
## Plot the p-values of the reco s-Fits fits, m(yy) < 85 GeV
filenames = [filename3] * n
workspaces = ['ws1'] * n
snapshot = 'chi2_sreco_mc_cbShape_mmMass85_%s_PhoEt%d-%d_iter0'

frp = FitResultPlotter(
    sources = zip([filename2] * n,
                  ['ws1'] * n,
                  [snapshot % ('EB_highR9', lo, hi) for lo, hi in binedges]),
    getters =  var_vs_pt('chi2Prob'),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 'p-value',
    title = 'Barrel, R_{9}^{#gamma} > 0.94',
    )

for icat in cats:
    frp.sources = zip(filenames, workspaces,
                      [snapshot % (icat.name, lo, hi) for lo, hi in binedges])
    frp.getters = var_vs_pt('chi2Prob')
    frp.title = ', '.join(icat.labels)
    frp.getdata()
    frp.makegraph()

canvases.next('sreco_pvalues_vs_phoEt_mmMass85')
frp.plotall(logy = True, title = 's_{reco} Fits')
plotters.append(frp)

## Make the distribution of the p-values
hist = frp.histogramall(
    name = 'h_sreco_pvalues_mmmass85',
    title = 's_{reco} = E^{#gamma}_{reco}/E^{#gamma}_{kin};p-value;Fits',
    nbins = 5, xlow = 0, xhigh = 1
    )
c1 = canvases.next('sreco_pvalues_distro_mmMass85')
hist.Draw('e0')
plotters.append(hist)

c1.Update()

################################################################################
## Plot the p-values of the reco s-Fits fits, m(yy) < 90 GeV
filenames = [filename2] * n
workspaces = ['ws1'] * n
snapshot = 'chi2_sreco_mc_cbShape_mmMass90_%s_PhoEt%d-%d_iter0'

frp = FitResultPlotter(
    sources = zip([filename2] * n,
                  ['ws1'] * n,
                  [snapshot % ('EB_highR9', lo, hi) for lo, hi in binedges]),
    getters =  var_vs_pt('chi2Prob'),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 'p-value',
    title = 'Barrel, R_{9}^{#gamma} > 0.94',
    )

for icat in cats:
    frp.sources = zip(filenames, workspaces,
                      [snapshot % (icat.name, lo, hi) for lo, hi in binedges])
    frp.getters = var_vs_pt('chi2Prob')
    frp.title = ', '.join(icat.labels)
    frp.getdata()
    frp.makegraph()

canvases.next('sreco_pvalues_vs_phoEt_mmMass90')
frp.plotall(logy = True, title = 's_{reco} Fits')

## Make the distribution of the p-values
hist = frp.histogramall(
    name = 'h_sreco_pvalues_mmMass90',
    title = 's_{reco} = E^{#gamma}_{reco}/E^{#gamma}_{kin};p-value;Fits',
    nbins = 5, xlow = 0, xhigh = 1
    )
c1 = canvases.next('sreco_pvalues_distro_mmMass90')
hist.Draw('e0')
plotters.append(hist)

c1.Update()

for c in canvases.canvases:
    if c:
        c.Update()

if __name__ == '__main__':
    import user
