import os
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases

from itertools import product
from widthprofile import Source, WidthProfile

basepath = '/home/cmorgoth/scratch/CMSSW_5_2_5/src/UserCode/CPena/src/PhosphorCorrFunctor/SIXIE_LAST_VERSION'

basecuts = [
    'DileptonMass + Mass < 180',
    #'0.4 < MinDeltaR',
    '0.05 < min(abs(Mu1Eta - PhotonEta), abs(Mu2Eta - PhotonEta)) || 0.3 < MinDeltaR',    
    'MinDeltaR < 1.5', 
    'Mu2Pt > 10.5',
    'Mu1Pt > 21', 
    'DileptonMass > 55',
    '25 < PhotonPt && PhotonPt < 99',
    ]
    
cut_title_map = {
    'EB' : ('PhotonIsEB', 'Barrel'),
    'EE' : ('!PhotonIsEB', 'Endcaps'),
    'highR9': ('PhotonR9 > 0.94', 'R9 > 0.94'),
    'lowR9': ('PhotonR9 < 0.94', 'R9 < 0.94'),
    '2012AB': ('RunNumber < 197770', '2012AB'),
    '2012CD': ('RunNumber >= 197770', '2012CD'),
    }

names_to_process = []
etabins = 'EB EE'.split()
r9bins = 'lowR9 highR9'.split()
periodbins = '2012AB 2012CD'.split()
catdimensions = (etabins, r9bins)
names_to_process.extend(['_'.join(p) for p in product(*catdimensions)])
catdimensions = (etabins, r9bins, periodbins)
names_to_process.extend(['_'.join(p) for p in product(*catdimensions)])
print 'Processing:', names_to_process

#==============================================================================
def main():
    '''
    Main entry point for execution
    '''
    global widthprofiles
    widthprofiles = []
    for name in names_to_process:
        catcuts = [cut_title_map[tok][0] for tok in name.split('_')]
        title = ', '.join([cut_title_map[tok][1] for tok in name.split('_')])
        wp = WidthProfile(name, title, get_sources(catcuts), 20, 500)
        wp.run()
        widthprofiles.append(wp)
    canvases.update()
## End of main()


#==============================================================================
def get_sources(catcuts):
    return [
        Source(
            name = 'Regression',
            title = 'Regression',
            filename = os.path.join(
                basepath, 
                'PhotonRegression/ZmumuGammaNtuple_Full2012_MuCorr.root'
                ),
            cuts = basecuts + catcuts,
            ),
        
        Source(
            name = 'Default',
            title = 'Default',
            filename = os.path.join(
                basepath, 
                'NoPhotonRegression/ZmumuGammaNtuple_Full2012_MuCorr.root',
                ),
            cuts = basecuts + catcuts,
            )
        ]
## End of get_sources(..)

#==============================================================================
if __name__ == '__main__':
    main()
    import user
