from ROOT import *

infile = TFile("ootpu.root")

## Grab the histograms from a file in a dictionary
hist = {
  'Early'  : {},
  'InTime' : {},
  'Late'   : {}
}

for puType in hist.keys():
    for npu in range(20):
        hist[puType][npu] = infile.Get( 'hR9_varBins_PU%s%d_Norm' % (puType, npu) )


if __name__ == "__main__": import user
