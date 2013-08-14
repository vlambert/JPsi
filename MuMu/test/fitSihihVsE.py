import sys
import ROOT

from ROOT import *
from MuMuGammaChain import *

##############################################################################
## Common stuff


file = TFile("sihihHistos.root")

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

lumi = 34. # pb^-1
realData = "data38x"
mcSamples = "zfsr qcd w tt".split()
mcRefSample = "zg"

prof1 = file.Get("prof_ebSihihVsE_zg")
prof1.Draw()
prof1.GetYaxis().SetRangeUser(0., 0.02)
fit1 = TF1("fit1", "[0] + [1] * pow(TMath::Abs(x - [2]), [3])", 5, 100)
for i in range(4):
    fit1.SetParName(i, chr(i + ord("a")))

pars1 = [0.01, 1., 0., -1.]
for p in pars1:
    fit1.SetParameter(pars1.index(p), p)
