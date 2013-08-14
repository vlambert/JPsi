#!/bin/env python
## Creates PHOSPHOR fit jobs for the OSG.

import os
import commands

# project_name = 'phosphor_baseline_s6mc_v2'
# project_name = 'test6'
# project_name = 'eg_paper_dr0p1'
# project_name = 'eg_paper_jul2012rereco'
# project_name = 'eg_paper_rochcor_exp_v3'
# project_name = 'eg_paper_rochcor_exp_v4'
# project_name = 'eg_paper_rochcor_exp_fabrice'
# project_name = 'vg_baseline_rerecos'
# project_name = 'regressions_no_muon_bias'
# project_name = 'regressions_no_muon_bias_egpaper'
# project_name = 'regressions_with_muon_bias_egpaper_4ptbins'
# project_name = 'egm_fc_rscan'
# project_name = 'egm_fc_sscan_v2'
# project_name = 'regressions_no_muon_bias_v2'
# project_name = 'regressions_at_low_pt'
# project_name = 'regressions_no_muon_bias_12cat'
# project_name = 'regressions_no_muon_bias_8cat'
# project_name = 'regressions_no_muon_bias_6cat'
# project_name = 'regressions_with_muon_bias_6cat'
## 16JanReReco + Hggv2 + Rochcorr + Exp bkgd + EE incl. R9 + EB high/low R9
## cuts = ['mmMass + mmgMass < 180', 'minDeltaR < 1.5', 
##         'mu1Pt > 15', 'mu2Pt > 10']
project_name = 'htozg_v1'

# output_base = '/raid2/veverka/jobs/outputs'
output_base = '/home/veverka/jobs/outputs'
template_filename='JPsi/MuMu/scripts/phosphor-job.template'

#______________________________________________________________________________
def get_egpaper_list():
    '''
    Returns a list of job names for plots for the EGM-11-001 paper.
    '''
    job_names = []

    total_sections = 4

    for subdet in 'EB EE'.split():
        for pt in '25to999'.split():
            # for version in 'yyv3 yyv4 yyv4NoJSON'.split():
            #for version in 'yyv5'.split():
            for version in 'yyv6'.split():
                for source in 'data'.split():
                #for source in 'data mc'.split():
                    ## inclusive r9 job name
                    name = '_'.join(['egm_expbkg', source, subdet, 'pt'+pt, version])
                    job_names.append(name)                    
                    for r9 in 'lowR9 highR9'.split():
                        ## job name
                        name = '_'.join(['egm_expbkg', source, subdet, 'pt'+pt, 
                                          version, r9])
                        job_names.append(name) 
                
    ## Use only subsection of events for the training 
    ## and indepenedent events for MC fit
    #for basename in job_names[:]:
        #for section in range(1, total_sections + 1):
            #part = 'evt%dof%d' % (section, total_sections)
            #name = basename + '_' + part
            #job_names.append(name)
            
    return job_names
## End of get_egpaper_list()


#______________________________________________________________________________
def get_egpaper_francesca_list():
    '''
    Returns a list of job names for closure test requested by 
    Francesca on 22 October.
    '''
    job_names = []

    total_sections = 4

    for subdet in 'EB EE'.split():
        for pt in '25to999'.split():
            for version in 'yyv5'.split():
                for source in 'mc'.split():
                    ## inclusive r9 job name
                    name = '_'.join(['egm_fc', source, subdet, 'pt'+pt, version])
                    job_names.append(name)
                    for r9 in 'lowR9 highR9'.split():
                        ## job name
                        name = '_'.join(['egm_fc', source, subdet, 'pt'+pt, 
                                         version, r9])
                        job_names.append(name)                

    job_names2 = []
    for name in job_names:
        # for rfit in [str(0.5 + 0.5*i) for i in range(20)]:
            #job_names2.append(name + '_rfit' + rfit)
        for sfit in [str(-5.0 + 0.5*i) for i in range(21)]:
            job_names2.append(name + '_sfit' + sfit)
    job_names = job_names2
    
    ## Use only subsection of events for the training 
    ## and indepenedent events for MC fit
    #for basename in job_names[:]:
        #for section in range(1, total_sections + 1):
            #part = 'evt%dof%d' % (section, total_sections)
            #name = basename + '_' + part
            #job_names.append(name)
            
    return job_names
