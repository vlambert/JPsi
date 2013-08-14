import array
import math
import yurii
import ROOT
from ROOT import *

selection = "abs(eta)>1.5 & m2 < 80 & pt > 10"
label = "Endcaps"
#selection = "abs(eta)>1.5 & m2 < 80"
scale = 1.
xRange = (-15., 5.) ## Dec22 rereco
# xRange = (-16., -1.) ## Jan's data
# xRange = (-11., 4.) ## Olivier's data - tight m window
# xRange = (-17., 5.) ## Olivier's data - loose m window
# yRange = (-2., 7.)
yRange = (-3., 12.)  ## Olivier's data - loose m window
numScanSteps = 100
fitRange = xRange

xMin, xMax = xRange

gROOT.LoadMacro("../CMSStyle.C")
ROOT.CMSstyle()
gStyle.SetOptFit(11)
gStyle.SetOptTitle(0)

canvases = []
graphs = []
latexLabels = []

latexLabel = TLatex()
latexLabel.SetNDC()
latexLabel.SetTextFont(132)
latexLabel.SetTextSize(0.06)

def drawLatex(x, y, text):
    latexLabel.SetText(x, y, text)
    latexLabels.append(latexLabel.DrawClone())

yurii.applySelection(selection)

iteration = 1
xvar = []
nll = []
dx = (xMax - xMin) / (numScanSteps - 1)
#print "Begin iteration %d: scanning over [%.2g, %.2g]" % \
    #(iteration, xMin, xMax)
## Scan the NLL
for istep in range(numScanSteps):
    xvar.append(xMin + dx * istep)
    nll.append( yurii.nllm3(scale=xvar[-1], res=0., m3min=84, m3max=96, nbinsMC=60) )
## Make a graph
x = array.array("d", xvar)
y = array.array("d", nll)
gr = TGraph(len(xvar), x, y)
## Draw the graph
c1 =  TCanvas("iter%d" % iteration, "Iteration %d" % iteration)
canvases.append(c1)
c1.SetGridx()
c1.SetGridy()
#gr.Draw("ap")
gr.GetXaxis().SetTitle("Photon Energy Scale (%)")
gr.GetYaxis().SetTitle("- log L")
gr.SetNameTitle("gr%d" % iteration, "Iteration %d" % iteration)
gr.Draw("ap")
graphs.append(gr)

## Extract the xvar
fit = TF1("fit", "pol2", -16, -1)
fit.SetLineWidth(1)
fit.SetLineColor(kRed)
fit.SetParNames("p_{0}", "p_{1}", "p_{2}")
gr.Fit(fit, "Q", "", fitRange[0], fitRange[1])
#fit = gr.GetFunction("pol2")
a = fit.GetParameter(2)
b = fit.GetParameter(1)
c = fit.GetParameter(0)
xvarVal = -0.5 * b / a
# 1.92 for 95% CI
# 0.5 for 68.25% CI
xvarErr = math.sqrt(0.5 / a)
minNLL = c - 0.25*b*b/a
print "Iteration %d results" % iteration
print "  x estimate: (%.3g +/- %.3g)%%" % (xvarVal, xvarErr)
print "  min -log(L)        : %.4g" % minNLL

## Make a graph on Delta NLL
dnll = [x - minNLL for x in nll]
x = array.array("d", xvar)
y = array.array("d", dnll)
gr = TGraph(len(xvar), x, y)

## Draw the graph
c1 =  TCanvas("DNLL", "DNLL")
canvases.append(c1)
#c.SetGridx()
#c.SetGridy()
gr.GetXaxis().SetTitle("Photon Energy Scale (%)")
gr.GetYaxis().SetTitle("- #Delta log L  for m(#mu#mu#gamma)")
gr.SetNameTitle("gr%d" % iteration, "")
gr.Draw("ap")
graphs.append(gr)
gr.GetYaxis().SetRangeUser(*yRange)
gr.Fit(fit, "", "", fitRange[0], fitRange[1])
a = fit.GetParameter(2)
b = fit.GetParameter(1)
c = fit.GetParameter(0)
# 1.92 for 95% CI
# 0.5 for 68.25% CI
xvarVal = -0.5 * b / a
xvarErr = math.sqrt(0.5 / a)
minNLL = c - 0.25*b*b/a
print "Iteration %d results" % iteration
print "  photon energy res: (%.3g +/- %.3g)%%" % (xvarVal, xvarErr)
print "  min -log(L)        : %.4g" % minNLL

## Move the stats box
stats1 = c1.GetPrimitive("stats")
sWidthNDC = stats1.GetX2NDC() - stats1.GetX1NDC()
sHeightNDC = stats1.GetY2NDC() - stats1.GetY1NDC()

stats1.SetX1NDC(0.375)
stats1.SetX2NDC(0.375 + sWidthNDC)
stats1.SetY1NDC(0.7)
stats1.SetY2NDC(0.7 + sHeightNDC)

##latexLabel.DrawLatex(0.2,  0.8, "p_{T}^{#gamma} > 10 GeV")
latexLabel.SetText(0.21,  0.35, label)
latexLabels.append(latexLabel.DrawClone())
#latexLabellatexLabels.append(latexLabel.DrawLatex(0.2,  0.35, label))
#drawLatex(0.2,  0.25, "Estimated Surplus Resolution: (%.1f #pm %.1f) %%" % (xvarVal, xvarErr))
drawLatex(0.21,  0.25, "Estimated Photon Energy Scale: (%.1f #pm %.1f) %%" % (xvarVal, xvarErr))
##latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
##latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")

def drawResults():
    "Redraw results on the canvas"
    for l in latexLabels:
        if l: l.Draw()

for c in canvases:
    i = canvases.index(c)
    if i < len(graphs):
        c.cd()
        graphs[i].Draw("ap")
    c.SetWindowPosition(10+20*i, 10+20*i)

if __name__ == "__main__": import user
