import array
import math
import yurii
import ROOT
from ROOT import *

selection = "abs(eta)>1.5 & m2 < 80"

xRange = (-30., 0.)
fitRange = (-13., -8.5)
epsilon = 0.005
numScanSteps = 1000
maxIterations = 1

gROOT.LoadMacro("../CMSStyle.C")
ROOT.CMSstyle()

canvases = []
graphs = []
latexLabel = TLatex()
latexLabel.SetNDC()
latexLabel.SetTextFont(132)
latexLabel.SetTextSize(0.06)
xMin, xMax = xRange
yurii.applySelection(selection)

xVal = 0.5 * sum(xRange)
xErr = 0.5 * (xRange[1] - xRange[0])
for iteration in range(maxIterations):
    scale = []
    nll = []
    dx = (xRange[1] - xRange[0]) / (numScanSteps - 1)
    print "Begin iteration %d: scanning over [%.2g, %.2g]" % \
        (iteration, xRange[0], xRange[1]
         )
    ## Scan the NLL
    for istep in range(numScanSteps):
        scale.append(xMin + dx * istep)
        nll.append( yurii.nll(scale[-1]) )
    ## Make a graph
    x = array.array("d", scale)
    y = array.array("d", nll)
    gr = TGraph(len(scale), x, y)
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
    
    ## Extract the scale
    gr.Fit("pol2", "", "", fitRange[0], fitRange[1])
    fit = gr.GetFunction("pol2")
    a = fit.GetParameter(2)
    b = fit.GetParameter(1)
    c = fit.GetParameter(0)
    scaleVal = -0.5 * b / a
    # 1.92 for 95% CI
    # 0.5 for 68.25% CI
    scaleErr = math.sqrt(0.5 / a)
    minNLL = c - 0.25*b*b/a
    print "Iteration %d results" % iteration
    print "  photon energy scale: (%.3g +/- %.3g)%%" % (scaleVal, scaleErr)
    print "  min -log(L)        : %.4g" % minNLL
    latexLabel.DrawLatex(0.75,  0.25, "(%.2g #pm %.2g) %%" % (scaleVal, scaleErr))
    if abs(scaleVal - xVal) < epsilon and \
       abs(scaleErr - xErr) < epsilon:
        break
    xVal, xErr = scaleVal, scaleErr

gr = graphs[-1]
fit = gr.GetFunction("pol2")
a = fit.GetParameter(2)
b = fit.GetParameter(1)
c = fit.GetParameter(0)
scaleVal = -0.5 * b / a
# 1.92 for 95% CI
# 0.5 for 68.25% CI
scaleErr = math.sqrt(0.5 / a)
minNLL = c - 0.25*b*b/a
print "Iteration %d results" % iteration
print "  photon energy scale: (%.3g +/- %.3g)%%" % (scaleVal, scaleErr)
print "  min -log(L)        : %.4g" % minNLL

## Make a graph on Delta NLL
dnll = [x - minNLL for x in nll]
x = array.array("d", scale)
y = array.array("d", dnll)
gr = TGraph(len(scale), x, y)
gr.Fit("pol2", "", "", fitRange[0], fitRange[1])

## Draw the graph
c1 =  TCanvas("DNLL", "DNLL")
canvases.append(c1)
#c.SetGridx()
#c.SetGridy()
gr.GetXaxis().SetTitle("Photon Energy Scale [%]")
gr.GetYaxis().SetTitle("- #Delta log L")
gr.SetNameTitle("gr%d" % iteration, "")
gr.Draw("ap")
graphs.append(gr)
gr.Fit("pol2", "", "", -7, 3)

#latexLabel.DrawLatex(0.2,  0.8, "p_{T}^{#gamma} > 10 GeV")
latexLabel.DrawLatex(0.2,  0.3, "|#eta^{#gamma}| > 1.5")
latexLabel.DrawLatex(0.2,  0.2, "Estimated Scale: (%.2f #pm %.2f) %%" % (scaleVal, scaleErr))
#latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
#latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")

for c1 in canvases:
    i = canvases.index(c1)
    if i < len(graphs):
        c1.cd()
        graphs[i].Draw("ap")
    c1.SetWindowPosition(10+20*i, 10+20*i)

if __name__ == "__main__": import user
