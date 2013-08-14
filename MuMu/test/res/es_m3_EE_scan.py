import array
import math
import yurii
import ROOT
from ROOT import *

selection = "abs(eta)>1.5 & m2 < 80 & pt > 10"
label = "|#eta^{#gamma}| > 1.5"
#selection = "abs(eta)>1.5 & m2 < 80"
scale = 1.
xRange = (-15., 5.) ## Jan's data
# xRange = (-11., 4.) ## Olivier's data - tight m window
# xRange = (-17., 5.) ## Olivier's data - loose m window
# yRange = (-2., 7.)
yRange = (-3., 12.)  ## Olivier's data - loose m window
numScanSteps = 100
fitRange = xRange
m3WindowSizeScanRange = (5., 30.)
m3Center = 91.12
numM3ScanSteps = int(m3WindowSizeScanRange[1] - m3WindowSizeScanRange[0] + 1)


xMin, xMax = xRange

gROOT.LoadMacro("../CMSStyle.C")
ROOT.CMSstyle()
gStyle.SetOptFit(11)

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
xvarVal, xvarErr, m3Window = [], [], []
for im3 in range(numM3ScanSteps):
    xvar = []
    nll = []
    dx = (xMax - xMin) / (numScanSteps - 1)
    dm3 = m3WindowSizeScanRange[0] + \
          (m3WindowSizeScanRange[1] -  m3WindowSizeScanRange[0]) * \
          im3 / (numM3ScanSteps - 1)
    dm3 *= 0.5
    m3min = m3Center - dm3
    m3max = m3Center + dm3
    print "Begin iteration %d: scanning over [%f, %f]" % \
        (im3, m3min, m3max)
    ## Scan the NLL
    for istep in range(numScanSteps):
        xvar.append(xMin + dx * istep)
        nll.append( yurii.nllm3(scale=xvar[-1], res=0., m3min=m3min, m3max=m3max) )
    ## Make a graph
    x = array.array("d", xvar)
    y = array.array("d", nll)
    gr = TGraph(len(xvar), x, y)
    ## Draw the graph
    c1 =  TCanvas("iter%d" % im3, "Iteration %d" % im3)
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
    ixvarVal = -0.5 * b / a
    # 1.92 for 95% CI
    # 0.5 for 68.25% CI
    ixvarErr = math.sqrt(0.5 / a)
    minNLL = c - 0.25*b*b/a
    print "Iteration %d results" % im3
    print "  x estimate: (%.3g +/- %.3g)%%" % (ixvarVal, ixvarErr)
    print "  min -log(L)        : %.4g" % minNLL
    xvarVal.append(ixvarVal)
    xvarErr.append(ixvarErr)
    m3Window.append(2.* dm3)

## Make a graph on Delta NLL
x = array.array("d", m3Window)
y = array.array("d", xvarVal)
gr = TGraph(len(m3Window), x, y)

## Draw the graph
c1 =  TCanvas("XvsWindow", "x vs m3 widow size")
canvases.append(c1)
#c.SetGridx()
#c.SetGridy()
gr.GetXaxis().SetTitle("m(#mu#mu#gamma) window size (GeV)")
gr.GetYaxis().SetTitle("scale estimate (%)")
gr.SetNameTitle("gr%d" % iteration, "")
gr.Draw("ap")
graphs.append(gr)
#
#
# ##latexLabel.DrawLatex(0.2,  0.8, "p_{T}^{#gamma} > 10 GeV")
# latexLabel.SetText(0.21,  0.35, label)
# latexLabels.append(latexLabel.DrawClone())
# #latexLabellatexLabels.append(latexLabel.DrawLatex(0.2,  0.35, label))
# #drawLatex(0.2,  0.25, "Estimated Surplus Resolution: (%.1f #pm %.1f) %%" % (xvarVal, xvarErr))
# drawLatex(0.21,  0.25, "Estimated Photon Energy Scale: (%.1f #pm %.1f) %%" % (xvarVal, xvarErr))
# ##latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
# ##latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
#
# def drawResults():
#     "Redraw results on the canvas"
#     for l in latexLabels:
#         if l: l.Draw()

for c in canvases:
    if not c: continue
    i = canvases.index(c)
    if i < len(graphs):
        c.cd()
        graphs[i].Draw("ap")
    c.SetWindowPosition(10+20*i, 10+20*i)

if __name__ == "__main__": import user
