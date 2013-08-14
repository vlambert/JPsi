'''
Facilitates the plotting of variables versus the the fit range iteration.
    Usage: python -i plotScaleVsFitRangeIter.py
'''
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.escale.fitResultPlotter as frp

canvases.wwidth = 400
canvases.wheight = 400
canvases.yperiod = 10

## Plot the Delta s vs iteration number
canvases.next()
frp.filenames = ('mc_mmMass85_EB_lowR9_PhoEt12-15.root',) * 8
frp.wsnames = ('ws1',) * 8
name = 'sFit_strue_mc_mmMass85_EB_lowR9_PhoEt12-15_gamma_iter%d'
frp.snapshots = [name % i for i in range(8)]

frp.yname = '#Deltas'
frp.ytitle = '#Deltas'

frp.name = None
frp.xtitle = 'Fit Range Iteration'
frp.xdata = range(8)
frp.exdata = [0] * 8

frp.main()

## Plot sigma vs iteration number for the same fit
canvases.next()
frp.yname = '#sigma'
frp.ytitle = '#sigma'
frp.main()


## Swtich the parameter set
frp.snapshots = ['chi2' + name[4:] for name in frp.snapshots]

## Plot chi2/ndof vs iteration number for the same fit
frp.yname = 'reducedChi2'
frp.ytitle = '#chi^{2}/ndof'
canvases.next()
frp.main()

## Plot chi2/ndof vs iteration number for the same fit
frp.yname = 'ndof'
frp.ytitle = 'ndof'
canvases.next()
frp.main()

## Plot chi2 prob vs iteration number for the same fit
frp.yname = 'chi2Prob'
frp.ytitle = 'P(#chi^{2}, ndof)'
frp.logy = True
canvases.next().SetLogy()
frp.main()

canvases.canvases[-1].Update()

if __name__ == '__main__':
    import user
