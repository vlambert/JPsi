
'''
Photon Energy Scale (PhoES) and Photon Energy Resolution (PHOSPHOR) Fit model 5.

Model Z+jets background with a parametrized KEYS pdf trained on MC.
Model other backgrounds with an exponential.
Use custom class for the signal PDF that caches and interpolates
the normalization integral to speed up the fitting and reduce numerical noise. 

Jan Veverka, Caltech, 17 February 2012.
'''

## TODO LIST:
## - Store fit results only
## - Add model validation plots
##     - probability density vs mmg mass and phos
##     - switch the x and y axis for the probability density vs mmg and phor
##     - mmg spectra for the reference phor values
## - Add fit validation plots
##     - Likelihood scans vs phos phor and purity
##     - Likelihood profiles vs phos phor and purity
##     - 2D likelihood scan vs phos and phor
## - Support for different tree version for model training and fit, e.g.
##   test_mc_EE_highR9_pt30to999_v13model_v15fit
## - Understand crashes when model is read from a file


##- Boilerplate imports --------------------------------------------------------
import math
import re
import sys


import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf
from JPsi.MuMu.common.parametrizedndkeyspdf import ParametrizedNDKeysPdf
from JPsi.MuMu.escale.logphoereskeyspdf import LogPhoeresKeysPdf
from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator
from JPsi.MuMu.escale.phosphormodel5 import PhosphorModel5

from JPsi.MuMu.phosphor.globals import Globals, use_independent_fake_data

##-- Configuration -------------------------------------------------------------
## Selection
# name = 'EB_highR9_pt15to20'

##  Fits events passing Event$ % 4 == 0 and uses all the other events to build 
##+ the model.

#name = 'test_mc_EE_highR9_pt30to999_v13_evt1of4' #Original Line from jan

#name = 'test_data_EB_pt25to999_yyv3_evt1of4_R9Range0.0to0.823'
name = 'test_CRIS_data_EB_pt25to999_yyv3_evt1of4_R9Range0.0to0.823'

## Fits the same MC events that were used for the model training
# name = 'test_mc_EE_highR9_pt30to999_v13'

## Fits real data
# name = 'test_data_EE_highR9_pt30to999_v13'

inputfile = 'phosphor5_model_and_fit_' + name + '.root'
outputfile = 'phosphor5_model_and_fit_' + name + '.root'

strain = 'nominal'
rtrain = 'nominal'

sfit = 'nominal'
rfit = 'nominal'

fit_data_fraction = 0.25
reduce_data = False

#fake_data_cut = 'Entry$ % 4 == 0'
#use_independent_fake_data = True

sw = ROOT.TStopwatch()
sw2 = ROOT.TStopwatch()

times = []


##------------------------------------------------------------------------------
def parse_command_line_arguments():
    '''
    Uses the name supplied as a command-line argument if any.
    '''
    global name, inputfile, outputfile
    
    ## Use the name supplied on the command-line if any:
    for arg in sys.argv[1:]:
        ## Skip options
        if arg[0] == '-':
            continue
        else:
            name = arg
            inputfile = 'phosphor5_model_and_fit_' + name + '.root'
            outputfile = 'phosphor5_model_and_fit_' + name + '.root'
## End of parse_command_line_arguments().    
    

##------------------------------------------------------------------------------
def parse_name_to_fake_data_cut(name):
    '''
    Parses the name for a fake data cut for MC of the form evtKofN.
    This corresponds to Event$ % N == (K-1) for the fit data.
    '''
    fake_data_cut = None

    pattern = re.compile(
        r'''evt  # short for "event" at the beginning
           (\d+) # integer K giving the K-th section
           of    # preposition separating the two integers
           (\d+) # integer N giving the total number of sections
           ''', re.VERBOSE)
    
    parsed = False
    
    for tok in name.split('_'):
        match = pattern.match(tok)
        if match:
            section = int(match.group(1))
            total_sections = int(match.group(2))
            if parsed or section < 1 or total_sections < section:
                raise RuntimeError, 'Illegal token %s in %s' % (tok, name)
            fake_data_cut = 'Entry$ % {N} == {K}'.format(
                N = total_sections, K = int(section) - 1
                )
            parsed = True

    print "==================FAKE DATA CUT==========================", fake_data_cut
    return fake_data_cut
## End of parse_name_to_fake_data_cut().


##------------------------------------------------------------------------------
def parse_name_to_use_real_data(name):
    '''
    Parses the name and decides whether to use real data or MC for the fit.
    Returns True if the former is true, False otherwise.
    If the name is split into tokens separated by the underscore "_" and
    one of the tokens is "data" then it means that real data should be fitted,
    otherwise use MC for the fit.
    '''
    for tok in name.split('_'):
        if tok == 'data':
            return True
    return False
## End of parse_name_to_use_real_data(name)


