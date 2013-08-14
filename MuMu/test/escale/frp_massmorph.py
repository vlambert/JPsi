#!/usr/bin/env python -i
import os
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases
from JPsi.MuMu.common.binedges import BinEdges
from JPsi.MuMu.escale.fitResultPlotter import FitResultPlotter

# subdetr9 = 'EB_highR9'
# subdetr9 = 'EB_lowR9'
subdetr9 = 'EE_highR9'
# subdetr9 = 'EE_lowR9'

scalescanfilemask = 'massmorph_scalescan_' + subdetr9 + '_phoPt%d-%d.root'
resscanfilemask = 'massmorph_resscan_' + subdetr9 + '_phoPt%d-%d.root'

scalescanfilemask = '_'.join([os.path.join('~/Work/Data/escale/masstransform/',
                                           'masstransform_scalescan'),
                              subdetr9,
                              'phoPt%d-%d.root'])
resscanfilemask = '_'.join([os.path.join('~/Work/Data/escale/masstransform/',
                                         'masstransform_resscan'),
                            subdetr9,
                            'phoPt%d-%d.root'])
wsname = 'w'

ROOT.gStyle.SetPadTopMargin(0.1)
ROOT.gStyle.SetTitleYOffset(1.25)

canvases.wwidth = 600
canvases.wheight = 600
canvases.yperiod = 10

frps = []
ptitle = {
    'EB_highR9': 'Barrel, R_{9} > 0.94',
    'EB_lowR9' : 'Barrel, R_{9} < 0.94',
    'EE_highR9': 'Endcaps, R_{9} > 0.95',
    'EE_lowR9' : 'Endcaps, R_{9} < 0.95',
    }[subdetr9]
ptbinedges = list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:]


axistitles = {
    'phoScale'  : 'photon energy scale (%)',
    'phoRes'    : 'photon energy resolution (%)',
    'massScale' : 'm_{#mu#mu#gamma} scale (%)',
    'massRes'   : 'm_{#mu#mu#gamma} width (%)',
    'massWidth' : 'm_{#mu#mu#gamma} width (GeV)',
    }

##------------------------------------------------------------------------------
def sources(filename, wsname):
    maxpoints = 999
    rootfile = ROOT.TFile(filename)
    ws = rootfile.Get(wsname)
    ret = []
    ## Loop over snapshots.
    for snapshot in ['smear_%d' % i for i in range(maxpoints)]:
        if ws.loadSnapshot(snapshot):
            ret.append((filename, wsname, snapshot))
        else:
            break
    return ret
    ## End loop over snapshots.
## End sources

##------------------------------------------------------------------------------
def valuegetter(xname, xtype):
    if xtype == 'var':
        return lambda ws: ws.var(xname).getVal()
    elif xtype == 'function':
        return lambda ws: ws.function(xname).getVal()
    else:
        raise RuntimeError, 'Unsupported xtype: %s' % xtype
## End of valuegetter().

##------------------------------------------------------------------------------
def errorgetter(xname, xtype):
    if xtype == 'var':
        return lambda ws: ws.var(xname).getError()
    elif xtype == 'function':
        return lambda ws: 0
    else:
        raise RuntimeError, 'Unsupported xtype: %s' % xtype
## End of errorgetter().

##------------------------------------------------------------------------------
def xygetters(xname, yname, xtype='var', ytype='var'):
    '''Given the names of the x and y arguments, returns a tuple of
    getter functions acting on a workspace and providing the values
    and errors of the x and y in the order (x, y, ex, ey).'''
    return (
        valuegetter(xname, xtype), # x
        valuegetter(yname, ytype), # y
        errorgetter(xname, xtype), # ex
        errorgetter(yname, ytype), # ey
        )
## End of xygetters.


##-- Make plots ----------------------------------------------------------------
def plot_xy(xname, yname, filemask, xtype='var', ytype='var'):
    filename = filemask % ptbinedges[0]
    ## Mass scale vs photon scale
    frp = FitResultPlotter(
        sources = sources(filename, wsname),
        getters = xygetters(xname, yname, xtype, ytype),
        xtitle = axistitles[xname],
        ytitle = axistitles[yname],
        title = 'Dummy Legend Entry',
        )
    for ptrange in ptbinedges:
        filename = filemask % ptrange
        frp.sources = sources(filename, wsname)
        frp.title = 'E_{T}^{#gamma} #in [%d, %d] GeV' % ptrange
        frp.getdata()
        frp.makegraph()
    canvases.next(yname + '_vs_' + xname).SetGrid()
    frp.plotall(title = ptitle)
    frps.append(frp)
## End of plot_xy().

