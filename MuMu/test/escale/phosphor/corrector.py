'''
Dumps snippet of code for the PhosphoCorrectorFunctor
That gives the results of the scale and resolution
measurements.
'''

import os
import socket
import ROOT
import JPsi.MuMu.common.roofit as roo

ROOT.gSystem.Load('libJPsiMuMu')

##------------------------------------------------------------------------------
def main():
    '''
    Main entry point of execution.  Writes a snippet of c++
    code to STDOUT.
    '''
    elines = get_enum_lines()

    lines = get_snippet_lines('scale')
    lines.extend(get_snippet_lines('resolution'))

    indent(elines, '    ')
    indent(lines, '  ')    

    print '\n'.join(elines)
    print
    print '\n'.join(lines)
## End of main().

 
##------------------------------------------------------------------------------
def get_snippet_lines(varname):
    '''
    Returns a list of strings representing lines of a snippet of c++ code
    that inicializes the vector or scales or resolutions (depending on given
    varname) with their measured values in %.
    '''
    lines = get_header_lines(varname)
    lines.extend(loop_over_categories(varname))
    return lines
## End of dump_scale_snippet()


##------------------------------------------------------------------------------
def get_header_lines(varname):
    '''
    Returns the header lines for both the scale and resolution.
    '''
    lines = ['/// Measured values of {x} in (%)',
             'std::vector<double> {x}s(kNumCategories);',
             '']
    return [l.format(x=varname) for l in lines]
## End of print_header()


##------------------------------------------------------------------------------
def loop_over_categories(varname):
    '''
    Loops over the photon categories and provides a line for each. Returns
    a string of the lines.
    '''
    categories = get_categories()

    names = get_category_names(categories)
    max_name_length = max([len(n) for n in names])

    varname_to_correctorname_map = {
        'scale' : 'scaleMeasurement',
        'resolution' : 'resolutionMeasurement',
        }

    correctorname = varname_to_correctorname_map[varname]
    
    lines = []
    for name, (data, period, subdet, pt) in zip(names, categories):
        value = get_value(varname, data, period, subdet, pt)
        protoline = '{x}s[{c:{width}s}] = {v:>6.2f};'
        lines.append(protoline.format(x=correctorname, c=name, v=value,
                                      width=max_name_length))
        ## Add an empty line for greater readability.
        if (data, period) == ('RealData', '2011all'):
            lines.append('')
    return lines
## End of loop_over_categories.


##------------------------------------------------------------------------------
def get_categories():
    '''
    Returns a list of strings that are the category enumearation variables.
    '''
    categories = []
    for subdet in 'Barrel Endcaps'.split():
        for pt in '10to12 12to15 15to20 20to999'.split():
            for data in 'MonteCarlo RealData'.split():
                for period in '2011A 2011B 2011all'.split():
                    categories.append((data, period, subdet, pt))
    return categories
## End of get_categories


##------------------------------------------------------------------------------
def get_category_names(categories):
    '''
    Returns a list of the categories of enum names.
    '''
    names = []
    for data, period, subdet, pt in categories:
        names.append('k' + ''.join([data, period, subdet, 'Et', pt]))
    return names
## End of get_category_names(categories)


def get_enum_lines():
    '''
    Returns a list of strings corresponding to lines of a c++ code snippet
    defining the enum Category.
    '''
    ## Get the list of category names
    lines = get_category_names(get_categories())
    lines.sort()
    lines.append('kUnspecified')
    lines.append('kNumCategories')
    ## Make sure the first category has value equal to "0":
    lines[0] = lines[0] + ' = 0'
    ## Pad lines with whitespace from the right.
    width = max([len(l) for l in lines])
    for i in range(len(lines)):
        lines[i] = '{0:<{width}}'.format(lines[i], width=width)
    ## Add the prefix to the first line, pad other lines with spaces:
    prefix = 'enum Category {'
    indent(lines, ' ' * len(prefix))
    lines[0] = lines[0].replace(' ' * len(prefix), prefix)
    ## Add trailing commas
    for i in range(len(lines) - 1):
        lines[i] = lines[i] + ','
    ## Add the final closing brace:
    lines[-1] = lines[-1] + '};'
    return lines
## End of get_enum_lines().

##------------------------------------------------------------------------------
def indent(lines, prefix):
    '''
    Indents lines with the given prefix.
    '''
    for i, l in enumerate(lines):
        lines[i] = prefix + l
## End of indent.


##------------------------------------------------------------------------------
def get_value(varname, data, period, subdet, pt):
    
    varname_to_xname_map = {
        'scale' : 'phoScale',
        'resolution' : 'phoRes',
        }

    data_to_getter_factory_map = {
        'MonteCarlo' :
            lambda workspace, period, xname: workspace.var(xname).getVal(),
            
        'RealData' : (
            lambda w, fitresult, x:
            w.obj(fitresult).floatParsFinal().find(x).getVal()
            ),
        }

    period_to_fitresult_map = {
        '2011A'   : 'fitresult_2011A',
        '2011B'   : 'fitresult_2011B',
        '2011all' : 'fitresult_data',
        }

    workspace = get_workspace(data, period, subdet, pt)
    xname = varname_to_xname_map[varname]
    fitresult = period_to_fitresult_map[period]
    getter = data_to_getter_factory_map[data]
    
    if data == 'MonteCarlo':
        xname = xname + 'True'
        workspace.loadSnapshot('mc_fit')
        
    return getter(workspace, fitresult, xname)
## End of get_value().


##------------------------------------------------------------------------------
def get_jobname(data, period, subdet, pt):
    '''
    Returns the jobname for the given data, period, subdet and pt.
    '''
    data_label_postfix_map = {
        'MonteCarlo' : ('mc', '_evt3of4'),
        'RealData' : ('data', '')
        }

    period_version_map = {
        '2011A' : 'v14',
        '2011B' : 'v15',
        '2011all' : 'v13',
        }
    
    subdet_label_map = {
        'Barrel' : 'EB',
        'Endcaps' : 'EE',
        }

    data_label, postfix = data_label_postfix_map[data]
    version = period_version_map[period]
    subdet_label = subdet_label_map[subdet]

    jobname = 'sge_{data}_{subdet}_pt{pt}_{version}'.format(
        data=data_label, subdet=subdet_label, pt=pt, version=version
        ) + postfix

    return jobname
## End of get_jobname(data, period, subdet, pt)
    
##------------------------------------------------------------------------------
def get_workspace(data, period, subdet, pt):
    '''
    Returns the workspace for the given data, subdet and pt.
    '''
    jobname = get_jobname(data, period, subdet, pt)
    basepath = get_basepath()
    basefilename = ('phosphor5_model_and_fit_'
                    'test_mc_EE_highR9_pt30to999_v13_evt1of4.root')
    filename = os.path.join(basepath, jobname, basefilename)
    file = ROOT.TFile.Open(filename)
    return file.Get(jobname + '_workspace')
## End of get_workspace()


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


##------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
    import user
