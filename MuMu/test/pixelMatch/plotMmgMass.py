import os
from ROOT import *
from array import array

path = "/raid2/veverka/PMVTrees_v1/"
realData = "data38x"
mcSamples = "z qcd w tt".split()

lumi = 36.15 # pb^-1


fileName = {
    #"data": "pmvTree_Mu_Run2010AB-Dec22ReReco_v1_json_V3.root",
    "data": "pmvTree_ZMu-May10ReReco-42X-v3_V5.root",
    #"z"   : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v1_V3.root",
    #"z"  : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v2_V3.root",
    #"tt"  : "pmvTree_TTJets_TuneZ2-madgraph-Winter10_V3.root",
    #"w"   : "pmvTree_WJetsToLNu_TuneZ2_7TeV-madgraph_Winter10_V3.root",
    #"qcd" : "pmvTree_QCD_Pt-20_MuEnrichedPt-15_Winter10_V3.root",
        
    'w': 'pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V5.root',
    'qcd': 'pmvTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V5.root',
    'tt': 'pmvTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V5.root',
    'z': 'pmvTree_Z-RECO-41X-v2_V5.root',
}


cweight = {
    "data": 1.,
    #"z"  : 0.030541912803076,
    #"qcd": 0.10306919044126,
    #"w"  : 0.074139194512438,
    #"tt" : 0.005083191122289,
    
    'z'  : 0.17175592557735,
    'tt' : 0.019860956416475,
    'w'  : 0.54974976060237,
    'qcd': 0.27884236321449,
    
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
file = {}
for tag, name in fileName.items():
    file[tag] = TFile(os.path.join(path, name))

## get trees
tree = {}
for tag, f in file.items():
    tree[tag] = f.Get("pmvTree/pmv")

## make histos of pmv vs mmgMass

#ebSelection = "phoIsEB & abs(mmgMass-90)<15 & (minDEta > 0.04 | minDPhi > 0.3)"
#eeSelection = "!phoIsEB & abs(mmgMass-90)<15 & (minDEta > 0.08 | minDPhi > 0.3)"
selection = "1"
#selection = 'phoIsEB'
#selection = '!phoIsEB'

###############################################################################
# Plot a quantity in data for EB
yRange = (1e-4, 1000.)

c1 = TCanvas()
canvases.append(c1)

var = RooRealVar("mmgMass", "m_{#mu#mu#gamma}", 60, 120, "GeV")
var.setBins(60)

h_temp = TH1F("h_temp", "", var.getBins(), var.getMin(), var.getMax() )
h_temp.GetXaxis().SetTitle( var.GetTitle() )
h_temp.GetYaxis().SetTitle("Events / 1 GeV")
h_temp.SetTitle("")
h_temp.SetStats(0)
histos = {}
for tag, t in tree.items():
    sel = 'puWeight *%f * (%s) ' % (cweight[tag], selection,)
    if tag == 'z':
        sel += ' && isFSR'
    if tag == 'data':
        continue
    t.Draw(var.GetName() + '>>h_temp', sel )
    histos[tag] = h_temp.Clone( 'h_' + tag )

tree['z'].Draw(var.GetName() + '>>h_temp', "puWeight * %f * (%s) && !isFSR" % (cweight[tag], selection) )
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

for hist in hstacks:
    hist.Scale( hdata.GetEntries() / mcIntegral )


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
latexLabel.DrawLatex(0.2, 0.875, "May10ReReco + Spring11 MC")
latexLabel.DrawLatex(0.2, 0.8, "Total events: %d" % (int( hdata.GetEntries() ),) )
latexLabel.DrawLatex(0.2, 0.725, "L = 191 pb^{-1}")

c1.Update()


