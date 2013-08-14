import sys
import os
import ROOT

from ROOT import *
from JPsi.MuMu.common.MuMuGammaChain import *

##############################################################################
## Common stuff


file = TFile("test2.root")
weight = cweight
weight["zfsr" ] = weight["z"]
weight["zjets"] = weight["z"]

## Set TDR style
macroPath = os.path.join(os.environ["CMSSW_BASE"], "src/JPsi/MuMu/test/tdrstyle.C")
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

canvases = {}
legends = {}
_module = sys.modules[__name__]

def newCanvas(name, title="", windowWidth=600, windowHeight=600):
    if title == "":
        title = name
    if len(gROOT.GetListOfCanvases()) > 0:
        lastCanvas = gROOT.GetListOfCanvases()[-1]
        topX = lastCanvas.GetWindowTopX() + canvasDX
        topY = lastCanvas.GetWindowTopY() + canvasDY
    else:
        topX = topY = 20
    c1 = TCanvas(name, title, topX, topY, windowWidth, windowHeight)
    canvases[name] = c1
    return c1


lumi = 36.1 # pb^-1
kfactor = 1.1398774513437029

##############################################################################
## Make the mmg mass plot

yRange = (0., 205.)
realData = "data38x"
mcSamples = "zfsr zjets qcd w tt".split()

colors = {
    "zfsr"  : kAzure - 9,
    "zjets" : kSpring + 5,
    "qcd"   : kYellow - 7,
    "tt"    : kOrange - 2,
    "w"     : kRed -3,
}

#yRange = (0., 2000.)

legendTitles = {
    "zfsr"  : "FSR",
    "zjets" : "Z+jets",
    "qcd"   : "QCD",
    "tt"    : "t#bar{t}",
    "w"     : "W",
}

var = RooRealVar("mmgMass", "m(#mu^{+}#mu^{-}#gamma)", 60, 120, "GeV")

c1 = TCanvas(var.GetName(), var.GetName(), 80, 80, wWidth, wHeight)
canvases["mmgMass"] = c1

weight30["zfsr" ] = weight30["z"]
weight30["zjets"] = weight30["z"]

histos = {}
mcIntegral = 0.
for dataset in mcSamples + [realData]:
    hname = "h_%s_%s" % (var.GetName(), dataset)
    setattr(_module, hname, file.Get(hname) )
    h = getattr(_module, hname)
    if not h:
        raise RuntimeError, "Didn't find %s in %s!" % (hname, file.GetName())

    if dataset in mcSamples:
        ## Normalize to the expected lumi
        h.Scale(kfactor * weight[dataset])

        ## Add to the total integral
        mcIntegral += h.Integral(1, var.getBins())

        ## Set Colors
        h.SetLineColor(colors[dataset])
        h.SetFillColor(colors[dataset])

        histos[dataset] = h

    else:
        hdata = h

    ## Set Titles
    xtitle = var.GetTitle()
    ytitle = "Events / %.2g pb^{-1} / %.2g" % (lumi, h.GetBinWidth(1))
    if var.getUnit():
        xtitle += " [%s]" % var.getUnit()
        ytitle += " %s" % var.getUnit()
    h.GetXaxis().SetTitle(xtitle)
    h.GetYaxis().SetTitle(ytitle)

## Report yield and purity
print "Z -> uuy (FSR) results for m in [60, 120] GeV"
print "  MC expectaion : %.1f +/- %.1f" % (mcIntegral, sqrt(mcIntegral))
print "  Observed yield:", hdata.Integral(1, var.getBins())
print "  Signal purity : %.1f%%" % (100 * histos["zfsr"].Integral(1, var.getBins()) / mcIntegral)

## Sort histos
sortedHistos = histos.values()
sortedHistos.sort(key=lambda h: h.Integral())

## Make stacked histos (THStack can't redraw axis!? -> roottalk)
hstacks = []
for h in sortedHistos:
    hstemp = h.Clone(h.GetName().replace("h_", "hs_"))
    setattr(_module, hstemp.GetName(), hstemp)
    if hstacks:
        hstemp.Add(hstacks[-1])
    hstacks.append(hstemp)

## Draw
hstacks.reverse()
for h in hstacks:
    h.GetYaxis().SetRangeUser(*yRange)
    if hstacks.index(h) == 0: h.DrawCopy()
    else:                     h.DrawCopy("same")
hdata.DrawCopy("e0 same")
c1.RedrawAxis()


## Legend
ihistos = {}
for d, h in histos.items():
    ihistos[h] = d

legend = TLegend(0.75, 0.6, 0.9, 0.9)
legends[var.GetName()] = legend
legend.SetFillColor(0)
legend.SetShadowColor(0)
legend.SetBorderSize(0)

legend.AddEntry(hdata, "Data", "pl")

sortedHistos.reverse()
for h in sortedHistos:
    legend.AddEntry(h, legendTitles[ihistos[h]], "f")

legend.Draw()

## Final touch
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
c1.Update()


##############################################################################
## Make the MMG mass plot on logy scale

yRange = (5.e-2, 1.e3)
c1 = TCanvas(var.GetName() + "_logy", var.GetName() + "_logy", 100, 100, wWidth, wHeight)
canvases[c1.GetName()] = c1
c1.SetLogy()
c1.cd()

## Draw with new y range
# ymin = 0.5 * min(weight30.values())
for h in hstacks:
    h.GetYaxis().SetRangeUser(*yRange)
    if hstacks.index(h) == 0: h.DrawCopy()
    else                    : h.DrawCopy("same")

hdata.DrawCopy("e0 same")
c1.RedrawAxis()

## Final touches
# legend.DrawClone()
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
legend.Draw()



##############################################################################
## Make the mmg mass Data / MC plot

yRange = (0., 2.)
cname = var.GetName() + "_ratio"
c1 = TCanvas(cname, cname, 120, 120, wWidth, wHeight)
canvases[cname] = c1
c1.SetGridy()
c1.cd()

## Create the ratio
hist = hdata.Clone(hdata.GetName() + "_ratio")
setattr(_module, hist.GetName(), hist)
hist.Sumw2()
hist.Divide(hstacks[0])
hist.GetYaxis().SetRangeUser(*yRange)
hist.GetYaxis().SetTitle("Data / MC")
hist.Draw()

c1.RedrawAxis()

## Final touches
# legend.DrawClone()
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")


