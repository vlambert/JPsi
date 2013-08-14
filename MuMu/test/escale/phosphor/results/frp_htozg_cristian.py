'''
Plot photon energy scale vs pt in the 4 categories 
of (EB, EE) x (low R9, high R9) for MC truth, MC fit and real-data fit
with the PHOSPHOR method for the fits done by Cristian ib Si's ntuples
around 18 September 2012.
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

binedges  = list(BinEdges([10, 12, 15, 20, 50]))
binedges2 = list(BinEdges([10, 12, 15, 20, 999]))
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
            '/home/cmorgoth/phosphor/CMSSW_4_2_8_patch7/src/JPsi/MuMu/test/escale/phosphor/Phosphor_Interface/results_zgamma',
            # '/mnt/hadoop/user/veverka/phosphor/Cristian_17Sep2012_HtoZg/',
        #'Jan-Veverkas-MacBook-Pro.local':
            #'/Users/veverka/Work/Data/phosphor/sge_correction',
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

    ## Common to all fits.
    snapshot = 'mc_fit'

    ## Loop over the pt bins:
    for lo, hi in binedges2:
        ## The job name encodes the pt, category and data/MC
        jobname = jobname_template.format(lo=lo, hi=hi)
        filename = 'phosphor5_model_and_fit_' + jobname + '.root'
        
        filename = os.path.join(basepath, filename)
        workspace = jobname + '_workspace'
        if 'mc' in jobname_template.split('_'):
            snapshot = 'mc_fit'
        else:
            snapshot = None
        
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


#______________________________________________________________________________
def get_scale_configs():
    '''
    Returns a list of configurations for the scale plots.
    '''
    configurations = [
        ###########################################################################
        ## Barrel 2012ABC
        Config(
            ## Canvas name
            name = 'corr_scale_EB_2012ABC',
            ## Canvas title
            title = 'Barrel, 2012ABC',
            ## 1 : MC truth, 2: MC fit, 3: data fit
            sources1 = make_list_of_sources('mc_EB_sixie_R9Low_0_R9high_99_PtLow_{lo}_PtHigh_{hi}'),
            sources2 = make_list_of_sources('mc_EB_sixie_R9Low_0_R9high_99_PtLow_{lo}_PtHigh_{hi}'),
            sources3 = make_list_of_sources('data_EB_sixie_R9Low_0_R9high_99_PtLow_{lo}_PtHigh_{hi}'),
            getters1 = var_vs_pt_getter_factory('phoScaleTrue'),
            getters2 = var_vs_pt_getter_factory('phoScale'),
            getters3 = var_vs_pt_fitresult_getter_factory('fitresult_data',
                                                          'phoScale'),
            ),

        ###########################################################################
        ## Endcaps 2012ABC
        Config(
            ## Canvas name
            name = 'corr_scale_EE_2012ABC',
            ## Canvas title
            title = 'Endcaps, 2012ABC',
            ## 1 : MC truth, 2: MC fit, 3: data fit
            sources1 = make_list_of_sources('mc_EE_sixie_R9Low_0_R9high_99_PtLow_{lo}_PtHigh_{hi}'),
            sources2 = make_list_of_sources('mc_EE_sixie_R9Low_0_R9high_99_PtLow_{lo}_PtHigh_{hi}'),
            sources3 = make_list_of_sources('data_EE_sixie_R9Low_0_R9high_99_PtLow_{lo}_PtHigh_{hi}'),
            getters1 = var_vs_pt_getter_factory('phoScaleTrue'),
            getters2 = var_vs_pt_getter_factory('phoScale'),
            getters3 = var_vs_pt_fitresult_getter_factory('fitresult_data',
                                                          'phoScale'),
            ),

        ] # configurations
    return configurations
## End of get_scale_configs().


#______________________________________________________________________________
def get_resolution_configs():
    '''
    Returns the list of configurations for the resolution plots.
    '''
    configurations  = [
       ###########################################################################
        ## Barrel 2012ABC
        Config(
            ## Canvas name
            name = 'corr_resoln_EB_2012ABC',
            ## Canvas title
            title = 'Barrel, 2012ABC',
            ## 1 : MC truth, 2: MC fit, 3: data fit
            sources1 = make_list_of_sources('mc_EB_sixie_R9Low_0_R9high_99_PtLow_{lo}_PtHigh_{hi}'),
            sources2 = make_list_of_sources('mc_EB_sixie_R9Low_0_R9high_99_PtLow_{lo}_PtHigh_{hi}'),
            sources3 = make_list_of_sources('data_EB_sixie_R9Low_0_R9high_99_PtLow_{lo}_PtHigh_{hi}'),
            getters1 = var_vs_pt_getter_factory('phoResTrue'),
            getters2 = var_vs_pt_getter_factory('phoRes'),
            getters3 = var_vs_pt_fitresult_getter_factory('fitresult_data',
                                                          'phoRes'),
            ),

        ###########################################################################
        ## Endcaps 2012ABC
        Config(
            ## Canvas name
            name = 'corr_resoln_EE_2012ABC',
            ## Canvas title
            title = 'Endcaps, 2012ABC',
            ## 1 : MC truth, 2: MC fit, 3: data fit
            sources1 = make_list_of_sources('mc_EE_sixie_R9Low_0_R9high_99_PtLow_{lo}_PtHigh_{hi}'),
            sources2 = make_list_of_sources('mc_EE_sixie_R9Low_0_R9high_99_PtLow_{lo}_PtHigh_{hi}'),
            sources3 = make_list_of_sources('data_EE_sixie_R9Low_0_R9high_99_PtLow_{lo}_PtHigh_{hi}'),
            getters1 = var_vs_pt_getter_factory('phoResTrue'),
            getters2 = var_vs_pt_getter_factory('phoRes'),
            getters3 = var_vs_pt_fitresult_getter_factory('fitresult_data',
                                                          'phoRes'),
            ),
        ] ## configurations
    return configurations
## End of get_resolution_configs()


#______________________________________________________________________________
def make_scale_plots():
    '''
    Makes the canvases with the scale plots.
    '''
    global plotters
    #==========================================================================
    for cfg in get_scale_configs()[:]:
        ## MC, EB, 2011A+B, 1 of 4 statistically independent tests
        xtitle = 'E_{T}^{#gamma} (GeV)'
        ytitle = 'E^{#gamma} Scale (%)'
        plotter = FitResultPlotter(cfg.sources1, cfg.getters1, xtitle, ytitle, 
                                   title = 'MC Truth')                          
        plotter.getdata()
        plotter.makegraph()

        plotter.sources = cfg.sources2
        plotter.getters = cfg.getters2
        plotter.title = 'MC Fit'
        plotter.getdata()
        plotter.makegraph()

        plotter.sources = cfg.sources3
        plotter.getters = cfg.getters3
        plotter.title = 'Data Fit'
        plotter.getdata()
        plotter.makegraph()

        canvases.next('c_' + cfg.name).SetGrid()
        plotter.plotall(title = cfg.title,
                        styles = [20, 25, 26],
                        colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kRed])
        plotters.append(plotter)
    ## End of loop over configurations.
## End of make_scale_plots().


#______________________________________________________________________________
def make_resolution_plots():
    '''
    Makes canvases with resolution plots.
    '''
    global plotters
    #==========================================================================
    for cfg in get_resolution_configs()[:]:
        ## MC, EB, 2011A+B, 1 of 4 statistically independent tests
        xtitle = 'E_{T}^{#gamma} (GeV)'
        ytitle = 'E^{#gamma} Resolution (%)'
        plotter = FitResultPlotter(cfg.sources1, cfg.getters1, xtitle, ytitle, 
                                   title = 'MC Truth')                          
        plotter.getdata()
        plotter.makegraph()

        plotter.sources = cfg.sources2
        plotter.getters = cfg.getters2
        plotter.title = 'MC Fit'
        plotter.getdata()
        plotter.makegraph()

        plotter.sources = cfg.sources3
        plotter.getters = cfg.getters3
        plotter.title = 'Data Fit'
        plotter.getdata()
        plotter.makegraph()

        canvases.next('c_' + cfg.name).SetGrid()
        plotter.plotall(title = cfg.title,
                        styles = [20, 25, 26],
                        colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kRed])
        plotters.append(plotter)
    ## End of loop over configurations.
## Ens of make_resolution_plots()


#______________________________________________________________________________
def main():
    '''
    Main entry point of execution.
    '''
    # make_scale_plots()
    make_resolution_plots()
## End of main()


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
