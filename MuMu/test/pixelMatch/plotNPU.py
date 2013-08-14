import os
from ROOT import *
from array import array

path = "/home/veverka/Work/data/pmv"

fileName = {
    #"data": "pmvTree_Mu_Run2010AB-Dec22ReReco_v1_json_V3.root",
    #"z"   : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v1_V3.root",
    #"z"  : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v2_V3.root",
    'z'   : 'pmvTree_DYToMuMu_pythia6_AOD-42X-v4_V7.root',
    #"tt"  : "pmvTree_TTJets_TuneZ2-madgraph-Winter10_V2.root",
    #"w"   : "",
    #"qcd" : "",
#     "gj"  : "pmvTree_GJets_TuneD6T_HT-40To100-madgraph_Winter10_V3.root",
    #"gj"  : "pmvTree_GJets_TuneD6T_HT-40To100-madgraph_Winter10_V3_numEvents40k.root",
    "gj"  : 'pmvTree_G_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_Summer11_AOD_42X-v4_V6.root',
    #'gj'  : 'pmvTree_G_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_Summer11_AOD_42X-v4_V6_numEvent80k.root',
}

## Set TDR style
macroPath = "tdrstyle.C"
if os.path.exists(macroPath):
    gROOT.LoadMacro(macroPath)
    ROOT.setTDRStyle()
    gROOT.ForceStyle()

gStyle.SetPadRightMargin(0.05)
gStyle.SetPadTopMargin(0.05)
wWidth = 600
wHeight = 600
canvasDX = 20
canvasDY = 20

latexLabel = TLatex()
latexLabel.SetNDC()

## open files
file = {}
for tag, name in fileName.items():
    file[tag] = TFile(os.path.join(path, name))

## get trees
tree1 = {}
for tag, f in file.items():
    tree1[tag] = f.Get("pmvTree/pmv")

import JPsi.MuMu.common.energyScaleChains as esChains
tree = esChains.getChains('v4')
esChainsV2 = esChains.getChains('v2')
tree['w'] = esChainsV2['w']
tree['tt'] = esChainsV2['tt']
tree['qcd'] = esChainsV2['qcd']

pmv = tree1['gj']

## Restrict to first 10k events for testing
#for tag, t in tree.items():
    #t.Draw(">>elist_" + tag , '', 'entrylist', 10000)
    #t.SetEntryList( gDirectory.Get('elist_' + tag) )

file2 = TFile('/home/veverka/Work/data/pmv/pudist_160404-165542_7TeV_PromptReco_Collisions11_JSON.root')
pu_data = file2.Get('pileup').Clone()
pu_data.Scale( 1./pu_data.Integral() )
pu_data.GetXaxis().SetRangeUser(-0.5, 19.5)
pu_data.GetXaxis().SetTitle('# of interactions')
pu_data.GetYaxis().SetTitle('a. u.')


legends, hnpu = {}, {}
canvases = []

titles = {
    'h_bx-1_gj_weight': '#gamma+nj, BX=-1, IT weight',
    'h_bx0_gj_weight': '#gamma+nj, BX=0, IT weight',
    'h_bx1_gj_weight': '#gamma+nj, BX=1, IT weight',
    'h_bx-1_gj_weightOOT': '#gamma+nj, BX=-1, OOT weight',
    'h_bx0_gj_weightOOT': '#gamma+nj, BX=0, OOT weight',
    'h_bx1_gj_weightOOT': '#gamma+nj, BX=1, OOT weight',
    'h_bx-1_z_weight': 'Z#rightarrow#mu#mu, BX=-1, IT weight',
    'h_bx0_z_weight': 'Z#rightarrow#mu#mu, BX=0, IT weight',
    'h_bx1_z_weight': 'Z#rightarrow#mu#mu, BX=1, IT weight',
    'h_bx-1_z_weightOOT': 'Z#rightarrow#mu#mu, BX=-1, OOT weight',
    'h_bx0_z_weightOOT': 'Z#rightarrow#mu#mu, BX=0, OOT weight',
    'h_bx1_z_weightOOT': 'Z#rightarrow#mu#mu, BX=1, OOT weight',
}

for tag, pmv in tree.items():
    for bx in [-1, 0, 1]:
        for w in ['weight', 'weightOOT']:
            hname = 'h_bx%d_%s_%s' % (bx, tag, w)
            canvases.append( TCanvas(hname, hname) )
            pmv.Draw('pileup.numInteractions>>' + hname + '(20,-0.5,19.5)', '(pileup.bunchCrossing==%d)*pileup.%s' % (bx, w) )
            h1 = hnpu[hname] = gDirectory.Get(hname)
            h1.Sumw2()
            h1.Scale( 1. / h1.Integral() )
            pu_data.Draw('hist')
            h1.Draw('e0same')
            legend = TLegend(0.5, 0.75, 0.9, 0.9)
            legends[hname] = legend
            legend.SetFillColor(0)
            legend.SetShadowColor(0)
            legend.SetBorderSize(0)
            legend.AddEntry(pu_data, "Data", "l")
            legend.AddEntry(h1, titles[hname], "pl")
            legend.Draw()
            canvases[-1].Print(hname + '.eps')


if __name__ == '__main__': import user