##------------------------------------------------------------------------------
def parse_name_to_cuts():
    'Parse the name and apply the relevant cuts.'
    global name
    
    global cuts
    cuts = ['mmMass + mmgMass < 180', 'minDeltaR < 1.5']
    if 'EB' in name:
        cuts.append('phoIsEB')
        if 'highR9' in name:
            cuts.append('phoR9 > 0.94')
        elif 'lowR9' in name:
            cuts.append('phoR9 < 0.94')
    elif 'EE' in name:
        cuts.append('!phoIsEB')
        if 'highR9' in name:
            cuts.append('phoR9 > 0.95')
        elif 'lowRl9' in name:
            cuts.append('phoR9 < 0.95')

    if 'pt' in name:
        ## Split the name into tokens.
        for tok in name.split('_'):
            ## Get the token with the pt

            print '================WHAT IS IN TOK==================-----> ', tok
            if 'pt' in tok:
                if '-' in tok:
                    separator = '-'
                elif 'to' in tok:
                    separator = 'to'
                else:
                    raise RuntimeError, 'Error parsing %s in %s!' % (tok, name)
                lo, hi = tok.replace('pt', '').split(separator)
                print '================LOW AND HIGH PT==================-----> ', lo, ' ', hi 
                cuts.append('%s <= phoPt & phoPt < %s' % (lo, hi))

    if 'R9Range' in name:
        ## Split the name into tokens.
        for tok1 in name.split('_'):
            ## Get the token with the pt

            print '================WHAT IS IN TOK1==================-----> ', tok1
            if 'R9Range' in tok1:
                if '-' in tok1:
                    separator = '-'
                elif 'to' in tok1:
                    separator = 'to'
                else:
                    raise RuntimeError, 'Error parsing %s in %s!' % (tok1, name)
                loR9, hiR9 = tok1.replace('R9Range', '').split(separator)
                print '================LOW AND HIGH PT==================-----> ', loR9, ' ', hiR9
                cuts.append('%s < phoR9 & phoR9 <= %s' % (loR9, hiR9))
   
    global model_tree_version, data_tree_version
    ## Set the default
    model_tree_version, data_tree_version = 'v11', 'v11'
    
    for tree_version in 'yyv1 yyv2 yyv3 yyv3_e5x5 v11 v13 v14 v15'.split():
        if tree_version in name.split('_'):
            model_tree_version = data_tree_version = tree_version  
    
    global fake_data_cut, use_independent_fake_data
    fake_data_cut = parse_name_to_fake_data_cut(name)
    if fake_data_cut:
        use_independent_fake_data = True
    else:
        use_independent_fake_data = False

    global use_real_data
    use_real_data = parse_name_to_use_real_data(name)

    ##Need to add this line to implement Global variable outside phosphor calculator
    Globals.use_real_data = use_real_data
        
## End of parse_name_to_cuts().


##------------------------------------------------------------------------------
def parse_name_to_title():
    'Parse the name and translate it into a title.'
    global title
    global latex_labels
    global latex_title
    tokens = []
    latex_labels = []

    parse_name_to_cuts()
    
    if model_tree_version in 'v11'.split():
        tokens.append('2011A+B PU S4 MC Model')
        latex_labels.append('2011A+B PU S4 MC Model')
    elif model_tree_version in 'v13 yyv1 yyv2 yyv3 yyv3_e5x5'.split():
        tokens.append('2011A+B PU S6 MC Model')
        latex_labels.append('2011A+B PU S6 MC Model')
    elif model_tree_version == 'v14':
        tokens.append('2011A PU S6 MC Model')
        latex_labels.append('2011A PU S6 MC Model')        
    elif model_tree_version == 'v15':
        tokens.append('2011B PU')
        latex_labels.append('2011B PU S6 MC Model')
    
    if 'EB' in name:
        tokens.append('Barrel')
        latex_labels.append('Barrel')
        if 'highR9' in name:
            tokens.append('R9 > 0.94')
            latex_labels.append('R_{9}^{#gamma} > 0.94')
        elif 'lowR9' in name:
            tokens.append('R9 < 0.94')
            latex_labels.append('R_{9}^{#gamma} < 0.94')
    elif 'EE' in name:
        tokens.append('Endcaps')
        latex_labels.append('Endcaps')
        if 'highR9' in name:
            tokens.append('R9 > 0.95')
            latex_labels.append('R_{9}^{#gamma} > 0.95')
        elif 'lowR9' in name:
            tokens.append('R9 < 0.95')
            latex_labels.append('R_{9}^{#gamma} < 0.95')

    if 'pt' in name:
        ## Split the name into tokens.
        for tok in name.split('_'):
            ## Get the token with the pt
            if 'pt' in tok:
                if '-' in tok:
                    separator = '-'
                elif 'to' in tok:
                    separator = 'to'
                else:
                    raise RuntimeError, 'Error parsing %s in %s!' % (tok, name)
                lo, hi = tok.replace('pt', '').split(separator)
                tokens.append('pt %s-%s GeV' % (lo, hi))
                latex_labels.append(
                    'E_{T}^{#gamma} #in [%s, %s] GeV' % (lo, hi)
                    )

    
    if model_tree_version in 'yyv1 v11 v12 v13 v14 v15'.split():
        tokens.append('Default Cluster Corr.')
        latex_labels.append('Default Cluster Corr.')
    elif model_tree_version == 'yyv2':        
        tokens.append('Caltech Regression')
        latex_labels.append('Caltech Regression')
    elif model_tree_version == 'yyv3':        
        tokens.append('Hgg v2 Regression')
        latex_labels.append('Hgg v2 Regression')
    elif model_tree_version == 'yyv3_e5x5':        
        tokens.append('E5x5')
        latex_labels.append('E5x5')

    title = ', '.join(tokens)
    latex_title = ', '.join(latex_labels)
## End of parse_name_to_title().


##------------------------------------------------------------------------------
def define_globals():
    '''
    Define global variables, title, cuts, outputfilename, workspace w.
    '''
    global plots
    plots = []
    parse_name_to_cuts()    
    parse_name_to_title()
## End of define_globals()


##------------------------------------------------------------------------------
def define_workspace():
    '''
    Define the default workspace w.
    '''
    global w
    w = ROOT.RooWorkspace(name + '_workspace')
## End of define_workspace().  
  

##------------------------------------------------------------------------------
def read_workspace_from_file(filename):
    '''
    Read the default workspace w from a file of the given filename.
    '''
    global w
    w = ROOT.TFile.Open(filename).Get(name + '_workspace')
## End of read_workspace_from_file()


##------------------------------------------------------------------------------
def define_data_observables():
    '''
    Defines variables for observables in data in the workspace as python 
    globals.
    '''
    global mmgMass, mmMass, phoERes, mmgMassPhoGenE, weight
    mmgMass        = w.factory('mmgMass[40, 140]')
    mmMass         = w.factory('mmMass[10, 140]')
    phoERes        = w.factory('phoERes[-70, 100]')
    mmgMassPhoGenE = w.factory('mmgMassPhoGenE[0, 200]')
    weight         = w.factory('weight[1]')

    ## Dictionary for variable properties (name) -> (title, unit)
    title_unit_map = {
        'mmgMass': 'm_{#mu#mu#gamma} GeV'.split(),
        'mmMass' : 'm_{#mu#mu} GeV'.split(),
        'phoERes': ('E_{reco}^{#gamma}/E_{gen}^{#gamma} - 1', ''),
        'mmgMassPhoGenE': ('gen. level m_{#mu#mu#gamma}', 'GeV'),
        }

    ## Set nice latex names and titles:
    for xname, (xtitle, xunit) in title_unit_map.items():
        xvar = w.var(xname)
        xvar.SetTitle(xtitle)
        xvar.setUnit(xunit)
