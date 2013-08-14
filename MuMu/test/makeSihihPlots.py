import sys
import ROOT

from ROOT import *
from MuMuGammaChain import *

##############################################################################
## Common stuff


# file = TFile("sihihHistos.root")
file = TFile("sihihHistos_Nov4ReReco_Fall10.root")
weight = cweight

gROOT.LoadMacro("tdrstyle.C")
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


##############################################################################
## Make the dimuon mass plot on linear scale
# lumi = 34. # pb^-1
lumi = 36.15 # pb^-1
realData = "data38x"
mcSamples = "z qcd w tt".split()
colors = {
    "z"     : kAzure - 9,
    "qcd"   : kYellow - 7,
    "tt"    : kOrange - 2,
    "w"     : kRed -3,
    #"qcd": kSpring + 5,
    #"tt" : kOrange - 2,
    #"w"  : kRed + 1,
}

yRange = (0., 2000.)

legendTitles = {
    "z"   : "Z",
    "qcd" : "QCD",
    "tt"  : "t#bar{t}",
    "w"   : "W",
}

var = RooRealVar("mass", "m(#mu^{+}#mu^{-})", 30, 130, "GeV")

c1 = TCanvas(var.GetName(), var.GetName(), 20, 20, wWidth, wHeight)
canvases["mass"] = c1

histos = {}
mcIntegral = 0.
for dataset in mcSamples + [realData]:
    hname = "h_%s_%s" % (var.GetName(), dataset)
    setattr(_module, hname, file.Get(hname))
    h = getattr(_module, hname)
    if not h:
        raise RuntimeError, "Didn't find %s in %s!" % (hname, file.GetName())

    if dataset in mcSamples:
        ## Normalize to the expected lumi
        h.Scale(weight[dataset])

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

## Normalize MC to data
#kfactor = hdata.Integral(1, var.getBins()) / mcIntegral
print "Z -> uu for m(uu) in [60, 120] GeV"
print "  MC expectation:", hstacks[0].Integral(31, 90)
print "  Observed yield:", hdata.Integral(31, 90)
print "  Signal purity : %.1f%%" % (100 * histos["z"].Integral(1, var.getBins()) / mcIntegral)
kfactor = hdata.Integral(31, 90) / hstacks[0].Integral(31, 90) ## normalize to (60,120)
print "  Normalizing MC to data by", kfactor
for h in histos.values():
    h.Scale(kfactor)

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


##############################################################################
## Make the dimuon mass plot on logy scale

yRange = (1.e-2, 1.e5)
c1 = TCanvas(var.GetName() + "_logy", var.GetName() + "_logy", 40, 40, wWidth, wHeight)
canvases["mass_logy"] = c1
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
## Make the dimuon mass Data / MC plot

yRange = (0., 2.)
cname = var.GetName() + "_DataOverMC"
c1 = TCanvas(cname, cname, 60, 60, wWidth, wHeight)
canvases["mass_ratio"] = c1
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


##############################################################################
## Make the mmg mass plot

yRange = (0., 105.)
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

weight["zfsr" ] = weight["z"]
weight["zjets"] = weight["z"]

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




##############################################################################
## Make the EB sigma ihih plot

yRange = (0., 160.)
xRange = (0.004, 0.025)

var = RooRealVar("ebSihih", "#sigma_{i#etai#eta}", 0., 0.03)

c1 = TCanvas(var.GetName(), var.GetName(), 140, 140, wWidth, wHeight)
canvases[var.GetName()] = c1

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
print "Z -> uuy (FSR) results for EB, |m-mz| < 4 GeV"
print "  MC expectaion : %.1f" % mcIntegral
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
    h.GetXaxis().SetRangeUser(*xRange)
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
latexLabel.DrawLatex(0.2, 0.85, "|#eta^{#gamma}| < 1.5")
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
c1.Update()


##############################################################################
## Make the EB sigma ihih plot on logy scale

yRange = (5.e-2, 1.e3)
c1 = TCanvas(var.GetName() + "_logy", var.GetName() + "_logy", 160, 160, wWidth, wHeight)
canvases[c1.GetName()] = c1
c1.SetLogy()
c1.cd()

## Draw with new y range
for h in hstacks:
    h.GetXaxis().SetRangeUser(*xRange)
    h.GetYaxis().SetRangeUser(*yRange)
    if hstacks.index(h) == 0: h.DrawCopy()
    else                    : h.DrawCopy("same")

hdata.DrawCopy("e0 same")
c1.RedrawAxis()

## Final touches
latexLabel.DrawLatex(0.2, 0.85, "|#eta^{#gamma}| < 1.5")
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
legend.Draw()


##############################################################################
## Make the EB sigma ihih Data / MC plot

yRange = (0., 2.)
cname = var.GetName() + "_ratio"
c1 = TCanvas(cname, cname, 180, 180, wWidth, wHeight)
canvases[cname] = c1
c1.SetGridy()
c1.cd()

