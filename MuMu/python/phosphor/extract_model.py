import ROOT
import FWLite.Tools.roofit as roo
import JPsi.MuMu.tools

source_path = '/home/veverka/jobs/outputs/eg_paper_exp_jul2012rereco2_v15/egm_expbkg_data_EB_pt25to999_yyv16/phosphor5_model_and_fit_egm_expbkg_data_EB_pt25to999_yyv16.root'
source_name = 'egm_expbkg_data_EB_pt25to999_yyv16'
destination_path = '/home/veverka/phosphor_for_goofit.root'

## Open the source, get the workspace
source = ROOT.TFile.Open(source_path)
source_workspace = source.Get(source_name + '_workspace')

## Get the models and the trasform from the workspace
signal_model = source_workspace.pdf("signal_model0")
#signal_transform = source_workspace.function("signal_model0_msubs_5")
background_model = source_workspace.pdf("zj0_pdf")

## Set the scale to 0
source_workspace.var('phoScale').setVal(0.)

## Store the model pieces in the output file
destination_workspace = ROOT.RooWorkspace('phosphor_workspace')
destination_workspace.Import(ROOT.RooHistPdf(signal_model))
# destination_workspace.Import(signal_transform)
destination_workspace.Import(background_model)
phosphor_model = destination_workspace.factory('''
    SUM::phosphor_model(signal_yield[1e3,0,1e9] * signal_model0,
                        background_yield[2e2,0,1e9] * zj0_pdf)
    ''')
destination_workspace.writeToFile(destination_path)

## Open the destination file
destination = ROOT.TFile.Open(destination_path, "UPDATE")

## Sample the pdf into a histogram
signal_hist = signal_model.createHistogram("mmgMass:phoRes", 500, 100)
background_hist = background_model.createHistogram("mmgMass", 500)
signal_hist.SetName("signal_hist")
background_hist.SetName("background_hist")
destination.Write()

destination.Get('phosphor_workspace').Print()
destination.ls()

