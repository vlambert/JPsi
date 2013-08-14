import os
import socket
from JPsi.MuMu.common.basicRoot import *

_hostname = socket.gethostname()
if _hostname == 't3-susy.ultralight.org':
    ## Path for the t3-susy
    _path = {
        'v5' : '/raid2/veverka/PMVTrees_v5',
        'v9' : '/raid2/veverka/pmvTrees/',
        'v10': '/raid2/veverka/pmvTrees/',
        'v11': '/raid2/veverka/pmvTrees/',
        'v12': '/raid2/veverka/pmvTrees/',
        'v15': '/raid2/veverka/pmvTrees/',
        'v15reco': '/raid2/veverka/pmvTrees/',
        'v19': '/raid2/veverka/pmvTrees/',
        'v20': '/raid2/veverka/pmvTrees/',
        'v21': '/raid2/veverka/pmvTrees/',
    }
elif _hostname == 'nbcitjv':
    ## Path for Jan's Dell Inspiron 6000 laptop
    _path = {
        'v5': '/home/veverka/Work/data/PMVTrees_v5',
        'v9' : '/home/veverka/Work/data/pmvTrees',
        'v10': '/home/veverka/Work/data/pmvTrees',
        'v11': '/home/veverka/Work/data/pmvTrees',
        'v12': '/home/veverka/Work/data/pmvTrees',
        'v15': '/home/veverka/Work/data/pmvTrees',
        'v15reco': '/home/veverka/Work/data/pmvTrees',
        'v19': '/home/veverka/Work/data/pmvTrees',
        'v20': '/home/veverka/Work/data/pmvTrees',
        'v21': '/home/veverka/Work/data/pmvTrees',
    }
elif _hostname == 'eee.home' or _hostname == 'Jan-Veverkas-MacBook-Pro.local':
    ## Path for Jan's MacBook Pro
    _path = {
        'v9' : '/Users/veverka/Work/Data/pmvTrees',
        'v10': '/Users/veverka/Work/Data/pmvTrees',
        'v11': '/Users/veverka/Work/Data/pmvTrees',
        'v12': '/Users/veverka/Work/Data/pmvTrees',
        'v15': '/Users/veverka/Work/Data/pmvTrees',
        'v15reco': '/Users/veverka/Work/Data/pmvTrees',
        'v19': '/Users/veverka/Work/Data/pmvTrees',
        'v20': '/Users/veverka/Work/Data/pmvTrees',
        'v21': '/Users/veverka/Work/Data/pmvTrees',
    }
else:
    raise RuntimeError, "Unknown hostname `%s'" % _hostname


_files = {}

_files['v5'] = {
    'data': ['pmvTree_ZMu-May10ReReco-42X-v3_V5.root'],
    'z'   : ['pmvTree_Z-RECO-41X-v2_V5.root'],
    'qcd' : ['pmvTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V5.root'],
    'w'   : ['pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V5.root'],
    'tt'  : ['pmvTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V5.root'],
}

