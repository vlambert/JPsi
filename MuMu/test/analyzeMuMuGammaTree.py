from ROOT import TChain, gDirectory, TCanvas, gROOT, TH1F, gPad
from ROOT import kBlue, kGreen, kYellow, kRed, kWhite, kBlack
from ROOT import kSpring, kOrange, kPink, kMagenta, kViolet, kAzure, kCyan, kTeal, kGray
from math import log, exp, log10

inputFiles = """
MuMuGammaTree_MinimumBias_Commissioning10-SD_Mu-Jun14thSkim_v1_132440-137028.root
MuMuGammaTree_Mu_Run2010A-Jun14thReReco_v1_135803-137436.root
MuMuGammaTree_Mu_Run2010A-Jul16thReReco-v1_139559-140159.root
MuMuGammaTree_Mu_Run2010A-PromptReco-v4_137437-139558_v2.root
MuMuGammaTree_Mu_Run2010A-PromptReco-v4_140160-140399.root
MuMuGammaTree_Mu_Run2010A-PromptReco-v4_140400-141961.root
MuMuGammaTree_Mu_Run2010A-PromptReco-v4_141962-142264_DCSTRONLY.root
""".split()

#

ch = TChain("MuMuGammaTree/mmg")
for f in inputFiles: ch.Add(f)

print "total entries:", ch.GetEntries()
canvases = gROOT.GetListOfCanvases()
pdgMass = {
  "eta"   :  0.548,
  "rho"   :  0.775,
  "omega" :  0.782,
  "phi"   :  1.019,
  "JPsi"  :  3.097,
  "psi2S" :  3.686,
  "Y1S"   :  9.460,
  "Y2S"   : 10.023,
  "Y3S"   : 10.355,
  "Z"     : 91.187,
}

colors = [kRed, kYellow, kGreen, kBlue]

def fillHistoRange(hist, xmin=85, xmax=98, color=kBlue):
  newh = hist.Clone(hist.GetName() + "_%f_%f" % (xmin, xmax))
  newh.SetFillColor(color)
  newh.SetLineColor(color)
  for bin in range(1, newh.GetNbinsX()):
    if newh.GetBinCenter(bin) < xmin or newh.GetBinCenter(bin) > xmax:
      newh.SetBinContent(bin, 0)
  newh.DrawCopy("same")
  return newh

def makeAndSelection(selString):
  # get a list of newline-separated cuts; strip their whitespace
  cuts = [cut.strip() for cut in selString.split("\n")]
  # remove "empty cuts"
  while "" in cuts:
    cuts.remove("")
  # add braces around each cut and return their `and'
  return "&".join(["({c})".format(c=cut) for cut in cuts])

def transformHisto(h, transform = lambda x, dx: 1.):
  """tranformHisto(h, tranform([x,dx]))
  Tranform bin content from the count of entries into e.g. density.
  Assumes Poisson errors of h."""
  for i in range(h.GetNbinsX()):
    bin = i+1
    x = h.GetBinCenter(bin)
    y = h.GetBinContent(bin)
    dx = h.GetBinWidth(bin)
    h.SetBinContent(bin, y * transform(x, dx))

def plotOSvsSS(name, expression, selectionString, binning):
  selection = makeAndSelection(selectionString)
  print name, "selection:", selection
  canvases.append(TCanvas())
  expr = expression + ">>" + name + binning
  exprSS = expression + ">>" + name + "_SS" + binning
  ch.Draw(expr, selection + "& charge==0")
  ch.Draw(exprSS, selection + "& charge!=0", "goff")
  hss = gDirectory.Get(name + "_SS")
  hss.SetLineColor(kRed)
  hss.Draw("same")

