import os
from ROOT import *

infile = TFile("ootpu.root")

## Grab the histograms from a file in a dictionary
hist = {
  'Early'  : {},
  'InTime' : {},
  'Late'   : {}
}

puMax = 10

for puType in hist.keys():
    for npu in range(puMax):
        hist[puType][npu] = infile.Get( 'hR9_PU%s%d' % (puType, npu) )

h1 = hist['Early'][0]
bin094 = h1.GetXaxis().FindBin(0.9401)
binMax = h1.GetNbinsX()
#print h1.GetXaxis().GetBinLowEdge(bin094)

xtitles = {
    'Early'  : 'Number of Interactions at -50 ns',
    'InTime' : 'Number of In-Time Interactions',
    'Late'   : 'Number of Interactions at +50 ns'
}

hpass, htot, geff = {}, {}, {}
for tag in hist.keys():
    hpass[tag] = TH1F('hpass_' + tag, 'Events passing R9 > 0.94 ' + tag, puMax, -0.5, puMax-0.5)
    htot [tag] = TH1F('htot_'  + tag, 'All events ' + tag              , puMax, -0.5, puMax-0.5)
    geff [tag] = TGraphAsymmErrors()
    for npu in range(puMax):
        hpass[tag].Fill( npu, hist[tag][npu].Integral(bin094, binMax) )
        htot [tag].Fill( npu, hist[tag][npu].Integral(1     , binMax) )
    geff[tag].BayesDivide( hpass[tag], htot[tag] )
    for ih in [hpass, htot, geff]:
        ih[tag].GetXaxis().SetTitle( xtitles[tag] )


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


canvases = []
for tag in htot.keys():
    c1 = TCanvas()
    c1.Divide(2,2)
    c1.cd(1); hpass[tag].Draw()
    c1.cd(3); htot [tag].Draw()
    c1.cd(2); geff [tag].Draw('ap')
    canvases.append(c1)

c1 = TCanvas()
c1.SetGridx()
c1.SetGridy()

colors = {
    'Early': kBlue,
    'InTime': kBlack,
    'Late': kRed
}

markerStyles = {
    'Early': 20,
    'InTime': 21,
    'Late': 22
}

for tag, graph in geff.items():
    graph.SetMarkerColor( colors[tag] )
    graph.SetLineColor( colors[tag] )
    graph.SetMarkerStyle( markerStyles[tag] )
    #graph.GetXaxis().SetRangeUser(-0.5, 10.5)
    #graph.GetYaxis().SetRangeUser(0.57, 0.605)
    graph.GetXaxis().SetTitle( 'Number of Interactions' )
    graph.GetYaxis().SetTitle( 'Fraction of photons with R_{9} > 0.94' )

legend = TLegend(0.55, 0.6, 0.9, 0.9)
legend.SetFillColor(0)
legend.SetShadowColor(0)
legend.SetBorderSize(0)

legend.AddEntry( geff['InTime'], "in-time", "pl" )
legend.AddEntry( geff['Late'], "+50 ns", "pl" )
legend.AddEntry( geff['Early'], "-50 ns", "pl" )

geff['InTime'].Draw('ap')
geff['Early'].Draw('p')
geff['Late'].Draw('p')

legend.Draw()


if __name__ == "__main__": import user
