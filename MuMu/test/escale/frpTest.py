'''
Facilitates the plotting of variables versus the the fit range iteration.
    Usage: python -i plotScaleVsFitRangeIter.py
'''
import JPsi.MuMu.common.canvases as canvases
from JPsi.MuMu.escale.fitResultPlotter import FitResultPlotter
from JPsi.MuMu.common.binedges import BinEdges

canvases.wwidth = 400
canvases.wheight = 400
canvases.yperiod = 10

## Configuration for plots vs Pt
binedges = list(BinEdges([10, 12, 15, 20, 25, 30, 100]))
bincenters = [0.5*(lo + hi)
              for lo, hi in BinEdges([10, 12, 15, 20, 25, 30, 50])]
binhalfwidths = [0.5*(hi - lo)
                 for lo, hi in BinEdges([10, 12, 15, 20, 25, 30, 50])]
n = len(binedges)


filenames = ['mc_mmMass80_EB_lowR9_PhoEt_mmgMass87.2-95.2_cbShape.root'] * n
wsnames = ('ws1',) * n
## MC truth scale
strue_snapshots = ['sFit_strue_mc_mmMass80_EB_lowR9_cbShape_PhoEt%d-%d_iter0' % (lo, hi)
                   for lo, hi in binedges]
sreco_snapshots = ['sFit_sreco_mc_mmMass80_EB_lowR9_cbShape_PhoEt%d-%d_iter0' % (lo, hi)
                   for lo, hi in binedges]
shyb_snapshots = ['sFit_shyb_mc_mmMass80_EB_lowR9_cbShape_PhoEt%d-%d_iter0' % (lo, hi)
                   for lo, hi in binedges]
sgen_snapshots = ['sFit_sgen_mc_mmMass80_EB_lowR9_cbShape_PhoEt%d-%d_iter0' % (lo, hi)
                   for lo, hi in binedges]

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
frp = FitResultPlotter(
    sources = zip(filenames, wsnames, strue_snapshots),
    getters = var_vs_pt('#Deltas'),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 's_{true} = E^{#gamma}_{reco}/E^{#gamma}_{gen} - 1 (%)'
)

canvases.next()
frp.main()
print frp.ytitle
frp.dump()
print

## MC truth resolution
# canvases.next()
# frp.main(getters = var_vs_pt('#sigma'),
#          ytitle = '#sigma(E^{#gamma}_{reco}/E^{#gamma}_{gen})')
# frp.dump()

## Scale from mmg
canvases.next()
frp.main(sources = zip(filenames, wsnames, sreco_snapshots),
         getters = var_vs_pt('#Deltas'),
         ytitle = 's_{reco} = E^{#gamma}_{reco}/E^{kin}_{reco} - 1 (%)')
print frp.ytitle
frp.dump()
print

## Scale from mmg photon-only gen-level
canvases.next()
frp.main(sources = zip(filenames, wsnames, shyb_snapshots),
         getters = var_vs_pt('#Deltas'),
         ytitle = 's_{hyb} = E^{#gamma}_{gen}/E^{kin}_{reco} - 1 (%)')
print frp.ytitle
frp.dump()
print

## Scale from mmg gen-level
canvases.next()
frp.main(sources = zip(filenames, wsnames, sgen_snapshots),
         getters = var_vs_pt('#Deltas'),
         ytitle = 's_{gen} = E^{#gamma}_{gen}/E^{kin}_{gen} - 1 (%)')
print frp.ytitle
frp.dump()
print

if __name__ == '__main__':
    import user
