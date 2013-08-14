import os
from ROOT import *
from array import array

path = "/home/veverka/Work/data/pmv"

fileName = 'ootpu.roo'

## Set TDR style
macroPath = "tdrstyle.C"
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

## open file
file = TFile(os.path.join(path, name))

## get the histograms
hist = {
    'bx_0' : {},
    'bx_-1': {},
    'bx_+1': {},
}

for npu in range( 20 ):
    hR9_PUInTime[npu] = TH1F('hR9_PUInTime%d' % npu, 'In-Time PU = %d;R9' % npu, 2000, 0, 2)
    hR9_PUEarly[npu] = TH1F('hR9_PUEarly%d' % npu, '-50 ns PU = %d;R9' % npu, 2000, 0, 2)
    hR9_PULate[npu] = TH1F('hR9_PULate%d' % npu, '+50 ns PU = %d;R9' % npu, 2000, 0, 2)

## Read only needed branches
t.fChain.SetBranchStatus('*', 0)
for b in '''pileup.bunchCrossing
            pileup.numInteractions
            pileup.size
            nPhotons
            phoPt
            phoMomPdgId
            phoR9
            '''.split():
    t.fChain.SetBranchStatus(b, 1)

## Loop over entries
for iEntry in range( t.fChain.GetEntriesFast() ):
    t.GetEntry(iEntry)
    ## Get the numbers for early, in-time and late pile-up
    for ibx in range( t.pileup_size ):
        if t.pileup_bunchCrossing[ibx] == -1:
            npuEarly = t.pileup_numInteractions[ibx]
        elif t.pileup_bunchCrossing[ibx] == 0:
            npuInTime = t.pileup_numInteractions[ibx]
        elif t.pileup_bunchCrossing[ibx] == 1:
            npuLate = t.pileup_numInteractions[ibx]
    ## Loop over photons
    for iPhoton in range( t.nPhotons ):
        if t.phoMomPdgId[iPhoton] != 22: continue
        if t.phoPt[iPhoton] < 20: continue
        if t.phoPt[iPhoton] > 100: continue
        hR9_all.Fill( t.phoR9[iPhoton] )
        if npuEarly < 20:
            hR9_PUEarly[npuEarly].Fill( t.phoR9[iPhoton] )
        if npuInTime < 20:
            hR9_PUInTime[npuInTime].Fill( t.phoR9[iPhoton] )
        if npuLate < 20:
            hR9_PULate[npuLate].Fill( t.phoR9[iPhoton] )


## Normalize the histograms to unit area
hR9_PUEarly_Norm, hR9_PUInTime_Norm, hR9_PULate_Norm = {}, {}, {}
binWidth = hR9_PUEarly[0].GetBinWidth(1)
for npu in range( 20 ):
    for hnorm, h in [(hR9_PUEarly_Norm,  hR9_PUEarly ),
                     (hR9_PUInTime_Norm, hR9_PUInTime),
                     (hR9_PULate_Norm  , hR9_PULate  ),]:
        hnorm[npu] = h[npu].Clone( h[npu].GetName() + "_Norm" )
        hnorm[npu].Scale( 1./ ( h[npu].Integral() * binWidth ) )

from array import array
nbins = 100
probabilities = array( 'd', [float(i) / 100. for i in range(nbins + 1)] )
quantiles = array( 'd', [0. for i in range(nbins + 1)] )
hR9_all.GetQuantiles(nbins + 1, quantiles, probabilities)

hR9_varBins_all = TH1F('hR9_varBins_all', 'R9 all', nbins, quantiles)

hR9_varBins_PUEarly = {}
hR9_varBins_PUInTime = {}
hR9_varBins_PULate = {}

for npu in range( 20 ):
    hR9_varBins_PUInTime[npu] = TH1F('hR9_varBins_PUInTime%d' % npu, 'In-Time PU = %d;R9' % npu, nbins, quantiles)
    hR9_varBins_PUEarly[npu] = TH1F('hR9_varBins_PUEarly%d' % npu, '-50 ns PU = %d;R9' % npu, nbins, quantiles)
    hR9_varBins_PULate[npu] = TH1F('hR9_varBins_PULate%d' % npu, '+50 ns PU = %d;R9' % npu, nbins, quantiles)

## Loop over entries
for iEntry in range( t.fChain.GetEntriesFast() ):
    t.GetEntry(iEntry)
    ## Get the numbers for early, in-time and late pile-up
    for ibx in range( t.pileup_size ):
        if t.pileup_bunchCrossing[ibx] == -1:
            npuEarly = t.pileup_numInteractions[ibx]
        elif t.pileup_bunchCrossing[ibx] == 0:
            npuInTime = t.pileup_numInteractions[ibx]
        elif t.pileup_bunchCrossing[ibx] == 1:
            npuLate = t.pileup_numInteractions[ibx]
    ## Loop over photons
    for iPhoton in range( t.nPhotons ):
        if t.phoMomPdgId[iPhoton] != 22: continue
        if t.phoPt[iPhoton] < 20: continue
        if t.phoPt[iPhoton] > 100: continue
        hR9_varBins_all.Fill( t.phoR9[iPhoton] )
        if npuEarly < 20:
            hR9_varBins_PUEarly[npuEarly].Fill( t.phoR9[iPhoton] )
        if npuInTime < 20:
            hR9_varBins_PUInTime[npuInTime].Fill( t.phoR9[iPhoton] )
        if npuLate < 20:
            hR9_varBins_PULate[npuLate].Fill( t.phoR9[iPhoton] )

## Normalize the histograms to unit area
hR9_varBins_PUEarly_Norm = {}
hR9_varBins_PUInTime_Norm = {}
hR9_varBins_PULate_Norm = {}
for npu in range( 20 ):
    for hnorm, h in [(hR9_varBins_PUEarly_Norm,  hR9_varBins_PUEarly ),
                     (hR9_varBins_PUInTime_Norm, hR9_varBins_PUInTime),
                     (hR9_varBins_PULate_Norm  , hR9_varBins_PULate  ),]:
        hnorm[npu] = h[npu].Clone( h[npu].GetName() + "_Norm" )
        hnorm[npu].Sumw2()
        hnorm[npu].Scale( 1./ ( h[npu].Integral() * binWidth ) )
        for bin in [i+1 for i in range(hnorm[npu].GetNbinsX())]:
            scaled = hnorm[npu].GetBinContent(bin) / hnorm[npu].GetBinWidth(bin)
            hnorm[npu].SetBinContent(bin, scaled)



outFile.Write()

hR9_all.Draw()

if __name__ == '__main__': import user
