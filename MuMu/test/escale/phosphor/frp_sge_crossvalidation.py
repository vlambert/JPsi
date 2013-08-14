'''
Plot photon energy scale vs pt in the 4 categories 
of (EB, EE) x (low R9, high R9) for MC truth, MC fit and real-data fit
with the PHOSPHOR method
'''

import os
import socket
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases
from JPsi.MuMu.common.binedges import BinEdges
from JPsi.MuMu.scaleFitter import subdet_r9_categories
from JPsi.MuMu.escale.fitResultPlotter import FitResultPlotter

ROOT.gStyle.SetPadTopMargin(0.1)
canvases.wwidth = 400
canvases.wheight = 400
canvases.yperiod = 10

categories = list(subdet_r9_categories)
binedges  = list(BinEdges([10, 12, 15, 20, 25, 30, 50]))
binedges2 = list(BinEdges([10, 12, 15, 20, 25, 30, 999]))
bincenters    = [0.5 * (lo + hi) for lo, hi in binedges]
binhalfwidths = [0.5 * (hi - lo) for lo, hi in binedges]
xgetter_factory  = lambda: lambda workspace, i = iter(bincenters)    : i.next()
exgetter_factory = lambda: lambda workspace, i = iter(binhalfwidths) : i.next()

plotters = []

#______________________________________________________________________________
def get_basepath():
    '''
    Return the common part of the path to data files depending
    on the host machine.
    '''
    hostname_to_basepath_map = {
        't3-susy.ultralight.org':
            '/raid2/veverka/phosphor/sge_baseline',
        'Jan-Veverkas-MacBook-Pro.local':
            '/Users/veverka/Work/Data/phosphor/sge_baseline',
        }
    return hostname_to_basepath_map[socket.gethostname()]
## End of get_basepath()


#______________________________________________________________________________
def make_list_of_sources(jobname_template):
    '''
    Returns a list of the tuples [(f1, w1, s1), ..., (fN, wN sN)]
    where (f, w, s) stand for (filename, workspace, snapshot).
    The jobname_template is expected to contain the {lo} and {hi}
    strings that will be substituted for the pt ranges, for example
    sge_mc_EB_pt{lo}to{hi}_v13_evt1of4 will be formatted to
    sge_mc_EB_pt10to12_v13_evt1of4, sge_mc_EB_pt12to15_v13_evt1of4, etc.    
    '''
    filenames, workspaces, snapshots = [], [], []

    ## Common path to all the fit result.
    basepath = get_basepath()
    ## Allways the same (due to a bug).
    basefilename = ('phosphor5_model_and_fit_'
                    'test_mc_EE_highR9_pt30to999_v13_evt1of4.root')
    ## Common to all MC fits.
    if 'mc' in jobname_template.split('_'):
        snapshot = 'mc_fit'
    else:
        snapshot = None

    ## Loop over the pt bins:
    for lo, hi in binedges2:
        ## The job name encodes the pt, category and data/MC
        jobname = jobname_template.format(lo=lo, hi=hi)
        
        filename = os.path.join(basepath, jobname, basefilename)
        workspace = jobname + '_workspace'
        
        filenames.append(filename)
        workspaces.append(workspace)
        snapshots.append(snapshot)
        
    return zip(filenames, workspaces, snapshots)
## End of make_list_of_sources(jobname_template)


#______________________________________________________________________________
def value_getter_factory(varname):
    '''
    Returns a function that takes a workspace and returns the value of the
    variable of the given name.
    '''
    return lambda workspace: workspace.var(varname).getVal()
## value_getter_factory(name)


#______________________________________________________________________________
def error_getter_factory(varname):
    '''
    Returns a function that takes a workspace and returns the error of the
    variable of the given name.
    '''
    return lambda workspace: workspace.var(varname).getError()
## error_getter_factory(name)


#______________________________________________________________________________
def var_vs_pt_getter_factory(varname):
    """
    Returns a tupler of 4 functions that take a workspace and return
    x, y, ex, ey where y and ey correspond to the value and error of
    a workspace variable of the given name and x and ex are pt bins defined
    in the global xgetter_factory function.
    """
    xgetter  = xgetter_factory()
    exgetter = exgetter_factory()
    ygetter  = value_getter_factory(varname)
    eygetter = error_getter_factory(varname)
    return (xgetter, ygetter, exgetter, eygetter)
