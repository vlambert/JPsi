import os
from ROOT import *
from array import array

#path = "/home/veverka/Work/data/pmv"
path = "/raid2/veverka/PMVTrees_v7"

fileName = {
    #"data": "pmvTree_Mu_Run2010AB-Dec22ReReco_v1_json_V3.root",
    #"z"   : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v1_V3.root",
    #"z"  : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v2_V3.root",
    #"tt"  : "pmvTree_TTJets_TuneZ2-madgraph-Winter10_V2.root",
    #"w"   : "",
    #"qcd" : "",
#     "gj"  : "pmvTree_GJets_TuneD6T_HT-40To100-madgraph_Winter10_V3.root",
    #"gj"  : "pmvTree_GJets_TuneD6T_HT-40To100-madgraph_Winter10_V3_numEvents40k.root",
    "gj"  : 'pmvTree_G_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_Summer11_AOD_42X-v4_V7.root',
    #'gj'  : 'pmvTree_G_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_Summer11_AOD_42X-v4_V6_numEvent80k.root',
}

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

## open files
file = {}
for tag, name in fileName.items():
    file[tag] = TFile(os.path.join(path, name))

## get trees
tree = {}
for tag, f in file.items():
    tree[tag] = f.Get("pmvTree/pmv")

pmv = tree['gj']

## Restrict to first 10k events for testing
pmv.Draw(">>elist", '', 'entrylist', 10000)
pmv.SetEntryList( gDirectory.Get('elist') )

## pick only photons matched to prompt photons from the ME
genCuts = [
    'phoMomPdgId == 22',
]

andCuts = lambda cuts: "&".join( "(%s)" % c for c in cuts )

gROOT.LoadMacro('PmvTree.C+')
from ROOT import PmvTree
t = PmvTree(pmv)

nbinsFixed = 500

outFile = TFile ('ootpu_EE.root', 'recreate')
hR9_all = TH1F('hR9_all', 'R9 all', nbinsFixed, 0.1, 1.1)
hR9_PUInTime, hR9_PUEarly, hR9_PULate = {}, {}, {}
for npu in range( 20 ):
    hR9_PUInTime[npu] = TH1F('hR9_PUInTime%d' % npu, 'In-Time PU = %d;R9' % npu, nbinsFixed, 0.1, 1.1)
    hR9_PUEarly[npu] = TH1F('hR9_PUEarly%d' % npu, '-50 ns PU = %d;R9' % npu, nbinsFixed, 0.1, 1.1)
    hR9_PULate[npu] = TH1F('hR9_PULate%d' % npu, '+50 ns PU = %d;R9' % npu, nbinsFixed, 0.1, 1.1)

## Read only needed branches
t.fChain.SetBranchStatus('*', 0)
for b in '''pileup.bunchCrossing
            pileup.numInteractions
            pileup.size
            nPhotons
            phoPt
            phoMomPdgId
            phoR9
            phoIsEB
            '''.split():
    t.fChain.SetBranchStatus(b, 1)

maxEvents = 100000000
npuInTimeForOOT = 0  ## negative to ignore this
## Loop over entries
for iEntry in range( min(t.fChain.GetEntriesFast(), maxEvents) ):
    t.GetEntry(iEntry)
    ## Get the numbers for early, in-time and late pile-up
    for ibx in range( t.pileup_size ):
        if t.pileup_bunchCrossing[ibx] == -1:
            npuEarly = t.pileup_numInteractions[ibx]
        elif t.pileup_bunchCrossing[ibx] == 0:
            npuInTime = t.pileup_numInteractions[ibx]
        elif t.pileup_bunchCrossing[ibx] == 1:
            npuLate = t.pileup_numInteractions[ibx]
    if npuInTimeForOOT >= 0 and npuInTimeForOOT != npuInTime:
        # ignore this event for OOT PU
        npuEarly = npuLate = 99
    ## Loop over photons
    for iPhoton in range( t.nPhotons ):
        if t.phoMomPdgId[iPhoton] != 22: continue
        if t.phoPt[iPhoton] < 20: continue
        if t.phoPt[iPhoton] > 100: continue
        if t.phoIsEB[iPhoton] != 0: continue # Barrel or encap?
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
        if hnorm[npu].Integral() <= 0.001:
            continue
        hnorm[npu].Sumw2()
        hnorm[npu].Scale( 1./ ( h[npu].Integral() * binWidth ) )

from array import array
nbins = 50
probabilities = array( 'd', [float(i) / float(nbins) for i in range(nbins + 1)] )
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
        if hnorm[npu].Integral() <= 0.001:
            continue
        hnorm[npu].Sumw2()
        hnorm[npu].Scale( 1. / hnorm[npu].Integral() )
        for bin in [i+1 for i in range(hnorm[npu].GetNbinsX())]:
            scaledBinContent = hnorm[npu].GetBinContent(bin) / hnorm[npu].GetBinWidth(bin)
            scaledBinError   = hnorm[npu].GetBinError  (bin) / hnorm[npu].GetBinWidth(bin)
            hnorm[npu].SetBinContent(bin, scaledBinContent)
            hnorm[npu].SetBinError  (bin, scaledBinError)



outFile.Write()

hR9_all.Draw()

if __name__ == '__main__': import user