## End of define_data_observables()


##------------------------------------------------------------------------------
def read_data_observables_from_workspace(workspace):
    '''
    Reads variables for observables in data from a given workspace
    and defines them as python globals.
    '''
    global mmgMass, mmMass, phoERes, mmgMassPhoGenE, weight
    mmgMass        = workspace.var('mmgMass')
    mmMass         = workspace.var('mmMass')
    phoERes        = workspace.var('phoERes')
    mmgMassPhoGenE = workspace.var('mmgMassPhoGenE')
    weight         = workspace.var('weight')
## End of read_data_observables_from_file()


##------------------------------------------------------------------------------
def set_ranges_for_data_observables():
    '''
    Sets the ranges used for fitting and plotting.
    '''
    mmgMass.setRange('plot', 70, 110)
    mmgMass.setRange('fit', 60, 120)
## End of set_ranges_for_data_observables().


##------------------------------------------------------------------------------
def define_model_parameters():
    '''
    Defines model parameters and related variables in the workspace 
    as python globals.
    '''
    ## Define model parameters.
    global phoScale, phoRes, phoScaleTrue, phoResTrue
    phoScale     = w.factory('phoScale[0,-50,50]')
    phoRes       = w.factory('phoRes[3,0.1,20.1]')
    phoScaleTrue = w.factory('phoScaleTrue[0,-50,50]')
    phoResTrue   = w.factory('phoResTrue[1.5,0.01,50]')

    ## Prep for storing fit results in the workspace.
    global phoScaleTarget, phoResTarget, params
    phoScaleTarget = w.factory('phoScaleTarget[0,-50,50]')
    phoResTarget   = w.factory('phoResTarget[5,0.01,50]')
    params         = ROOT.RooArgSet(phoScaleTarget, phoResTarget)
    w.defineSet('params', params)

    ## Set units.
    for x, u in zip([phoScale, phoRes, phoScaleTrue, phoResTrue,
                     phoScaleTarget, phoResTarget],
                    '% % % % % %'.split()):
        x.setUnit(u)

## End of define_model_parameters().


##------------------------------------------------------------------------------
def read_model_parameters_from_workspace(workspace):
    '''
    Reads model parameters form the given workspace and defines them as 
    python globals.
    '''
    global phoScale, phoRes, phoScaleTrue, phoResTrue
    phoScale     = workspace.var('phoScale')
    phoRes       = workspace.var('phoRes')
    phoScaleTrue = workspace.var('phoScaleTrue')
    phoResTrue   = workspace.var('phoResTrue')
    
    
    ## Prep for storing fit results in the workspace.
    global phoScaleTarget, phoResTarget, params
    phoScaleTarget = workspace.var('phoScaleTarget')
    phoResTarget   = workspace.var('phoResTarget')
    params         = workspace.set('params')
  
## End of read_model_parameters_from_workspace


##------------------------------------------------------------------------------
def set_signal_model_normalization_integral_cache_binnings():
    '''
    Define the binning for the normalization integral caching.
    '''
    ## This setting was used as a default for Adi's e/gamma paper placeholders.
    phosbins = ROOT.RooBinning(15, -15, 15, 'normcache')
    phorbins = ROOT.RooBinning(15, 0.1, 25.1, 'normcache')
    phoScale.setBinning(phosbins, 'normcache')
    phoRes.setBinning(phorbins, 'normcache')
## End of set_signal_model_normalization_integral_cache_binnings().


##------------------------------------------------------------------------------
def define_mass_derivative_function_and_mean():
    '''
    Defines the function for the derivateve of the logarithm of the 
    mu-mu-gamma system invariant mass w.r.t. to photon energy
    d log m(mmg) / d log E(g) 
    and a variable holding it's mean for a given sample.  These are created
    in the workspace and declared as python global variables.
    '''
    global xfunc
    xfunc = w.factory('''FormulaVar::xfunc(
        "0.5 * (1 - mmMass^2 / mmgMass^2)",
        {mmMass, mmgMass}
        )''')

    global xmean
    xmean = w.factory('xmean[0.1, 0, 1]')
## End of define_mass_derivative_function_and_mean()


##------------------------------------------------------------------------------
def read_mass_derivative_function_and_mean_from_workspace(workspace):
    '''
    Reads the function for the derivateve of the logarithm of the 
    mu-mu-gamma system invariant mass w.r.t. to photon energy
    d log m(mmg) / d log E(g) 
    and a variable holding it's mean for a given sample from thei
    given workspace.  These are declared as python global variables.
    '''
    global xfunc, xmean
    xfunc = workspace.function('xfunc')
    xmean = workspace.var('xmean')
## End of read_mass_derivative_function_and_mean_from_workspace().


##------------------------------------------------------------------------------
def replace_variable_titles(new_titles, workspace):
    '''
    Replaces the titles of variables in the workspace using the given
    dictionary (name)->(new title) and returns the dictionary of the
    original titles (name)->(old title).
    '''
    old_titles = {}
    for name in new_titles:
        old_titles[name] = workspace.var(name).GetTitle()
        workspace.var(name).SetTitle(new_titles[name])
    return old_titles
## End of replace_variable_titles().


##------------------------------------------------------------------------------
def set_default_integrator_precision(eps_abs, eps_rel):
    '''
    Sets the default integration relative and absolute precition to eps
    and returns the old precision values
    '''
    old_precision = (ROOT.RooAbsReal.defaultIntegratorConfig().epsAbs(),
                     ROOT.RooAbsReal.defaultIntegratorConfig().epsRel())
    ROOT.RooAbsReal.defaultIntegratorConfig().setEpsAbs(eps_abs)
    ROOT.RooAbsReal.defaultIntegratorConfig().setEpsRel(eps_rel)
    return old_precision