## End of get_egpaper_list()


#______________________________________________________________________________
def get_egpaper_ptdpendence_list():
    '''
    Returns a list of job names for plots for the EGM-11-001 paper.
    '''
    job_names = []

    total_sections = 4

    for subdet in 'EB EE'.split():
        for pt in '10to12 12to15 15to25 25to999'.split():
        # for pt in '10to12 12to15 15to20 20to25 25to30 30to999'.split():
            ## The yyv4 corresponds to the July 2012 rereco datasets
            ## That got partially lost with the /raid2 crash.
            # for version in 'yyv3 yyv4 yyv4NoJSON'.split():
            for version in 'yyv3 yyv4 yyv4NoJSON'.split():
                for source in 'data mc'.split():
                    ## inclusive r9 job name
                    name = '_'.join(['egm', source, subdet, 'pt' + pt, version])
                    job_names.append(name)
                    for r9 in 'lowR9 highR9'.split():
                        ## job name
                        name = '_'.join(['egm', source, subdet, 'pt' + pt, 
                                         version, r9])
                        job_names.append(name)                
                
    ## Use only subsection of events for the training 
    ## and indepenedent events for MC fit
    for basename in job_names[:]:
        for section in range(1, total_sections + 1):
            part = 'evt%dof%d' % (section, total_sections)
            name = basename + '_' + part
            job_names.append(name)
            
    return job_names
## End of get_egpaper_ptdpendence_list()


#______________________________________________________________________________
def get_large_list():
    job_names = []

    total_sections = 4

    for subdet in 'EB EE'.split():
        for r9 in 'highR9 lowR9'.split():
            for pt in '10to12 12to15 15to20 20to25 25to30 30to999'.split():
                for version in 'v13 v14 v15'.split():
                    ## real data job name
                    name = '_'.join(['sgetest_data', subdet, r9, 'pt'+pt,
                                     version])
                    job_names.append(name)

                    ## monte carlo job names
                    for section in range(1, total_sections + 1):
                        part = 'evt%dof%d' % (section, total_sections)
                        name = '_'.join(['sgetest_mc', subdet, r9, 
                                        'pt'+pt, version, part])
                        job_names.append(name)
    return job_names
## End of get_large_list()


#______________________________________________________________________________
def get_large_list_regression():
    job_names = []

    total_sections = 4

    for subdet in 'EB EE'.split():
        for r9 in 'highR9 lowR9'.split():
            for pt in '10to12 12to15 15to20 20to25 25to30 30to999'.split():
                for version in 'yyv1 yyv2 yyv3 v13'.split():
                    ## real data job name
                    name = '_'.join(['sge_data', subdet, r9, 'pt'+pt,
                                     version])
                    job_names.append(name)

                    ## monte carlo job names
                    for section in range(1, total_sections + 1):
                        part = 'evt%dof%d' % (section, total_sections)
                        name = '_'.join(['sge_mc', subdet, r9, 
                                        'pt'+pt, version, part])
                        job_names.append(name)
    return job_names
## End of get_large_list_regression()


#______________________________________________________________________________
def get_12cat_regression_list():
    job_names = []

    total_sections = 4

    for subdet in 'EB EE'.split():
        for pt in '10to12 12to15 15to20 20to25 25to30 30to999'.split():
            for version in 'yyv1 yyv2 yyv3 v13'.split():
                ## real data job name
                name = '_'.join(['sge_data', subdet, 'pt'+pt,
                                  version])
                job_names.append(name)

                ## monte carlo job names
                for section in range(1, total_sections + 1):
                    part = 'evt%dof%d' % (section, total_sections)
                    name = '_'.join(['sge_mc', subdet, 
                                     'pt'+pt, version, part])
                    job_names.append(name)
    return job_names
## End of get_12cat_regression_list()


