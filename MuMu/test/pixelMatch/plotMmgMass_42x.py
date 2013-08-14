import os
from ROOT import *
from array import array

# path = "/raid2/veverka/PMVTrees_v6"
path = "/raid2/veverka/esTrees"
realData = "data"
mcSamples = "z qcd w tt".split()

fileName = {
    #"data": "pmvTree_Mu_Run2010AB-Dec22ReReco_v1_json_V3.root",
#     "data": "pmvTree_ZMu-May10ReReco-42X-v3_V5.root",
#     "data": "pmvTree_ZMu_May10ReReco-42X-v3_Plus_PromptSkim-v4_42X-v5_V6.root",

    #"z"   : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v1_V3.root",
    #"z"  : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v2_V3.root",
    #"tt"  : "pmvTree_TTJets_TuneZ2-madgraph-Winter10_V3.root",
    #"w"   : "pmvTree_WJetsToLNu_TuneZ2_7TeV-madgraph_Winter10_V3.root",
    #"qcd" : "pmvTree_QCD_Pt-20_MuEnrichedPt-15_Winter10_V3.root",

#     'w': 'pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V5.root',
#     'w'  : 'pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V6.root',
#     'qcd': 'pmvTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V6.root',
#     'tt' : 'pmvTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V6.root',
#     'z': 'pmvTree_Z-RECO-41X-v2_V5.root',
#     'z'  : 'pmvTree_DYToMuMu_pythia6_AOD-42X-v4_V6.root',

    'data' : 'esTree_ZMu-May10ReReco_PromptReco-v4_FNAL_42X-v3_V2.root',
    'z' : 'esTree_DYToMuMu_pythia6_AOD-42X-v4_V2.root',
    'w' : 'esTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V2.root',
    'tt' : 'esTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V2.root',
    'qcd' : 'esTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V2.root',

}


cweight = {
    "data": 1.,
    #"z"  : 0.030541912803076,
    #"qcd": 0.10306919044126,
    #"w"  : 0.074139194512438,
    #"tt" : 0.005083191122289,

#     'z'  : 0.17175592557735 * 1795714. / 2008540., ## read events Spring11 / Summer11
#     'tt' : 0.019860956416475,
#     'w'  : 0.54974976060237,
#     'qcd': 0.27884236321449,

    'z'  : 0.2578237765992,
    'tt' : 0.20516095989489,
    'w'  : 1.77177343641992,
    'qcd': 15.5412157722089,
}

puWeight = {
    'data': '1.',

    'z'  : 'pileup.weight',
    'tt' : 'pileup.weight',
    'w'  : 'pileup.weight',
    'qcd': 'pileup.weight',

}



mcSamples = 'z zj qcd tt w'.split()

colors = {
    "z"     : kAzure - 9,
    'zj'    : kSpring + 5,
    "qcd"   : kYellow - 7,
    "tt"    : kOrange - 2,
    "w"     : kRed -3,
}

legendTitles = {
    "z"   : "FSR",
    'zj'  : 'Z+jets',
    "qcd" : "QCD",
    "tt"  : "t#bar{t}",
    "w"   : "W",
}

canvases = []
graphs = []

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
# file = {}
# for tag, name in fileName.items():
#     file[tag] = TFile(os.path.join(path, name))

## get trees
tree = {}
# for tag, f in file.items():
#     tree[tag] = f.Get("pmvTree/pmv")
# import JPsi.MuMu.common.energyScaleChains as esChains
import JPsi.MuMu.common.pmvTrees as pmvTrees
chains = pmvTrees.getChains('v15')
tree = {}
for tag in 'data z qcd w tt'.split():
  tree[tag] = chains[tag]

## make histos of pmv vs mmgMass

#ebSelection = "phoIsEB & abs(mmgMass-90)<15 & (minDEta > 0.04 | minDPhi > 0.3)"
#eeSelection = "!phoIsEB & abs(mmgMass-90)<15 & (minDEta > 0.08 | minDPhi > 0.3)"
selection = "scEt > 10 && phoHoE < 0.5 && mmMass < 80"
#selection = 'phoIsEB'
#selection = '!phoIsEB'

