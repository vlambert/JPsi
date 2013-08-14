import ROOT
import JPsi.MuMu.pmvplotter as plotter

output_filename = 'Zmmg_Zee_sihih.root'


#______________________________________________________________________________
def main():
    '''
    Main entry point to execution.
    '''
    print '>>> Welcome to save_histogram_sihih! <<<\n'
    hist_map = get_histograms()
    
    ## Open the output file
    output_file = ROOT.TFile(output_filename, 'recreate')
    
    save_histograms(hist_map, output_file)
    
    output_file.ls()
    output_file.Close()
    
    print '\n>>> Exiting save_histogram_sihih with success. <<<'
## End of main()



#______________________________________________________________________________
def get_histograms():
    '''
    Returns a map of the histograms of sigmaIetaIeta for photons and electrons 
    in data and MC.
    '''
    ## Make the Zmmg histograms
    plotter.make_plot('sihih_highR9_EB')
    plotter.make_plot('sihih_highR9_EE')
    hist_map = {
        'pho_eb_data': 
            plotter.histograms['sihih_highR9_EB'][0].Clone('hist_sihih_pho_eb_data'),
        'pho_eb_mc':
            plotter.histograms['sihih_highR9_EB'][1][0].Clone('hist_sihih_pho_eb_mc'),
        'pho_ee_data': 
            plotter.histograms['sihih_highR9_EE'][0].Clone('hist_sihih_pho_ee_data'),
        'pho_ee_mc':
            plotter.histograms['sihih_highR9_EE'][1][0].Clone('hist_sihih_pho_ee_mc'),
    }
    
    ## Make the Zee histograms
    path = '/raid2/veverka/various/Zee_Sihih_1_Poter.root'
    ifile = ROOT.TFile.Open(path)
    zee_histname_map = dict(
        zip('eb_data  eb_mc  ee_data  ee_mc'.split(),
            '''Data_Sihih_Barrel 
               MC_Sihih_Barrel 
               Data_Sihih_Endcap 
               MC_Sihih_Endcap'''.split())
        )
    
    ehist_map = {}
    for key, ghist in hist_map.items():
        histname = zee_histname_map[key.replace('pho_', '')]
        ehist_orig = ifile.Get(histname)
        if not ehist_orig:
            raise RuntimeError(
                "Did not find %s in %s" % (histname, path)
                )
        if not 1000 * ehist_orig.GetBinWidth(1) == ghist.GetBinWidth(1):
            raise RuntimeError(
                "%s and %s have different bin widths: %f and %f!" % (
                    ehist_orig.GetName(), ghist.GetName(),
                    ehist_orig.GetBinWidth(1), ghist.GetBinWidth(1)
                    )
                )
        ## Transfrom the x-axis
        ehist = ghist.Clone(ghist.GetName().replace('pho', 'ele'))
        ehist.SetEntries(ehist_orig.GetEntries())
        for xbin in range(1, ehist.GetXaxis().GetNbins()):
            xval = ehist.GetBinCenter(xbin)
            xbin_orig = ehist_orig.GetXaxis().FindBin(xval / 1e3)
            content = ehist_orig.GetBinContent(xbin_orig)
            error = ehist_orig.GetBinError(xbin_orig)
            ehist.SetBinContent(xbin, content)
            ehist.SetBinError(xbin, error)
        ehist_map[key.replace('pho', 'ele')] = ehist

    hist_map.update(ehist_map)
    
    return hist_map
## End of get_histograms()


#______________________________________________________________________________
def save_histograms(hist_map, output_file):
    for hist in hist_map.values():
        hist.SetDirectory(output_file)
    output_file.Write()
## End of save_histograms(..)


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