## End of set_default_integrator_precision.


##------------------------------------------------------------------------------
def get_data(chains = getChains('v11')):
    '''
    Get the nominal data that is used for smearing.
    '''
    global cuts
    if Globals.debug:
        print '====== CUTS INSIDE phosphorcalculator ======', cuts

    ## TODO: Break this down into several smaller methods.
    ## Map of variable names and corresponding TTree expressions to
    ## calculate it.
    expression_map = {
        'mmgMass': 'mmgMass',
        'mmMass' : 'mmMass' ,
        'phoERes'    : '100 * phoERes',
        'mmgMassPhoGenE': ('threeBodyMass(mu1Pt, mu1Eta, mu1Phi, 0.106, '
                            '              mu2Pt, mu2Eta, mu2Phi, 0.106, '
                            '              phoGenE * phoPt / phoE, '
                            '                     phoEta, phoPhi, 0)'),
        'weight' : 'pileup.weight',
        }
    
    ## The TFormula expression defining the data is given in the titles.
    # print '+++ DEBUG: before title replacement:', mmgMass.GetTitle()
    latex_map = replace_variable_titles(expression_map, w)
    # print '+++ DEBUG: after title replacement:', mmgMass.GetTitle()
    #global cuts
    ## Create a preselected tree
    tree = {}
    tree['z'] = chains['z'].CopyTree('&'.join(cuts))
    # dtree = chains['data'].
    ## Have to copy aliases by hand
    
    for a in chains['z'].GetListOfAliases():
        tree['z'].SetAlias(a.GetName(), a.GetTitle())

    cuts0 = cuts[:]
    cuts1 = cuts[:]
    if use_independent_fake_data:
        cuts0.append('!(%s)' % fake_data_cut)
        cuts1.append(fake_data_cut)
           
    ## Get the nominal dataset
    global data
    data = {}
    for xvar in [weight, mmgMass, mmMass, phoERes, mmgMassPhoGenE]:
        print xvar.GetName(), ':', xvar.GetTitle()        
    
    data['fsr0'] = dataset.get(tree=tree['z'], weight=weight,
                               cuts = cuts0 + ['isFSR'],
                               variables=[mmgMass, mmMass, phoERes,
                                          mmgMassPhoGenE])
    data['fsr1'] = dataset.get(tree=tree['z'], weight=weight,
                               cuts=cuts1 + ['isFSR'],
                               variables=[mmgMass, mmMass, phoERes,
                                          mmgMassPhoGenE])
    data['zj0'] = dataset.get(tree=tree['z'], weight=weight,
                              cuts=cuts0 + ['!isFSR'],
                              variables=[mmgMass, mmMass])
    data['zj1'] = dataset.get(tree=tree['z'], weight=weight,
                              cuts=cuts1 + ['!isFSR'],
                              variables=[mmgMass, mmMass])

    ## Set units and nice titles
    replace_variable_titles(latex_map, w)
        
    ## Do we want to reduce the data?
    if reduce_data:
        reduced_entries = int( (1 - fit_data_fraction) * 
                               data['fsr0'].numEntries() )
        data['fsr0'] = data['fsr0'].reduce(
            roo.EventRange(0, int(reduced_entries))
            )

    data['zj0'].SetName('zj0_mc')
    w.Import(data['zj0'])

    ##-- Calculate MC Truth Purity ---------------------------------------------
    if use_independent_fake_data:
        num_fsr_events = data['fsr1'].sumEntries()
        num_zj_events = data['zj1'].sumEntries()
    else:
        num_fsr_events = data['fsr0'].sumEntries()
        num_zj_events = data['zj0'].sumEntries()
    global fsr_purity
    fsr_purity = 100 * num_fsr_events / (num_fsr_events + num_zj_events)
    
    ##-- Get Smeared Data ------------------------------------------------------
    old_precision = set_default_integrator_precision(2e-9, 2e-9)
    global calibrator0, calibrator1, fit_calibrator
    calibrator0 = MonteCarloCalibrator(data['fsr0'], printlevel=1, rho=1.5)
    if use_independent_fake_data:
        calibrator1 = MonteCarloCalibrator(data['fsr1'], printlevel=1, rho=1.5)
        fit_calibrator = calibrator1
    else:
        fit_calibrator = calibrator0
    set_default_integrator_precision(*old_precision)

    ##-- Check the time -------------------------------------------------------
    check_timer(
        '1. init and get_data (%d entries)' % (
            data['fsr0'].numEntries() + data['fsr1'].numEntries() +
            data['zj0'].numEntries() + data['zj1'].numEntries()
            )
        )
## End of get_data.


##------------------------------------------------------------------------------
def get_confint(x, cl=5):
    if x.hasAsymError():
        if x.getErrorHi() <= 0.:
            ehi = x.getError()
        else:
            ehi = x.getErrorHi()
        if x.getErrorLo() >= 0.:
            elo = -x.getError()
        else:
            elo = x.getErrorLo()
        return (max(x.getVal() + cl * elo, x.getMin()),
                min(x.getVal() + cl * ehi, x.getMax()))
    else:
        return (max(x.getVal() - cl * x.getError(), x.getMin()),
                min(x.getVal() + cl * x.getError(), x.getMax()))
## End of get_confint().


##------------------------------------------------------------------------------
def unite_intervals(ilist):
    '''Takes a list of n 1-dimensional intervals [(a_1, b_1), (a_2, b_2), ...,
    (a_n, b_n)] where a_i < b_i and returns their union
    (min(a_1, .., a_n), max(a_1, .., a_n)).'''
    lower_bounds, upper_bounds = zip(*ilist)
    return (min(lower_bounds), max(upper_bounds))
## End of unite_intervals()


##------------------------------------------------------------------------------
def check_timer(label = ''):
    sw.Stop()
    ct, rt = sw.CpuTime(), sw.RealTime()
    print '+++', label, 'CPU time:', ct, 's, real time: %.2f' % rt, 's'
    sw.Reset()
    sw.Start()
    times.append((label, ct, rt))
    return ct, rt
## End of check_timer()


