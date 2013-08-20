import os
import socket
import JPsi.MuMu.common.clusterCorrections as clusterCorrs

from JPsi.MuMu.common.basicRoot import *

_hostname = socket.gethostname()
if (_hostname == 't3-higgs.ultralight.org'
    or ('compute-' in _hostname and '.local' in _hostname)) :
    ## Path for the t3-susy
    ##_path = '/raid2/veverka/esTrees/'#original place changed after raid2 problem
    _path = '/mnt/hadoop/store/user/vlambert/MuMuGamma/'
    ##_path = '/home/cmorgoth/ZmumuGammaData/sixie_2012_hgg_regresion_v3/'
    ##_path = '/home/cmorgoth/scratch/CMSSW_5_2_5/src/UserCode/CPena/src/PhosphorCorrFunctor/MuonCorrectedTrees/'##MuonCorrectedTrees 2011 and 2012
    # _path = '/home/cmorgoth/scratch/CMSSW_5_2_5/src/UserCode/CPena/src/PhosphorCorrFunctor/GaussSmearingTrees'##Test for Gaussian Smearing
    #_path = '/home/cmorgoth/scratch/CMSSW_5_2_5/src/UserCode/CPena/src/PhosphorCorrFunctor/FabSmearing'##Test for Fabrice Smearing
    ##_path = '/home/cmorgoth/ZmumuGammaData/SIXIE_LAST_VERSION/'
    
elif _hostname == 'nbcitjv':
    ## Path for Jan's Dell Inspiron 6000 laptop
    _path = '/home/veverka/Work/data/esTrees'
elif (_hostname == 'eee.home' or
      _hostname == 'Jan-Veverkas-MacBook-Pro.local' or
      (_hostname[:8] == 'pb-d-128' and _hostname[-8:] == '.cern.ch')):
    ## Path for Jan's MacBook Pro
    _path = '/Users/veverka/Work/Data/esTrees'
else:
    raise RuntimeError, "Unknown hostname `%s'" % _hostname

##_list is a pyhton dictionary map    
_files = {}
_files['v1'] = {
    'data' : '''
    esTree_ZMu-May10ReReco-42X-v3_V1.root
    esTree_PromptReco-v4_FNAL_42X-v3_V1.root
    '''.split(),
    'z' : ['esTree_DYToMuMu_pythia6_AOD-42X-v4_V1.root'],
}

_files['v2'] = {
    ## pmvTree format
    'data' : '''
            esTree_ZMu-May10ReReco-42X-v3_V2.root
            esTree_PromptReco-v4_FNAL_42X-v3_V2.root
            '''.split(),
    'z' : ['esTree_DYToMuMu_pythia6_AOD-42X-v4_V2.root'],
    'w'    : ['esTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V2.root'],
    'tt'   : ['esTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V2.root'],
    'qcd'  : ['esTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V2.root'],
}

