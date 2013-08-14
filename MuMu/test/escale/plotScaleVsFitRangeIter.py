'''
Facilitates the plotting of variables versus the the fit range iteration.
    Usage: python -i plotScaleVsFitRangeIter.py
'''
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.escale.fitRangeIterationPlotter as frip

canvases.next()
frip.filename = 'mc_mmMass85_EB_lowR9_PhoEt12-15.root'
frip.wsname = 'ws1'
frip.snapshot = 'sFit_strue_mc_mmMass85_EB_lowR9_PhoEt12-15_gamma'
frip.variable = '#Deltas'
frip.ytitle = '#Deltas'
frip.main()

canvases.next()
frip.variable = '#sigma'
frip.ytitle = '#sigma'
frip.main()

canvases.next()
# frip.fit = ''

if __name__ == '__main__':
    import user
