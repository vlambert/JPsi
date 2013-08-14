import os
import socket
import ROOT

_hostname = socket.gethostname()
if _hostname == 't3-susy.ultralight.org':
    ## Path for the t3-susy
    _path = ('/raid2/veverka/r9Trees/'
             'SingleGammaFlatPt10To100_GEN_SIM_DIGI_L1_DIGI2RAW_HLT_RAW2DIGI_'
             'L1Reco_noPU_noOOTPU')
elif _hostname == 'nbcitjv':
    ## Path for Jan's Dell Inspiron 6000 laptop
    _path = ('/home/veverka/Work/data/r9Trees/'
             'SingleGammaFlatPt10To100_GEN_SIM_DIGI_L1_DIGI2RAW_HLT_RAW2DIGI_'
             'L1Reco_noPU_noOOTPU')
elif (_hostname == 'eee.home' or
      _hostname == 'Jan-Veverkas-MacBook-Pro.local' or
      _hostname == 'dlink-a38e11' or
      (_hostname[:8] == 'pb-d-128' and _hostname[-8:] == '.cern.ch')):
    ## Path for Jan's MacBook Pro
    _path = ('/Users/veverka/Work/Data/r9Trees/'
             'SingleGammaFlatPt10To100_GEN_SIM_DIGI_L1_DIGI2RAW_HLT_RAW2DIGI_'
             'L1Reco_noPU_noOOTPU')
else:
    raise RuntimeError, "Unknown hostname `%s'" % _hostname

_files = {}
_files['v1'] = {
    'g93p01' : ['r9Tree_V1_g93p01.root'],
    'g94p02' : ['r9Tree_V1_g94p02.root'],
    'g94cms' : ['r9Tree_V1_g94cms.root'],
}

_treeNames = {
    'v1' : 'r9Tree/tree',
}


def getChains(version='v1'):
    chains = {}
    for name, flist in _files[version].items():
        chains[name] = ROOT.TChain( _treeNames[version] )
        for f in flist:
            print "Loading ", name, ":", f
            chains[name].Add( os.path.join(_path, f) )

    ## Set aliases
    for ch in chains.values():
        ch.SetAlias('e', 'pt*cosh(eta)')
        ch.SetAlias('brem', 'scPhiWidth / scEtaWidth')
        ch.SetAlias('rawE', 'scRawE + preshowerE' )

    return chains

if __name__ == "__main__":
    import user