def makeVarBins(nbins, xmin, xmax, f, inverseF):
  """makeVarBins(nbins, xmin, xmax, f, inverseF)
  Make bins equidistant in f(x). Require monotonic f"""
  ymin = f(float(xmin))
  ymax = f(float(xmax))
  yBinWidth = (ymax - ymin) / nbins
  # is automagically ok even if f is falling
  next = lambda y : y + yBinWidth
  last = ymin
  bins = [last]
  for bin in range(nbins):
    last = next(last)
    bins.append(last)
  return [inverseF(x) for x in bins]

## plot the J/psi
def plotJPsi():
  selection = makeAndSelection("""
    isJPsiCand
    2.6 < mass & mass < 3.5
  """)
  print "J/Psi selection: ", selection
  canvases.append(TCanvas())
  ch.Draw("mass>>hJPsi(100,2.6,3.5)", selection + "& charge==0")
  # same sign pairs
  ch.Draw("mass>>hJPsiSS(100,2.6,3.5)", selection + "& charge!=0", "goff")
  hJPsiSS = gDirectory.Get("hJPsiSS")
  hJPsiSS.SetLineColor(kRed)
  hJPsiSS.Draw("same")

## plot the psi(2S)
def plotPsi2S():
  selection = makeAndSelection("""
    isJPsiCand
    3.3 < mass & mass < 4.2
  """)
  print "Psi(2S) selection: ", selection
  canvases.append(TCanvas())
  ch.Draw("mass>>hPsi2S(20,3.4,4.0)", selection + "& charge==0")
  # same sign pairs
  ch.Draw("mass>>hPsi2SSS(20,3.4,4.0)", selection + "& charge!=0", "goff")
  hPsi2SSS = gDirectory.Get("hPsi2SSS")
  hPsi2SSS.SetLineColor(kRed)
  hPsi2SSS.Draw("same")

## plot the Y(nS)
def plotY():
  selection = makeAndSelection("""
    isYCand
    8 < mass & mass < 12
  """)
  print "Y selection: ", selection
  canvases.append(TCanvas())
  ch.Draw("mass>>hY(40,8,12)", selection + "& charge==0")
  # same sign pairs
  ch.Draw("mass>>hYSS(40,8,12)", selection + "& charge!=0", "goff")
  hYSS = gDirectory.Get("hYSS")
  hYSS.SetLineColor(kRed)
  hYSS.Draw("same")

## plot the Z
def plotZ():
  selection = makeAndSelection("""
    isZCand
    60 < mass & mass < 120
  """)
  print "Z selection: ", selection
  canvases.append(TCanvas())
  ch.Draw("mass>>hZ(20,60,120)", selection + "& charge==0")
  # same sign pairs
  ch.Draw("mass>>hZSS(20,60,120)", selection + "& charge!=0", "goff")
  hZSS = gDirectory.Get("hZSS")
  hZSS.SetLineColor(kRed)
  hZSS.Draw("same")

## plot the full SM spectrum
def plotSM(nbins=1000, massMin=0.5, massMax=200, binf = lambda x: 1./x, inverseF = lambda x: 1./x):
  """plotSM(nbins=1000, massMin=0.5, massMax=200, binf = lambda x: 1./x, inverseF = lambda x: 1./x)"""
  selection = makeAndSelection("""
    isJPsiCand || isYCand || isZCand
    {mMin} < mass & mass < {mMax}
    orderByVProb == 0
    backToBack < 0.95
    vProb > 0.001
  """.format(mMin=massMin, mMax=massMax) )

  from math import log10
  # make bins quadratic in log10(mass)
#   increment = ( log10(massMax) - log10(massMin) ) / pow(nbins, 2)
#   bins = [log10(massMin) + pow(i,2) * increment for i in range(nbins)]
  # make bins quadratic in log10(mass)
#   bins.append(log10(massMax))
#   bins = [pow(10, x) for x in bins]
  bins = makeVarBins(nbins, massMin, massMax, binf, inverseF)
  massRange = {} # +/- epsilon% from the PDG value
  epsilon = 0.03 # 3.0 %
  for k in pdgMass.keys():
    massRange[k] = [ (1. - epsilon) * pdgMass[k], (1. + epsilon) * pdgMass[k] ]
  # remove overlap between YnS
