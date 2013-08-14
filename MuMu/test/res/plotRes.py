import array
import math
import yurii
import ROOT
from ROOT import *

#selection = "abs(eta)>1.5 & m2 < 80"
#label = "|#eta^{#gamma}| > 1.5"
selection = "pt > 10 & m2 < 80"
label = ""
scale = 1.
xRange = (0., 20.)
numScanSteps = 100
fitRange = xRange

xMin, xMax = xRange

gROOT.LoadMacro("../CMSStyle.C")
ROOT.CMSstyle()

canvases = []
graphs = []
latexLabel = TLatex()
latexLabel.SetNDC()
latexLabel.SetTextFont(132)
latexLabel.SetTextSize(0.06)
    
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
    nll.append( yurii.nllm3(scale, res=xvar[-1]) )
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
gr.GetXaxis().SetTitle("Photon Energy Scale [%]")
gr.GetYaxis().SetTitle("- log L")
gr.SetNameTitle("gr%d" % iteration, "Iteration %d" % iteration)
gr.Draw("ap")
graphs.append(gr)

## Extract the xvar
gr.Fit("pol2", "Q", "", fitRange[0], fitRange[1])
fit = gr.GetFunction("pol2")
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
latexLabel.DrawLatex(0.75,  0.25, "(%.2g #pm %.2g) %%" % (xvarVal, xvarErr))
#if abs(resVal - xVal) < epsilon and \
    #abs(resErr - xErr) < epsilon:
        #break
#xVal, xErr = resVal, resErr

#gr = graphs[-1]
#fit = gr.GetFunction("pol2")

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
gr.GetXaxis().SetTitle("Photon Surplus Resolution (%)")
gr.GetYaxis().SetTitle("- #Delta log L from m(#mu#mu#gamma)")
gr.SetNameTitle("gr%d" % iteration, "")
gr.Draw("ap")
graphs.append(gr)
gr.Fit("pol2", "", "", fitRange[0], fitRange[1])
fit = gr.GetFunction("pol2")
fit.SetLineWidth(1)
fit.SetLineColor(kRed)
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


##latexLabel.DrawLatex(0.2,  0.8, "p_{T}^{#gamma} > 10 GeV")
latexLabels = []
latexLabels.append(latexLabel.DrawLatex(0.2,  0.35, label))
#latexLabel.DrawLatex(0.2,  0.25, "Estimated Surplus Resolution: (%.1f #pm %.1f) %%" % (xvarVal, xvarErr))
latexLabels.append(
    latexLabel.DrawLatex(0.2,  0.25, "Estimated Photon Surplus Resolution: (%.1f #pm %.1f) %%" % (xvarVal, xvarErr))
    )
##latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
##latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")

for c in canvases:
    i = canvases.index(c)
    if i < len(graphs):
        c.cd()
        graphs[i].Draw("ap")
    c.SetWindowPosition(10+20*i, 10+20*i)

if __name__ == "__main__": import user
