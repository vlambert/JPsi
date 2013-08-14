import array
import math
import yurii
import ROOT
from ROOT import *

selection = "abs(eta)<1.5 & m2 < 80"

xVal = 1.
xErr = 3.
rangeFactor = 1.
epsilon = 0.005
numScanSteps = 200
maxIterations = 1

gROOT.LoadMacro("../CMSStyle.C")
ROOT.CMSstyle()

canvases = []
graphs = []
latexLabel = TLatex()
latexLabel.SetNDC()
latexLabel.SetTextFont(132)
latexLabel.SetTextSize(0.06)

yurii.applySelection(selection)
    
for iteration in range(maxIterations):
    scale = []
    nll = []
    xLow = xVal - rangeFactor * xErr
    dx = 2 * rangeFactor * xErr / (numScanSteps - 1)
    print "Begin iteration %d: scanning over [%.2g, %.2g]" % \
        (iteration, xLow, xLow + dx * (numScanSteps-1)
         )
    ## Scan the NLL
    for istep in range(numScanSteps):
        scale.append(xLow + dx * istep)
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
    gr.Fit("pol2", "Q", "", -2, 4)
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
scaleErr = math.sqrt(1.92 / a)
minNLL = c - 0.25*b*b/a
print "Iteration %d results" % iteration
print "  photon energy scale: (%.3g +/- %.3g)%%" % (scaleVal, scaleErr)
print "  min -log(L)        : %.4g" % minNLL

## Make a graph on Delta NLL
dnll = [x - minNLL for x in nll]
x = array.array("d", scale)
y = array.array("d", dnll)
gr = TGraph(len(scale), x, y)

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
gr.Fit("pol2", "", "", -2, 4)

#latexLabel.DrawLatex(0.2,  0.8, "p_{T}^{#gamma} > 10 GeV")
latexLabel.DrawLatex(0.2,  0.3, "|#eta^{#gamma}| < 1.5")
latexLabel.DrawLatex(0.2,  0.2, "Estimated Scale: (%.1f #pm %.1f) %%" % (scaleVal, scaleErr))
#latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
#latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")

for c in canvases:
    i = canvases.index(c)
    if i < len(graphs):
        c.cd()
        graphs[i].Draw("ap")
    c.SetWindowPosition(10+20*i, 10+20*i)

if __name__ == "__main__": import user