##------------------------------------------------------------------------------
def outro(make_plots=True, save_workspace=True):
    'Closing stuff'
    canvases.update()
    if make_plots:
        canvases.make_plots(['png', 'eps'])

    if save_workspace:
        for c in canvases.canvases:
            if c:
                w.Import(c, 'c_' + c.GetName())
        w.writeToFile(outputfile, False)

    check_timer('14. outro')
    
    ct, rt = sw2.CpuTime(), sw2.RealTime()
    print '+++ TOTAL CPU time:', ct, 's, real time: %.2f' % rt, 's'
## End of outro().


##------------------------------------------------------------------------------
def build_signal_model():       
    '''Builds the signal model and stores it as a global variable signal_model.'''
    
    ## Define the binning for the 2D histograms sampled off of the moment 
    ## morphs.
    mmgMass.setBins(500, 'cache')
    phoRes.setBins(100, 'cache')
    # phoScale.setBins(40, 'cache')
    # phortargets =  [0.5 + 0.5 * i for i in range(30)]

    ## This was used as a default for Adi's placeholders plots
    phortargets = [0.1, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 25]

    # phortargets = [0.5, 6, 7, 7.5, 8, 8.5, 8.75, 9, 9.5, 10, 10.5, 11, 11.5, 11.75, 12, 12.5, 13, 14]
    # phortargets = [0.5, fit_calibrator.r0.getVal(), 10, 20]
    # phortargets.append(fit_calibrator.r0.getVal())
    phortargets.sort()

    ROOT.RooAbsReal.defaultIntegratorConfig().setEpsAbs(0.1e-08)
    ROOT.RooAbsReal.defaultIntegratorConfig().setEpsRel(0.1e-08)

    ## Build the signal PDF
    global signal_model
    signal_model = PhosphorModel5('signal_model0', 'signal_model0',
                                  mmgMass, phoScale, phoRes,
                                  data['fsr0'], w, 'nominal', phortargets,
                                  rho=1.5)

    ROOT.RooAbsReal.defaultIntegratorConfig().setEpsAbs(1e-07)
    ROOT.RooAbsReal.defaultIntegratorConfig().setEpsRel(1e-07)

    check_timer('2. build PhosphorModel5')

    # signal_model.getVal(ROOT.RooArgSet(mmgMass))
    signal_model.analyticalIntegral(1, 'fit')
    check_timer('2.1 get the nomalization integral cache for range fit')
    signal_model.analyticalIntegral(1, 'plot')
    check_timer('2.2 get the nomalization integral cache for range plot')
    signal_model.analyticalIntegral(1, '')
    check_timer('2.3 get the nomalization integral cache for range <none>')

    w.Import(signal_model)
## End of build_signal_model


##------------------------------------------------------------------------------
def build_model():
    '''Builds the PDFs for the backgrounds and the full signal + background
    model.'''
    build_signal_model()

    ## Build the Z+jets background PDF.
    global zj_pdf
    zj_pdf = ROOT.RooKeysPdf('zj0_pdf', 'zj0_pdf', mmgMass,
                            data['zj0'], ROOT.RooKeysPdf.NoMirror, 3)
    w.Import(zj_pdf)

    ## Build the PDF for other backgrounds.
    global bkg_pdf
    bkg_pdf = w.factory('Exponential::bkg_pdf(mmgMass, bkg_c[-1,-10,10])')

    ## Build the composite model PDF
    global pm
    pm = w.factory(
        ## '''SUM::{name}_pm5({name}_signal_N[1000,0,1e6] * {name}_signal_model,
        ##                    {name}_zj_N    [10,0,1e6]   * {name}_zj_pdf,
        ##                    {name}_bkg_N   [10,0,1e6]   * {name}_bkg_pdf)
        ## '''SUM::{name}_pm5({name}_signal_N[1000,0,1e6] * {name}_signal_model,
        ##                    {name}_zj_N[50,0,1e6] * {name}_zj_pdf)
        ## '''.format(name=name)
        'SUM::pm(signal_f[0.97,0,1] * signal_model0, zj0_pdf)'
        )
    
    check_timer('2.4 build full S+B model')
## End build_full_model()
        

##------------------------------------------------------------------------------
def read_model_from_workspace(workspace):
    '''
    Reads the full signa + background model from a given workspace.
    '''
    global signal_model, zj_pdf, bkg_pdf, pm
    signal_model = workspace.pdf('signal_model0')
    zj_pdf = workspace.pdf('zj0_pdf')
    bkg_pdf = workspace.pdf('bkg_pdf')
    pm = workspace.pdf('pm')
## End of read_model_from_workspace().


##------------------------------------------------------------------------------
def init():
    '''
    Initialize workspace and common variables and functions.
    '''
    define_globals()
    define_workspace()
    define_data_observables()
    define_model_parameters()
    define_mass_derivative_function_and_mean()   
    set_ranges_for_data_observables()
    set_signal_model_normalization_integral_cache_binnings()
    get_data(getChains(model_tree_version))
    build_model()
## End of init().

##------------------------------------------------------------------------------
def init_cfg_file():
    '''
    Initialize workspace and common variables and functions.
    '''
    global cuts, model_tree_version, data_tree_version, latex_title, latex_labels, outputfile, name
    cuts = Globals.cuts
    data_tree_version = model_tree_version = Globals.model_tree_version
    name = latex_title = latex_labels = Globals.latex_title
    outputfile = Globals.outputfile
    if Globals.debug:
        print '======Model Tree Version======', model_tree_version
        print '======Cuts Inside phosphorcalculator======', cuts
        print '======Latex Title Inside phosphorcalculator======', latex_title
        print '======Output File Inside phosphorcalculator======', outputfile
        print '===== name =====', name
        
    define_workspace()
    define_data_observables()
    define_model_parameters()
    define_mass_derivative_function_and_mean()   
    set_ranges_for_data_observables()
    set_signal_model_normalization_integral_cache_binnings()
    get_data(getChains(model_tree_version))
    build_model()
## End of init().


