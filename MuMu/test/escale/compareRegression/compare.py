import os
import ROOT

basepath = '/home/cmorgoth/scratch/CMSSW_5_2_5/src/UserCode/CPena/src/PhosphorCorrFunctor/SIXIE_LAST_VERSION'

subpath = 'NoPhotonRegression/ZmumuGammaNtuple_Full2012_MuCorr.root'

outpath = 'noregression.root'

basecuts = [
    'DileptonMass + Mass < 180',
    # '0.1 < MinDeltaR',
    'MinDeltaR < 1.5', 
    'Mu2Pt > 10.5',
    'Mu1Pt > 21', 
    'DileptonMass > 55',
    ]
    
catcuts = [
    'PhotonIsEB',
    'PhotonPt > 25',
    'PhotonR9 > 0.94',
    ]


source = ROOT.TFile.Open(os.path.join(basepath, subpath))
tree = source.Get('ZmumuGammaEvent')
output = ROOT.TFile(outpath, 'RECREATE')
expression = 'Mass >> hmmg(120,60,120)'
selection = '&'.join(['(%s)' % c for c in basecuts + catcuts])
tree.Draw(expression, selection, 'goff')
output.Write()