_files['v9'] = {
    'data' : [ 'pmvTree_V9_Run2010B-ZMu-Apr21ReReco-v1.root',
              'pmvTree_V9_ZMu-May10ReReco-42X-v3.root',
              'pmvTree_V9_PromptReco-v4_FNAL_42X-v3.root', ],
    'data2011' : [ 'pmvTree_V9_ZMu-May10ReReco-42X-v3.root',
                   'pmvTree_V9_PromptReco-v4_FNAL_42X-v3.root', ],
    'z'    : [ 'pmvTree_V9_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
    'qcd'  : [ 'pmvTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V6.root' ],
    'w'    : [ 'pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V6.root' ],
    'tt'   : [ 'pmvTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V6.root' ],
}

_files['v10'] = {
    'gj' : [ 'pmvTree_V10_G_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_' + \
                'S4-v1_condor_Inclusive_AOD-42X-v9.root' ],
}

_files['v11'] = {
    'z' : [ 'pmvTree_V11_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_' + \
                'S4-v1_condor_Dimuon_AOD-42X-v9.root' ],
}

_files['v12'] = {
    'z' : ['pmvTree_V12_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_' +\
           'S4-v1_condor_Dimuon_AOD-42X-v9.root' ],
    'z1' : ['pmvTree_V12_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_' +\
           'S4-v1_condor_Dimuon_AOD-42X-v9_1.root' ],
    'gj': [ 'pmvTree_V12_G_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_' +\
                'S4-v1_condor_Inclusive_AOD-42X-v9.root' ],
}

_files['v15'] = {
    '2011A': ['pmvTree_V15_05Jul2011ReReco_05Aug2011_03Oct2011-v1.root',],
    '2011B': ['pmvTree_V15_DoubleMu_Run2011B-PromptReco-v1_condor_Dimuon_AOD-42X-v9.root',],
    'data' : ['pmvTree_V15_05Jul2011ReReco_05Aug2011_03Oct2011-v1_PromptReco-v1B.root',],
    'z'    : ['pmvTree_V15_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9.root',],
    'qcd'  : ['pmvTree_V15_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_S4-v1_condor_Dimuon_AOD-42X-v9.root',],
    'tt'   : ['pmvTree_V15_TTJets_TuneZ2_7TeV-madgraph-tauola_S4-v2_condor_Dimuon_AOD-42X-v9.root',],
    'w'    : ['pmvTree_V15_WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_Summer11-PU_S4_START42_V11-v1_condor_Dimuon_AOD-42X-v9.root',],
}

_files['v15reco'] = {
    'data' : ['pmvTree_V15_05Jul2011ReReco_05Aug2011_03Oct2011-v1_PromptReco-v1B_RECO.root',],
    'z'    : ['pmvTree_V15_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_Summer11-PU_S4_START42_V11-v1_glidein_Dimuon_RECO-42X-v9.root',],
#    'qcd'  : ['pmvTree_V15_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_S4-v1_condor_Dimuon_AOD-42X-v9.root',],
#     'tt'   : ['pmvTree_V15_TTJets_TuneZ2_7TeV-madgraph-tauola_S4-v2_condor_Dimuon_AOD-42X-v9.root',],
#    'w'    : ['pmvTree_V15_WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_Summer11-PU_S4_START42_V11-v1_condor_Dimuon_AOD-42X-v9.root',],
}

_files['v19'] = {
    'z' : ['pmvTree_V19_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root'],
    'data' :  ['pmvTree_V19_DoubleMu_Run2011A-30Nov2011-v1_condor_Dimuon_AOD-42X-v10_DBS.root',
               'pmvTree_V19_DoubleMu_Run2011B-30Nov2011-v1_condor_Dimuon_AOD-42X-v10_DBS.root'],
    '2011A': ['pmvTree_V19_DoubleMu_Run2011A-30Nov2011-v1_condor_Dimuon_AOD-42X-v10_DBS.root'],
    '2011B': ['pmvTree_V19_DoubleMu_Run2011B-30Nov2011-v1_condor_Dimuon_AOD-42X-v10_DBS.root'],
    'qcd': ['pmvTree_V19_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root'],
    'tt': ['pmvTree_V19_TT_TuneZ2_7TeV-powheg-tauola_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root'],
    'w': ['pmvTree_V19_WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root'],
    }

_treeNames = {
    'v5' : 'pmvTree/pmv',
    'v9' : 'pmvTree/pmv',
    'v10': 'pmvTree/pmv',
    'v11': 'pmvTree/pmv',
    'v12': 'pmvTree/pmv',
    'v15': 'pmvTree/pmv',
    'v15reco': 'pmvTree/pmv',
    'v19': 'pmvTree/pmv',
    'v20': 'pmvTree/pmv',
    'v21': 'pmvTree/pmv',
}

#------------------------------------------------------------------------------
def getChains(version='v9'):
    'Given a version string returns a dictionary of name:TChain.'
    chains = {}
    for name, flist in _files[version].items():
        chains[name] = TChain( _treeNames[version] )
        for f in flist:
            print "Loading ", name, ":", f
            chains[name].Add( os.path.join(_path[version], f) )
    return chains
# getChains <--

## Enable tab completion and history during interactive inspection
if __name__ == "__main__": import user
