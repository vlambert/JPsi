'''
Plot photon energy scale vs pt in the EB for MC truth, MC fit and real-data fit
with the PHOSPHOR method polished for the EWK-11-009 paper.
'''

import os
import socket
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.binedges import BinEdges
from JPsi.MuMu.scaleFitter import subdet_r9_categories
from JPsi.MuMu.escale.fitResultPlotter import FitResultPlotter

ROOT.gStyle.SetPadTopMargin(0.1)
canvases.wwidth = 800
canvases.wheight = 600
canvases.yperiod = 10

binedges  = list(BinEdges([10, 12, 15, 20, 50]))
binedges2 = list(BinEdges([10, 12, 15, 20, 999]))
bincenters    = [0.5 * (lo + hi) for lo, hi in binedges]
binhalfwidths = [0.5 * (hi - lo) for lo, hi in binedges]
xgetter_factory  = lambda: lambda workspace, i = iter(bincenters)    : i.next()
exgetter_factory = lambda: lambda workspace, i = iter(binhalfwidths) : i.next()
plotters = []

latex_labels = []

#______________________________________________________________________________
def get_basepath():
    '''
    Return the common part of the path to data files depending
    on the host machine.
    '''
    hostname_to_basepath_map = {
        't3-susy.ultralight.org':
            '/raid2/veverka/phosphor/sge_correction',
        'Jan-Veverkas-MacBook-Pro.local':
            '/Users/veverka/Work/Data/phosphor/sge_correction',
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
    ## Common to all fits.
    snapshot = 'mc_fit'

    ## Loop over the pt bins:
    for lo, hi in binedges2:
        ## The job name encodes the pt, category and data/MC
        jobname = jobname_template.format(lo=lo, hi=hi)
        
        filename = os.path.join(basepath, jobname, basefilename)
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
        #######################################################################
        ## Barrel 2011A+B
        Config(
            ## Canvas name
            name = 'PHOSPHOR_Fit_ScaleVsPt_EB_2011AB',
            ## Canvas title
            title = '',
            ## 1 : MC truth, 2: MC fit, 3: data fit
            sources1 = make_list_of_sources('sge_mc_EB_pt{lo}to{hi}_v13_evt1of4'),
            sources2 = make_list_of_sources('sge_mc_EB_pt{lo}to{hi}_v13_evt1of4'),
            sources3 = make_list_of_sources('sge_data_EB_pt{lo}to{hi}_v13'),
            getters1 = var_vs_pt_getter_factory('phoScaleTrue'),
            getters2 = var_vs_pt_getter_factory('phoScale'),
            getters3 = var_vs_pt_fitresult_getter_factory('fitresult_data',
                                                          'phoScale'),
            ),
        ] # configurations
    return configurations
## End of get_scale_configs().

#______________________________________________________________________________
def make_scale_plots():
    '''
    Makes the canvases with the scale plots.
    '''
    global plotters
    #==========================================================================
    for cfg in get_scale_configs()[:]:
        ## MC, EB, 2011A+B, 1 of 4 statistically independent tests
        xtitle = 'Photon E_{T} (GeV)'
        ytitle = 'Photon Energy Scale (%)'
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

        canvas = canvases.next(cfg.name)
        plotter.plotall(title = cfg.title, 
                        legend_position = (0.68, 0.64, 0.92, 0.86),
                        yrange = (-3, 3),
                        styles = [20, 25, 26],
                        colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kRed])
        plotters.append(plotter)
        decorate(canvas)
    ## End of loop over configurations.
## End of make_scale_plots().

#______________________________________________________________________________
def decorate(canvas):
    '''
    Draw label(s) on the given canvas.
    '''
    canvas.cd()
    labels = []
    labels.append(Latex(['CMS 2011,  #sqrt{s} = 7 TeV'], 
                        position=(0.17, 0.93),
                        textsize=22))
                        
    labels.append(Latex(['L = 4.89 fb^{-1}'], position=(0.22, 0.8), 
                        textsize=22))
    for l in labels:
        l.draw()
    
    canvas.Modified()
    canvas.Update()
    latex_labels.extend(labels)
## End of decorate()


#______________________________________________________________________________
def main():
    '''
    Main entry point of execution.
    '''
    make_scale_plots()
    canvases
    canvases.make_pdf_from_eps()
    canvases.make_plots('eps C root'.split())
## End of main()


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
