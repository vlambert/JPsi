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
    #elines = get_enum_lines()

    #lines = get_snippet_lines('scale')
    #lines.extend(get_snippet_lines('resolution'))

    #indent(elines, '    ')
    #indent(lines, '  ')    

    #print '\n'.join(elines)
    #print
    #print '\n'.join(lines)
    
    
    get_category_names(get_categories())

        
## End of main().

 
##------------------------------------------------------------------------------
def get_snippet_lines(varname):
    '''
    Returns a list of strings representing lines of a snippet of c++ code
    that initializes the vector or scales or resolutions (depending on given
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
    for name, (data, pileup, subdet, pt, r9) in zip(names, categories):
        value = get_value(varname, data, pileup, subdet, pt, r9)
        protoline = '{x}s[{c:{width}s}] = {v:>6.2f};'
        lines.append(protoline.format(x=correctorname, c=name, v=value,
                                      width=max_name_length))
        ## Add an empty line for greater readability.
        if (data, pileup) == ('RealData', 'HighNV'):
            lines.append('')
    return lines
## End of loop_over_categories.


##------------------------------------------------------------------------------
def get_categories():
    '''
    Returns a list of strings that are the category enumearation variables.
    '''
    categories = []
    #for subdet in 'Barrel Endcaps'.split():
    #    for pt in 'pt10to12 pt12to15 pt15to20 pt20to999 pt20to25 pt25to30 pt30to999'.split():
    #        for r9 in 'HighR9 LowR9'.split():
    #            for data in 'MonteCarlo RealData'.split():
    #                for pileup in 'HighNV LowNV'.split():
                        #for period in '2011 2012'.split():
    #                    categories.append((data, pileup, subdet, pt, r9))

    for subdet in 'Endcaps'.split():
        for pt in 'pt10to12 pt12to15 pt15to20'.split():
            for r9 in 'LowR9'.split():
                for data in 'RealData'.split():
                    for pileup in 'HighNV LowNV'.split():
                        categories.append((data,pileup,subdet,pt,r9))



    #print "CATEGORIES" ,categories               
    return categories
## End of get_categories


##------------------------------------------------------------------------------
def get_category_names(categories):
    '''
    Returns a list of the categories of enum names.
    '''
    names = []
    name_to_number = {
        'MonteCarlo' : '0',
        'RealData' : '1',
        'HighNV' : '0',
        'LowNV' : '1',
        'HighR9': '0',
        'LowR9' : '1',
        'Barrel' : '0',
        'Endcaps' : '1',
        'pt10to12' : '0',
        'pt12to15' : '1',
        'pt15to20': '2',
        'pt20to999' : '3',
        'pt20to25'  : '4',
        'pt25to30'  : '5',
        'pt30to999' : '6',
        'scale' : '0',
        'resolution' : '1',
        }
    #print "Scales"
    print "PileUp(High, Low)=(0,1) DATA(mc,data)=(0,1) Detector(EB,EE)=(0,1) R9(high, low)=(0,1) Pt(0,1,2,3,4,5,6) Correction(scale,resolution)=(0,1)"
    for data, pileup, subdet, pt, r9 in categories:
        print name_to_number[pileup],name_to_number[data],name_to_number[subdet],name_to_number[r9], name_to_number[pt], name_to_number['scale'], "%0.2f"%get_value('scale' , data, pileup, subdet, pt, r9)
    for data, pileup, subdet, pt, r9 in categories:   
        print name_to_number[pileup], name_to_number[data], name_to_number[subdet], name_to_number[r9], name_to_number[pt], name_to_number['resolution'], "%0.2f"%get_value('resolution' , data, pileup, subdet, pt, r9)
        
    return names
## End of get_category_names(categories)

##------------------------------------------------------------------------------
def get_value(varname, data, pileup, subdet, pt, r9):
    
    varname_to_xname_map = {
        'scale' : 'phoScale',
        'resolution' : 'phoRes',
        }

    data_to_getter_factory_map = {
        'MonteCarlo' :
            lambda workspace, pileup, xname: workspace.var(xname).getVal(),
            
        'RealData' : (
            lambda w, fitresult, x:
            #w.obj(fitresult).floatParsFinal().find(x).getVal()
            w.var(x).getVal()
            ),
        }

    pileup_to_fitresult_map = {
        'HighNV'   : 'fitresult_data_SEB',
        'LowNV'   : 'fitresult_data_SEB',
        }

    workspace = get_workspace(data, pileup, subdet, pt, r9)
    #workspace.Print()
    xname = varname_to_xname_map[varname]
    fitresult = pileup_to_fitresult_map[pileup]
    getter = data_to_getter_factory_map[data]

    #print "fit_result= " , fitresult
    #print "data= " , data
    
    if data == 'MonteCarlo':
        xname = xname + 'True'
        workspace.loadSnapshot('mc_fit')
        
    return getter(workspace, fitresult, xname)
## End of get_value().


##------------------------------------------------------------------------------
def get_jobname(data, pileup, subdet, pt, r9):
    '''
    Returns the jobname for the given data, period, subdet and pt.
    '''
    data_label_postfix_map = {
        'MonteCarlo' : ('mc', ''),
        'RealData' : ('data', '')
        }

    pileup_version_map = {
        'HighNV' : 'HighNV',#name on file
        'LowNV' : 'LowNV',#name on file
        }
    
    subdet_label_map = {
        'Barrel' : 'EB',
        'Endcaps' : 'EE',
        }

    pt_label_map = {
        'pt10to12' : 'PtLow_10_PtHigh_12',
        'pt12to15' : 'PtLow_12_PtHigh_15',
        'pt15to20' : 'PtLow_15_PtHigh_20',
        'pt20to25' : 'PtLow_20_PtHigh_25',
        'pt25to30' : 'PtLow_25_PtHigh_30',
        'pt30to999': 'PtLow_30_PtHigh_999',
        'pt20to999': 'PtLow_30_PtHigh_999',
        }

    r9_label_map = {
        'HighR9' : 'R9Low_0.94_R9high_999',
        'LowR9'  : 'R9Low_0_R9high_0.94',
        }

    data_label, postfix = data_label_postfix_map[data]
    version = pileup_version_map[pileup]
    subdet_label = subdet_label_map[subdet]
    pt_label = pt_label_map[pt]
    r9_label = r9_label_map[r9]

    if pileup == 'HighNV':
        if subdet_label == 'EB' :
            jobname = 'phosphor5_model_and_fit_{data}_{subdet}_sixie_{version}_{r9}_{pt}.root'.format(
                data=data_label, subdet=subdet_label, pt=pt_label, r9=r9_label,version=version) + postfix
        elif subdet_label == 'EE' :
             jobname = 'phosphor5_model_and_fit_{data}_{subdet}_sixie_{version}_{r9}_{pt}.root'.format(
                 data=data_label, subdet=subdet_label, pt=pt_label, r9=r9_label, version=version) + postfix
             
    elif pileup == 'LowNV':
        if subdet_label == 'EB' :
            jobname = 'phosphor5_model_and_fit_{data}_{subdet}_sixie_{version}_{r9}_{pt}.root'.format(
                data=data_label, subdet=subdet_label, pt=pt_label, r9=r9_label, version=version) + postfix 
        elif subdet_label == 'EE' :
            jobname = 'phosphor5_model_and_fit_{data}_{subdet}_sixie_{version}_{r9}_{pt}.root'.format(
                data=data_label, subdet=subdet_label, pt=pt_label, r9=r9_label, version=version) + postfix 
            

    return jobname
## End of get_jobname(data, period, subdet, pt)
    
##------------------------------------------------------------------------------
def get_workspace(data, pileup, subdet, pt, r9):
    '''
    Returns the workspace for the given data, subdet and pt.
    '''
    jobname = get_jobname(data, pileup, subdet, pt, r9)
    #print "jobname: ", jobname
    basepath = get_basepath()
    #print "basepath: ", basepath
    basefilename = ('phosphor5_model_and_fit_'
                    )
                   ##'test_mc_EE_highR9_pt30to999_v13_evt1of4.root')
    
    pileup_version_map = {
        'HighNV' : 'HighNV',#modifiy folder inside day it was created
        'LowNV' :  'LowNV',#modifiy folder inside day it was created
        }
    version = pileup_version_map[pileup]
    
    #filename = os.path.join(basepath, jobname, basefilename)
    #print "filename= ", filename
    filename = os.path.join(basepath, version, jobname)
    #print "filename= ", filename
    #print "jobname= ",  jobname.replace(" ", "").rstrip(jobname[-5:])
    jobname_aux =jobname.replace(" ", "").rstrip(jobname[-5:])
    #print "jobname= ",  jobname_aux[24:]
    file = ROOT.TFile.Open(filename)
    return file.Get(jobname_aux[24:] + '_workspace')
 
## End of get_workspace()


#______________________________________________________________________________
def get_basepath():
    '''
    Return the common part of the path to data files depending
    on the host machine.
    '''
    hostname_to_basepath_map = {
        't3-higgs.ultralight.org':
        '/home/vlambert/scratch_phosphor/CMSSW_4_2_8/src/JPsi/MuMu/test/escale/phosphor/Phosphor_Interface/Dir_Results/ExpFit_Numbers/'
        }
    
        #'t3-susy.ultralight.org':
        ##     '/home/cmorgoth/Jan_ExpFit_Numbers/',
        ##'Jan-Veverkas-MacBook-Pro.local':
        ##    '/Users/veverka/Work/Data/phosphor/sge_correction',
        ##}
    return hostname_to_basepath_map[socket.gethostname()]
## End of get_basepath()


##------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
    import user
