'''
Plot photon energy scale vs pt in the 4 categories 
of (EB, EE) x (low R9, high R9) for MC truth, MC fit and real-data fit
with the PHOSPHOR method
'''

import os
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
binedges3 = list(BinEdges([10, 12, 15, 20, 25, 30, 100]))
bincenters    = [0.5 * (lo + hi) for lo, hi in binedges]
binhalfwidths = [0.5 * (hi - lo) for lo, hi in binedges]
xgetter_factory  = lambda: lambda workspace, i = iter(bincenters)    : i.next()
exgetter_factory = lambda: lambda workspace, i = iter(binhalfwidths) : i.next()

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
    basepath = '/raid2/veverka/phosphor/sge_baseline'
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
def make_list_of_sources_2011baseline(category):
    filename = '/raid2/veverka/esFitResults/mc_sreco_strue_Baseline_mod1.root'
    filenames = [filename] * len(binedges3)
    workspaces = ('ws1',) * len(binedges3)
    snapshots = ['sFit_sreco_mc_cbShape_mmMass80_%s_PhoEt%d-%d'
                 % (category, lo, hi) for lo, hi in binedges3]
    return zip(filenames, workspaces, snapshots)
## End of make_list_of_sources_2011baseline()

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
    period = '2011AB'
    period_title = '2011A+B'
    version = 'v13'
    test = 'evt2of4'
    name_base = '%s_pt{lo}to{hi}_%s_%s' % (cat.name, version, test)
    jobname_template1 = 'sgetest_mc_%s' % name_base
    jobname_template3 = 'sgetest_mc_%s' % name_base
    cfg = Config(
        ## Canvas name
        name = 'propaganda_scale_%s_%s' % (cat.name, period), 
        ## Canvas title
        title = ', '.join(cat.labels + (period_title,)),
        ## 1 : MC truth, 2: MC 2011 baseline fit, 3: MC PHOSPHOR fit
        sources1 = make_list_of_sources(jobname_template1),
        sources2 = make_list_of_sources_2011baseline(cat.name),
        sources3 = make_list_of_sources(jobname_template3),
        getters1 = var_vs_pt_getter_factory('phoScaleTrue'),
        getters2 = var_vs_pt_getter_factory('#Deltas'),
        getters3 = var_vs_pt_getter_factory('phoScale'),
        )
    scale_configurations.append(cfg)
## End of loop categories

plotters = []

#==============================================================================
for cfg in scale_configurations[:]:
    ## MC, EB, 2011A+B, 1 of 4 statistically independent tests
    xtitle = 'E_{T}^{#gamma} (GeV)'
    ytitle = 'E^{#gamma} Scale (%)'
    plotter = FitResultPlotter(cfg.sources1, cfg.getters1, xtitle, ytitle, 
                               title = 'MC Truth')                          
    plotter.getdata()
    plotter.makegraph()
    
    plotter.sources = cfg.sources2
    plotter.getters = cfg.getters2
    plotter.title = '2011 Baseline'
    plotter.getdata()
    plotter.makegraph()

    plotter.sources = cfg.sources3
    plotter.getters = cfg.getters3
    plotter.title = 'PHOSPHOR'
    plotter.getdata()
    plotter.makegraph()
    
    canvases.next('c_' + cfg.name).SetGrid()
    plotter.plotall(title = cfg.title,
                    styles = [20, 25, 26],
                    colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kRed])
    plotters.append(plotter)
## End of loop over configurations.