##------------------------------------------------------------------------------
def plot_scalescan():
    '''Plot the dependence of the mmg mass peak postion and width on the
    photon energy scale for various pt bins.'''
    ## Mass scale vs photon scale
    plot_xy(xname = 'phoScale',
            yname = 'massScale',
            filemask = scalescanfilemask)
    
    ## Relative mass width vs photon scale
    plot_xy(xname = 'phoScale',
            yname = 'massRes',
            filemask = scalescanfilemask)
    
    ## Absolute mass width vs photon scale
    plot_xy(xname = 'phoScale',
            yname = 'massWidth',
            filemask = scalescanfilemask,
            ytype = 'function')
## End of plot_scalescan().

##------------------------------------------------------------------------------
def plot_resscan():    
    '''Plot the dependence of the mmg mass peak postion and width on the
    photon energy resolution for various pt bins.'''

    ## Mass scale vs photon resolution
    plot_xy(xname = 'phoRes',
            yname = 'massScale',
            ## xtitle = 'photon energy resolution (%)',
            ## ytitle = 'm_{#mu#mu#gamma} scale (%)',
            filemask = resscanfilemask)
    
    ## Mass width vs photon resolution
    plot_xy(xname = 'phoRes',
            yname = 'massRes',
            ## xtitle = 'photon energy resolution (%)',
            ## ytitle = 'm_{#mu#mu#gamma} width (%)',
            filemask = resscanfilemask)
## End of plot_resscan().    

##------------------------------------------------------------------------------
def guess_scale_slope(filename):
    '''Guess the slope of the mmg mass scale dependence on the photon energy
    scale from a sample of mmMass and mmgMass retreived from a file.'''
    # tfile = ROOT.TFile.Open(filename)
    w = ROOT.TFile.Open(filename).Get('w')
    sdata = w.data('sdata_10')
    slopeFunc = w.factory('''FormulaVar::slope(
        0.5 * (1 - mmMass^2 / mmgMass^2),
        {mmMass, mmgMass}
        )''')
    sdata.addColumn(slopeFunc)
    slopeFunc.SetName('slopeFunc')
    slope = w.factory('slope[0,1]')
    return sdata.mean(slope)
## End of guess_scale_slope().

##------------------------------------------------------------------------------
def compare_scale_slopes():
    ## Find the frp of scale vs scale
    for frp in frps:
        if 'scale' in frp.xtitle and 'scale' in frp.ytitle:
            break
    fitslopes = []
    for g in frp.graphs:
        res = g.Fit('pol1', 'qs', 'goff', -15, 15)
        fitslopes.append(res.Parameter(1))
    print '--'
    print 'pt range, fit slope, guessed slope'
    for ptrange, fitslope in zip(ptbinedges, fitslopes):
        filename = scalescanfilemask % ptrange
        print '%d-%3d GeV' % ptrange,
        print '%.3f %.3f' % (fitslope, guess_scale_slope(filename))
## End of compare_scale_slopes().

##------------------------------------------------------------------------------
def compare_res_slopes():
    ## Find the frp of scale vs scale
    for frp in frps:
        if 'resolution' in frp.xtitle and 'width' in frp.ytitle:
            break
    fitpars = []
    # myfunc = ROOT.TF1('myfunc', '[0] + sqrt([1]^2 + [2]^2 * x^2)', 0, 10)
    myfunc = ROOT.TF1('myfunc', '[0] + sqrt([1]^2 + [2]^2 * (x-[3])^2)', 0, 10)
    myfunc.SetParameters(1, 1, 0.2, 0)
    for g in frp.graphs:
        res = g.Fit(myfunc, 'qs', 'goff', 0, 10)
        fitpars.append([res.Parameter(i) for i in range(4)])
    print '-- Resoluton slopes --'
    print 'pt range, guessed slope, fitted slope, offset, r2'
    for ptrange, (p0, p1, p2, p3) in zip(ptbinedges, fitpars):
        filename = resscanfilemask % ptrange
        print '%d-%3d GeV' % ptrange,
        print '%.3f  %.3f  %.3f  %.3f %.3f' % (guess_scale_slope(filename),
                                          p2, p0, p1, p3)
## End of compare_res_slopes().
    
##------------------------------------------------------------------------------
def main():
    plot_scalescan()
    plot_resscan()

    ## Mass scale vs photon scale
    ## plot_xy(xname = 'phoScale',
    ##         yname = 'massScale',
    ##         filemask = ('massmorph_scalescan_' +
    ##                     subdetr9 +
    ##                     '_phoPt%d-%d.root'))
    ## compare_scale_slopes()

    ## plot_xy(xname = 'phoRes',
    ##         yname = 'massRes',
    ##         filemask = ('massmorph_resscan_' +
    ##                     subdetr9 +
    ##                     '_phoPt%d-%d.root'))
    ## compare_res_slopes()

## End of main().

##------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
    canvases.update()
    import user

