'''
Plot photon energy scale fitted to the mass vs response
resolution with the PHOSPHOR method (scale versus resolution,
i.e. "svr").
'''

import os
import socket
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases
from JPsi.MuMu.common.binedges import BinEdges
from JPsi.MuMu.scaleFitter import subdet_r9_categories
from JPsi.MuMu.scaleFitter import subdet_categories
from JPsi.MuMu.escale.fitResultPlotter import FitResultPlotter

ROOT.gStyle.SetPadTopMargin(0.1)
canvases.wwidth = 400
canvases.wheight = 400
canvases.yperiod = 10

categories = list(subdet_r9_categories) + list(subdet_categories)
#binedges  = list(BinEdges([10, 12, 15, 20, 25, 30, 50]))
# binedges2 = list(BinEdges([10, 12, 15, 20, 25, 30, 999]))
# bincenters    = [0.5 * (lo + hi) for lo, hi in binedges]
## From JPsi/MuMu/test/escale/phosphor/results/et_bins.py
bincenters = [str(0.5 + 0.5 * i) for i in range(0, 20)]
binlowerrors = [0.25] * len(bincenters)
binhigherrors = [0.25] * len(bincenters)
#binhalfwidths = [0.5 * (hi - lo) for lo, hi in binedges]
xgetter_factory   = lambda: lambda workspace, i = iter(bincenters   ) : i.next()
exgetter_factory  = lambda: lambda workspace, i = iter(binhalfwidths) : i.next()
exlgetter_factory = lambda: lambda workspace, i = iter(binlowerrors ) : i.next()
exhgetter_factory = lambda: lambda workspace, i = iter(binhigherrors) : i.next()

plotters = []

oplus = lambda x,y: ROOT.TMath.Sqrt(x*x + y*y)

