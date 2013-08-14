import os
import ROOT

import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.legend import Legend

## Permanent location
filename = "/raid2/veverka/various/Zmmg_Zee_sihih.root"

#______________________________________________________________________________
def decorate_canvas(canvas):
    '''
    Writes various Latex labels on the current canvas.
    '''
    canvas.SetTopMargin(0.1)
    canvas.cd()
    
    ## CMS Preliminary:
    Latex(['CMS Preliminary 2011,  #sqrt{s} = 7 TeV'], 
          position=(0.17, 0.93), textsize=22).draw()
    
    labels = []
    
    if 'data' in name:
        labels.append('L = 4.9 fb^{-1}')
    else:
        labels.append('Simulation')
    
    
    labels.append('E_{T}^{e/#gamma} > 25 GeV')
    
    ## EB or EE
    if 'eb' in name:
        labels.append('R_{9}^{e} > 0.94')
        labels.append('ECAL Barrel')
    else:
        labels.append('R_{9}^{e} > 0.95')
        labels.append('ECAL Endcaps')

    Latex(labels, position=(0.22, 0.8), textsize=22, 
          rowheight=0.07
          ).draw()
## End of decorate_canvas()
     

#______________________________________________________________________________
def decorate_histos(hpho, hele):
    '''
    Sets the line and fill colors.
    '''
    hpho.SetLineColor(ROOT.kBlack)
    hele.SetLineColor(ROOT.kAzure - 9)
    hpho.SetFillColor(ROOT.kWhite)
    hele.SetFillColor(ROOT.kAzure - 9)
## End of decorate_histos(..)


#______________________________________________________________________________
def get_legend(hpho, hele):
    '''
    Returns legend for the histograms.
    '''
    legend = Legend([hpho, hele],
                    ['Z #rightarrow #mu#mu#gamma',
                     'Z #rightarrow ee'],
                    position = (0.65, 0.7, 0.92, 0.85),
                    optlist = ['pl', 'f']
                    )
    return legend
## End of get_legend()


rootfile = ROOT.TFile.Open(filename)

histmap = {}
for source in 'data mc'.split():
    for subdet in 'eb ee'.split():
        name = '_'.join(['sihih', subdet, source])
        hist = histmap[subdet] = {}
        for eg in 'pho ele'.split():
            hist_name = 'hist_sihih_%s_%s_%s' % (eg, subdet, source)
            hist[eg] = rootfile.Get(hist_name)
            xa = hist[eg].GetXaxis()
            xa.SetTitle(xa.GetTitle().replace('Photon ', ''))

        hist['ele'].Scale(hist['pho'].Integral() / hist['ele'].Integral())
        
        decorate_histos(hist['pho'], hist['ele'])
        
        c1 = canvases.next(name)
        hist['ele'].Draw('hist')
        hist['pho'].Draw('e0 same')
        
        decorate_canvas(c1)
        legend = get_legend(hist['pho'], hist['ele'])
        legend.Draw()

canvases.update()

if __name__ == '__main__': 
    import user