###############################################################################
# Plot a quantity in data for EB
yRange = (1e-4, 7000.)

c1 = TCanvas()
canvases.append(c1)

# var = RooRealVar("mmgMass", "m_{#mu#mu#gamma}", 60, 120, "GeV")
var = RooRealVar("mmgMass", "m_{#mu#mu#gamma}", 70, 110, "GeV")
var.setBins(40)

h_temp = TH1F("h_temp", "", var.getBins(), var.getMin(), var.getMax() )
h_temp.GetXaxis().SetTitle( var.GetTitle() )
h_temp.GetYaxis().SetTitle("Events / 1 GeV")
h_temp.SetTitle("")
h_temp.SetStats(0)
histos = {}
for tag, t in tree.items():
    sel = '(%s)' % (selection,)
#    if tag == 'z':
#        sel += ' && isFSR'
    if tag == 'data':
        continue
    sel = '%s * %f * (%s) ' % (puWeight[tag], cweight[tag], sel,)
    print tag, ':', sel
    t.Draw(var.GetName() + '>>h_temp', sel )
    histos[tag] = h_temp.Clone( 'h_' + tag )

sel = "%s * %f * ( (%s) && !isFSR )" % (puWeight['z'], cweight['z'], selection)
tree['z'].Draw(var.GetName() + '>>h_temp', sel)
histos['zj'] = h_temp.Clone( 'h_zj' )

tree['data'].Draw(var.GetName() + '>>h_temp', selection )
hdata = h_temp.Clone( 'hdata' )

for tag in mcSamples:
    histos[tag].SetFillColor( colors[tag] )
    histos[tag].SetLineColor( colors[tag] )

## Sort histos
sortedHistos = histos.values()
sortedHistos.sort( key=lambda h: h.Integral() )

## Make stacked histos (THStack can't redraw axis!? -> roottalk)
hstacks = []
for h in sortedHistos:
    hstemp = h.Clone( h.GetName().replace("h_", "hs_") )
    if hstacks:
        hstemp.Add( hstacks[-1] )
    hstacks.append( hstemp )

## Draw
hstacks.reverse()

## Normalize MC to data
mcIntegral = hstacks[0].Integral( 1, var.getBins() )
dataIntegral = hdata.Integral( 1, var.getBins() )

for hist in hstacks:
    hist.Scale( dataIntegral / mcIntegral )


for h in hstacks:
    h.GetYaxis().SetRangeUser(*yRange)
    if hstacks.index(h) == 0: h.Draw()
    else:                     h.Draw("same")




hdata.Draw("e1 same")
c1.RedrawAxis()

latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2011")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
#latexLabel.DrawLatex(0.7, 0.2, "Barrel")
#latexLabel.DrawLatex(0.7, 0.2, "Endcaps")
latexLabel.DrawLatex(0.2, 0.875, "42X data and MC")
latexLabel.DrawLatex(0.2, 0.8, "Total events: %d" % (int( hdata.GetEntries() ),) )
# latexLabel.DrawLatex(0.2, 0.725, "L = 332 pb^{-1}")
latexLabel.DrawLatex(0.2, 0.725, "L = 4.603 fb^{-1}")
latexLabel.DrawLatex(0.2, 0.65, "E_{T}^{#gamma} > 10 GeV")

c1.Update()

## Print yields:
print "--++ Yields and Purities"
print "%10s %10.f" % ( 'data', hdata.Integral() )
nbins = var.getBins()
for i in range( len(hstacks) ):
    if i < len(hstacks) - 1:
        res = hstacks[i].Integral(1, nbins) - hstacks[i+1].Integral(1, nbins)
    else:
        res = hstacks[i].Integral(1, nbins)
    print "%10s %10.2f %10.3g%%" % ( hstacks[i].GetName().replace('hs_', ''),
                                 res,
                                 100. * res/hdata.Integral(1, nbins) )

