import os
from ROOT import *
from array import array

## Permanent location
path = "/raid2/veverka/various"

fileName = {
    'pho' : 'r9_fsr.root',
    'ele' : 'r9_Vlad.root',
}

colors = {
    'ele_mc'   : kOrange - 2,
    'ele_data' : kRed - 3,
}

legendTitles = {
    'ele_mc'   : 'Z#rightarrow ee MC',
    'ele_data' : 'Z#rightarrow ee data' ,
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

## open files and get histos
file = {}
hist = {}
for tag, name in fileName.items():
    file[tag] = TFile(os.path.join(path, name))
    if tag == 'pho':
        htag = 'FSR'
    else:
        htag = 'VBTF95'
    for subdet in ['Barrel', 'Endcap']:
        for src in ['data', 'mc']:
            hname = 'h_r9_%s_%s_%s' % (src, htag, subdet)
            hkey = '%s_%s_%s' % (tag, src, subdet)
            hist[hkey] = file[tag].Get(hname)

## Normalize
xlo = hist['pho_data_Barrel'].GetBinCenter(1)
xhi = hist['pho_data_Barrel'].GetBinCenter(80)

blo = hist['ele_data_Barrel'].GetXaxis().FindBin(xlo)
bhi = hist['ele_data_Barrel'].GetXaxis().FindBin(xhi)

nBarrel = hist['pho_data_Barrel'].Integral(1,80)
nEndcap = hist['pho_data_Endcap'].Integral(1,80)

hist['ele_data_Barrel'].Scale(
    nBarrel / hist['ele_data_Barrel'].Integral(blo, bhi)
)

hist['ele_mc_Barrel'].Scale(
    nBarrel / hist['ele_mc_Barrel'].Integral(blo, bhi)
)

hist['ele_data_Endcap'].Scale(
    nEndcap / hist['ele_data_Endcap'].Integral(blo, bhi)
)

hist['ele_mc_Endcap'].Scale(
    nEndcap / hist['ele_mc_Endcap'].Integral(blo, bhi)
)

for hkey in '''ele_data_Barrel
               ele_data_Endcap
               ele_mc_Barrel
               ele_mc_Endcap'''.split():
    hist[hkey].GetXaxis().SetRangeUser(xlo, xhi)

# hdata.Draw("e1 same")
# c1.RedrawAxis()
#
# latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2011")
# latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
# # latexLabel.DrawLatex(0.7, 0.2, "Barrel")
# latexLabel.DrawLatex(0.7, 0.2, "Endcaps")
# latexLabel.DrawLatex(0.2, 0.875, "42X data + MC")
# latexLabel.DrawLatex(0.2, 0.8,
#                      "Total events: %d" % \
#                      int( hdata.Integral(1, var.getBins() ) )
#                      )
# # latexLabel.DrawLatex(0.2, 0.725, "L = 332 pb^{-1}")
# latexLabel.DrawLatex(0.2, 0.725, "L = 499 pb^{-1}")
# #latexLabel.DrawLatex(0.2, 0.65, "E_{T}^{#gamma} #in [5,10] GeV")
# #latexLabel.DrawLatex(0.2, 0.65, "E_{T}^{#gamma} #in [10,15] GeV")
# #latexLabel.DrawLatex(0.2, 0.65, "E_{T}^{#gamma} #in [15,20] GeV")
# latexLabel.DrawLatex(0.2, 0.65, "E_{T}^{#gamma} > 20 GeV")


# latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2011")
# latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
# #latexLabel.DrawLatex(0.7, 0.2, "Barrel")
# #latexLabel.DrawLatex(0.7, 0.2, "Endcaps")
# latexLabel.DrawLatex(0.2, 0.875, "42X data and MC")
# latexLabel.DrawLatex(0.2, 0.8, "Total events: %d" % (int( hdata.GetEntries() ),) )
# latexLabel.DrawLatex(0.2, 0.725, "L = 332 pb^{-1}")
# latexLabel.DrawLatex(0.2, 0.65, "E_{T}^{#gamma} > 10 GeV")

# c1.Update()

if __name__ == '__main__': import user
