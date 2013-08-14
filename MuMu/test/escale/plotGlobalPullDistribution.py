import ROOT
import JPsi.MuMu.common.roofit
ROOT.gSystem.Load('libJPsiMuMu')

filename = 'mc_sreco_strue_Baseline.root'
filename = '/Users/veverka/Work/Talks/11-11-09/Baseline_mod1/mc_sreco_strue_Baseline_mod1.root'

rootfile = ROOT.TFile.Open(filename)
w = rootfile.Get('ws1')
pull = w.var('pull')
pulldata_sreco = ROOT.RooDataSet('pulldata_sreco', 'sreco pulls',
                                 ROOT.RooArgSet(pull))
pulldata_strue = ROOT.RooDataSet('pulldata_strue', 'strue pulls',
                                 ROOT.RooArgSet(pull))

alldata = w.allData()

while len(alldata) > 0:
    data = alldata.front()
    if 'pulldata_sreco' in data.GetName():
        pulldata_sreco.append(data)
    elif 'pulldata_strue' in data.GetName():
        pulldata_strue.append(data)
    alldata.pop_front()
    

pull.setBins(60)
unitg = w.factory('Gaussian::unitg(pull, zero[0], one[1])')

plot_sreco = pull.frame()
plot_sreco.SetTitle('s_{reco} = E^{#gamma}_{reco}/E^{#gamma}_{kin}')
pulldata_sreco.plotOn(plot_sreco)
unitg.plotOn(plot_sreco)
c_sreco = ROOT.TCanvas('pulls_sreco', 'pulls_sreco')
plot_sreco.Draw()
c_sreco.Print('pulls_sreco.png')

plot_strue = pull.frame()
plot_strue.SetTitle('s_{true} = E^{#gamma}_{reco}/E^{#gamma}_{gen}')
pulldata_strue.plotOn(plot_strue)
unitg.plotOn(plot_strue)
c_strue = ROOT.TCanvas('pulls_strue', 'pulls_strue')
plot_strue.Draw()
c_strue.Print('pulls_strue.png')