## End of var_vs_pt_getter_factory(varname)


#______________________________________________________________________________
def value_fitresult_getter_factory(fitresult, varname):
    '''
    Returns a function that takes a workspace and returns the final value
    of a floated parameter of the given name for the given fit result 
    name.
    '''
    return lambda w: w.obj(fitresult).floatParsFinal().find(varname).getVal()
## value_fitresult_getter_factory(fitresult, varname)


#______________________________________________________________________________
def error_fitresult_getter_factory(fitresult, varname):
    '''
    Returns a function that takes a workspace and returns the final error
    of a floated parameter of the given name for the given fit result 
    name.
    '''
    return lambda w: w.obj(fitresult).floatParsFinal().find(varname).getError()
## error_fitresult_getter_factory(fitresult, varname)


#______________________________________________________________________________
def var_vs_pt_fitresult_getter_factory(fitresult, varname):
    """
    Returns a tupler of 4 functions that take a workspace and return
    x, y, ex, ey where y and ey correspond to the value and error of
    a final state of a floated parameter of a fit result stored in the 
    workspace of the given name and x and ex are pt bins defined
    in the global xgetter function.
    """
    xgetter  = xgetter_factory()
    exgetter = exgetter_factory()
    ygetter  = value_fitresult_getter_factory(fitresult, varname)
    eygetter = error_fitresult_getter_factory(fitresult, varname)
    return (xgetter, ygetter, exgetter, eygetter)
## End of var_vs_pt_fitresult_getter_factory(fitresult, varname)


#______________________________________________________________________________
class Config():
    """Holds fitResultPlotter configuration data."""
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
## end of Config

scale_configurations = []
for cat in categories:
    for period, version in zip('2011A 2011B 2011AB'.split(),
                               'v14 v15 v13'.split()):        
        if period == '2011AB':
            fitresult = 'fitresult_data'
            period_title = '2011A+B'
        else:
            fitresult = 'fitresult_' + period
            period_title = period
        cfg = Config(
            ## Canvas name
            name = '4xvalidation_scale_%s_%s' % (cat.name, period), 
            ## Canvas title
            title = ', '.join(cat.labels + (period_title,)),
            ## Axis titles
            xtitle = 'E_{T}^{#gamma} (GeV)',
            ytitle = 'E^{#gamma} Scale (%)',
            ## Initialize maps for sources and getters
            ## keys 1-4 correspond to evt1of4, evt2of4, ..., evt4of4
            sources = {},
            getters_fit = {},
            getters_true = {}
            )
        ## Add the sources and getters
        name_base = '%s_pt{lo}to{hi}_%s' % (cat.name, version)
        for i in range(1, 5):
            jobname_template = 'sgetest_mc_%s_evt%dof4' % (name_base, i)
            cfg.sources[i] = make_list_of_sources(jobname_template)
            cfg.getters_true[i] = var_vs_pt_getter_factory('phoScaleTrue')
            cfg.getters_fit[i] = var_vs_pt_getter_factory('phoScale')
        scale_configurations.append(cfg)
## End of loop categories


resolution_configurations = []
for cat in categories:
    for period, version in zip('2011A 2011B 2011AB'.split(),
                               'v14 v15 v13'.split()):        
        if period == '2011AB':
            fitresult = 'fitresult_data'
            period_title = '2011A+B'
        else:
            fitresult = 'fitresult_' + period
            period_title = period
        cfg = Config(
            ## Canvas name
            name = '4xvalidation_resoln_%s_%s' % (cat.name, period), 
            ## Canvas title
            title = ', '.join(cat.labels + (period_title,)),
            ## Axis titles
            xtitle = 'E_{T}^{#gamma} (GeV)',
            ytitle = 'E^{#gamma} Resolution (%)',
            ## Initialize maps for sources and getters
            ## keys 1-4 correspond to evt1of4, evt2of4, ..., evt4of4
            sources = {},
            getters_fit = {},
            getters_true = {}
            )
        ## Add the sources and getters
        name_base = '%s_pt{lo}to{hi}_%s' % (cat.name, version)
        for i in range(1, 5):
            jobname_template = 'sgetest_mc_%s_evt%dof4' % (name_base, i)
            cfg.sources[i] = make_list_of_sources(jobname_template)
            cfg.getters_true[i] = var_vs_pt_getter_factory('phoResTrue')
            cfg.getters_fit[i] = var_vs_pt_getter_factory('phoRes')

        resolution_configurations.append(cfg)