_files['v3'] = {
    # Results with 715 / pb of June 17 up to run 166861
    'data' : [ 'esTree_V3_ZMu-May10ReReco-42X-v3.root',
               'esTree-V3_PromptReco-v4_FNAL_42X-v3.root', ],
    'z'    : [ 'esTree_V3_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v4'] = {
    'data' : '''
             esTree_V4_Run2010B-ZMu-Apr21ReReco-v1.root
             esTree_V4_PromptReco-v4_FNAL_42X-v3.root
             esTree_V4_ZMu-May10ReReco-42X-v3.root
             '''.split(),
    'z'    : [ 'esTree_V4_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v5'] = {
    'z'    : [ 'esTree_V5_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v6'] = {
    'z'    : [ 'esTree_V6_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v7'] = {
    'data' : '''
             esTree_V7_Run2010B-ZMu-Apr21ReReco-v1.root
             esTree_V7_ZMu-May10ReReco-42X-v3.root
             esTree_V7_PromptReco-v4_FNAL_42X-v3.root
             '''.split(),
    'z'    : [ 'esTree_V7_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v8'] = {
    'data' : '''
             esTree_V8_05Jul2011ReReco-ECAL-v1_condor_Dimuon_RECO-42X-v9_test.root
             esTree_V8_DoubleMu_Dimuon_AOD_Aug5rereco.root
             esTree_V8_DoubleMu_Dimuon_AOD_Prompt_v6.root
             '''.split(),
    'z_test'    : '''
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job5_of40.root
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job16_of40.root
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job20_of40.root
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job31_of40.root
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job39_of40.root
             '''.split(),
    'z'    : '''
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9.root
             '''.split(),
}

_files['v10'] = {
    'data' : '''
             esTree_V10_DoubleMu_Run2011A-May10ReReco-v1_glite_Dimuon_RECO-42X-v9.root
             esTree_V10_DoubleMu_Run2011A-PromptReco-v4_glite_Dimuon_RECO-42X-v9.root
             '''.split(),
    'z'    : [ 'esTree_V10_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9.root' ]
}

_files['v11'] = {
    'data' : '''
             esTree_V11_DoubleMu_Run2011A-May10ReReco-v1_glite_Dimuon_RECO-42X-v9.root
             esTree_V11_DoubleMu_Run2011A-PromptReco-v4_glite_Dimuon_RECO-42X-v9.root
             '''.split(),
    'z'    : [ 'esTree_V11_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9.root' ]
}

## Full 2011 data as used by the Vgamma AN-11-251
_files['v12'] = {
    'data': '''
            esTree_V12_DoubleMu_Run2011A-May10ReReco-v1_glite_Dimuon_RECO-42X-v9.root
            esTree_V12_DoubleMu_Run2011A-PromptReco-v4_glite_Dimuon_RECO-42X-v9.root
            esTree_V12_DoubleMu_Run2011A-05Aug2011-v1_glite_Dimuon_AOD-42X-v9.root
            esTree_V12_DoubleMu_Run2011A-03Oct2011-v1_condor_Dimuon_AOD-42X-v9.root
            esTree_V12_DoubleMu_Run2011B-PromptReco-v1_condor_Dimuon_AOD-42X-v9.root
            '''.split(),
    '2011A': '''
            esTree_V12_DoubleMu_Run2011A-May10ReReco-v1_glite_Dimuon_RECO-42X-v9.root
            esTree_V12_DoubleMu_Run2011A-PromptReco-v4_glite_Dimuon_RECO-42X-v9.root
            esTree_V12_DoubleMu_Run2011A-05Aug2011-v1_glite_Dimuon_AOD-42X-v9.root
            esTree_V12_DoubleMu_Run2011A-03Oct2011-v1_condor_Dimuon_AOD-42X-v9.root
            '''.split(),
    '2011B': '''
            esTree_V12_DoubleMu_Run2011B-PromptReco-v1_condor_Dimuon_AOD-42X-v9.root
            '''.split(),
    }

## Yong's trees with the default CMSSW photon cluster corrections
_files['yyv1'] = {
    'data': [('testSelectionfsr.v3.DoubleMuRun2011AB16Jan2012v1AOD.'
              'muid2.phtid1.phtcorr360.datapu0.mcpu0.r1to129.root')],
    'z'   : [('testSelectionfsr.v3.DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia'
              'Fall11-PU_S6_START42_V14B-v1AODSIM.'
              'muid2.phtid1.phtcorr360.datapu6.mcpu1.r1to50.root')],
    }
    

## Yong's trees with the Caltech photon regression
_files['yyv2'] = {
    'data': [('testSelectionfsr.v3.DoubleMuRun2011AB16Jan2012v1AOD.'
              'muid2.phtid1.phtcorr360.datapu0.mcpu0.r1to129.root')],
    'z'   : [('testSelectionfsr.v3.DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia'
              'Fall11-PU_S6_START42_V14B-v1AODSIM.'
              'muid2.phtid1.phtcorr360.datapu6.mcpu1.r1to50.root')],
    }
    

## Yong's trees with the Hgg photon regression v2
_files['yyv3'] = {
#    'data': [('testSelectionfsr.v3.DoubleMuRun2011AB16Jan2012v1AOD.'
#              'muid2.phtid1.phtcorr96.datapu0.mcpu0.r1to129.root')],#Original from Jan

#    'z'   : [('testSelectionfsr.v3.DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia'
#              'Fall11-PU_S6_START42_V14B-v1AODSIM.'
#              'muid2.phtid1.phtcorr96.datapu6.mcpu1.r1to50.root')],#Original from Jan    
#    'data': [('testSelectionfsr.v3.DoubleMuRun2011AB16Jan2012v1AODv02b.muid2.phtid2.phtcorr96.datapu0.mcpu0.r1to129.scale0.root')],
#    'z': [('testSelectionfsr.v3.DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythiaFall11-PU_S6_START42_V14B-v1AODSIMv02b.muid2.phtid2.phtcorr96.datapu6.mcpu1.r1to38.scale0.root')],
#    'z': [('MC_yyv3_muon_corr_2011.root')],##Muon Corrected Trees
#    'data': [('Data_yyv3_muon_corr_2011.root')],##Muon Corrected Trees
    
    'data': [('MC_yyv3_muon_corr_2011_1.5PercentGaussSmearing.root')],##Muon Corrected Trees + Gaussian Smearing
    'z': [('MC_yyv3_muon_corr_2011.root')],##Muon Corrected Trees
    }

## Yong's trees with the Hgg photon regression v2
## Montecarlo Scale is corrected to zero, resolution is corrected to match data(resolution)
## For now data is uncorrected/. todo correct data!
_files['yyv3corr'] = {
    'data': [('testSelectionfsr.v3.DoubleMuRun2011AB16Jan2012v1AOD.'
              'muid2.phtid1.phtcorr96.datapu0.mcpu0.r1to129.root')],
    'z': [('small.root')],
#    'z'   : [('testSelectionfsr.v3.DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia'
#              'Fall11-PU_S6_START42_V14B-v1AODSIM.'
#              'muid2.phtid1.phtcorr96.datapu6.mcpu1.r1to50.root')],
    }
    
## Yong's trees with e5x5 for the photon energy
_files['yyv3_e5x5'] = {
    'data': [('testSelectionfsr.v3.DoubleMuRun2011AB16Jan2012v1AOD.'
              'muid2.phtid1.phtcorr96.datapu0.mcpu0.r1to129.root')],
    'z'   : [('testSelectionfsr.v3.DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia'
              'Fall11-PU_S6_START42_V14B-v1AODSIM.'
              'muid2.phtid1.phtcorr96.datapu6.mcpu1.r1to50.root')],
    }
    
## Yong's trees with the Hgg photon regression v2 for Jul2012 private rereco
_files['yyv4'] = {
    'data': 
        '''
        Jul2012ReReco/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r1.scale0.root
        Jul2012ReReco/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r2.scale0.root
        Jul2012ReReco/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r3.scale0.root
        Jul2012ReReco/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r4.scale0.root
        Jul2012ReReco/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r5.scale0.root
        Jul2012ReReco/testSelectionfsr.v3.veverkaRun2011AZMuPromptSkimv5ZmmgSkim11Jul2011ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r1.scale0.root
        Jul2012ReReco/testSelectionfsr.v3.veverkaRun2011AZMu03OctZmmg11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r1.scale0.root
        Jul2012ReReco/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r1.scale0.root
        Jul2012ReReco/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r2.scale0.root
        Jul2012ReReco/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r3.scale0.root
        Jul2012ReReco/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r4.scale0.root
        Jul2012ReReco/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r5.scale0.root
        Jul2012ReReco/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r6.scale0.root'''.split(),
    'z'   : [('testSelectionfsr.v3.DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia'
              'Fall11-PU_S6_START42_V14B-v1AODSIM.'
              'muid2.phtid1.phtcorr96.datapu6.mcpu1.r1to50.root')],
    }
    
_files['yyv4NoJSON'] = {
    'data': 
        '''
        Jul2012ReReco_noJSON/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r1.scale0.root
        Jul2012ReReco_noJSON/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r2.scale0.root
        Jul2012ReReco_noJSON/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r3.scale0.root
        Jul2012ReReco_noJSON/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r4.scale0.root
        Jul2012ReReco_noJSON/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r5.scale0.root
        Jul2012ReReco_noJSON/testSelectionfsr.v3.veverkaRun2011AZMuPromptSkimv5ZmmgSkim11Jul2011ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r1.scale0.root
        Jul2012ReReco_noJSON/testSelectionfsr.v3.veverkaRun2011AZMu03OctZmmg11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r1.scale0.root
        Jul2012ReReco_noJSON/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r1.scale0.root
        Jul2012ReReco_noJSON/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r2.scale0.root
        Jul2012ReReco_noJSON/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r3.scale0.root
        Jul2012ReReco_noJSON/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r4.scale0.root
        Jul2012ReReco_noJSON/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r5.scale0.root
        Jul2012ReReco_noJSON/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.r6.scale0.root'''.split(),
    'z'   : [('testSelectionfsr.v3.DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia'
              'Fall11-PU_S6_START42_V14B-v1AODSIM.'
              'muid2.phtid1.phtcorr96.datapu6.mcpu1.r1to50.root')],
    }
    
## Yong's trees with the Hgg photon regression v2, looser selection
## and Rochester corrections applied.
_files['yyv5'] = {
    'data': ['Data_yyv3_muon_corr_2011.root'],
    'z'   : ['MC_yyv3_muon_corr_2011.root']
    }
    
## Yong's trees with the Hgg photon regression v2, looser selection,
## Rochester muon corrections and Fabrice's photon energy smearing.
_files['yyv6'] = {
    'data': [('Data_yyv3_muon_corr_2011.root')],##Muon Corrected Trees 
    'z': [('MC_muon_corr_2011_FabSmearTest.root')],##Muon Corrected Trees + Fab Smearing
    }
    
## Yong's trees for Jul2012ReReco (JSON applied) with Hggv2 regression
## looser selection (dr < 2.0, no sum-pt combinatorics arbitration), and 
## muon charge information for the Rochcor (which is not applied).
## MC is the defualt PU S6 2011 as for yyv3 but with the looser selection,
## same as data.  Also no Rochcor.
_files['yyv7'] = {
    'data': '''
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011AZMu03Oct2011v1ZmmgSkim11Jul2011ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r1.scale0.root
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011AZMu03Oct2011v1ZmmgSkim11Jul2011ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r2.scale0.root
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim10Jul2011ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r1.scale0.root
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim10Jul2011ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r2.scale0.root
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim10Jul2011ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r3.scale0.root
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim10Jul2011ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r4.scale0.root
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011AZMu05Jul2011ReRecoECALv1ZmmgSkim10Jul2011ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r5.scale0.root
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011AZMuPromptSkimv5ZmmgSkim111111111111Jul2011ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r1.scale0.root
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011AZMuPromptSkimv5ZmmgSkim111111111111Jul2011ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r2.scale0.root
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r1.scale0.root
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r2.scale0.root
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r3.scale0.root
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r4.scale0.root
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r5.scale0.root
        Jul2012ReReco_v2/testSelectionfsr.v3.veverkaRun2011BZMuPromptSkimv1ZmmgSkim11Jul2012ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.r6.scale0.root
    '''.split(),
    'z'   : [('testSelectionfsr.v3.dy2mmpowhegpythias6v02b.muid2.'
              'phtid2.phtcorr96.datapu0.mcpu0.scale0.root'),],
    }

## Yong's trees for Jul2012ReReco (JSON applied) with Hggv2 regression
## looser selection (dr < 2.0, no sum-pt combinatorics arbitration), and 
## muon charge information for the Rochcor (which is not applied).
## MC is the defualt PU S6 2011 as for yyv3 but with the looser selection,
## same as data.  Rochcor for data only.
_files['yyv8'] = {
    'data': 'esTree_yyv7_data_Jul2012ReRecoTotal_rochcor.root',
    'z'   : [('testSelectionfsr.v3.dy2mmpowhegpythias6v02b.muid2.'
              'phtid2.phtcorr96.datapu0.mcpu0.scale0.root'),],
}

## Same as yyv7 but the same for both data and MC.  Both have muon charge info.
_files['yyv9'] = {
    'data': '''
        testSelectionfsr.v3.Data2011.Jul2012ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.scale0.root
    '''.split(),
    'z'   : '''
        testSelectionfsr.v3.dy2mmpowhegpythias6v02bAODSIM.muid2.phtid2.phtcorr96.datapu6.mcpu1.scale0.root
    '''.split(),
    }


## Same as yyv9 but tighter selection ("phtid1": dr < 0.8, sum-pt combinatorics)
_files['yyv10'] = {
    'data': '''
        testSelectionfsr.v3.Data2011.Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.scale0.root
    '''.split(),
    'z'   : '''
        testSelectionfsr.v3.dy2mmpowhegpythias6v02bAODSIM.muid2.phtid1.phtcorr96.datapu6.mcpu1.scale0.root
    '''.split(),
    }


## Same as yyv9 but with rochcor for both data and MC.
_files['yyv11'] = {
    'data': '''
        testSelectionfsr.v3.Data2011.Jul2012ReReco.muid2.phtid2.phtcorr96.datapu0.mcpu0.scale0.rochcor.root
    '''.split(),
    'z'   : '''
        testSelectionfsr.v3.dy2mmpowhegpythias6v02bAODSIM.muid2.phtid2.phtcorr96.datapu6.mcpu1.scale0.rochcor.root
    '''.split(),
    }


## Same as yyv10 but with rochcor for both data and MC.
_files['yyv12'] = {
    'data': '''
        testSelectionfsr.v3.Data2011.Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.scale0.rochcor.root
    '''.split(),
    'z'   : '''
        testSelectionfsr.v3.dy2mmpowhegpythias6v02bAODSIM.muid2.phtid1.phtcorr96.datapu6.mcpu1.scale0.rochcor.root
    '''.split(),
    }


## Same as yyv12 but with Lyon trees (phoPt > 25 GeV) for data.
_files['yyv13'] = {
    'data': '''
        Data_2011LyonSync_Louis_28Jan2013.root
    '''.split(),
    'z'   : '''
        testSelectionfsr.v3.dy2mmpowhegpythias6v02bAODSIM.muid2.phtid1.phtcorr96.datapu6.mcpu1.scale0.rochcor.root
    '''.split(),
    }


## Same as yyv13 but with Lyon MC trees (phoPt > 25 GeV) for data.
_files['yyv14'] = {
    'data': '''
        MC_2011LyonSync_Louis_28Jan2013.root
    '''.split(),
    'z'   : '''
        testSelectionfsr.v3.dy2mmpowhegpythias6v02bAODSIM.muid2.phtid1.phtcorr96.datapu6.mcpu1.scale0.rochcor.root
    '''.split(),
    }


## Same as yyv13 but with dummy values for mmMass for data to 
## circumvent the mmMass > 30 GeV cut for the 0.5% of events that have it.
_files['yyv15'] = {
    'data': '''
        Data_2011LyonSync_Louis_28Jan2013_mmMassDummies.root
    '''.split(),
    'z'   : '''
        testSelectionfsr.v3.dy2mmpowhegpythias6v02bAODSIM.muid2.phtid1.phtcorr96.datapu6.mcpu1.scale0.rochcor.root
    '''.split(),
    }


## Same as yyv14 but with dummy values for mmMass for data to 
## circumvent the mmMass > 30 GeV cut for the 0.5% of events that have it.
_files['yyv16'] = {
    'data': '''
        MC_2011LyonSync_Louis_28Jan2013_mmMassDummies.root
    '''.split(),
    'z'   : '''
        testSelectionfsr.v3.dy2mmpowhegpythias6v02bAODSIM.muid2.phtid1.phtcorr96.datapu6.mcpu1.scale0.rochcor.root
    '''.split(),
    }



_files['v13'] = {
    'z' : [('esTree_V13_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_'
            'Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb_'
            'batch1of2.root'),
           ('esTree_V13_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_'
            'Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb_'
            'batch2of2.root')],
    }

_files['v14'] = {
    'z' : [('esTree_V14_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_'
            'Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb_'
            'batch1_of2.root'),
           ('esTree_V14_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_'
            'Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb_'
            'batch2_of2.root')],
    }
    
_files['v15'] = {
    'data' : '''
        esTree_V15_DoubleMu_Run2011A-May10ReReco-v1_glite_Dimuon_RECO-42X-v9.root
        esTree_V15_DoubleMu_Run2011A-PromptReco-v4_glite_Dimuon_RECO-42X-v9.root
        esTree_V15_DoubleMu_Run2011A-05Aug2011-v1_glite_Dimuon_AOD-42X-v9.root
        esTree_V15_DoubleMu_Run2011A-03Oct2011-v1_condor_Dimuon_AOD-42X-v9.root
        esTree_V15_DoubleMu_Run2011B-PromptReco-v1_condor_Dimuon_AOD-42X-v9.root
        '''.split(),
    '2011A' : '''
        esTree_V15_DoubleMu_Run2011A-May10ReReco-v1_glite_Dimuon_RECO-42X-v9.root
        esTree_V15_DoubleMu_Run2011A-PromptReco-v4_glite_Dimuon_RECO-42X-v9.root
        esTree_V15_DoubleMu_Run2011A-05Aug2011-v1_glite_Dimuon_AOD-42X-v9.root
        esTree_V15_DoubleMu_Run2011A-03Oct2011-v1_condor_Dimuon_AOD-42X-v9.root
        '''.split(),
    '2011B' : '''
        esTree_V15_DoubleMu_Run2011B-PromptReco-v1_condor_Dimuon_AOD-42X-v9.root
        '''.split(),  
    'z' : [('esTree_V15_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_'
            'Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb_'
            'batch1_of2.root'),
           ('esTree_V15_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_'
            'Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb_'
            'batch2_of2.root')],       
}


## PU reweighting for 2011A + 2011B, has muon charge
_files['v16'] = {
    'z': [('esTree_V16_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_'
           'Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb_'
           'reduced.root')],
    'data': '''
        esTree_V16_data_2011A.root
        esTree_V16_DoubleMu_Run2011B-PromptReco-v4_glite_Dimuon_RECO-42X-v9_reduced.root
        '''.split(),
    '2011A': '''
        esTree_V16_data_2011A
        '''.split(),
    '2011B': '''
        esTree_V16_DoubleMu_Run2011B-PromptReco-v4_glite_Dimuon_RECO-42X-v9_reduced.root
        '''.split(),
}


## PU reweighting for 2011A, has muon charge
_files['v17'] = {
    'z': [('esTree_V17_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_'
           'Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb_'
           'reduced.root')],
}

## PU reweighting for 2011B, has muon charge
_files['v18'] = {
    'z': [('esTree_V18_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_'
           'Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb_'
           'reduced.root')],
    'data': '''
        esTree_V16_data_2011A.root
        esTree_V16_DoubleMu_Run2011B-PromptReco-v4_glite_Dimuon_RECO-42X-v9_reduced.root
        '''.split(),
    '2011A': '''
        esTree_V16_data_2011A
        '''.split(),
    '2011B': '''
        esTree_V16_DoubleMu_Run2011B-PromptReco-v4_glite_Dimuon_RECO-42X-v9_reduced.root
        '''.split(),
}

## Same as v16 with Rochcor applied
## PU reweighting for 2011A + 2011B
_files['v19'] = {
    'z': ['MC_V16_muon_corr_2011.root'],
    'data': ['Data_V16_muon_corr_2011.root'],
}

##New Sixie trees first try to make it work
_files['sixie'] = {
        #'data': [ ( 'ZmumuGammaNtuple_Run2012AB_Jun29Rereco.root' ) ],#Original Line
        #'z'   : [ ( 'ZmumuGammaNtuple_DYM50_52X.root' ) ],#Original Line
        #THIS LINE IS USED AS CLOSURE TEST(Must Comment other MC->z)        
    'z': [('MC/small_reweight.root')],
    'data': [('Data/ZmumuGammaNtuple_Full2012_MuCorr.root')],
    
    }

_files['sixie2'] = {
    'data': [ ( 'ZmumuGammaNtuple_Run2012AB_Jun29Rereco.root' ) ],
    'z'   : [ ( 'testSelectionfsr.v3.DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythiaFall11-PU_S6_START42_V14B-v1AODSIM.muid2.phtid1.phtcorr96.datapu6.mcpu1.r1to50.root' ) ],
    }

_files['sixie3'] = {
    'data': ['CPena/SIXIE_LAST_VERSION/PhotonRegression/ZmumuGammaNtuple_Full2012_MuCorr.root'],
    'z'   : ['CPena/SIXIE_LAST_VERSION/PhotonRegression/ZmumuGammaNtuple_DYM50_MuCorr.root'],
    }

_treeNames = {
    'v1' : 'tree/es',
    'v2' : 'pmvTree/pmv',
    'v3' : 'tree/es',
    'v4' : 'tree/pmv',
    'v5' : 'tree/pmv',
    'v6' : 'tree/pmv',
    'v7' : 'tree/pmv',
    'v8' : 'tree/pmv',
    'v10' : 'tree/pmv',
    'v11' : 'tree/pmv',
    'v12' : 'tree/pmv',
    'v13' : 'tree/pmv',
    'v14' : 'tree/pmv',
    'v15' : 'tree/pmv',
    'v16' : 'tree/pmv',
    'v17' : 'tree/pmv',
    'v18' : 'tree/pmv',
    'v19' : 'pmv',
    'yyv1' : 'Analysis',
    'yyv2' : 'Analysis',    
    'yyv3' : 'Analysis',
    'yyv3corr' : 'Analysis',
    'yyv3_e5x5' : 'Analysis',    
    'yyv4NoJSON' : 'Analysis',    
    'yyv4' : 'Analysis',
    'yyv5' : 'Analysis',
    'yyv6' : 'Analysis',
    'yyv7' : 'Analysis',
    'yyv8' : 'Analysis',
    'yyv9' : 'Analysis',
    'yyv10' : 'Analysis',
    'yyv11' : 'Analysis',
    'yyv12' : 'Analysis',
    'yyv13' : 'Analysis',
    'yyv14' : 'Analysis',
    'yyv15' : 'Analysis',
    'yyv16' : 'Analysis',
    'sixie' : 'ZmumuGammaEvent',
    'sixie2': 'ZmumuGammaEvent',
    'sixie3': 'ZmumuGammaEvent',
}


def getChains(version='v4'):
    chains = {}
    for name, flist in _files[version].items():
        if version != 'sixie2':
            chains[name] = TChain( _treeNames[version] )
        else : 
            if name == 'data':
                chains[name] = TChain( _treeNames['sixie'] )
            elif name == 'z':
                chains[name] = TChain( _treeNames['yyv3'] )
            
        for f in flist:
            print "Loading ", name, ":", f
            chains[name].Add( os.path.join(_path, f) )

    # print "=====version: ", version

    if version in 'sixie sixie2 sixie3'.split():
        print "version in 'sixie sixie2 sixie3'.split()"
	es_to_sixie_name_map ='''mmMass DileptonMass
        mmgMass Mass
        phoEta PhotonEta
        phoPhi PhotonPhi
        phoGenE GenPhoE
        phoIsEB	PhotonIsEB
        phoR9 PhotonR9
        phoPt PhotonPt
        mu1Pt Mu1Pt
        mu2Pt Mu2Pt
        mu1Eta Mu1Eta
        mu2Eta Mu2Eta
        mu1Phi Mu1Phi
        mu2Phi Mu2Phi
        pileup.weight Weight
        minDeltaR MinDeltaR
        NV NVertices
        isFSR IsFSR'''.split('\n')

    
	
        for name, ch in chains.items():
            print name, ch
            if (version, name) == ('sixie2', 'z'):
                print " (version, name) == ('sixie2', 'z')"
                continue
            print "ch sixie: ", ch 
            for name_pair in es_to_sixie_name_map:
                if len(name_pair.strip()) < 3:
                    raise RuntimeError, 'Illegal name pair %s' % name_paires_name
                es_name, sixie_name = name_pair.split()
                print "====es_name: ", es_name, "sixie_name:  ", sixie_name
                ch.SetAlias(es_name, sixie_name)
    if version in 'yyv1 yyv2 yyv3 yyv3corr yyv3_e5x5 yyv4 yyv4NoJSON yyv5 yyv6 yyv7 yyv8 yyv9 yyv10 yyv11 yyv12 yyv13 yyv14 yyv15 yyv16'.split():
        ## On each line corresponding to a list item, 
        ## 1st is esTree name, 2nd is YY tree name in Yong's trees.
        es_to_yy_name_map = '''mmMass          mm 
                               phoEta          gameta
                               phoPhi          gamphi
                               phoGenE         gametrue
                               phoIsEB         abs(gamsceta)<1.5
                               phoR9           gamr9
                               mu1Pt           mpt[0]
                               mu2Pt           mpt[1]
                               mu1Eta          meta[0]
                               mu2Eta          meta[1]
                               mu1Phi          mphi[0]
                               mu2Phi          mphi[1]
                               pileup.weight   evtweight
                               minDeltaR       mdrg[0]<mdrg[1]?mdrg[0]:mdrg[1]
                               isFSR           gametrue>0'''.split('\n')
    
        if version == 'yyv1':
            ## Use the default CMSSW cluster corrections
            es_to_yy_name_map.extend(
                '''mmgMass         mmg
                  phoPt           gamenergy/cosh(gameta)'''.split('\n')
                  )

        elif version in 'yyv2 yyv3 yyv3corr yyv4 yyv4NoJSON yyv5 yyv6 yyv7 yyv8 yyv9 yyv10 yyv11 yyv12 yyv13 yyv14 yyv15 yyv16 sixie2'.split():

            ## Use the regression cluster corrections
            es_to_yy_name_map.extend(
                '''mmgMass         mmgcorr
                   phoPt           gamscenergycorr/cosh(gameta)'''.split('\n')
                   )
        elif version in ['yyv3_e5x5']:
            ## Use the regression cluster corrections
            m2_m0m1 = 'mpt[0]*mpt[1]*(cosh(meta[0]-meta[1]) - cos(mphi[0]-mphi[1]))'
            m2_m0g  = ('mpt[0] * game5x5 / cosh(gameta) * ('
                           'cosh(meta[0] - gameta) - cos(mphi[0] - gamphi)'
                           ')')
            m2_m1g  = ('mpt[1] * game5x5 / cosh(gameta) * ('
                           'cosh(meta[1] - gameta) - cos(mphi[1] - gamphi)'
                           ')')
            m2_m = '0.106*0.106'
            mmgMassFormula = 'sqrt(2 * ({a} + {b} + {c} + {d}))'.format(
                a=m2_m, b=m2_m0m1, c=m2_m0g, d=m2_m1g
                )
                
            es_to_yy_name_map.extend([
                'mmgMass         %s' % mmgMassFormula.replace(' ', ''),
                'phoPt           game5x5/cosh(gameta)'
                ])
        ## Set aliases for Yong's trees so that one can use the same names
        ## as in esTrees
        for name, ch in chains.items():
            if (version, name) == ('sixie2', 'data'):
                continue
            
	    #print "ch: ", ch 
            for name_pair in es_to_yy_name_map:
                if len(name_pair.strip()) < 3:
                    raise RuntimeError, 'Illegal name pair %s' % name_pair
                es_name, yy_name = name_pair.split()
                #print "====es_name: ", es_name, "yy_name  "
                ch.SetAlias(es_name, yy_name)
    
    ## Set aliases
    for ch in chains.values():
        ch.SetAlias( 'phoE', 'phoPt * cosh(phoEta)' )
        ch.SetAlias( 'brem', 'scPhiWidth / scEtaWidth' )
        ch.SetAlias( 'rawE', 'scRawE + preshowerE' )
        ch.SetAlias( 'corrE', 'phoCrackCorr * corrE(rawE, scEta, brem)' )
        ch.SetAlias( 'newCorrE', 'phoCrackCorr * newCorrE(rawE, scEta, brem)' )
        ch.SetAlias( 'corrKRatio', 'phoE * kRatio / corrE' )
        ch.SetAlias( 'newCorrKRatio', 'phoE * kRatio / newCorrE' )
        ch.SetAlias('m1gMass',
                    'sqrt(2*mu1Pt*phoPt*(cosh(mu1Eta - phoEta) - cos(mu1Phi - phoPhi)))')
        ch.SetAlias('m2gMass',
                    'sqrt(2*mu2Pt*phoPt*(cosh(mu2Eta - phoEta) - cos(mu2Phi - phoPhi)))')
        ch.SetAlias('mmGenMass',
                    'sqrt(2*mu1GenPt*mu2GenPt*(cosh(mu1GenEta - mu2GenEta) - '
                                              'cos(mu1GenPhi - mu2GenPhi)))')
        ch.SetAlias('mmgGenMass',
                    'threeBodyMass(mu1GenPt, mu1GenEta, mu1GenPhi, 0.106, '
                                  'mu2GenPt, mu2GenEta, mu2GenPhi, 0.106, '
                                  'phoGenEt, phoGenEta, phoGenPhi, 0)')
                    ## 'sqrt(2*mu1GenPt*mu2GenPt*(cosh(mu1GenEta - mu2GenEta) - '
                    ##                           'cos( mu1GenPhi - mu2GenPhi)) + '
                    ##      '2*mu1GenPt*phoGenEt*(cosh(mu1GenEta - phoGenEta) - '
                    ##                           'cos( mu1GenPhi - phoGenPhi)) + '
                    ##      '2*mu2GenPt*phoGenEt*(cosh(mu2GenEta - phoGenEta) - '
                    ##                           'cos( mu2GenPhi - phoGenPhi)))')
        ch.SetAlias('mmgMassPhoGenE',
                    'threeBodyMass(mu1Pt, mu1Eta, mu1Phi, 0.106, '
                                  'mu2Pt, mu2Eta, mu2Phi, 0.106, '
                                  'phoGenE * phoPt / phoE, phoEta, phoPhi, 0)')
        ch.SetAlias('mmgMassPhoGenEMuGenPt',
                    'threeBodyMass(mu1GenPt, mu1Eta, mu1Phi, 0.106,'
                                  'mu2GenPt, mu2Eta, mu2Phi, 0.106,'
                                  'phoGenE * phoPt / phoE, phoEta, phoPhi, 0)')
        ch.SetAlias('phoERes', 'phoE/phoGenE - 1') 

    return chains

if __name__ == "__main__":
    import user