##------------------------------------------------------------------------------
# NOT USED ANYMORE
def init_from_file(filename):
    '''
    Initialize workspace and common variables and functions from a file
    of the given filename.
    '''
    define_globals()
    read_workspace_from_file(filename)
    read_data_observables_from_workspace(w)
    read_model_parameters_from_workspace(w)
    read_mass_derivative_function_and_mean_from_workspace(w)
    set_ranges_for_data_observables()
    set_signal_model_normalization_integral_cache_binnings()
    get_data(getChains(model_tree_version))
    read_model_from_workspace(w)
    # build_model()
## End of init_from_file().


#-------------------------------------------------------------------------------
def get_real_data(label):
    '''
    Get real data for the dataset specified by the label: "data" (full 2011A+B),
    "2011A" or "2011B".
    '''
    global model_tree_version, data_tree_version
    if model_tree_version == 'v11':
        data_tree_version = 'v12'
    if model_tree_version in 'v13 v14 v15'.split():
        data_tree_version = 'v15'
    dchain = getChains(data_tree_version)[label]
    expression_title_map = {
        'weight': '1',
        'mmgMass': 'mmgMass',
        'mmMass': 'mmMass',
        }
    latex_title_map = replace_variable_titles(expression_title_map, w)
    # weight.SetTitle('1')
    # mmgMass.SetTitle('mmgMass')
    # mmMass.SetTitle('mmMass')
    dataset.variables = []
    dataset.cuts = []
    data[label] = dataset.get(tree=dchain, cuts=cuts[:],
                               variables=[mmgMass, mmMass],
                               weight=weight)
    # mmgMass.SetTitle('m_{#mu#mu#gamma}')
    replace_variable_titles(latex_title_map, w)
## End of get_real_data()


#-------------------------------------------------------------------------------
def fit_real_data(label):
    '''
    Fit dataset specified by the label: "data" (full 2011A+B),
    "2011A" or "2011B".
    '''
    fit_result = pm.fitTo(data[label], roo.Range('fit'),  roo.NumCPU(8),
                             roo.Timer(), # roo.Verbose()
                             roo.InitialHesse(True), roo.Minos(),
                             roo.Save(), 
        )
    w.Import(fit_result, 'fitresult_' + label)
## End of fit_real_data()


#-------------------------------------------------------------------------------
def plot_fit_to_real_data(label):
    '''
    Plot fit to real data for a dataset specified by the label:
    "data" (full 2011A+B), "2011A" or "2011B".
    '''
    # mmgMass.setRange('plot', 70, 110)
    mmgMass.setBins(80)
    plot = mmgMass.frame(roo.Range('plot'))
    if label == 'data':
        title_start = '2011A+B'
    else:
        title_start = label
       
    plot.SetTitle('%s, %s' % (title_start, latex_title))
    data[label].plotOn(plot)
    pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'))
    pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'),
              roo.Components('*zj*'), roo.LineStyle(ROOT.kDashed))
    canvases.next(name + '_' + label).SetGrid()
    plot.Draw()
## End of plot_fit_to_real_data().


#-------------------------------------------------------------------------------
def draw_latex_for_fit_to_real_data():
    '''
    Draw latex results to the plot of the fit to real data.
    '''
    global fsr_purity
    Latex([
        'E^{#gamma} Scale (%)',
        '  MC Truth: %.2f #pm %.2f' % (fit_calibrator.s.getVal(),
                                       fit_calibrator.s.getError()),
        '  Data Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f}' % (
            phoScale.getVal(), phoScale.getError(), phoScale.getErrorHi(),
            phoScale.getErrorLo()
            ),
        '',
        'E^{#gamma} Resolution (%)',
        '  MC Truth: %.2f #pm %.2f' % (fit_calibrator.r.getVal(),
                                       fit_calibrator.r.getError()),
        '  Data Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f}' % (
            phoRes.getVal(), phoRes.getError(), phoRes.getErrorHi(),
            phoRes.getErrorLo()
            ),
        '',
            'Signal Purity (%)',
            '  MC Truth: %.2f' % fsr_purity,
            '  Data Fit: %.2f #pm %.2f' % (
                100 * w.var('signal_f').getVal(),
                100 * w.var('signal_f').getError()
                )
        ],
        position=(0.2, 0.8)
        ).draw()

    print 'E^{#gamma} Scale (%)','  MC Truth: %.2f #pm %.2f' % (fit_calibrator.s.getVal(),fit_calibrator.s.getError()),'  Data Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f}' % (phoScale.getVal(), phoScale.getError(), phoScale.getErrorHi(),phoScale.getErrorLo())
## Enf of draw_latex_for_fit_to_real_data().


#-------------------------------------------------------------------------------
def process_real_data_single_dataset(label):
    '''
    Get, fit and plot real data for a dataset specified by the label:
    "data" (full 2011A+B), "2011A" or "2011B".
    '''
    get_real_data(label)
    fit_real_data(label)
    plot_fit_to_real_data(label)
    draw_latex_for_fit_to_real_data()
## End of get_fit_and_plot_real_data_single_dataset().


#-------------------------------------------------------------------------------
def process_real_data():
    '''
    Get, fit and plot real data for all 3 dataset specified:
    "data" (full 2011A+B), "2011A" or "2011B".
    '''
    #process_real_data_single_dataset('2011A')
    #check_timer('13.1 get, fit and plot 2011A real data')

    #process_real_data_single_dataset('2011B')
    #check_timer('13.2 get, fit and plot 2011B real data')

    process_real_data_single_dataset('data')
    check_timer('13.3 get, fit and plot 2011A+B real data')
## End of process_real_data().
    

#-------------------------------------------------------------------------------
def set_mc_truth(phos, phor):
    '''
    Set phoScaleTrue and phoResTrue value and error to phos and phor.
    '''
    phoScaleTrue.setVal(phos.getVal())
    phoScaleTrue.setError(phos.getError())
    phoResTrue.setVal(phor.getVal())
    phoResTrue.setError(phor.getError())
## End of set_mc_truth().


