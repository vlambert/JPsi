import os
import socket

from JPsi.MuMu.common.basicRoot import *

_hostname = socket.gethostname()
if _hostname == 't3-susy.ultralight.org':
    ## Path for the t3-susy
    _path = '/raid2/veverka/zeeDataYong'
# elif _hostname == 'nbcitjv':
#     ## Path for Jan's Dell Inspiron 6000 laptop
#     _path = '/home/veverka/Work/data/zeeDataYong'
elif (_hostname == 'eee.home' or
      _hostname == 'Jan-Veverkas-MacBook-Pro.local' or
      (_hostname[:8] == 'pb-d-128' and _hostname[-8:] == '.cern.ch')):
    ## Path for Jan's MacBook Pro
    _path = '/Users/veverka/Work/Data/zeeDataYong'
else:
    raise RuntimeError, "Unknown hostname `%s'" % _hostname

_filename = 'mpair_ebebc_highr9_mcetcut25.corr10.eleid1.datapu5.mcpu5.m70to110.n20to38'
_files = {}
_files['v1'] = {
    'mc' : [_filename],
    'test1' : [_filename + '_testsmear1'],
    'test2' : [_filename + '_testsmear2'],
    'test3' : [_filename + '_testsmear3'],
}

def getChains(version='v1'):
    chains = {}
    for name, flist in _files[version].items():
        chains[name] = TTree('mpair', 'mpair')
        for f in flist:
            print "Loading ", name, ":", f
            chains[name].ReadFile(os.path.join(_path, f), 'mass/F:weight' )

    return chains

if __name__ == "__main__":
    import user

