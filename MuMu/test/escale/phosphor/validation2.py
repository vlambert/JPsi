import os
import ROOT
import FWLite.Tools.cmsstyle
import FWLite.Tools.canvases as canvases
import FWLite.Tools.roofit as roo

# path = '/raid2/veverka/phosphor/phosphor5_test9_res'
path = '/home/veverka/cmssw/CMSSW_4_2_3/src/JPsi/MuMu/test/escale/phosphor'
basenames = '''
    EB_pt10to12
    EE_pt10to12
    EB_pt20to999
    EE_pt20to999
    '''.split()

phos_true_list = [4.45467e-01,]# 2.86975e-01, 6.40960e-01, 4.68551e-01]
phor_true_list = [5.31726e+00,]# 4.14648e+00, 8.91343e+00, 7.13829e+00]

ROOT.gSystem.Load('libJPsiMuMu')
ROOT.gStyle.SetPadTopMargin(0.1)

phoScaleFits = []
phoResFits = []
phos_resid_hist = ROOT.TH1F('phos_resid_hist', 
                            ';'.join(['E^{#gamma} Scale Residuals',
                                      '(MC Fit) - (MC Truth) (%)',
                                      'Entries / 1%']),
                            11, -5.5, 5.5)

phor_ratio_hist = ROOT.TH1F('phor_ratio_hist', 
                            ';'.join(['E^{#gamma} Resolution Ratios',
                                      '(MC Fit) / (MC Truth)',
                                      'Entries / 0.1']),
                            11, 0.45, 1.55)

phor_resid_hist = ROOT.TH1F('phor_resid_hist', 
                            ';'.join(['E^{#gamma} Resolution Residuals',
                                      '(MC Fit) - (MC Truth) (%)',
                                      'Entries / 1%']),
                            11, -5.5, 5.5)

phor_resid_hist_eb = ROOT.TH1F('phor_resid_hist_eb', 
                               ';'.join(['Barrel E^{#gamma} Resolution Residuals',
                                         '(MC Fit) - (MC Truth) (%)',
                                         'Entries / 1%']),
                               11, -5.5, 5.5)

phor_resid_hist_ee = ROOT.TH1F('phor_resid_hist_ee', 
                               ';'.join(['Endcaps E^{#gamma} Resolution Residuals',
                                         '(MC Fit) - (MC Truth) (%)',
                                         'Entries / 1%']),
                               11, -5.5, 5.5)

for basename in basenames:
   for test in 'test0 test1 test2 test3'.split():
    #for test in 'test0'.split():
        name = '_'.join([test, basename])
        filename = 'phosphor5_model_and_fit_%s.root' % name
        rootfile = ROOT.TFile.Open(os.path.join(path, filename))
        w = rootfile.Get(name + '_workspace')
        phoScale = w.var('phoScale')
        phoRes = w.var('phoRes')
        phoScaleTrue = w.var('phoScaleTrue')
        phoResTrue = w.var('phoResTrue')
        fitres = w.obj(name + '_fitres4_minos')
        fitted_params = fitres.floatParsFinal()
        for i in range(fitted_params.getSize()):
            x = fitted_params[i]
            if x.GetName() == 'phoScale':
                phoScaleFit = x
            elif x.GetName() == 'phoRes':
                phoResFit = x
            elif x.GetName() == 'signal_f':
                purityFit = x
            else:
                raise RuntimeError, 'Unexpected parameter name!'
        phoScaleFits.append(phoScaleFit.getVal())
        phoResFits.append(phoResFit.getVal())
        phos_resid_hist.Fill(phoScaleFit.getVal() - phoScaleTrue.getVal())
        phor_ratio_hist.Fill(phoResFit.getVal() / phoResTrue.getVal())
        phor_resid_hist.Fill(phoResFit.getVal() - phoResTrue.getVal())
        if 'EB' in basename:
            phor_resid_hist_eb.Fill(phoResFit.getVal() - phoResTrue.getVal())
        else:
            phor_resid_hist_ee.Fill(phoResFit.getVal() - phoResTrue.getVal())
    

#phos_resid_hist.SetTitle('E^{#gamma} scale')
#phos_resid_hist.GetXaxis('(MC Fit) - (MC Truth) (%)')
#phos_resid_hist.GetYaxis('Entries / 1%')
for hist in [phos_resid_hist, phor_resid_hist, phor_resid_hist_eb, 
             phor_resid_hist_ee, phor_ratio_hist]:
    canvases.next(hist.GetName())
    hist.Fit('gaus')
    hist.Draw()
    
#phos_resid_hist.Fit('gaus')
#canvases.next('phos_resid_hist')
#phos_resid_hist.Draw()

#phor_resid_hist.Fit('gaus')
#canvases.next('phor_resid_hist')
#phor_resid_hist.Draw()

canvases.update()
canvases.make_plots('eps png pdf'.split())