#-------------------------------------------------------------------------------
def process_monte_carlo():
    '''
    Get, fit and plot monte carlo.
    '''
    global fitdata1
    fitdata1 = fit_calibrator.get_smeared_data(
        sfit, rfit, 'fitdata1', 'fitdata1', True
        )
    fitdata1.reduce(ROOT.RooArgSet(mmgMass, mmMass))
    fitdata1.append(data['zj1'])
    fitdata1.SetName('fitdata1')
    data['fit1'] = fitdata1

    if reduce_data == True:
        fitdata1 = fitdata1.reduce(roo.Range(reduced_entries,
                                           fitdata1.numEntries()))
    check_timer('3. get fit data (%d entries)' % fitdata1.numEntries())

    nll = pm.createNLL(fitdata1, roo.Range('fit'), roo.NumCPU(8))

    minuit = ROOT.RooMinuit(nll)
    minuit.setProfile()
    minuit.setVerbose()

    phoScale.setError(1)
    phoRes.setError(1)

    ## Initial HESSE
    status = minuit.hesse()
    fitres = minuit.save(name + '_fitres1_inithesse')
    w.Import(fitres, fitres.GetName())
    check_timer('4. initial hesse (status: %d)' % status)

    ## Minimization
    minuit.setStrategy(2)
    status = minuit.migrad()
    fitres = minuit.save(name + '_fitres2_migrad')
    w.Import(fitres, fitres.GetName())
    check_timer('5. migrad (status: %d)' % status)

    ## Parabolic errors
    status = minuit.hesse()
    fitres = minuit.save(name + '_fitres3_hesse')
    w.Import(fitres, fitres.GetName())
    check_timer('6. hesse (status: %d)' % status)

    ## Minos errors
    status = minuit.minos()
    fitres = minuit.save(name + '_fitres4_minos')
    w.Import(fitres, fitres.GetName())
    check_timer('7. minos (status: %d)' % status)

    #fres = pm.fitTo(fitdata1, roo.SumW2Error(True),
                    #roo.Range('fit'),
                    ## roo.Strategy(2),
                    #roo.InitialHesse(True),
                    #roo.Minos(),
                    #roo.Verbose(True),
                    #roo.NumCPU(8), roo.Save(), roo.Timer())

    signal_model._phorhist.GetXaxis().SetRangeUser(75, 105)
    signal_model._phorhist.GetYaxis().SetRangeUser(0, 15)
    signal_model._phorhist.GetXaxis().SetTitle('%s (%s)' % (mmgMass.GetTitle(),
                                                  mmgMass.getUnit()))
    signal_model._phorhist.GetYaxis().SetTitle('E^{#gamma} Resolution (%)')
    signal_model._phorhist.GetZaxis().SetTitle('Probability Density (1/GeV/%)')
    signal_model._phorhist.SetTitle(latex_title)
    signal_model._phorhist.GetXaxis().SetTitleOffset(1.5)
    signal_model._phorhist.GetYaxis().SetTitleOffset(1.5)
    signal_model._phorhist.GetZaxis().SetTitleOffset(1.5)
    signal_model._phorhist.SetStats(False)
    canvases.next(name + '_phorhist')
    signal_model._phorhist.Draw('surf1')

    global graph
    graph = signal_model.make_mctrue_graph()
    graph.GetXaxis().SetTitle('E^{#gamma} resolution (%)')
    graph.GetYaxis().SetTitle('m_{#mu^{+}#mu^{-}#gamma} effective #sigma (GeV)')
    graph.SetTitle(latex_title)
    canvases.next(name + '_mwidth_vs_phor').SetGrid()
    graph.Draw('ap')

    mmgMass.setBins(80)
    plot = mmgMass.frame(roo.Range('plot'))
    plot.SetTitle('Fall11 MC, ' + latex_title)
    fitdata1.plotOn(plot)
    pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'))
    pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'),
              roo.Components('*zj*'), roo.LineStyle(ROOT.kDashed))     
    canvases.next(name + '_fit').SetGrid()
    plot.Draw()
    ## Estimate the MC truth phos and phor:
    old_precision = set_default_integrator_precision(2e-9, 2e-9)
    calibrator0.s.setRange(-15, 15)
    calibrator0.r.setRange(0,25)
    calibrator0.phoEResPdf.fitTo(fitdata1, roo.Range(-50, 50), roo.Strategy(2))
    set_default_integrator_precision(*old_precision)
    set_mc_truth(calibrator0.s, calibrator0.r)

    ## Store the result in the workspace:
    w.saveSnapshot('mc_fit', ROOT.RooArgSet(phoScale, phoRes,
                                            phoScaleTrue, phoResTrue))
    ## Draw the results on the canvas:
    Latex([
        'E^{#gamma} Scale (%)',
        '  MC Truth: %.2f #pm %.2f' % (calibrator0.s.getVal(),
                                       calibrator0.s.getError()),
        '  MC Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f}' % (
            phoScale.getVal(), phoScale.getError(), phoScale.getErrorHi(),
            phoScale.getErrorLo()
            ),
        '',
        'E^{#gamma} Resolution (%)',
        '  MC Truth: %.2f #pm %.2f' % (calibrator0.r.getVal(),
                                       calibrator0.r.getError()),
        '  MC Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f}' % (
            phoRes.getVal(), phoRes.getError(), phoRes.getErrorHi(),
            phoRes.getErrorLo()
            ),
        '',
            'Signal Purity (%)',
            '  MC Truth: %.2f' % fsr_purity,
            '  MC Fit: %.2f #pm %.2f' % (
                100 * w.var('signal_f').getVal(),
                100 * w.var('signal_f').getError()
                )
        ],
        position=(0.2, 0.8)
        ).draw()
    
    check_timer('8. fast plots')
## End of process_real_data


##------------------------------------------------------------------------------
def main():
    sw.Start()
    sw2.Start()

    init()
    # init_from_file(inputfile)
    
    if use_real_data:
        process_real_data()
    else:
        process_monte_carlo()

    outro()
## End of main().

# ROOT.RooAbsReal.defaultIntegratorConfig().setEpsAbs(1e-07)
# ROOT.RooAbsReal.defaultIntegratorConfig().setEpsRel(1e-07)