#______________________________________________________________________________
def get_basepath():
    '''
    Return the common part of the path to data files depending
    on the host machine.
    '''
    hostname_to_basepath_map = {
        't3-susy.ultralight.org':
#            '/raid2/veverka/jobs/outputs/regressions_no_muon_bias',
#            '/raid2/veverka/jobs/outputs/regressions_at_low_pt',
#            '/home/veverka/jobs/outputs/egm_fc_rscan',
            '/mnt/hadoop/user/veverka/phosphor/egm_fc_rscan',
        #'Jan-Veverkas-MacBook-Pro.local':
            #'/Users/veverka/Work/Data/phosphor/regressions_no_muon_bias',
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
    
    ## Common to all MC fits.
    if 'mc' in jobname_template.split('_'):
        snapshot = 'mc_fit'
    else:
        snapshot = None

    ## Loop over the pt bins:
    for rfit in bincenters:
        ## The job name encodes the pt, category and data/MC
        jobname = jobname_template + '_rfit' + rfit
        filename = jobname + '.root'
        
        filename = os.path.join(basepath, jobname, filename)
        if not os.path.exists(filename):
            continue
        if 'R9' in jobname:
            workspace = 'egm_mc_' + jobname + '_workspace'
        else:
            workspace = 'egm_fc_mc_' + jobname + '_workspace'
        
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
def diff_getter_factory(varname1, varname2):
    '''
    Returns a function that takes a workspace and returns the difference
    "varname1 - varname2" of the values of the variables of the 
    given names.
    '''
    return lambda workspace: (workspace.var(varname1).getVal() -         
                              workspace.var(varname2).getVal())
## diff_getter_factory(name)


#______________________________________________________________________________
def low_error_getter_factory(varname):
    '''
    Returns a function that takes a workspace and returns the error of the
    variable of the given name.
    '''
    return lambda workspace: -workspace.var(varname).getErrorLo()
## low_error_getter_factory(name)


#______________________________________________________________________________
def high_error_getter_factory(varname):
    '''
    Returns a function that takes a workspace and returns the error of the
    variable of the given name.
    '''
    return lambda workspace: workspace.var(varname).getErrorHi()
## high_error_getter_factory(name)


#______________________________________________________________________________
def sfit_high_error_getter_factory(varname):
    '''
    Returns a function that takes a workspace and returns the error of the
    variable of the given name.
    '''
    return lambda workspace: oplus(workspace.var(varname).getErrorHi(),
                                   0.0)
## high_error_getter_factory(name)


#______________________________________________________________________________
def sfit_low_error_getter_factory(varname):
    '''
    Returns a function that takes a workspace and returns the error of the
    variable of the given name.
    '''
    return lambda workspace: oplus(workspace.var(varname).getErrorLo(),
                                   0.0)
## sfit_low_error_getter_factory(name)

#______________________________________________________________________________
def strue_high_error_getter_factory(varname):
    '''
    Returns a function that takes a workspace and returns the error of the
    variable of the given name.
    '''
    return lambda workspace: 6.0 * workspace.var(varname).getErrorHi()
## strue_high_error_getter_factory(name)


#______________________________________________________________________________
def strue_low_error_getter_factory(varname):
    '''
    Returns a function that takes a workspace and returns the error of the
    variable of the given name.
    '''
    return lambda workspace: 6.0 * workspace.var(varname).getErrorLo()
## strue_low_error_getter_factory(name)


#______________________________________________________________________________
def sbias_high_error_getter_factory(fitvarname, truevarname):
    '''
    Returns a function that takes a workspace and returns the error of the
    difference "fit - true" of the variables of the given names.
    '''
    return lambda w: oplus(sfit_high_error_getter_factory(fitvarname)(w),
                           strue_high_error_getter_factory(truevarname)(w))
## strue_high_error_getter_factory(fitvarname, truevarname)


#______________________________________________________________________________
def sbias_low_error_getter_factory(fitvarname, truevarname):
    '''
    Returns a function that takes a workspace and returns the error of the
    difference "fit - true" of the variables of the given names.
    '''
    return lambda w: oplus(sfit_low_error_getter_factory(fitvarname)(w),
                           strue_low_error_getter_factory(truevarname)(w))
## strue_high_error_getter_factory(fitvarname, truevarname)


#______________________________________________________________________________
def rfit_high_error_getter_factory(varname):
    '''
    Returns a function that takes a workspace and returns the error of the
    variable of the given name.
    '''
    return lambda workspace: oplus(workspace.var(varname).getErrorHi(),
                                   0.2 * workspace.var(varname).getVal())
## high_error_getter_factory(name)


#______________________________________________________________________________
def rfit_low_error_getter_factory(varname):
    '''
    Returns a function that takes a workspace and returns the error of the
    variable of the given name.
    '''
    return lambda workspace: oplus(workspace.var(varname).getErrorLo(),
                                   0.2 * workspace.var(varname).getVal())
## rfit_low_error_getter_factory(name)


#______________________________________________________________________________
def rtrue_high_error_getter_factory(varname):
    '''
    Returns a function that takes a workspace and returns the error of the
    variable of the given name.
    '''
    return lambda workspace: 1.2 * workspace.var(varname).getErrorHi()
## rtrue_high_error_getter_factory(name)


#______________________________________________________________________________
def rtrue_low_error_getter_factory(varname):
    '''
    Returns a function that takes a workspace and returns the error of the
    variable of the given name.
    '''
    return lambda workspace: 1.2 * workspace.var(varname).getErrorLo()
## rtrue_low_error_getter_factory(name)


#______________________________________________________________________________
def xyasymmerrors_bias_vs_var_getter_factory(xvarname, yfitvarname, 
                                             ytruevarname):
    """
    Returns a tuple of 6 functions that take a workspace and return
    x, y, exl, exh, eyl, eyh where x corresponds to the values 
    and asymmetric error of workspace variable of the given name
    xvarname, and y to the bias "fit - true" of the variable
    of the names yfitvarname - ytruevarname.
    """
    xgetter  = value_getter_factory(xvarname)
    exlgetter = rtrue_low_error_getter_factory(xvarname)
    exhgetter = rtrue_high_error_getter_factory(xvarname)
    ygetter  = diff_getter_factory(yfitvarname, ytruevarname)
    eylgetter = sbias_low_error_getter_factory(yfitvarname, ytruevarname)
    eyhgetter = sbias_high_error_getter_factory(yfitvarname, ytruevarname)
    return (xgetter, ygetter, exlgetter, exhgetter, eylgetter, eyhgetter)
## End of xyasymmerrors_bias_vs_var_getter_factory(xvarname, yfitvarname, 
##                                                 ytruevarname)


#______________________________________________________________________________
def xyasymmerrors_var_vs_pt_getter_factory(varname):
    """
    Returns a tupler of 6 functions that take a workspace and return
    x, y, exl, exh, eyl, eyh where y, eyl and eyh correspond to the value 
    and asymmetric error of a workspace variable of the given name 
    and x and exl, and exh, are pt bins defined in the global 
    xgetter_factory, exlgetter_factory, exhgetter_factory functions.
    """
    xgetter  = xgetter_factory()
    exlgetter = exlgetter_factory()
    exhgetter = exhgetter_factory()
    ygetter  = value_getter_factory(varname)
    eylgetter = low_error_getter_factory(varname)
    eyhgetter = high_error_getter_factory(varname)
    return (xgetter, ygetter, exlgetter, exhgetter, eylgetter, eyhgetter)
## End of xyasymmerrors_var_vs_pt_getter_factory(varname)


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

configurations = []
for cat in categories:
    fitresult = 'fitresult_data'
    cfg = Config(
        ## Canvas name
        name = 'egm_fc_rscan_%s' % (cat.name,), 
        ## Canvas title
        title = ', '.join(cat.labels),
        ## Axis titles
        xtitle = 'True E^{#gamma} Resolution (%)',
        ytitle = 'Fitted - True E^{#gamma} Scale (%)',
        ## Initialize maps for sources and getters
        ## keys 1-4 correspond to evt1of4, evt2of4, ..., evt4of4
        sources = [],
        titles = [],
        getters = [],
        )
    for title, version in [('Jan12 rereco + Rochcor', 'yyv5'),
                           ]:        
        ## Add the sources and getters
        labels = []
        ## EB/EE label
        labels.append(cat.name.split('_')[0])
        labels.append('pt25to999')
        labels.append(version)        
        if '_' in cat.name:
            ## R9 label
            labels.append(cat.name.split('_')[1])
        jobname_template = '_'.join(labels)
        cfg.sources.append(make_list_of_sources(jobname_template))
        cfg.titles.append(cat.title)
        cfg.getters.append(
            xyasymmerrors_bias_vs_var_getter_factory('phoResTrue',
                                                     'phoScale',
                                                     'phoScaleTrue')
            )
    configurations.append(cfg)
## End of loop categories


#==============================================================================
def make_plots(configurations):
    '''
    For each configuration in the given list, overlays the graphs of 
    scale versus pt for all sets of measurements specified.
    These measurements are either from the true or the PHOSPHOR fit.
    '''
    for cfg in configurations[:]:
        ## Only check EE 2011AB
        #if (not 'EE_lowR9' in cfg.name) or (not 'AB' in cfg.name):
            #continue
        ### Only check 2011AB
        #if not 'AB' in cfg.name:
            #continue
        ## MC, EB, 2011A+B, 1 of 4 statistically independent tests
        plotter = FitResultPlotter(cfg.sources[0], cfg.getters[0], cfg.xtitle, 
                                   cfg.ytitle, title = cfg.titles[0],
                                   name=cfg.name, 
                                   xasymmerrors=True,
                                   yasymmerrors=True,
                                   colors = [ROOT.kBlack])                          

        for isources, igetters, ititle in zip(cfg.sources, 
                                              cfg.getters, 
                                              cfg.titles):
            plotter.sources = isources
            plotter.getters = igetters
            plotter.title = ititle
            plotter.getdata()
            plotter.makegraph()
            # plotter.graph.Fit('pol1')

        canvases.next('c_' + cfg.name).SetGrid()
        plotter.graph.Draw('ap')
        plotter.graph.GetXaxis().SetTitle(cfg.xtitle)
        plotter.graph.GetYaxis().SetTitle(cfg.ytitle)
        #if 'EE_highR9' in cfg.name:
            #plotter.plotall(title = cfg.title,
                            ##xrange = (0, 10),
                            ##yrange = (0, 10),
                            #legend_position = 'topright')
        #else:
            #plotter.plotall(title = cfg.title,
                            ##xrange = (5, 55),
                            #legend_position = 'topright')
        #plotter.graphs[0].Draw('p')
        canvases.canvases[-1].Modified()
        canvases.canvases[-1].Update()
        canvases.update()
        plotters.append(plotter)
    ## End of loop over configurations.
## End of make_scale_plots(..)

#==============================================================================
def save_graphs_to_file(plotters, filename):
    '''
    Saves graphs attached to the list of FitResultPlotter objects "plotters"
    to a root file of the given filename.
    '''
    title_to_name_map = {
       'No Regr.': 'noregr',
       'Caltech': 'caltech',
       'MIT v2': 'mit2',
       'Jan12 rereco': 'jan2012rereco',
       'Jul12 rereco': 'jul2012rereco',
       }
    rootfile = ROOT.TFile.Open(filename, 'RECREATE')
    for plotter in plotters:
        for graph, title in zip(plotter.graphs, plotter.titles):
            name = title_to_name_map[title]
            graph.SetName(plotter.name + '_' + name)
            graph.Write()
    rootfile.Write()
    rootfile.Close()
## End of save_graphs_to_file(..)

#==============================================================================
def main():
    '''
    Main entry point of execution.
    '''
    # make_scale_plots(scale_configurations)
    make_plots(configurations[:])
    # save_graphs_to_file(plotters, 'test.root')
## End of main(..)


#==============================================================================
if __name__ == '__main__':
    main()
    import user
    