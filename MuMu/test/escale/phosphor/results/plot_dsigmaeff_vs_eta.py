import math
import ROOT
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.cmsstyle as cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains

tree = getChains('yyv5')['z']
resolution = {
    'EB' : {'highR9': {'data': 1.74, 'MC': 1.29},
            'lowR9' : {'data': 4.07, 'MC': 3.48},
            'allR9' : {'data': 2.48, 'MC': 2.21},},
    'EE' : {'highR9': {'data': 4.70, 'MC': 1.76},
            'lowR9' : {'data': 5.86, 'MC': 4.03},
            'allR9' : {'data': 4.91, 'MC': 2.95},},
    }

eexpr_template = 'abs({f}*phoERes):abs(gamsceta)'
expr_template = 'abs({f}*phoERes):abs(gamsceta)'
selection_base = 'mmMass + mmgMass < 180 & minDeltaR < 1.5 & mu1Pt> 15 & mu2Pt > 10 & phoPt > 25 & isFSR'

rsmearfun = lambda x : math.sqrt(math.pow(x['data']/x['MC'], 2) - 1)

rsmear = {
    'EB' : { 'highR9': rsmearfun(resolution['EB']['highR9']),
             'lowR9' : rsmearfun(resolution['EB']['lowR9' ]),
             'allR9' : rsmearfun(resolution['EB']['allR9' ]),},
    'EE' : { 'highR9': rsmearfun(resolution['EE']['highR9']),
             'lowR9' : rsmearfun(resolution['EE']['lowR9' ]),
             'allR9' : rsmearfun(resolution['EE']['allR9' ]),},
    }

ROOT.gStyle.SetPadTopMargin(0.1)

histos = []
   
#______________________________________________________________________________
## Low R9 with per-category smearing
expr = expr_template.format(f = 100.*rsmear['EB']['lowR9'])
ebname = 'h_ex2_bl'
tree.Draw(expr + '>>' + ebname + '(25, 0, 2.5)', 
          selection_base + ' & phoR9 < 0.94 & phoIsEB', 'profile goff')

eename = 'h_dseff_el'
expr = expr_template.format(f = 100.*rsmear['EE']['lowR9'])
tree.Draw(expr + '>>' + eename + '(25, 0, 2.5)', 
          selection_base + ' & phoR9 < 0.94 & !phoIsEB', 'profile goff')
          
heb = ROOT.gDirectory.Get(ebname)
heb.Add(ROOT.gDirectory.Get(eename))

heb.SetStats(0)
heb.SetTitle('Z#rightarrow#mu#mu#gamma Photons, E_{T} > 25 GeV, R_{9} < 0.94')
heb.GetXaxis().SetTitle('|#eta_{SC}|')
heb.GetYaxis().SetTitle('#Delta#sigma_{eff} (%)')
heb.SetMinimum(0)

canvases.next('dsigmaeff_vs_eta_lowR9_fromfittolowR9')
heb.Draw()
histos.append(heb)


##______________________________________________________________________________
### High R9 with per-category smearing
#expr = expr_template.format(f = 100.*rsmear['EB']['highR9'])
#ebname = 'h_dseff_bh'
#tree.Draw(expr + '>>' + ebname + '(25, 0, 2.5)', 
          #selection_base + ' & phoR9 > 0.94 & phoIsEB', 'profile goff')

#eename = 'h_dseff_eh'
#expr = expr_template.format(f = 100.*rsmear['EE']['highR9'])
#tree.Draw(expr + '>>' + eename + '(25, 0, 2.5)', 
          #selection_base + ' & phoR9 > 0.94 & !phoIsEB', 'profile goff')
          
#heb = ROOT.gDirectory.Get(ebname)
#heb.Add(ROOT.gDirectory.Get(eename))

#heb.SetStats(0)
#heb.SetTitle('Z#rightarrow#mu#mu#gamma Photons, E_{T} > 25 GeV, R_{9} > 0.94')
#heb.GetXaxis().SetTitle('|#eta_{SC}|')
#heb.GetYaxis().SetTitle('#Delta#sigma_{eff} (%)')
#heb.SetMinimum(0)

#canvases.next('dsigmaeff_vs_eta_highR9_fromfittohighR9')
#heb.Draw()
#histos.append(heb)

##canvases.make_plots('png root'.split())
##canvases.make_pdf_from_eps()

##______________________________________________________________________________
### High R9 with inclusive smearing
#expr = expr_template.format(f = 100.*rsmear['EB']['allR9'])
#ebname = 'h_dseff_bh2'
#tree.Draw(expr + '>>' + ebname + '(25, 0, 2.5)', 
          #selection_base + ' & phoR9 > 0.94 & phoIsEB', 'profile goff')

#eename = 'h_dseff_eh2'
#expr = expr_template.format(f = 100.*rsmear['EE']['allR9'])
#tree.Draw(expr + '>>' + eename + '(25, 0, 2.5)', 
          #selection_base + ' & phoR9 > 0.94 & !phoIsEB', 'profile goff')
          
#heb = ROOT.gDirectory.Get(ebname)
#heb.Add(ROOT.gDirectory.Get(eename))

#heb.SetStats(0)
#heb.SetTitle('Z#rightarrow#mu#mu#gamma Photons, E_{T} > 25 GeV, R_{9} > 0.94')
#heb.GetXaxis().SetTitle('|#eta_{SC}|')
#heb.GetYaxis().SetTitle('#Delta#sigma_{eff} (%)')
#heb.SetMinimum(0)

#canvases.next('dsigmaeff_vs_eta_highR9_fromfittoallR9')
#heb.Draw()
#histos.append(heb)

##canvases.make_plots('png root'.split())
##canvases.make_pdf_from_eps()

##______________________________________________________________________________
### High R9 with inclusive smearing
#expr = expr_template.format(f = 100.*rsmear['EB']['allR9'])
#ebname = 'h_dseff_bl2'
#tree.Draw(expr + '>>' + ebname + '(25, 0, 2.5)', 
          #selection_base + ' & phoR9 < 0.94 & phoIsEB', 'profile goff')

#eename = 'h_dseff_el2'
#expr = expr_template.format(f = 100.*rsmear['EE']['allR9'])
#tree.Draw(expr + '>>' + eename + '(25, 0, 2.5)', 
          #selection_base + ' & phoR9 < 0.94 & !phoIsEB', 'profile goff')
          
#heb = ROOT.gDirectory.Get(ebname)
#heb.Add(ROOT.gDirectory.Get(eename))

#heb.SetStats(0)
#heb.SetTitle('Z#rightarrow#mu#mu#gamma Photons, E_{T} > 25 GeV, R_{9} < 0.94')
#heb.GetXaxis().SetTitle('|#eta_{SC}|')
#heb.GetYaxis().SetTitle('#Delta#sigma_{eff} (%)')
#heb.SetMinimum(0)

#canvases.next('dsigmaeff_vs_eta_lowR9_fromfittoallR9')
#heb.Draw()
#histos.append(heb)

#canvases.make_plots('png root'.split())
#canvases.make_pdf_from_eps()

#______________________________________________________________________________

canvases.update()
