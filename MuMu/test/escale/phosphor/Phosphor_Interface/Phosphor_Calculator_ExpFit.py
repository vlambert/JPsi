'''
Photon Energy Scale (PhoES) and Photon Energy Resolution (PHOSPHOR) Fit model 5.

Model Z+jets background with a parametrized KEYS pdf trained on MC.
Model other backgrounds with an exponential.
Use custom class for the signal PDF that caches and interpolates
the normalization integral to speed up the fitting and reduce numerical noise. 

Adding more validation plots in addition to what is in the famous test9.

Jan Veverka, Caltech, 25 October 2012.
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
from JPsi.MuMu.common.padDivider import residPullDivide
from JPsi.MuMu.common.modalinterval import ModalInterval
from JPsi.MuMu.datadrivenbinning import DataDrivenBinning
from JPsi.MuMu.roochi2calculator import RooChi2Calculator

from Phosphor_Globals import *

##-- Configuration -------------------------------------------------------------
## Selection
# name = 'EB_highR9_pt15to20'

##  Fits events passing Event$ % 4 == 0 and uses all the other events to build 
##+ the model.
# name = 'test_mc_EE_highR9_pt30to999_v13_evt1of4'

## Fits the same MC events that were used for the model training
# name = 'test_mc_EE_highR9_pt30to999_v13'

## Fits real data
# name = 'test_data_EE_highR9_pt30to999_v13'

# name = 'test_data_EE_pt25to999_yyv3'
# name = 'truevalidation_mc_EE_lowR9_pt10to12_v13_evt2of4'
# name = 'egm_francesca_mc_EE_pt30to999_highR9_sfit0_rfit4.0_yyv5'
name = 'zg_test_data_EE_highR9_pt25to999_sixie'

inputfile = 'phosphor5_model_and_fit_' + name + '.root'
outputfile = 'phosphor5_model_and_fit_' + name + '.root'

strain = 'nominal'
rtrain = 'nominal'

sfit = 'nominal'
rfit = 'nominal'

#sfit = 'nominal'
#rfit = 1.0

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
    
    return fake_data_cut
## End of parse_name_to_fake_data_cut().


##------------------------------------------------------------------------------
def parse_name_to_target_smearing_of_mc_fit(name):
    '''
    Parses the name and decides whether to smear the MC used in the fit and
    extracts the target scale and resolution values.
    Stores their values in the global variables sfit and rfit.
    If the name is split into tokens separated by the underscore "_" and
    one of the tokens is "sfitX.X" or "rfitY.Y" then it means that 
    the MC fit sample should be smeared to scale sfit = X.X and
    resolution rfit = Y.Y.
    '''
    global sfit, rfit
    for tok in name.split('_'):
        if 'sfit' in tok:
            sfit = float(tok.replace('sfit', ''))
        if 'rfit' in tok:
            rfit = float(tok.replace('rfit', ''))
## End of parse_name_to_target_smearing_of_mc_fit(name)


##------------------------------------------------------------------------------
def parse_name_whether_use_exp_bkg(name):
    '''
    Parses the name and decides whether to add an exponential bkg model
    (use_exp_bkg = True).
    '''
    global use_exp_bkg
    use_exp_bkg = False
    print "==================NAME EXP============", name
    if 'expbkg' in name.split('_') and 'data' in name.split('_'):
        use_exp_bkg = True
## End of parse_name_whether_use_exp_bkg(name)


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
    ## For EGM-11-001 to help with regression
    # cuts = ['mmMass + mmgMass < 180', 'minDeltaR < 1.5', 'minDeltaR > 0.1']
    cuts = ['mmMass + mmgMass < 180', 
            'minDeltaR < 1.5', 
            'mu1Pt > 15', 
            'mu2Pt > 10']
    # cuts = ['mmMass + mmgMass < 180']
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
        elif 'lowR9' in name:
            cuts.append('phoR9 < 0.95')

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
                cuts.append('%s <= phoPt & phoPt < %s' % (lo, hi))
   
    global model_tree_version, data_tree_version
    ## Set the default
    model_tree_version, data_tree_version = 'v11', 'v11'
    
    for tree_version in 'yyv1 yyv2 yyv3 yyv4 yyv4NoJSON yyv5 yyv6 v11 v13 v14 v15 sixie'.split():
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
    
    if data_tree_version in 'yyv1 yyv2 yyv3'.split():
        tokens.append('16 Jan Re-reco')
        latex_labels.append('16 Jan Re-reco')
    elif data_tree_version in 'yyv4 yyv4NoJSON'.split():
        tokens.append('14 Jul Re-reco')
        latex_labels.append('14 Jul Re-reco')
    elif data_tree_version in 'sixie sixie2'.split():
        tokens.append('2012ABC')
        latex_labels.append('2012ABC')
    
    if model_tree_version in 'v11'.split():
        tokens.append('2011A+B PU S4 MC Model')
        latex_labels.append('2011A+B PU S4 MC Model')
    elif model_tree_version in 'v13 yyv1 yyv2 yyv3 yyv4 yyv4NoJSON yyv5 yyv6'.split():
        tokens.append('2011A+B PU S6 MC Model')
        latex_labels.append('2011A+B PU S6 MC Model')
    elif model_tree_version in 'sixie sixie2'.split():
        tokens.append('2012 Madgraph')
        latex_labels.append('2012 Madgraph')
    elif model_tree_version == 'v14':
        tokens.append('2011A PU S6 MC Model')
        latex_labels.append('2011A PU S6 MC Model')        
    elif model_tree_version == 'v15':
        tokens.append('2011B PU')
        latex_labels.append('2011B PU S6 MC Model')
        
    if model_tree_version in 'yyv5 yyv6 sixie'.split():
        tokens.append('mu corrections')
        latex_labels.append('#mu corr.')
    
    if model_tree_version in 'yyv6'.split():
        tokens.append('Fabrice smear.')
        latex_labels.append('Fabrice smear.')
    
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
    elif model_tree_version in 'yyv3 yyv4 yyv4NoJSON yyv5 yyv6'.split():
        tokens.append('Hgg v2 Regr.')
        latex_labels.append('Hgg v2 Regr.')
    elif model_tree_version in 'sixie sixie2'.split():
        tokens.append('Hgg v3 Regr.')
        latex_labels.append('Hgg v3 Regr.')
    
    if 'sfit' in name:
        tokens.append('starget: %g %%' % sfit)
        latex_labels.append('#mu_{target} = %g %%' % sfit)
    if 'rfit' in name:
        tokens.append('rtarget: %g %%' % rfit)
        latex_labels.append('#mu_{target} = %g %%' % rfit)

    if 'expbkg' in name.split('_'):
        tokens.append('exp. bkg.')
        latex_labels.append('exp. bkg.')
    
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
    parse_name_to_target_smearing_of_mc_fit(name)
    parse_name_whether_use_exp_bkg(name)
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
    global wsrc
    wsrc = ROOT.TFile.Open(filename).Get(name + '_workspace')
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
        'phoERes': ('E_{reco}^{#gamma}/E_{gen}^{#gamma} - 1', '%'),
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
    mmgMass.setRange('tails', 60, 120)
    mmgMass.setRange('peak', 80, 100)
## End of set_ranges_for_data_observables().


##------------------------------------------------------------------------------
def define_model_parameters():
    '''
    Defines model parameters and related variables in the workspace 
    as python globals.
    '''
    ## Define model parameters.
    global phoScale, phoRes
    phoScale     = w.factory('phoScale[0,-50,50]')
    phoRes       = w.factory('phoRes[3,0.1,20.1]')
    ## Set units.
    for x, u in zip([phoScale, phoRes], '% %'.split()):
        x.setUnit(u)
## End of define_model_parameters().


##------------------------------------------------------------------------------
def define_bookkeeping_parameters():
    ## Prep for storing fit results in the workspace.
    global phoScaleTrue, phoResTrue
    phoScaleTrue = w.factory('phoScaleTrue[0,-50,50]')
    phoResTrue   = w.factory('phoResTrue[1.5,0.01,50]')    
    ## Set units.
    for x, u in zip([phoScaleTrue, phoResTrue], '% %'.split()):
        x.setUnit(u)
    ## These are Goodness-of-Fit (GOF) parameters. They are not global.
    chi2 = w.factory('chi2[0,0,1e3]')
    ndof = w.factory('ndof[0,0,1e3]')
    pvalue = w.factory('pvalue[0,0,1]')
    chi2.removeMax()
    ndof.removeMax()
    chi2.setError(0)
    ndof.setError(0)
    pvalue.setError(0)
    gof = ROOT.RooArgSet(chi2, ndof, pvalue)
    w.defineSet('gof', gof)
## End of define_bookkeeping_parameters()

        
##------------------------------------------------------------------------------
def read_model_parameters_from_workspace(workspace):
    '''
    Reads model parameters form the given workspace and defines them as 
    python globals.
    '''
    global phoScale, phoRes
    phoScale     = workspace.var('phoScale')
    phoRes       = workspace.var('phoRes')
## End of read_model_parameters_from_workspace


##------------------------------------------------------------------------------
def set_signal_model_normalization_integral_cache_binnings():
    '''
    Define the binning for the normalization integral caching.
    '''
    ## This setting was used as a default for Adi's e/gamma paper placeholders.
    #phosbins = ROOT.RooBinning(15, -15, 15, 'normcache')#Original from Jan
    #phorbins = ROOT.RooBinning(15, 0.1, 25.1, 'normcache')#Original from Jan
    phosbins = ROOT.RooBinning(30, -15, 15, 'normcache')
    phorbins = ROOT.RooBinning(25, 0.1, 25.1, 'normcache')
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
def get_data(chains): # = getChains('v11')):
    '''
    Get the nominal data that is used for smearing.
    '''
    global cuts
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

    print "+++++CUTS0++++++", cuts0
    print "+++++CUTS1++++++", cuts1
    ## Get the nominal dataset
    global data
    data = {}
    for xvar in [weight, mmgMass, mmMass, phoERes, mmgMassPhoGenE]:
        print xvar.GetName(), ':', xvar.GetTitle()        
    
    data['fsr0'] = dataset.get(tree=tree['z'], weight=weight,
                               cuts=cuts0 + ['isFSR'],
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
    
    ##-- Check the time -------------------------------------------------------
    check_timer(
        '1. init and get_data (%d entries)' % (
            data['fsr0'].numEntries() + data['fsr1'].numEntries() +
            data['zj0'].numEntries() + data['zj1'].numEntries()
            )
        )
## End of get_data.


##------------------------------------------------------------------------------
def define_calibrators():
    '''
    Defines calibrators.
    '''
    old_precision = set_default_integrator_precision(2e-9, 2e-9)
    global calibrator0, calibrator1, fit_calibrator
    calibrator0 = MonteCarloCalibrator(data['fsr0'], printlevel=1, rho=1.5)
    if use_independent_fake_data:
        calibrator1 = MonteCarloCalibrator(data['fsr1'], printlevel=1, rho=1.5)
        fit_calibrator = calibrator1
    else:
        fit_calibrator = calibrator0
    set_default_integrator_precision(*old_precision)
## End of define_calibrators()


##------------------------------------------------------------------------------
def calculate_mc_true_purity():
    '''
    Defines a global variable fsr_purity and sets it to the MC truth purity.
    '''
    if use_independent_fake_data:
        num_fsr_events = data['fsr1'].sumEntries()
        num_zj_events = data['zj1'].sumEntries()
    else:
        num_fsr_events = data['fsr0'].sumEntries()
        print "++++Number of Entries, fsr0: ", num_fsr_events, "  ---  ", data['fsr0'].numEntries()
        num_zj_events = data['zj0'].sumEntries()
        print "++++Number of Entries, ZJ0: ", num_zj_events, " ----- ", data['zj0'].numEntries()
    global fsr_purity
    fsr_purity = 100 * num_fsr_events / (num_fsr_events + num_zj_events)
## End of calculate_mc_true_purity()


##------------------------------------------------------------------------------
def get_confint(x, cl=5):
    '''
    Returns the confidence interval of given confidence level cl for the
    given variable x.
    '''
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
        canvases.make_plots(['png', 'pdf', 'eps', 'root'],
                            ROOT.gSystem.WorkingDirectory())

    for label, dataset in data.items():
        dataset.SetName('data_' + label)
        # w.Import(dataset)
    
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
    #phortargets = [0.1, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 25]
    phortargets = [0.15, 0.55, 1.1, 2.1, 3.1, 4.1, 5.1, 7.1, 10.1, 15.1, 25.1]
    #phortargets = [0.1, 0.3, 0.6, 0.9, 1.2, 2.2, 3.2, 4.2, 5.2, 7.2, 10.5, 15.5, 25]
    ## Trying to find something that would not converge to the reference value
    ## for the EGM plots
    # phortargets = [0.1, 0.5, 1, 3, 5, 7, 10, 15, 25]

    # phortargets = [0.5, 6, 7, 7.5, 8, 8.5, 8.75, 9, 9.5, 10, 10.5, 11, 11.5, 11.75, 12, 12.5, 13, 14]
    # phortargets = [0.5, calibrator0.r0.getVal(), 10, 20]
    # phortargets.append(calibrator0.r0.getVal())
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
    global exp_pdf
    exp_pdf = w.factory('Exponential::exp_pdf(mmgMass, exp_c[-0.05,-0.1,0])')
    w.var('exp_c').setUnit('GeV^{-1}')
    
    # global bkg_pdf
    # bkg_pdf = w.factory('SUM::bkg_pdf(exp_f[0.2, 0, 1] * exp_pdf, zj0_pdf)')

    ## Build the composite model PDF
    global pm
    pm = w.factory('''SUM::pm(signal_N[1e3,0,1e4] * signal_model0,
                              exp_N   [2e2,0,1e3] * exp_pdf,
                              zj_N    [2e2,0,1e3] * zj0_pdf)''')

    for yieldvar in 'signal_N exp_N zj_N'.split():
        w.var(yieldvar).removeMax()
      
    if not use_exp_bkg:
        w.var('exp_N').setVal(0)
        w.var('exp_N').setConstant()
        w.var('exp_c').setConstant()
    
    check_timer('2.4 build full S+B model')
## End build_full_model()
        

##------------------------------------------------------------------------------
def read_model_from_workspace(workspace):
    '''
    Reads the full signa + background model from a given workspace.
    '''
    global signal_model, zj_pdf, exp_pdf, pm
    w.Import(workspace.pdf('pm'))
    pm = w.pdf('pm')
    signal_model = w.pdf('signal_model0')
    zj_pdf = w.pdf('zj0_pdf')
    exp_pdf = w.pdf('exp_pdf')
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
    define_bookkeeping_parameters()
    define_mass_derivative_function_and_mean()   
    set_ranges_for_data_observables()
    set_signal_model_normalization_integral_cache_binnings()
    get_data(getChains(model_tree_version))
    calculate_mc_true_purity()
    define_calibrators()
    build_model()
## End of init().


##------------------------------------------------------------------------------
def read_data_from_workspace(workspace):
    '''
    Reads the various datasets from the given workspace and imports them in 
    the current workspace.
    '''
    global data
    data = {}
    for name in 'fsr0 fsr1 zj0 zj1'.split():        
        data[name] = workspace.data('data_' + name)

    if 'data' in name.split('_'):
        for name in 'data 2011A 2011B'.split():
            if workspace.data('data_' + name):
                data[name] = workspace.data('data_' + name)
## End of read_data_from_workspace(workspace).


##------------------------------------------------------------------------------

##------------------------------------------------------------------------------
def init_cfg_file():
    '''
    Initialize workspace and common variables and functions.
    '''
    #define_globals()
    #from common import *
    #global cuts
    global inputfile, outputfile, use_exp_bkg, plots, cuts, name, output, latex_title, model_tree_version, data_tree_version
    plots = []
    cuts = Globals.cuts
    print '===============CUTS======================', cuts
    #global model_tree_version, data_tree_version
    data_tree_version = model_tree_version = Globals.model_tree_version
    print '====================Model Tree Version===========================', model_tree_version
    #global name, output, latex_title
    name = Globals.name
    latex_title = Globals.latex_title
    outputfile = 'phosphor5_model_and_fit_' + name + '.root'
    print  '===================Name===========================', name
    
    inputfile = 'phosphor5_model_and_fit_' + name + '.root'
    outputfile = 'phosphor5_model_and_fit_' + name + '.root'

    #define_globals()
    print  '===================Name2===========================', name
    parse_name_to_target_smearing_of_mc_fit(name)
    #parse_name_whether_use_exp_bkg(name)
    use_exp_bkg = Globals.exp_bkg
    print  '===================EXP BKG===========================', use_exp_bkg
    define_workspace()
    define_data_observables()
    define_model_parameters()
    define_bookkeeping_parameters()
    define_mass_derivative_function_and_mean()   
    set_ranges_for_data_observables()
    set_signal_model_normalization_integral_cache_binnings()
    get_data(getChains(model_tree_version))
    calculate_mc_true_purity()
    define_calibrators()
    build_model()

## End of init().
                
def init_from_file(filename):
    '''
    Initialize workspace and common variables and functions from a file
    of the given filename.
    '''
    define_globals()
    define_workspace()
    define_data_observables()
    read_workspace_from_file(filename)
    read_data_from_workspace(wsrc)
    calculate_mc_true_purity()
    define_calibrators()
    read_model_from_workspace(wsrc)
    read_model_parameters_from_workspace(w)
    define_bookkeeping_parameters()
    read_mass_derivative_function_and_mean_from_workspace(w)
    set_ranges_for_data_observables()
    set_signal_model_normalization_integral_cache_binnings()
## End of init_from_file().


#-------------------------------------------------------------------------------
def get_real_data(label):
    '''
    Get real data for the dataset specified by the label: "data" (full 2011A+B),
    "2011A" or "2011B".
    '''
    global model_tree_version
    global data_tree_version
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
    ## Set initial values to MC truth
    phoScale.setVal(calibrator0.s.getVal())
    phoRes.setVal(calibrator0.r.getVal())
    ## Do the fit
    fit_result = pm.fitTo(data[label], roo.Range('fit'),  roo.NumCPU(8),
                          roo.Timer(), # roo.Verbose()
                          roo.InitialHesse(True), roo.Minos(),
                          roo.Save(), roo.Extended(True)
        )
    # w.Import(fit_result, 'fitresult_' + label)
    return fit_result
## End of fit_real_data()


#-------------------------------------------------------------------------------
def plot_fit_to_real_data(label):
    '''
    Plot fit to real data for a dataset specified by the label:
    "data" (full 2011A+B), "2011A" or "2011B".
    '''
    mmgMass.setBins(80)
    plot = mmgMass.frame(roo.Range('plot'))
    plot.SetTitle('%s, %s' % (title_prefix, latex_title))
    data[label].plotOn(plot)
    pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'),
              roo.Components('*zj*,*exp*'), roo.LineStyle(ROOT.kDashed))
    pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'),
              roo.Components('*exp*'), roo.LineStyle(ROOT.kDotted))
    pm.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'))
    canvases.next(name + '_' + label).SetGrid()
    plot.Draw()
    global plots
    plots.append(plot)
## End of plot_fit_to_real_data().


#-------------------------------------------------------------------------------
def draw_latex_for_fit_to_real_data():
    '''
    Draw latex results to the plot of the fit to real data.
    '''
    global fsr_purity
    ntot, nztot = 0, 0
    for x in 'signal_N zj_N exp_N'.split():
        ntot += w.var(x).getVal()
        if x != 'exp_N':
            nztot += w.var(x).getVal()
    
    oplus = lambda x, y: math.sqrt(x*x + y*y)
    
    nsig = w.var('signal_N').getVal()
    nbkg = w.var('zj_N').getVal() + w.var('exp_N').getVal()
    
    esig = w.var('signal_N').getError()
    ebkg = oplus(w.var('zj_N').getError(), w.var('exp_N').getError())
    
    fsigerr = 100 * oplus(nbkg * esig, nsig * ebkg) / pow(nsig + nbkg, 2)
    
    Latex([
        'E^{#gamma} Scale (%)',
        '  MC Truth: %.2f #pm %.2f' % (calibrator0.s.getVal(),
                                       calibrator0.s.getError()),
        '  Data Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f}' % (
            phoScale.getVal(), phoScale.getError(), phoScale.getErrorHi(),
            phoScale.getErrorLo()
            ),
        '',
        'E^{#gamma} Resolution (%)',
        '  MC Truth: %.2f #pm %.2f' % (calibrator0.r.getVal(),
                                       calibrator0.r.getError()),
        '  Data Fit: %.2f #pm %.2f ^{+%.2f}_{%.2f}' % (
            phoRes.getVal(), phoRes.getError(), phoRes.getErrorHi(),
            phoRes.getErrorLo()
            ),
        '',
            'Signal Purity (%)',
            '  MC Truth: %.2f' % (
                fsr_purity / (1. + w.var('exp_N').getVal() / nztot)
                ),
            '  Data Fit: %.2f #pm %.2f' % (
                100 * w.var('signal_N').getVal() / ntot,
                fsigerr
                )
        ],
        position=(0.2, 0.8)
        ).draw()
## Enf of draw_latex_for_fit_to_real_data().


#-------------------------------------------------------------------------------
def process_real_data_single_dataset(label):
    '''
    Get, fit and plot real data for a dataset specified by the label:
    "data" (full 2011A+B), "2011A" or "2011B".
    '''
    global title_prefix
    if label == 'data':
        #title_prefix = '2011A+B'
        title_prefix = '2012 ABCD'
    else:
        title_prefix = label
    
    get_real_data(label)
    var1 = 'phoScale'
    var2 = 'phoRes'
    w.saveSnapshot('_'.join(['mc_truth', label]),
                   ROOT.RooArgSet(phoScaleTrue, phoResTrue))
    components_combinations = [''] + 'B E EB S SB SE SEB'.split()
    #components_combinations = 'S SB SE SEB'.split()
    pvalue_combo_map = {}
    for components in components_combinations:
        process_real_data_for_label_and_components(label, components)
        ####(Cristian) Reject crazy errors
        fit_r = '_'.join(['fitresult', label, components])
        print fit_r
        err1_c = 10.
        err2_c = 10.
        if fit_r == 'fitresult_data_S' or fit_r == 'fitresult_data_SB' or fit_r == 'fitresult_data_SE' or fit_r == 'fitresult_data_SEB':        
            err1_c = w.obj(fit_r).floatParsFinal().find(var1).getError()
            err2_c = w.obj(fit_r).floatParsFinal().find(var2).getError()

            print 'errScale: ', err1_c, ' errRes: ', err2_c
        #val1_c = w.obj('_'.join(['fitresult', label, components])).floatParsFinal().find(var1).getVal()
        #val2_c = w.obj('_'.join(['fitresult', label, components])).floatParsFinal().find(var2).getVal()
        if err1_c > 5. or err2_c > 5. :
            continue

        pvalue_combo_map[w.var('pvalue').getVal()] = components
        
    remove_fit_components_from_name()
    plot_combo_summaries(label, components_combinations)
    ## Load the combo with the best pvalue.
    best_pvalue = max(pvalue_combo_map.keys())
    best_combo = pvalue_combo_map[best_pvalue]
    print 'Best p-value: %.2g for %s' % (best_pvalue, best_combo)
    load_fit_result(label, best_combo)
## End of process_real_data_single_dataset().


#-------------------------------------------------------------------------------
def process_real_data_for_label_and_components(label, components):
    set_fit_components(components)
    fit_result = fit_real_data(label)
    w.Import(fit_result, '_'.join(['fitresult', label, components]))
    plot_fit_to_real_data(label)
    draw_latex_for_fit_to_real_data()
    validate_mass_fit(data[label], fit_result)
    w.saveSnapshot('_'.join(['gof', label, components]), w.set('gof'))    
## End of process_real_data_for_label_and_components(label, components)


#-------------------------------------------------------------------------------
def remove_fit_components_from_name():
    global name
    tokens = name.split('_')
    for i, tok in enumerate(tokens):
        if 'fit' in tok:
            del tokens[i]
    name = '_'.join(tokens)
## End of remove_fit_components_from_name()


#-------------------------------------------------------------------------------
def plot_combo_summaries(label, combos):
    ## p-value
    title = ','.join([title_prefix, latex_title])
    hist = plot_gofvar_vs_combo('pvalue', label, combos)
    hist.SetTitle(title)
    hist.GetYaxis().SetTitle('Fit #chi^{2} p-value')
    canvas = canvases.next(name + '_pvalue_vs_combo').SetGridy()
    hist.DrawCopy('p')
    canvas = canvases.next(name + '_pvalue_vs_combo_logy')
    canvas.SetGridy()
    canvas.SetLogy()
    hist.DrawCopy('p')
    hist0 = hist
    w.Import(hist)
    ## chi2
    hist = plot_gofvar_vs_combo('chi2', label, combos)
    hist.SetTitle(title)
    hist.GetYaxis().SetTitle('Fit #chi^{2}')
    canvases.next(name + '_chi2_vs_combo').SetGridy()
    hist.DrawCopy('p')
    w.Import(hist)
    ## chi2 and p-value overlayed
    #c1 = canvases.next('chi2npval_vs_combo')
    #global pad1, pad2
    #pad1 = ROOT.TPad("pad1","",0,0,1,1)
    #pad2 = ROOT.TPad("pad2","",0,0,1,1)
    #pad2.SetFillStyle(4000) #will be transparent
    #pad1.Draw()
    #pad1.cd()
    #hist.DrawCopy('p')
    #pad1.Update() #this will force the generation of the "stats" box
    #pad1.Modified()
    #c1.cd()
    #ymin = hist0.GetYaxis().GetXmin()
    #ymax = hist0.GetYaxis().GetXmax()
    #dy = (ymax-ymin)/0.8 #10 per cent margins top and bottom
    #xmin = hist0.GetYaxis().GetXmin()
    #xmax = hist0.GetYaxis().GetXmax()
    #dx = (xmax-xmin)/0.8 #10 per cent margins left and right
    #pad2.Range(xmin-0.1*dx,ymin-0.1*dy,xmax+0.1*dx,ymax+0.1*dy)
    #pad2.Draw()
    #pad2.cd()
    #hist0.SetLineColor(ROOT.kRed)
    #hist0.DrawCopy("][sames")
    #pad2.Update()
    #global axis
    #axis = ROOT.TGaxis(xmax,ymin,xmax,ymax,ymin,ymax,50510,"+L")
    #axis.SetLabelColor(ROOT.kRed)
    #axis.Draw()
    ## Resolution
    hist = plot_floatvar_vs_combo('phoRes', label, combos)
    hist.SetMinimum(0)
    hist.SetTitle(title)
    hist.GetYaxis().SetTitle('E^{#gamma} Resolution (%)')
    canvases.next(name + '_phoRes_vs_combo').SetGridy()
    hist.DrawCopy('e1x0')
    w.Import(hist)
    ## Scale
    hist = plot_floatvar_vs_combo('phoScale', label, combos)
    hist.SetTitle(title)
    hist.GetYaxis().SetTitle('E^{#gamma} Scale (%)')
    canvases.next(name + '_phoScale_vs_combo').SetGridy()
    hist.DrawCopy('e1x0')
    w.Import(hist)
## End of plot_combo_summaries(label, combos)


#-------------------------------------------------------------------------------
def load_fit_result(label, combo):
    fit_result = w.obj('_'.join(['fitresult', label, combo]))
    phos = fit_result.floatParsFinal().find('phoScale')
    phor = fit_result.floatParsFinal().find('phoRes')
    if not phos:
        phos = fit_result.constPars().find('phoScale')
    if not phor:
        phor = fit_result.constPars().find('phoRes')
    copy_value_and_errors(phos, phoScale)
    copy_value_and_errors(phor, phoRes)
## End of load_fit_result(label, combo)


#-------------------------------------------------------------------------------
def copy_value_and_errors(source_var, destination_var):
    destination_var.setVal(source_var.getVal())
    destination_var.setError(source_var.getError())
    if source_var.hasAsymError():
        destination_var.setAsymError(source_var.getErrorLo(),
                                     source_var.getErrorHi())
## End of copy_value_and_errors(source_var, destination_var)




#-------------------------------------------------------------------------------
def plot_floatvar_vs_combo(varname, label, combos):
    hname = 'h_%s_vs_combo' % varname
    npoints = len(combos)
    hist = ROOT.TH1F(hname, '', npoints, -0.5, npoints - 0.5)
    hist.SetStats(0)
    hist.GetXaxis().SetTitle('Fit Model Components')
    for ibin, components in enumerate(combos):
        hist.GetXaxis().SetBinLabel(ibin + 1, components)
        fitresult = w.obj('_'.join(['fitresult', label, components]))
        yvar = fitresult.floatParsFinal().find(varname)
        if not yvar:
            yvar = fitresult.constPars().find(varname)
        hist.Fill(ibin, yvar.getVal())
        hist.SetBinError(ibin + 1, yvar.getError())
    return hist
## End of plot_floatvar_vs_combo(varname, label, combos)


#-------------------------------------------------------------------------------
def plot_gofvar_vs_combo(varname, label, combos):
    hname = 'h_%s_vs_combo' % varname
    npoints = len(combos)
    hist = ROOT.TH1F(hname, '', npoints, -0.5, npoints - 0.5)
    hist.SetStats(0)
    hist.GetXaxis().SetTitle('Fit Model Components')
    yvar = w.var(varname)
    for ibin, components in enumerate(combos):
        hist.GetXaxis().SetBinLabel(ibin + 1, components)
        fitresult = w.obj('_'.join(['fitresult', label, components]))
        snapshot = '_'.join(['gof', label, components])
        if not w.loadSnapshot(snapshot):
            RuntimeError, "Snapshot `%s' not found!" % snapshot
        hist.Fill(ibin, yvar.getVal())
        hist.SetBinError(ibin + 1, yvar.getError())
    return hist
## End of plot_floatvar_vs_combo(varname, label, combos)


#-------------------------------------------------------------------------------
def set_fit_components(components):
    '''
    Sets components that should be fitted given a string.  Each
    letter in the string corresponds to a commponent:
    S : signal
    B : Z+jets background
    E : exponential background
    '''
    ## yieds
    global name
    global w
    num = {'S': 'signal_N', 'B': 'zj_N', 'E': 'exp_N'}
    params = {'S': 'phoScale phoRes'.split(), 'B': [], 'E': ['exp_c']}    
    for c in 'S B E'.split():
        if c in components:
            w.var(num[c]).setConstant(False)
            w.var(num[c]).setVal(200)
            for p in params[c]:
                w.var(p).setConstant(False)
        else:
            w.var(num[c]).setVal(0)
            w.var(num[c]).setConstant(True)
            w.var(num[c]).setError(0)
            for p in params[c]:
                w.var(p).setConstant(True)
                w.var(p).setError(0)
    ## Always float the signal fraction
    w.var('signal_N').setConstant(False)
    w.var('signal_N').setVal(1000)
    ## Set the scale and resolution defaults to MC truth
    phoScale.setVal(phoScaleTrue.getVal())
    phoRes.setVal(phoResTrue.getVal())
    ## Change the name
    tokens = name.split('_')
    if 'fit' in tokens[-1]:
        del tokens[-1]
    tokens.append('fit' + components)
    name = '_'.join(tokens)
## End of set_fit_components(components)


#-------------------------------------------------------------------------------
def process_real_data():
    '''
    Get, fit and plot real data for all 3 dataset specified:
    "data" (full 2011A+B), "2011A" or "2011B".
    '''
    ## store the the mc truth values in the workspace
    fitresult = fit_mc_truth(data['fsr1'])
    w.Import(fitresult, 'fitresult_mctruth')
    set_mc_truth(calibrator0.s, calibrator0.r)
    validate_response_fit(data['fsr1'], fitresult)

    #process_real_data_single_dataset('2011A')
    #check_timer('13.1 get, fit and plot 2011A real data')

    #process_real_data_single_dataset('2011B')
    #check_timer('13.2 get, fit and plot 2011B real data')

    process_real_data_single_dataset('data')
    check_timer('13.3 get, fit and plot 2011A+B real data')
## End of process_real_data().
    

#-------------------------------------------------------------------------------
def fit_mc_truth(idata):
    '''
    Fits the MC truth for the model sample and returns the fit result.
    '''
    old_precision = set_default_integrator_precision(2e-9, 2e-9)
    calibrator0.s.setRange(-15, 15)
    calibrator0.r.setRange(0,25)
    fitresult = calibrator0.phoEResPdf.fitTo(
        idata, roo.Range(-50, 50), roo.Strategy(2), roo.Save()
        )
    ## Include systematics
    scale_errors(calibrator0.s, 5.)
    scale_errors(calibrator0.r, 1.2)
    set_default_integrator_precision(*old_precision)
    return fitresult
## End of fit_mc_truth().


#-------------------------------------------------------------------------------
def scale_errors(var, factor):
    '''
    Scales the errors of var by the given factor.
    '''
    var.setError(factor * var.getError())
    if var.hasAsymError():
        var.setAsymError(factor * var.getErrorLo(), factor * var.getErrorHi())
## End of scale_errors(var, factor)


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

    nll = pm.createNLL(fitdata1, roo.Range('fit'), roo.NumCPU(8), 
                       roo.Extended(True))

    minuit = ROOT.RooMinuit(nll)
    minuit.setProfile()
    minuit.setVerbose()

    phoScale.setError(1)
    phoRes.setError(1)
    
    ## Set initial values equal to MC truth
    phoScale.setVal(calibrator0.s.getVal())
    phoRes.setVal(calibrator0.r.getVal())

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
    fitresult_mctruth = fit_mc_truth(data['fsr1'])
    draw_latex_for_fit_to_monte_carlo()
    set_mc_truth(calibrator0.s, calibrator0.r)
    validate_response_fit(data['fsr1'], fitresult_mctruth)
    ## Store the result in the workspace:
    w.Import(fitresult_mctruth, 'fitresult_mctruth')
    w.saveSnapshot('mc_fit', ROOT.RooArgSet(phoScale, phoRes,
                                            phoScaleTrue, phoResTrue))
    validate_mass_fit(fitdata1, fitres)
                                                
    check_timer('8. fast plots')
## End of process_monte_carlo


#-------------------------------------------------------------------------------
def draw_latex_for_fit_to_monte_carlo():
    ## Draw the results on the canvas:
    global fsr_purity
    ntot, nztot = 0, 0
    for x in 'signal_N zj_N exp_N'.split():
        ntot += w.var(x).getVal()
        if x != 'exp_N':
            nztot += w.var(x).getVal()
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
            '  MC Truth: %.2f' % (
                fsr_purity / (1. + w.var('exp_N').getVal() / nztot)
                ),
            '  MC Fit: %.2f #pm %.2f' % (
                100 * w.var('signal_N').getVal() / ntot,
                100 * w.var('signal_N').getError() / ntot
                )
        ],
        position=(0.2, 0.8)
        ).draw()
## End of draw_latex_for_fit_to_monte_carlo()


#-------------------------------------------------------------------------------
def validate_mass_fit(dataset, fit_result):
    '''
    Plot the data/fit in small and large range, residuals, pulls, pull
    distribution, chi2 prob and parameters for a dataset specified by the label:
    "data" (full 2011A+B), "2011A" or "2011B".
    '''
    # plot_mass_tails(dataset, fit_result)
    tails_plot = plot_mass_varbins(dataset, (60, 120), True)
    save_gof(tails_plot, fit_result)
    # draw_gof_latex()
    pulls_plot = plot_mass_residuals(tails_plot, fit_result, True)
    # draw_gof_latex()
    pulldist_plot = plot_pull_distribution(pulls_plot)
    # plot_mass_peak(dataset, fit_result)
    peak_plot = plot_mass_varbins(dataset, (60, 120))
    resid_plot = plot_mass_residuals(peak_plot, fit_result)
    for p in [peak_plot, resid_plot]:
        p.GetXaxis().SetRangeUser(80, 100)
    ## Make a landscape canvas
    canvas = canvases.next(name + '_mass_landscape')
    canvas.SetWindowSize(1200, 600)
    canvas.Divide(3,2)
    myplots = [tails_plot, peak_plot, pulldist_plot, pulls_plot, resid_plot]
    mytitles = ['Full Fit Range', 'Peak Detail',
                'Distribution of #chi^{2} Pulls Overlayed with Unit Gaussian', 
                '#chi^{2} Pulls', '#chi^{2} Residuals', '']
    pads = [canvas.cd(i) for i in range(1, 7)]        
    pads[0].SetLogy()
    ## Draw frames
    for i, (plot, title) in enumerate(zip(myplots, mytitles)):
        pad = canvas.cd(i+1)
        pad.SetGrid()
        plot.SetTitle(title)
        plot.Draw()
    canvas.cd(6)
    Latex(['Mass Fit (PHOSPHOR)'], position=(0.1, 0.9)).draw()
    draw_gof_latex(position=(0.1, 0.8), rowheight=0.08)
    Latex(['s_{true}: ' + latexpm(phoScaleTrue),
           's_{fit} : ' + latexpm(phoScale),],
           position=(0.1, 0.6), rowheight=0.08).draw()
    Latex(['r_{true}: ' + latexpm(phoResTrue),
           'r_{fit} : ' + latexpm(phoRes),],
           position=(0.55, 0.6), rowheight=0.08).draw()
    Latex(['N_{S}: ' + latexpm(w.var('signal_N')),
           'N_{Z+j}: ' + latexpm(w.var('zj_N')),
           'N_{exp}: ' + latexpm(w.var('exp_N')),
           '#lambda_{exp}: ' + latexpm(w.var('exp_c')),],
           position = (0.1, 0.4), rowheight=0.08).draw()
## End of validate_mass_fit().


#-------------------------------------------------------------------------------
def latexpm(var):
    '''
    Returns a string that is a ROOT-style latex code for the variable
    value +/- error unit.
    '''
    if var.isConstant():
        ret = '%g' % var.getVal()
    else:
        if var.getError() < 1e-6:
            ret = '%g #pm %g' % (var.getVal(), var.getError())
        else:
            precission = max(0, 1 + int(0.5 - ROOT.TMath.Log10(var.getError())))
            ret = '%.*f #pm %.*f' % (precission, var.getVal(), 
                                     precission, var.getError())
    if var.getUnit():
        ret += ' ' + var.getUnit()
    return ret
## End of latexpm(var)


#-------------------------------------------------------------------------------
def validate_response_fit(idata, fit_result):
    '''
    Plot the data/fit in small and large range, residuals, pulls, pull
    distribution, chi2 prob and parameters for a dataset specified by the label:
    "data" (full 2011A+B), "2011A" or "2011B".
    '''
    sval = fit_result.floatParsFinal().find('s').getVal()
    rval = fit_result.floatParsFinal().find('r').getVal()
    zoom_range =  (sval - 2 * rval, sval + 2 * rval)
    full_range = (-50, 50)
    tails_plot = plot_response_varbins(idata, full_range, True)
    save_gof(tails_plot, fit_result, mctruth=True)
    pulls_plot = plot_response_residuals(tails_plot, fit_result, True)
    pulldist_plot = plot_pull_distribution(pulls_plot)
    peak_plot = plot_response_varbins(idata, full_range)
    resid_plot = plot_response_residuals(peak_plot, fit_result)
    for p in [peak_plot, resid_plot]:
        p.GetXaxis().SetRangeUser(*zoom_range)
    canvas = canvases.next(name + '_response_landscape')
    canvas.SetWindowSize(1200, 600)
    canvas.Divide(3,2)
    myplots = [tails_plot, peak_plot, pulldist_plot, pulls_plot, resid_plot]
    mytitles = ['Full Fit Range', 'Peak Detail',
                'Distribution of #chi^{2} Pulls Overlayed with Unit Gaussian', 
                '#chi^{2} Pulls', '#chi^{2} Residuals', '']
    pads = [canvas.cd(i) for i in range(1, 7)]        
    pads[0].SetLogy()
    ## Draw frames
    for i, (plot, title) in enumerate(zip(myplots, mytitles)):
        pad = canvas.cd(i+1)
        pad.SetGrid()
        plot.SetTitle(title)
        plot.Draw()
    canvas.cd(6)
    Latex(['Response Fit (MC Truth)'], position=(0.1, 0.9)).draw()
    draw_gof_latex(position=(0.1, 0.8), rowheight=0.08)
    Latex(['s_{true}: ' + latexpm(phoScaleTrue),],
           position=(0.1, 0.6), rowheight=0.08).draw()
    Latex(['r_{true}: ' + latexpm(phoResTrue),],
           position=(0.55, 0.6), rowheight=0.08).draw()    
## End of validate_response_fit().


#-------------------------------------------------------------------------------
def plot_mass_varbins(dataset, plot_range, logy=False):
    global plots    
    #mmgMass.setBins(40)
    mmgMass.setRange('varbins', *plot_range)
    plot = mmgMass.frame(roo.Range('varbins'))
    plots.append(plot)
    plot.SetTitle('Mass Peak with Variable Binning')
    reduced_data = dataset.reduce(
        '%f < mmgMass & mmgMass < %f' % plot_range
        )
    reduced_data = reduced_data.reduce(ROOT.RooArgSet(mmgMass))
    ddbins = get_auto_binning(reduced_data)
    bins = ddbins.binning(ROOT.RooBinning())
    bins.SetName('chi2')
    uniformBins = ddbins.uniformBinning(ROOT.RooUniformBinning())
    uniformBins.SetName('normalization')
    ## This is hack to make RooFit use a nice normaliztion.
    ## First plot the data with uniform binning but don't display it.
    reduced_data.plotOn(plot, roo.Binning(uniformBins), roo.Invisible())
    reduced_data.plotOn(plot, roo.Binning(bins))    
    hist = plot.getHist('h_' + reduced_data.GetName())
    ddbins.applyTo(hist)
    norm = reduced_data.sumEntries()
    pm.plotOn(plot, roo.Range('varbins'), roo.NormRange('varbins'),
              roo.Normalization(norm, ROOT.RooAbsReal.NumEvent),
              roo.Components('*zj*,*exp*'), roo.LineStyle(ROOT.kDashed))
    pm.plotOn(plot, roo.Range('varbins'), roo.NormRange('varbins'),
              roo.Normalization(norm, ROOT.RooAbsReal.NumEvent),        
              roo.Components('*exp*'), roo.LineStyle(ROOT.kDotted))
    pm.plotOn(plot, roo.Range('varbins'), roo.NormRange('varbins'),
              roo.Normalization(norm, ROOT.RooAbsReal.NumEvent),)
    myname = name + '_' + dataset.GetName() + '_peak_varbins'
    plot.SetName(myname)
    #canvas = canvases.next(myname)
    #canvas.SetGrid()
    #plot.Draw()
    if (logy):
        plot.SetMaximum(math.pow(plot.GetMaximum(), 1.2))
        plot.SetMinimum(1e-1)
        #canvas.SetLogy()
    return plot
## End of plot_mass_varbins(dataset).


#-------------------------------------------------------------------------------
def plot_response_varbins(idata, plot_range, logy=False):
    global plots    
    phoERes.setRange('varbins', *plot_range)
    plot = phoERes.frame(roo.Range('varbins'))
    plots.append(plot)
    plot.SetTitle('Response Peak with Variable Binning')
    idata = idata.reduce(
        '%f < phoERes & phoERes < %f' % plot_range
        )
    idata = idata.reduce(ROOT.RooArgSet(phoERes))
    ddbins = get_auto_binning(idata)
    bins = ddbins.binning(ROOT.RooBinning())
    bins.SetName('chi2')
    uniformBins = ddbins.uniformBinning(ROOT.RooUniformBinning())
    uniformBins.SetName('normalization')
    ## This is hack to make RooFit use a nice normaliztion.
    ## First plot the data with uniform binning but don't display it.
    idata.plotOn(plot, roo.Binning(uniformBins), roo.Invisible())
    idata.plotOn(plot, roo.Binning(bins))    
    hist = plot.getHist('h_' + idata.GetName())
    ddbins.applyTo(hist)
    norm = idata.sumEntries()
    model = calibrator0.phoEResPdf
    model.plotOn(plot, roo.Range('varbins'), roo.NormRange('varbins'),
                 roo.Normalization(norm, ROOT.RooAbsReal.NumEvent),)
    myname = name + '_' + idata.GetName() + '_response_varbins'
    plot.SetName(myname)
    if (logy):
        plot.SetMaximum(math.pow(plot.GetMaximum(), 1.2))
        plot.SetMinimum(1e-1)
    return plot
## End of plot_response_varbins(idata).


#-------------------------------------------------------------------------------
def plot_mass_residuals(source, fit_result, normalize=False):
    global plots
    plot = mmgMass.frame(roo.Range(*get_plot_range(source)))
    plots.append(plot)
    chi2calculator = RooChi2Calculator(source)
    for hname in 'h_data h_data_fit1 h_fitdata1'.split():
        if source.getHist(hname):
            break
    if normalize:
        hist = chi2calculator.pullHist(hname, 'pm_Norm[mmgMass]', True)
        plot.SetTitle('#chi^{2} Pulls')
        ytitle = '(Data - Fit) / #sqrt{Fit}'
        # canvases.next(source.GetName() + '_pulls').SetGrid()
    else:
        hist = chi2calculator.residHist(hname, 'pm_Norm[mmgMass]', False, True)
        plot.SetTitle('#chi^{2} Residuals')
        ytitle = 'Data - Fit'
        # canvases.next(source.GetName() + '_residuals').SetGrid()
    plot.GetYaxis().SetTitle(ytitle)
    plot.addPlotable(hist, 'P')    
    # plot.Draw()
    return plot
## End of plot_mass_residuals(plot, fit_result)


#-------------------------------------------------------------------------------
def plot_response_residuals(source, fit_result, normalize=False):
    global plots
    plot = phoERes.frame(roo.Range(*get_plot_range(source)))
    plots.append(plot)
    chi2calculator = RooChi2Calculator(source)
    for histname in 'h_data h_data_fsr1'.split():
        if source.getHist(histname):
            break
    if normalize:
        hist = chi2calculator.pullHist(histname, 'phoEResPdf_Norm[phoERes]', True)
        plot.SetTitle('#chi^{2} Pulls')
        ytitle = '(Data - Fit) / #sqrt{Fit}'
        # canvases.next(source.GetName() + '_pulls').SetGrid()
    else:
        hist = chi2calculator.residHist(histname, 'phoEResPdf_Norm[phoERes]', False, True)
        plot.SetTitle('#chi^{2} Residuals')
        ytitle = 'Data - Fit'
        # canvases.next(source.GetName() + '_residuals').SetGrid()
    plot.GetYaxis().SetTitle(ytitle)
    plot.addPlotable(hist, 'P')    
    # plot.Draw()
    return plot
## End of plot_mass_residuals(plot, fit_result)


#-------------------------------------------------------------------------------
def save_gof(plot, fit_result, mctruth=False):
    '''
    Calculates GOF parameters and stores them in the workspace.
    '''
    ## Subtract one parameter for the normalization that is fixed
    ## for the chi2 calculation.
    npars = fit_result.floatParsFinal().getSize() - 1
    chi2calculator = RooChi2Calculator(plot)
    ndof = chi2calculator.numDOF(npars)
    ## Second parameter is to renormalize: guarantees that the total
    ## observed and expected events is the same.  This is to
    ## avoid some spurious disagreements in the normalization presumably due
    ## to the finickiness of RooFit and numarical rounding.
    chi2 = chi2calculator.chiSquare(npars, True) * ndof
    pvalue = ROOT.TMath.Prob(chi2, ndof)
    w.var('chi2').setVal(chi2)
    w.var('ndof').setVal(ndof)
    w.var('pvalue').setVal(pvalue)
    if mctruth:
        tok = 'mctruth'
    else:
        for tok in name.split('_'):
            if 'fit' in tok:
                break
    w.saveSnapshot(tok, w.set('gof'))
## End of save_gof(plot)


#-------------------------------------------------------------------------------
def draw_gof_latex(position=(0.2, 0.8), rowheight=0.055):
    '''
    Draws latex labes with GOF information: chi2 / ndof, and p-value.
    Precondition: a canvas exists.
    '''
    ndof = w.var('ndof').getVal()
    chi2 = w.var('chi2').getVal()
    pval = w.var('pvalue').getVal()
    if pval < 1e-3:
        pvaltext = '%.2g' % pval
    else:
        pvaltext = '%.2g %%' % (100 * pval)
    Latex(['#chi^{2} / N_{DOF}: %.2g / %d' % (chi2, ndof),
           'p-value: ' + pvaltext,],
          position, rowheight=rowheight,
          ).draw()
## End of draw_gof_latex()
    

#-------------------------------------------------------------------------------
def get_plot_range(plot):
    '''
    Returns the x-axis range of the given RooPlot.
    '''
    xaxis = plot.GetXaxis()
    xmin = xaxis.GetBinLowEdge(1)
    xmax = xaxis.GetBinUpEdge(xaxis.GetNbins())
    return (xmin, xmax)
## End of get_plot_range(plot)


#-------------------------------------------------------------------------------
def get_hist_range(hist):
    '''
    Returns the x-axis range of the given RooHist.
    '''
    xaxis = plot.GetXaxis()
    xmin = xaxis.GetBinLowEdge(1)
    xmax = xaxis.GetBinUpEdge(xaxis.GetNbins())
    return (xmin, xmax)
## End of get_plot_range(plot)


#-------------------------------------------------------------------------------
def plot_pull_distribution(pull_plot):
    '''
    Returns a RooPlot with the distribution of pulls overlayed with
    a unit Gaussian.
    '''
    ## Plot the pull spectrum
    normal_pdf = w.pdf('normal_pdf')
    if not normal_pdf:
        normal_pdf = w.factory(
            'Gaussian::normal_pdf(pull[-6,6],zero[0],unit[1])'
            )
    pull = w.var('pull')
    pull.SetTitle('#chi^{2} Pulls (Data - Fit) / #sqrt{Fit}')
    pull.setBins(10)
    plot = pull.frame()
    plot.SetYTitle('Bins of %s' % mmgMass.GetTitle())
    data = ROOT.RooDataSet(name + '_pulls', 'Pulls', ROOT.RooArgSet(pull))
    hpull = pull_plot.getHist()
    for i in range(hpull.GetN()):
        pull.setVal(hpull.GetY()[i])
        data.add(ROOT.RooArgSet(pull))
    w.Import(data)
    data.plotOn(plot)
    normal_pdf.plotOn(plot)
    return plot
## End plot_pull_distribution(pull_plot)


#-------------------------------------------------------------------------------
def plot_mass_peak(dataset, fit_result):
    global plots
    label = dataset.GetName()
    mmgMass.setBins(60)
    plot = mmgMass.frame(roo.Range('peak'))
    plots.append(plot)
    plot.SetTitle('Mass Peak')
    dataset.plotOn(plot)
    pm.plotOn(plot, roo.Range('peak'), roo.NormRange('peak'))
    pm.plotOn(plot, roo.Range('peak'), roo.NormRange('peak'),
              roo.Components('*zj*,*exp*'), roo.LineStyle(ROOT.kDashed))
    pm.plotOn(plot, roo.Range('peak'), roo.NormRange('peak'),
              roo.Components('*exp*'), roo.LineStyle(ROOT.kDotted))
    canvas = canvases.next(name + '_' + label + '_peak')
    canvas.SetGrid()
    plot.Draw()
    npars = fit_result.floatParsFinal().getSize()
    ndof = plot.getHist('h_data').GetN() - npars
    chi2 = plot.chiSquare('pm_Norm[mmgMass]_Range[peak]_NormRange[peak]',
                          'h_data', npars) * ndof
    Latex(['#chi^{2} / N_{DOF}: %.2g / %d' % (chi2, ndof),
           'p-value: %.2g %%' % (100 * ROOT.TMath.Prob(chi2, ndof)),
           ],
          position=(0.2, 0.8)
          ).draw()
    ## Residuals
    canvas = canvases.next(name + '_' + label + '_peak_residuals').SetGrid()
    rhist = plot.residHist('h_data',
                           'pm_Norm[mmgMass]_Range[peak]_NormRange[peak]')
    rplot = mmgMass.frame(roo.Range('peak'))
    rplot.SetTitle('Mass Peak Fit Residuals')
    ytitle = plot.GetYaxis().GetTitle().replace('Events', 'Data - Fit')
    rplot.GetYaxis().SetTitle(ytitle)
    rplot.addPlotable(rhist, 'P')
    rplot.Draw()
    Latex(['#chi^{2} / N_{DOF}: %.2g / %d' % (chi2, ndof),
           'p-value: %.2g %%' % (100 * ROOT.TMath.Prob(chi2, ndof)),
           ],
          position=(0.2, 0.8)
          ).draw()    
    plots.append(rplot)
## End of plot_mass_peak().


#-------------------------------------------------------------------------------
def plot_mass_tails(dataset, fit_result):
    global plots
    label = dataset.GetName()
    mmgMass.setBins(60)
    plot = mmgMass.frame(roo.Range('tails'))
    plots.append(plot)
    plot.SetTitle('Mass Tails')
    dataset.plotOn(plot)
    pm.plotOn(plot, roo.Range('tails'), roo.NormRange('tails'))
    pm.plotOn(plot, roo.Range('tails'), roo.NormRange('tails'),
              roo.Components('*zj*,*exp*'), roo.LineStyle(ROOT.kDashed))
    pm.plotOn(plot, roo.Range('tails'), roo.NormRange('tails'),
              roo.Components('*exp*'), roo.LineStyle(ROOT.kDotted))
    canvas = canvases.next(name + '_' + label + '_tails')
    canvas.SetGrid()
    canvas.SetLogy()
    plot.Draw()
    plot.SetMaximum(math.pow(plot.GetMaximum(), 1.2))
    npars = fit_result.floatParsFinal().getSize()
    ndof = plot.getHist('h_data').GetN() - npars
    chi2 = plot.chiSquare('pm_Norm[mmgMass]_Range[peak]_NormRange[peak]',
                          'h_data', npars) * ndof
    print 'plot_mass_tails: npars, ndof, chi2:', npars, ndof, chi2
    Latex(['#chi^{2} / N_{DOF}: %.2g / %d' % (chi2, ndof),
           'p-value: %.2g %%' % (100 * ROOT.TMath.Prob(chi2, ndof)),
           ],
          position=(0.2, 0.8)
          ).draw()    
    ## Pulls
    canvas = canvases.next(name + '_' + label + '_tails_pulls')
    rhist = plot.residHist(
        'h_data', 
        'pm_Norm[mmgMass]_Range[tails]_NormRange[tails]',
        True)
    rplot = mmgMass.frame(roo.Range('tails'))
    rplot.SetTitle('Mass Tails Fit Pulls')
    ytitle = plot.GetYaxis().GetTitle().replace(
        'Events', '(Data - Fit) / Error'
        )
    rplot.GetYaxis().SetTitle(ytitle)
    rplot.addPlotable(rhist, 'P')
    rplot.Draw()
    plots.append(rplot)
    Latex(['#chi^{2} / N_{DOF}: %.2g / %d' % (chi2, ndof),
           'p-value: %.2g %%' % (100 * ROOT.TMath.Prob(chi2, ndof)),
           ],
          position=(0.2, 0.8)
          ).draw()    
## End of plot_mass_tails().


#--------------------------------------------------------------------------
def get_auto_binning(idata):
    '''
    Get binning that is uniform around that peak area and non-uniform
    in the tails.  It guaranties that the number of entries per bin is
    in a given range [minEntriesPerBin, maxEntriesPerBin] by merging
    neighboring bins in the tails. This is useful for calculation of
    chi2 statistic that obeys the chi2 PDF.
    Optional features:
      * the bin width is a pretty number, e.g. 1, 0.5, 0.2, etc.
      * calculate the median for each bin. (->better looking plot)
    '''
    ## Get the data as an array of doubles pointed by a tree
    name = idata.get().first().GetName()
    entries = idata.tree().Draw(name, '', 'goff')
    ## Create the DataDrivenBinning object with bincontent in 35-200
    bins = DataDrivenBinning(entries, idata.tree().GetV1(), 20, 500)
    return bins
## end of get_auto_binning(data)


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
