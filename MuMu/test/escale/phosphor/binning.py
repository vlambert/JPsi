import copy
import glob
import os

import ROOT
import JPsi.MuMu.tools

#import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.cmsstyle as cmsstyle

from JPsi.MuMu.phosphor.binning.histogram import Histogram


source_dir = '/mnt/hadoop/user/veverka/MC/DYToMuMu_M_20_FSRFilter_8_TuneZ2star_8TeV_pythia6_GEN_SIM_v2/veverka-Summer12-PU_S7_START52_V9_step3_RAW2DIGI_L1Reco_RECO_PU_v2-90a3c643a4855c1621ba3bfcbef2e742_VecBosV20-5_2_X/Selected'

base_cuts = [
    'massMuMuGamma + massMuMu < 180',
    'min(Muon1.pt, Muon2.pt) > 10',
    'max(Muon1.pt, Muon2.pt) > 20',
    'massMuMu > 30',
    'abs(massMuMuGamma-90) < 30', # Fit window
    #'Entry$ < 10000', # Reduce the number of events for debugging
    ]
    
max_events = 1000

output_file_name = 'binning.root'

pyrootdir = ROOT.gDirectory

#______________________________________________________________________________
def main():
    '''
    Main entry point of execution.
    '''
    #global chain, source, histos
    
    chain = get_chain()
    selected = chain.CopyTree('&'.join(base_cuts), '', max_events)
    
    destination = ROOT.TFile(output_file_name, 'RECREATE')
    
    process(selected, 'all', 'All', [], destination.mkdir('all'))
    process(selected, 'eb', 'Barrel', ['abs(Photon.SC.eta) < 1.5'], 
            destination.mkdir('eb'))
        
    output_file.Write()
## End of main()


#______________________________________________________________________________
def get_chain():
    chain = ROOT.TChain('MuMuGamma')
    for source_path in glob.glob(os.path.join(source_dir, '*.root'))[-1:]:
        chain.Add(source_path)
    return chain
## End of get_chain()


#______________________________________________________________________________
def process(chain, name, title, cuts, destination):
    
    histos = get_histos('_' + name, ' ' + title)
        
    selection = '&'.join(['(%s)' % c for c in cuts])
    pyrootdir.cd()
    source = chain.CopyTree(selection)
    
    analyze(histos, source, destination)
    
    del source
## End of process(..)


#______________________________________________________________________________
def get_histos(name_suffix = '', title_suffix = ''):
    effective_weight = '0.5 * (1 - massMuMu^2 / massMuMuGamma^2)'

    histos = [
        Histogram(
            name ='h_pho_e',
            title = 'h_pho_e;E^{#gamma} (GeV);Events', 
            nbins = 500,
            xstart = 0,
            xstop = 500,
            quantity = 'Photon.energy',
            ),
            
        #Histogram(
            #name ='h_pho_e_eff',
            #title = 'h_pho_e_eff;E^{#gamma} (GeV);Events', 
            #nbins = 500,
            #xstart = 0,
            #xstop = 500,
            #quantity = 'Photon.energy',
            #weight = effective_weight,
            #),
                
        #Histogram(
            #name ='h_pho_pt',
            #title = 'h_pho_pt;P_{T}^{#gamma} (GeV);Events', 
            #nbins = 500,
            #xstart = 0,
            #xstop = 200,
            #quantity = 'Photon.energy / cosh(Photon.eta)',
            #),
                
        #Histogram(
            #name ='h_pho_pt_eff',
            #title = 'h_pho_pt;P_{T}^{#gamma} (GeV);Effective Events', 
            #nbins = 500,
            #xstart = 0,
            #xstop = 200,
            #quantity = 'Photon.energy / cosh(Photon.eta)',
            #weight = effective_weight,
            #)
        ]
                
    for hist in histos:
        hist.SetName(hist.GetName() + name_suffix)
        hist.SetTitle(hist.GetTitle() + title_suffix)
        
    return histos
## End of get_histos()


#______________________________________________________________________________
def analyze(histos, source, destination):
    destination.cd()
    for hist in histos:
        hist.fill_with(source)
        hist.make_plot()
        hist.plot_quantiles()
        hist.quantiles.Write(hist.GetName() + '_quant')
# End of make_histos(..)


#______________________________________________________________________________
def print_bin_edges(nbins = 10):
    print '%d bins with the same number of %s in %s:' % (
        nbins,
        hist.GetYaxis().GetTitle(),
        hist.GetXaxis().GetTitle(),
        )
    print ', '.join('%.1f' % edge for edge in hist.get_bin_edges(nbins))
## End of print_bin_edges()


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
# output_file.Close()
