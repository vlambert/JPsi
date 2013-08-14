'''
Reads ASCII files provided by Louis Sgandurra in an email on
2013/01/28 at
https://twiki.cern.ch/twiki/pub/Main/LouisSgandurra/data.txt
https://twiki.cern.ch/twiki/pub/Main/LouisSgandurra/MC.txt
and produces root trees with branches using 
the internal PHOSPHOR names.

The data are colon-separated with the format:
iRunID:iLumiID:iEventID:Mmumugamma:Mmumu:Photon_E:Photon_SC_Eta:Photon_r9


The goal is to compare PHOSPHOR with Lyon/Beijing scale results
on the exact same events.

Jan Veverka, Caltech, 10 Feb 2013
'''

import os
import ROOT

## Path to the directory with the source ASCII file relative
## to CMSSW_BASE
source_directory = 'src/JPsi/MuMu/data/phosphor/LyonSyncFeb2012'
## space-separated, branch description given on the first line
source_filename = 'data_with_dummies2.dat'
destination_filename = 'data2.root'
source_path = os.path.join(os.environ['CMSSW_BASE'], 
                           source_directory, source_filename)
destination_path = os.path.join(os.environ['CMSSW_BASE'], 
                                source_directory, destination_filename)
                                
## Create destination file
destination_file = ROOT.TFile(destination_path, 'RECREATE')
tree = ROOT.TTree('Analysis', 'Lyon/Beijing mmg events')
tree.ReadFile(source_path)
destination_file.Write()
destination_file.Close()
