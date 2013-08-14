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
from JPsi.MuMu.escale.keystranslationdata import data_2011_11_18_confID_163190 as ktrans
from JPsi.MuMu.scaleFitter import subdet_r9_categories
from math import sqrt

gStyle.SetPadTopMargin(0.1)
canvases.wwidth = 400
canvases.wheight = 400
canvases.yperiod = 10

filename = '/raid2/veverka/esFitResults/mc_sreco_strue_Baseline_V1.root'
filename = '/Users/veverka/Work/Talks/11-11-04/mc_sreco_strue_Baseline_V1.root'
filename = '/Users/veverka/Work/Talks/11-11-09/Baseline_mod1/mc_sreco_strue_Baseline_mod1.root'

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
ktransmc = ktrans['mc']

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
        filenames = [filename] * n,
        wsnames = ('ws1',) * n,
        sreco_snapshots = ['sFit_sreco_mc_cbShape_mmMass80_EB_lowR9_PhoEt%d-%d'
                           % (lo, hi) for lo, hi in binedges],
        ## MC truth scale
        strue_snapshots = ['sFit_strue_mc_bifurGauss_mmMass80_EB_lowR9_'
                           'PhoEt%d-%d' % (lo, hi) for lo, hi in binedges],
    ),
    ###########################################################################
    ## EB, R9 > 0.94, mmMass < 80 GeV, mmgMass in [87.2, 95.2]
    Config(
        ## Used to pick the right Lyon data and in canvas name
        name = 'EB_highR9',
        ## Used in canvas title
        title = 'Barrel, R_{9} > 0.94, Baseline Selection, POWHEG S4',
        filenames = [filename] * n,
        wsnames = ('ws1',) * n,
        sreco_snapshots = ['sFit_sreco_mc_cbShape_mmMass80_EB_highR9_PhoEt%d-%d'
                           % (lo, hi) for lo, hi in binedges],
        ## MC truth scale
        strue_snapshots = ['sFit_strue_mc_bifurGauss_mmMass80_EB_highR9_'
                           'PhoEt%d-%d' % (lo, hi) for lo, hi in binedges],
    ),
    ###########################################################################
    ## EE, R9 < 0.95, mmMass < 80 GeV, mmgMass in [87.2, 95.2]
    Config(
        ## Used to pick the right Lyon data and in canvas name
        name = 'EE_lowR9',
        ## Used in canvas title
        title = 'Endcaps, R_{9} < 0.95, Baseline Selection, POWHEG S4',
        filenames = [filename] * n,
        wsnames = ('ws1',) * n,
        sreco_snapshots = ['sFit_sreco_mc_cbShape_mmMass80_EE_lowR9_PhoEt%d-%d'
                           % (lo, hi) for lo, hi in binedges],
        ## MC truth scale
        strue_snapshots = ['sFit_strue_mc_bifurGauss_mmMass80_EE_lowR9_'
                           'PhoEt%d-%d' % (lo, hi) for lo, hi in binedges],
    ),
    ###########################################################################
    ## EE, R9 > 0.95, mmMass < 80 GeV, mmgMass in [87.2, 95.2]
    Config(
        ## Used to pick the right Lyon data and in canvas name
        name = 'EE_highR9',
        ## Used in canvas title
        title = 'Endcaps, R_{9} > 0.95, Baseline Selection, POWHEG S4',
        filenames = [filename] * n,
        wsnames = ('ws1',) * n,
        sreco_snapshots = ['sFit_sreco_mc_cbShape_mmMass80_EE_highR9_PhoEt%d-%d'
                           % (lo, hi) for lo, hi in binedges],
        ## MC truth scale
        strue_snapshots = ['sFit_strue_mc_bifurGauss_mmMass80_EE_highR9_'
                           'PhoEt%d-%d' % (lo, hi) for lo, hi in binedges],
    ),
]

oplus  = lambda x, y: sqrt(x*x + y*y)

for cfg in cfgs:
    #------------------------------------------------------------------------------
    ## Scale Comparison
    ## PDF Morph: m translation for photon scale
    frp = FitResultPlotter(
        sources = zip(cfg.filenames, cfg.wsnames, cfg.strue_snapshots),
        getters = (
            lambda ws, i = iter(bincenters): i.next(),    # x
            lambda ws, i = iter(ktransmc[cfg.name]['sreco']): (
                ws.var('#Deltas').getVal() + i.next() # y
                ),
            lambda ws, i = iter(binhalfwidths): i.next(), # ex
            lambda ws, i = iter(ktransmc[cfg.name]['esreco']): (
                oplus(ws.var('#Deltas').getError(), i.next())
                ), # ey
            ),
        xtitle = 'E_{T}^{#gamma} (GeV)',
        ytitle = 's_{reco} = E^{#gamma}_{reco}/E^{kin}_{reco} - 1 (%)',
        title = 'PDF Morph',
        )
    frp.getdata()
    frp.makegraph()

    ## New Baseline
    frp.sources = zip(cfg.filenames, cfg.wsnames, cfg.sreco_snapshots)
    frp.getters = var_vs_pt('#Deltas')
    frp.title = 'Baseline'
    frp.getdata()
    frp.makegraph()

    ## True
    frp.sources = zip(cfg.filenames, cfg.wsnames, cfg.strue_snapshots)
    frp.getters = var_vs_pt('#Deltas')
    frp.title = 'MC Truth'
    frp.getdata()
    frp.makegraph()

    ## Compare New Baseline, MC PDF and MC truth scale
    canvases.next('s_' + cfg.name).SetGrid()
    frp.plotall(title = cfg.title,
                styles = [20, 25, 22],
                colors = [kBlue, kRed, kBlack])

    plotters.append(frp)

## end of loop over cfgs

if __name__ == '__main__':
    import user