#______________________________________________________________________________
def get_8cat_regression_list():
    job_names = []

    total_sections = 4

    for subdet in 'EB EE'.split():
        for pt in '10to12 12to15 15to25 25to999'.split():
            for version in 'yyv1 yyv2 yyv3 v13'.split():
                ## real data job name
                name = '_'.join(['sge_data', subdet, 'pt'+pt,
                                  version])
                job_names.append(name)

                ## monte carlo job names
                for section in range(1, total_sections + 1):
                    part = 'evt%dof%d' % (section, total_sections)
                    name = '_'.join(['sge_mc', subdet, 
                                     'pt'+pt, version, part])
                    job_names.append(name)
    return job_names
## End of get_8cat_regression_list()


#______________________________________________________________________________
def get_6cat_regression_list():
    job_names = []

    total_sections = 4

    for subdet in 'EB EE'.split():
        for pt in '10to15 15to25 25to999'.split():
            for version in 'yyv1 yyv2 yyv3 v13'.split():
                ## real data job name
                name = '_'.join(['sge_data', subdet, 'pt'+pt,
                                  version])
                job_names.append(name)

                ## monte carlo job names
                for section in range(1, total_sections + 1):
                    part = 'evt%dof%d' % (section, total_sections)
                    name = '_'.join(['sge_mc', subdet, 
                                     'pt'+pt, version, part])
                    job_names.append(name)
    return job_names
## End of get_6cat_regression_list()


#______________________________________________________________________________
def get_baseline_list():
    job_names = []

    total_sections = 4

    for subdet in 'EB EE'.split():
        for pt in '10to12 12to15 15to20 20to999'.split():
            for version in 'yyv1 yyv4'.split():
                ## real data job name
                name = '_'.join(['sge_data', subdet, 'pt'+pt, version])
                job_names.append(name)

                ## monte carlo job names
                for section in range(1, total_sections + 1):
                    part = 'evt%dof%d' % (section, total_sections)
                    name = '_'.join(['sge_mc', subdet, 
                                    'pt'+pt, version, part])
                    job_names.append(name)
    return job_names
## End of get_baseline_list()

#______________________________________________________________________________
def get_htozg_12cats_list():
    job_names = []

    total_sections = 4

    for subdet in 'EB_highR9 EB_lowR9 EE'.split():
        for pt in '10to12 12to15 15to20 20to999'.split():
            for version in 'yyv5 sixie'.split():
                ## real data job name
                name = '_'.join(['htozg_data', subdet, 'pt'+pt, version])
                job_names.append(name)

                ## monte carlo job names
                name = '_'.join(['htozg_mc', subdet, 'pt'+pt, version])
                job_names.append(name)
                #for section in range(1, total_sections + 1):
                    #part = 'evt%dof%d' % (section, total_sections)
                    #name = '_'.join(['sge_mc', subdet, 
                                    #'pt'+pt, version, part])
                    #job_names.append(name)
    return job_names
## End of get_htozg_12cats_list()

# job_names = get_egpaper_list()
# job_names = get_egpaper_ptdpendence_list()
# job_names = get_egpaper_francesca_list()
# job_names = get_baseline_list()
# job_names = get_large_list()
# job_names = get_large_list_regression()
# job_names = get_12cat_regression_list()
# job_names = get_8cat_regression_list()
# job_names = get_6cat_regression_list()
job_names = get_htozg_12cats_list()

submission_dir = os.path.join(os.curdir, project_name)
output_dir = os.path.join(output_base, project_name)

for dir_path in [submission_dir, output_dir]:
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

template_path = os.path.join(os.environ['CMSSW_BASE'], 'src', 
                             template_filename)

print 'Submitting %d jobs:' % len(job_names)
for j in job_names:
    print j

with open(template_path, 'r') as template_file:
    template = template_file.read()
    for job_name in job_names:
        job_path = os.path.join(submission_dir, job_name + '.job')
        with open(job_path, 'w') as job_file:
            job_file.write(template.format(job_name=job_name,
                                           output_dir=output_dir))
            job_file.close()
            submission_cmd = 'qsub ' + job_path
            status, output = commands.getstatusoutput(submission_cmd)
            print output
            if status != 0:
                sys.exit('%s exited with status %d!' % submission_cmd, status)

print 'Submitted %d jobs with success!' % len(job_names)