## pm.fitTo(data['fsr'], roo.Verbose(), roo.Save(), roo.SumW2Error(True),
##          roo.Range(60, 120), roo.NumCPU(8))
## mmgMass.setRange('plot', 70, 110)
## mmgMass.setBins(80)
## plot = mmgMass.frame(roo.Range('plot'))
## plot.SetTitle(latex_title)
## fitdata1.plotOn(plot)
## pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'))
## pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'),
##           roo.Components('*zj*'), roo.LineStyle(ROOT.kDashed))
## canvases.next(name + '_fit_singal_only')
## plot.Draw()
## num_fsr_events = data['fsr'].sumEntries()
## num_zj_events = data['zj'].sumEntries()
## fsr_purity = num_fsr_events / (num_fsr_events + num_zj_events)
## Latex(
##     [
##         'E^{#gamma} Scale (%)',
##         '  MC Truth: %.2f #pm %.2f' % (fit_calibrator.s.getVal(),
##                                         fit_calibrator.s.getError()),
##         '  #mu#mu#gamma Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f}' % (
##             phoScale.getVal(), phoScale.getError(), phoScale.getErrorHi(),
##             phoScale.getErrorLo()
##             ),
##         '',
##         'E^{#gamma} resolution (%)',
##         '  MC Truth: %.2f #pm %.2f' % (fit_calibrator.r.getVal(),
##                                         fit_calibrator.r.getError()),
##         '  #mu#mu#gamma Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f}' % (
##             phoRes.getVal(), phoRes.getError(), phoRes.getErrorHi(),
##             phoRes.getErrorLo()
##             ),
##         '',
##         'Signal purity (%)',
##         '  MC Truth: %.2f' % 100.,
##         '  #mu#mu#gamma Fit: %.2f #pm %.2f' % (
##             100 * w.var(name + '_signal_f').getVal(),
##             100 * w.var(name + '_signal_f').getError()
##             )
##         ## 'N_{S} (events)',
##         ## '  MC Truth: %.1f' % fitdata1.sumEntries(),
##         ## '  #mu#mu#gamma Fit: %.1f #pm %.1f' % (
##         ##     w.var(name + '_signal_N').getVal(),
##         ##     w.var(name + '_signal_N').getError()
##         ##     )
##         ],
##     position=(0.2, 0.8)
##     ).draw()

#canvases.next(name + '_nll_vs_phos').SetGrid()
#plot = w.var('phoScale').frame(roo.Range(*get_confint(phoScale)))
#plot.SetTitle(latex_title)
#nll.plotOn(plot, roo.ShiftToZero())
## plot.GetYaxis().SetRangeUser(0, 10)
#plot.Draw()
#check_timer('9. nll vs phos')

### canvases.next(name + 'norm')
### norm = pm.getNormObj(ROOT.RooArgSet(), ROOT.RooArgSet(mmgMass))
### plot = phoScale.frame(roo.Range(*get_confint(phoScale)))
### norm.plotOn(plot)
### plot.GetYaxis().SetRangeUser(0.9995, 1.0005)
### plot.Draw()
### check_timer('10. norm vs phos')

#canvases.next(name + '_nll_vs_phor').SetGrid()
#plot = phoRes.frame(roo.Range(*get_confint(phoRes)))
#nll.plotOn(plot, roo.ShiftToZero())
## plot.GetYaxis().SetRangeUser(0, 10)
#plot.Draw()

#canvases.next(name + '_nll_vs_phor_zoom').SetGrid()
#plot = phoRes.frame(roo.Range(*get_confint(phoRes,1.5)))
#nll.plotOn(plot, roo.ShiftToZero())
## plot.GetYaxis().SetRangeUser(0, 10)
#plot.Draw()
#check_timer('11. nll vs phor')

#c1 = canvases.next(name + '_nll2d')
#c1.SetGrid()
#c1.SetRightMargin(0.15)
#phos_range = unite_intervals([get_confint(phoScale, 4),
                              #get_confint(fit_calibrator.s0, 4)])
#phor_range = unite_intervals([get_confint(phoRes, 4),
                              #get_confint(fit_calibrator.r0, 4)])
#h2nll = nll.createHistogram('h2nll', phoScale, roo.Binning(40, *phos_range),
                            #roo.YVar(phoRes, roo.Binning(40, *phor_range)),
                            #roo.Scaling(False))
#h2nll_min = h2nll.GetMinimum() + 0.001
#for binx in range(1, h2nll.GetNbinsX() + 1):
    #for biny in range(1, h2nll.GetNbinsY() + 1):
        #binxy = h2nll.GetBin(binx, biny)
        #binc = h2nll.GetBinContent(binxy)
        #h2nll.SetBinContent(binxy, binc - h2nll_min)
#h2nll.SetStats(False)
#h2nll.SetTitle(latex_title)
#h2nll.GetZaxis().SetTitle('-log(Likelihood)')
#h2nll.GetZaxis().SetTitleOffset(0.8)
#h2nll.Draw('colz')
#check_timer('12. 2d nll')

## Draw 1 and 2 sigma contours
#minuit = ROOT.RooMinuit(nll)
#contour = minuit.contour(phoScale, phoRes)
#contour.getObject(0).SetMarkerStyle(2)
#contour.getObject(0).SetMarkerSize(2)
#contour.getObject(0).SetMarkerColor(ROOT.kWhite)
#if contour.numItems() > 1.5:
    #contour.getObject(1).SetLineColor(ROOT.kWhite)
#if contour.numItems() > 2.5:
    #contour.getObject(2).SetLineColor(ROOT.kWhite)
#contour.Draw('same')

#mc_true_graph = ROOT.TGraphErrors(1)
#mc_true_graph.SetPoint(0, fit_calibrator.s0.getVal(), fit_calibrator.r0.getVal())
#mc_true_graph.SetPointError(0, fit_calibrator.s0.getError(),
                            #fit_calibrator.r0.getError())
#mc_true_graph.SetMarkerStyle(20)
#mc_true_graph.SetLineColor(ROOT.kRed)
#mc_true_graph.SetMarkerColor(ROOT.kRed)
#mc_true_graph.Draw("p")

#check_timer('12.1 1- and 2-sigma contours')



## End of main().


##------------------------------------------------------------------------------
if __name__ == '__main__':
    parse_command_line_arguments()
    main()
    import user