## Create the ratio
hist = hdata.Clone(hdata.GetName() + "_ratio")
setattr(_module, hist.GetName(), hist)
hist.Sumw2()
hist.Divide(hstacks[0])
hist.GetXaxis().SetRangeUser(*xRange)
hist.GetYaxis().SetRangeUser(*yRange)
hist.GetYaxis().SetTitle("Data / MC")
hist.Draw()

c1.RedrawAxis()

## Final touches
latexLabel.DrawLatex(0.2, 0.85, "|#eta^{#gamma}| < 1.5")
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")






##############################################################################
## Make the EE sigma ihih plot

yRange = (0., 50.)
xRange = (0.01, 0.065)

var = RooRealVar("eeSihih", "#sigma_{i#etai#eta}", 0., 0.1)

c1 = TCanvas(var.GetName(), var.GetName(), 200, 200, wWidth, wHeight)
canvases[var.GetName()] = c1

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
print "Z -> uuy (FSR) results for |eta| > 1.5 (EE), |m-mz| < 4 GeV"
print "  MC expectaion : %.1f" % mcIntegral
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
    h.GetXaxis().SetRangeUser(*xRange)
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
latexLabel.DrawLatex(0.2, 0.85, "|#eta^{#gamma}| > 1.5")
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
c1.Update()


##############################################################################
## Make the EE sigma ihih plot on logy scale

yRange = (5.e-2, 1.e3)
c1 = TCanvas(var.GetName() + "_logy", var.GetName() + "_logy", 220, 220, wWidth, wHeight)
canvases[c1.GetName()] = c1
c1.SetLogy()
c1.cd()

## Draw with new y range
for h in hstacks:
    h.GetXaxis().SetRangeUser(*xRange)
    h.GetYaxis().SetRangeUser(*yRange)
    if hstacks.index(h) == 0: h.DrawCopy()
    else                    : h.DrawCopy("same")

hdata.DrawCopy("e0 same")
c1.RedrawAxis()

## Final touches
latexLabel.DrawLatex(0.2, 0.85, "|#eta^{#gamma}| > 1.5")
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
legend.Draw()


##############################################################################
## Make the EE sigma ihih Data / MC plot

yRange = (0., 2.)
cname = var.GetName() + "_ratio"
c1 = TCanvas(cname, cname, 240, 240, wWidth, wHeight)
canvases[cname] = c1
c1.SetGridy()
c1.cd()

## Create the ratio
hist = hdata.Clone(hdata.GetName() + "_ratio")
setattr(_module, hist.GetName(), hist)
hist.Sumw2()
hist.Divide(hstacks[0])
hist.GetXaxis().SetRangeUser(*xRange)
hist.GetYaxis().SetRangeUser(*yRange)
hist.GetYaxis().SetTitle("Data / MC")
hist.Draw()

c1.RedrawAxis()

## Final touches
latexLabel.DrawLatex(0.2, 0.85, "|#eta^{#gamma}| > 1.5")
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")


##############################################################################
## Make the unbiased EB sigma ihih plot

xRange = (0.004, 0.025)
yRange = (0., 75.)

var = RooRealVar("ubebSihih", "#sigma_{i#etai#eta}", 0., 0.03)

c1 = newCanvas(var.GetName())

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
print "Z -> uuy (FSR) results for EB, |m-mz| < 4 GeV, pt(g) > 10 GeV, DR > 0.1"
print "  MC expectaion : %.1f" % mcIntegral
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
    h.GetXaxis().SetRangeUser(*xRange)
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
latexLabel.DrawLatex(0.2, 0.85, "|#eta^{#gamma}| < 1.5")
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
c1.Update()


##############################################################################
## Make the EB sigma ihih plot on logy scale

yRange = (5.e-2, 1.e3)

c1 = newCanvas(var.GetName() + "_logy")
c1.SetLogy()
c1.cd()

## Draw with new y range
for h in hstacks:
    h.GetXaxis().SetRangeUser(*xRange)
    h.GetYaxis().SetRangeUser(*yRange)
    if hstacks.index(h) == 0: h.DrawCopy()
    else                    : h.DrawCopy("same")

hdata.DrawCopy("e0 same")
c1.RedrawAxis()

## Final touches
latexLabel.DrawLatex(0.2, 0.85, "|#eta^{#gamma}| < 1.5")
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
legend.Draw()


##############################################################################
## Make the EB sigma ihih Data / MC plot

yRange = (0., 2.)
cname = var.GetName() + "_ratio"
c1 = TCanvas(cname, cname, 320, 320, wWidth, wHeight)
canvases[cname] = c1
c1.SetGridy()
c1.cd()

## Create the ratio
hist = hdata.Clone(hdata.GetName() + "_ratio")
setattr(_module, hist.GetName(), hist)
hist.Sumw2()
hist.Divide(hstacks[0])
hist.GetXaxis().SetRangeUser(*xRange)
hist.GetYaxis().SetRangeUser(*yRange)
hist.GetYaxis().SetTitle("Data / MC")
hist.Draw()

c1.RedrawAxis()

## Final touches
latexLabel.DrawLatex(0.2, 0.85, "|#eta^{#gamma}| < 1.5")
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")





