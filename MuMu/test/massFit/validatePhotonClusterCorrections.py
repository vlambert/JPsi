import os
import dataset

import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *

#gROOT.LoadMacro("tdrstyle.C");
#from ROOT import setTDRStyle
#setTDRStyle()
gROOT.LoadMacro('energyCorrection.cc+')

gROOT.LoadMacro("CMSStyle.C")
from ROOT import CMSstyle
CMSstyle()

gStyle.SetPadRightMargin(0.05)
gStyle.SetCanvasDefH(600) # Height of canvas
gStyle.SetCanvasDefW(600) # Width of canvas
gStyle.SetOptTitle(0)
gStyle.SetTitleYOffset(1.2)
gStyle.SetTextSize(0.055)


def customizeModelParamBox(stats):
    stats.SetX1NDC(0.635)
    stats.SetX2NDC(0.99)
    stats.SetY1NDC(0.45)
    stats.SetY2NDC(0.99)
    stats.Draw()

## Initialization
canvases = []
ws1 = RooWorkspace( 'ws1', 'mmg energy scale' )
x = RooRealVar( 's', '100 * (1/kRatio - 1)', -50, 50, '%' )
# newCorrE = "newCorrE(scRawE+preshowerE,scEta,scPhiWidth/scEtaWidth)"
# x = RooRealVar( 's',
#   '100 * (%s/(phoPt*cosh(phoEta))/kRatio - 1)' % newCorrE,
#   -50, 50, '%'
# )
x.setBins(50)
xtitle = 's = E_{RECO}/E_{KIN} - 1'
w = RooRealVar( 'w', '1', 0, 99 )
xw = RooArgSet(x, w)
ws1.Import(xw)
fitColor = kAzure - 9
latexLabel = TLatex()
latexLabel.SetNDC()

## Define model
model = ws1.factory("""CBShape::crystalBall( s,
                                             #Deltas[0, -50, 50],
                                             #sigma[20, 0.001, 100],
                                             #alpha[-1.5, -10, 0],
                                             n[1.5, 0.1, 10] )""")

## Categories
catTitleCut = {
    'highR9_eb' : ('high R9 barrel' , 'subdet == subdet::Barrel  && r9 == r9::High'),
    'highR9_ee' : ('high R9 endcaps', 'subdet == subdet::Endcaps && r9 == r9::High'),
    'lowR9_eb'  : ('low R9 barrel'  , 'subdet == subdet::Barrel  && r9 == r9::Low' ),
    'lowR9_ee'  : ('low R9 endcaps' , 'subdet == subdet::Endcaps && r9 == r9::Low' ),
}

## Get data
data = dataset.get( tree = esChains.getChains('v4')['data'],
                    variable = x,
                    weight = w )
data.SetName('realData')
data.SetTitle('scale real data 750/pb')
ws1.Import(data)

## Get data in categories
realData = {}
for cat, (title, cut) in catTitleCut.items():
    realData[cat] = data.reduce( Cut(cut), Name('data_' + cat), Title(title) )

## Get MC
w.SetTitle('pileup.weightOOT')
data = dataset.get( tree = esChains.getChains('v4')['z'],
                    variable = x,
                    weight = w )
data.SetName('MC')
data.SetTitle('scale Summer11 S4 MC')
ws1.Import(data)

## Get data in categories
mc = {}
for cat, (title, cut) in catTitleCut.items():
    mc[cat] = data.reduce( Cut(cut), Name('mc_' + cat), Title(title) )

## Save a snapshot of the initial parameter values
x.SetTitle( xtitle )
observables = RooArgSet(x)
parameters = model.getParameters(observables)
ws1.defineSet("parameters", parameters)
ws1.saveSnapshot("initial", parameters, True)

sources = {
    'Data' : realData,
    'MC'   : mc,
}

markerColor = {
    'Data_highR9_eb' : (20, kAzure - 9),
    'Data_highR9_ee' : (20, kOrange - 2),
    'Data_lowR9_eb'  : (20, kAzure - 9),
    'Data_lowR9_ee'  : (20, kOrange - 2),
    'MC_highR9_eb' : (20, kAzure - 9),
    'MC_highR9_ee' : (20, kOrange - 2),
    'MC_lowR9_eb'  : (20, kAzure - 9),
    'MC_lowR9_ee'  : (20, kOrange - 2),
}

ws1.var('#Deltas').setUnit('%')
ws1.var('#sigma').setUnit('%')

for name, src in sources.items():
    for cat, data in src.items():
        label = name + '_' + cat
        ## Fit model to data
        res = model.fitTo( data, Save(), SumW2Error(kTRUE), PrintLevel(-1) )
        ## Save fitted parameters in the workspace
        ws1.saveSnapshot( label, parameters, True )
        ws1.Import(res)
        ## Plot fitted model overlaid with data
        x.setBins(40)
        plot = x.frame(Range(-30,50))
        marker, color = markerColor[label]
        model.paramOn( plot,
                        Format('NEU', AutoPrecision(2) ),
                        Parameters(parameters),
                        Layout(.57, 0.92, 0.92) )
        data.plotOn( plot, MarkerStyle(marker) )
        model.plotOn( plot, LineColor(color) )
        canvases.append( TCanvas(label, label) )
        plot.Draw()

        data.get(0)
        latexLabel.DrawLatex(0.16, 0.96, "CMS Preliminary 2011")
        latexLabel.DrawLatex(0.74, 0.96, "#sqrt{s} = 7 TeV")

        latexLabel.DrawLatex(0.2, 0.875, data.get(0).getCatLabel('subdet') )
        latexLabel.DrawLatex(0.2, 0.8, data.get(0).getCatLabel('r9') + ' R_{9}^{#gamma}' )

        latexLabel.DrawLatex(0.7, 0.6, "42X " + name )
        #latexLabel.DrawLatex(0.66, 0.45, "E_{T}^{#gamma} > 10 GeV")
        if name == 'Data':
            latexLabel.DrawLatex(0.64, 0.525, "Entries: %d" % int( data.sumEntries() ) )
            latexLabel.DrawLatex(0.66, 0.45, "L = 715 pb^{-1}")

## Print fit results



for i in range( len(canvases) ):
    canvases[i].SetWindowPosition(10+20*i, 10+20*i)

def save(ext = 'png', prefix = 'UBML_SFit'):
    for c in canvases:
        c.Print( prefix + '_' + c.GetName() + '.' + ext )

if __name__ == "__main__": import user
