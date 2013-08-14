## TODO:
## * sihih vs photon pt for both EE and EB
## * unbiased template for the EE
## * closure test of the unbiased templates

import sys
import MuMuGammaChain
from ROOT import *
from MuMuGammaChain import *

chains = MuMuGammaChain.getChains(MuMuGammaChain.bfiles,
                                  MuMuGammaChain.bpath
                                  )
skipDatasets = ["zg", "zmg"]

def makeSelection(cuts):
  return " & ".join("(%s)" % cut for cut in cuts)

# handy shortcuts
flush = sys.stdout.flush
for ch in chains.values():
    ch.SetAlias("mm", "mmgDimuon")
    ch.SetAlias("mu1", "dau1[mmgDimuon]")
    ch.SetAlias("mu2", "dau2[mmgDimuon]")
    ch.SetAlias("g", "mmgPhoton")

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


## Preselection
print "Applying preselection ...\n  ",
for name, ch in chains.items():
    print name,; flush()
    lname = "eventList_%s" % name
    ch.Draw(">>%s" % lname, "isBaselineCand & min(muPt[dau1], muPt[dau2]) > 20")
    ch.SetEventList(gDirectory.Get(lname))

file = TFile("yongCheckHistos.root", "recreate")

###############################################################################
## Make Dimuon invariant mass histos
print "\nMaking dimuon invariant mass histos ...\n  ",; flush()
var = RooRealVar("mass", "mass", 50, 150, "GeV")
var.setBins(100)
sel = "orderByVProb==0 & min(muPt[dau1], muPt[dau2]) > 20"
dataTrigMatchSel = "(" + \
    "(run < 147196 && max(muHltMu9Match[dau1], muHltMu9Match[dau2]) > 0) ||" +\
    "(147196 <= run && run < 148822 && max(muHltMu11Match[dau1], muHltMu11Match[dau2]) > 0) ||" +\
    "(148822 <= run && max(muHltMu15v1Match[dau1], muHltMu15v1Match[dau2]) > 0)" +\
    ")"
dataTrigSel = "(" + \
    "(run < 147196 && HLT_Mu9) ||" +\
    "(147196 <= run && run < 148822 && HLT_Mu11) ||" +\
    "(148822 <= run && HLT_Mu15_v1)" +\
    ")"
mcTrigMatchSel = "max(muHltMu9Match[dau1], muHltMu9Match[dau2]) > 0"
mcTrigSel = "HLT_Mu9"




binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())
for dataset, ch in chains.items():
    if dataset in skipDatasets: continue
    print dataset,; flush()
    ## variable title holds the expression for TTree::Draw
    hname = "h_%s_%s" % (var.GetName(), dataset)
    expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
    if dataset == "data38x":
        ch.Draw(expr, sel +"&&"+ dataTrigSel , "goff")
    else:
        ch.Draw(expr, sel +"&&"+ mcTrigSel , "goff")


#################################################################


#######################################################################


##############################################################################
## Make the dimuon mass plot on linear scale
lumi = 34. # pb^-1
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
xRange = (60., 120.)

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
        h.Scale(lumi * weight30[dataset] / 30.)

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


## Normalize MC to data
# for h in histos.values():
#     h.Scale(kfactor)

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

## Reports
def reportYield(firstBin, lastBin):
    kfactor = hdata.Integral(firstBin, lastBin) / mcIntegral
    print "Yields in mass window [%f,%f] GeV" % \
        (hdata.GetBinLowEdge(firstBin), hdata.GetBinLowEdge(lastBin+1))
    print "  MC prediction :", hs_mass_z.Integral(firstBin, lastBin)
    print "  Observed yield:", hdata.Integral(firstBin, lastBin)
    print "  Data / MC     : %.4g %%" % (100 * kfactor)
    print "  Expected purity: %.4g %%" % \
        (h_mass_z.Integral(firstBin, lastBin) / hs_mass_z.Integral(firstBin, lastBin))

reportYield(1, var.getBins())
reportYield(11, 70)
reportYield(32, 51)

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



## Create a couple more ratios after rebinning
def xRebins(hin, minBinContent = 25.):
    import array
    content = 0.
    xbins = [hin.GetBinLowEdge(1)]
    for i in range(hin.GetNbinsX()):
        bin = i + 1
        content += hin.GetBinContent(bin)
        if content >= minBinContent:
            content = 0.
            xbins.append(hin.GetBinLowEdge(bin+1))
    ## Check the last bin, merge the last 2 if possible
    if len(xbins) < 2:
        xbins.append(hin.GetBinLowEdge(hin.GetNbinsX()+1))
    else:
        xbins[-1] = hin.GetBinLowEdge(hin.GetNbinsX()+1)
    return array.array("d", xbins)