#   massRange["Y1S"][1] = massRange["Y2S"][0] = 0.5 * (pdgMass["Y1S"] + pdgMass["Y2S"])
#   massRange["Y2S"][1] = massRange["Y3S"][0] = 0.5 * (pdgMass["Y2S"] + pdgMass["Y3S"])
#   binSubset = {}
#   for k in sorted(pdgMass.keys()):
#     binSubset[k] = []
#     for m in bins:
#       if massRange[k][0] < m and m < massRange[k][1]:
#         binSubset[k].append(m)
#     print k, str(binSubset[k])
  from array import array
  xbins = array('d', bins)
  hSM = TH1F("hSM", "Dimuon mass spectrum", nbins, xbins)
  hSMSS = TH1F("hSMSS", "Same-sign dimuon mass spectrum", nbins, xbins)
  cmass = "correctedMassJPsi * (mass<=7) + correctedMassY * (7<mass&mass<=15) + mass * (15<mass)"
#   ch.Draw(cmass + ">>hJPsi", selection + "& charge==0", "goff")
#   ch.Draw(cmass + ">>hPsi2S", selection + "& charge==0", "goff")
#   ch.Draw(cmass + ">>hY1S", selection + "& charge==0", "goff")
#   ch.Draw(cmass + ">>hY2S", selection + "& charge==0", "goff")
#   ch.Draw(cmass + ">>hY3S", selection + "& charge==0", "goff")
#   ch.Draw(cmass + ">>hZ", selection + "& charge==0", "goff")
  ch.Draw(cmass + ">>hSM", selection + "& charge==0", "goff")
  ch.Draw(cmass + ">>hSMSS", selection + "& charge!=0", "goff")
  # get the histograms
  h = gDirectory.Get("hSM")
  hss = gDirectory.Get("hSMSS")
  # store the poisson errors
  transformHisto(h, lambda x, dx : 1./dx) # v = [x, dx]
  transformHisto(hss, lambda x, dx: 1./dx)
  hss.SetLineColor(kYellow)
  hss.SetFillColor(kYellow)
  h.SetMarkerStyle(20)
  h.SetMarkerSize(0.5)
  c1 = TCanvas()
  canvases.append(c1)
  c1.SetLogx()
  c1.SetLogy()
  h.Draw("x0")
  hss.Draw("same hist")
  h.Draw("same x0")
  c1.RedrawAxis()
  return h, hss

h, hss = plotSM(binf = lambda x: log(x), inverseF = lambda x: exp(x))
transformHisto(hss, lambda x, dx: x/2.58) # scale to 100 nb^-1
transformHisto(h, lambda x, dx: x/2.58)
h.GetXaxis().SetTitle("m(#mu#mu) [GeV/c^{2}]")
h.GetYaxis().SetTitle("m(dN/dm) events per 100 nb^{-1}")
h.SetStatics(0)
hss.SetStatistics(0)
h.Draw()
hss.SetLineColor(kGray)
hss.SetFillColor(kGray)
resonances = ["rho", "omega", "phi", "JPsi", "psi2S", "Y1S", "Y2S", "Y3S", "Z"]
colors = {"Z": kBlue, "Y3S": kAzure, "Y2S": kTeal, "Y1S": kGreen,
  "psi2S": kYellow, "JPsi": kOrange, "phi": kRed, "omega": kPink,
  "rho": kMagenta
  }
lo, hi = 0.97, 1.03
for x in resonances:
  fillHistoRange(h, lo*pdgMass[x], hi*pdgMass[x], colors[x])

hss.Draw("same")
h.Draw("same")
gPad.RedrawAxis()

# order canvases
for c in canvases:
  i = canvases.index(c)
  c.SetWindowPosition(10+20*i, 10+20*i)

if __name__ == "__main__": import user