## End of loop categories


#==============================================================================
def make_scale_plots(configurations):
    '''
    For each configuration in the given list, overlays the graphs of 
    scale versus pt for all sets of measurements specified.
    These measurements are either from the true or the PHOSPHOR fit.
    '''
    for cfg in configurations[:2]:
        ## Only check EE 2011AB
        #if (not 'EE_lowR9' in cfg.name) or (not 'AB' in cfg.name):
            #continue
        ### Only check 2011AB
        #if not 'AB' in cfg.name:
            #continue
        ## MC, EB, 2011A+B, 1 of 4 statistically independent tests
        plotter = FitResultPlotter(cfg.sources[1], cfg.getters_true[1], cfg.xtitle, 
                                  cfg.ytitle, title = 'MC Truth 1', name=cfg.name)                          

        for i in range(1,5):
            plotter.sources = cfg.sources[i]
            plotter.getters = cfg.getters_true[i]
            plotter.title = 'MC Truth %d' % i
            plotter.getdata()
            plotter.makegraph()

        for i in range(1,5):
            plotter.sources = cfg.sources[i]
            plotter.getters = cfg.getters_fit[i]
            plotter.title = 'MC Fit %d' % i
            plotter.getdata()
            plotter.makegraph()

        canvases.next('c_' + cfg.name).SetGrid()
        plotter.plotall(title = cfg.title,
                        xrange = (0, 80),
                        legend_position = 'topright')
        plotter.graphs[0].Draw('p')
        canvases.canvases[-1].Modified()
        canvases.canvases[-1].Update()
        canvases.update()
        plotters.append(plotter)
    ## End of loop over configurations.
## End of make_scale_plots(..)


#==============================================================================
def make_resolution_plots(configurations):
    '''
    For each configuration in the given list, overlays the graphs of 
    resolution versus pt for all sets of measurements specified.
    These measurements are either from the true or the PHOSPHOR fit.
    '''
    for cfg in configurations[:]:
        ### Only check 2011AB
        #if not 'AB' in cfg.name:
            #continue
        ## MC, EB, 2011A+B, 1 of 4 statistically independent tests
        plotter = FitResultPlotter(cfg.sources[1], cfg.getters_true[1], cfg.xtitle, 
                                  cfg.ytitle, title = 'MC Truth 1', name=cfg.name)                          
        
        for i in range(1,5):
            plotter.sources = cfg.sources[i]
            plotter.getters = cfg.getters_true[i]
            plotter.title = 'MC Truth %d' % i
            plotter.getdata()
            plotter.makegraph()

        for i in range(1,5):
            plotter.sources = cfg.sources[i]
            plotter.getters = cfg.getters_fit[i]
            plotter.title = 'MC Fit %d' % i
            plotter.getdata()
            plotter.makegraph()
        
        canvases.next('c_' + cfg.name).SetGrid()
        plotter.plotall(title = cfg.title,
                        xrange = (0, 80),
                        legend_position = 'topright')
              
        plotter.graphs[0].Draw('p')
        canvases.canvases[-1].Modified()
        canvases.canvases[-1].Update()
        canvases.update()
        plotters.append(plotter)
    ## End of loop over configurations.
## End of make_resolution_plots(..)


#==============================================================================
def main():
    '''
    Main entry point of execution.
    '''
    make_scale_plots(scale_configurations)
    # make_resolution_plots(resolution_configurations)
    # histogram_residuals()
## End of main(..)


#==============================================================================
if __name__ == '__main__':
    main()
    import user
    