def makeRebinnedRatioPlot(minBinCount=25):
    xbins = xRebins(hdata, minBinCount)
    hmc = sortedHistos[0]
    hmc = hmc.Rebin(len(xbins)-1, hmc.GetName() + "_rebin%d" % minBinCount, xbins)
    hist = hdata.Rebin(len(xbins)-1, hdata.GetName() + "_ratio%d" % minBinCount, xbins)
    hist.Sumw2()
    hist.Divide(hmc)
    setattr(_module, hist.GetName(), hist)
    hist.GetYaxis().SetRangeUser(*yRange)
    hist.GetYaxis().SetTitle("Data / MC")
    c1 = newCanvas(var.GetName() + "_DataOverMC_%d" % minBinCount)
    canvases[hist.GetName()] = c1
    c1.SetGridy()
    c1.cd()
    hist.Draw()

gStyle.SetErrorX()
makeRebinnedRatioPlot(25.)
makeRebinnedRatioPlot(100.)
makeRebinnedRatioPlot(200.)





# ###############################################################################
# ## Make the mmg invariant mass histos
# ###############################################################################
# print "\nMaking mu-mu-gamma invariant mass histos ...\n  ",; flush()
#
# ## Cuts
# baselineCuts = [
#     "isBaselineCand[mm]",
#     "min(muPt[dau1[mm]], muPt[dau2[mm]]) > 20",
#     "orderByVProb[mm] == 0",
#     "40 < mass[mm] & mass[mm] < 85",
#     "nPhotons > 0",
#     "mmgPhoton == 0", # require the hardest photon in the events
#     "abs(phoScEta[g]) < 2.5",
#     "abs(phoScEta[g]) < 1.4442 || abs(phoScEta[g]) > 1.566",
#     "5 < phoPt[g]",
#     "60 < mmgMass & mmgMass < 120",
#     "mmgDeltaRNear < 1",
#     ]
#
# fsrCuts = [
#     "phoGenMatchPdgId[g] == 22",
#     "abs(phoGenMatchMomPdgId[g]) == 13",
#     ]
#
# fsrVeto = [ "!(%s)" % makeSelection(fsrCuts) ]
#
# ## TODO: dau1 --> mu1
# dataTrigSel = "(" + \
#     "(run < 147196 && max(muHltMu9Match[dau1], muHltMu9Match[dau2]) > 0) ||" +\
#     "(147196 <= run && run < 148822 && max(muHltMu11Match[dau1], muHltMu11Match[dau2]) > 0) ||" +\
#     "(148822 <= run && max(muHltMu15v1Match[dau1], muHltMu15v1Match[dau2]) > 0)" +\
#     ")"
# mcTrigSel = "max(muHltMu9Match[dau1], muHltMu9Match[dau2]) > 0)"
#
#
# photonCleaningCuts = [
#   "phoSeedRecoFlag[g] != 2",       # EcalRecHit::kOutOfTime = 2
#   "phoSeedSeverityLevel[g] != 4",  # EcalSeverityLevelAlgo::kWeird = 4
#   "phoSeedSeverityLevel[g] != 5",  # EcalSeverityLevelAlgo::kBad = 5
#   "phoSeedSwissCross[g] < 0.95",   # extra spike cleaning check
#   ]
#
#
# ## The variable - its title holds the expression for TTree::Draw
# var = RooRealVar("mmgMass", "mmgMass", 60, 120, "GeV")
# var.setBins(60)
# binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())
# for dataset, ch in chains.items():
#     if dataset in skipDatasets: continue
#     print dataset,; flush()
#     hname = "h_%s_%s" % (var.GetName(), dataset)
#     ## Update the preselection of events
#     #lname = "eventList_%s_%s" % (var.GetName(), dataset)
#     #ch.Draw(">>" + lname, makeSelection(baselineCuts))
#     #ch.SetEventList(gDirectory.Get(lname))
#     if dataset == "z":
#         ## Make separate plots for FSR and the rest
#         expr = "%s>>%sfsr(%s)" % (var.GetTitle(), hname, binning)
#         ch.Draw(expr, makeSelection(baselineCuts + mcTrigSel + fsrCuts), "goff")
#         expr = "%s>>%sjets(%s)" % (var.GetTitle(), hname, binning)
#         ch.Draw(expr, makeSelection(baselineCuts + fsrVeto), "goff")
#     else:
#         expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
#         if dataset == "data38x":
#             ch.Draw(expr, makeSelection(baselineCuts + photonCleaningCuts), "goff")
#         else:
#             ch.Draw(expr, makeSelection(baselineCuts), "goff")


file.Write()
# file.Close()


if __name__ == "__main__": import user
