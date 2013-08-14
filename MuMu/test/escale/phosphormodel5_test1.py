'''
Test partitioning of a fine (cache) binning by a coarse (reference) binning.
The n bins in the fine binning are split in m groups, where m is the number of
carse binning. 

The splitting is defined by the coarse bin in which a given fine bin center
falls:
bin i is in gropup j <=> low_j <= center_i < high_j
where low_j and high_j is the lower and upper boundary of the coarse bin j and
center_i is the bin center of the fine bin i.

For each group j = 0, .., m-1, a new binning fine_j is defined
such that the fine bin boundaries are preserved.
'''

import array
import ROOT
import JPsi.MuMu.common.roofit as roo

##------------------------------------------------------------------------------
def partition_binning(x, fine, coarse):
    '''partition_binning(RooAbsArg x, str fine, str coarse)
    fine .. name of the binning of x to be partitioned
    coarse .. name of the binning of x to define the partitioning
    '''
    fbins = x.getBinning(fine)
    cbins = x.getBinning(coarse)
    ## Create empty lists of bins, one for each group.
    boundaries = []
    for cbin in range(cbins.numBins()):
        boundaries.append([])
    ## Loop over the fine bins
    for fbin in range(fbins.numBins()):
        groupindex = cbins.binNumber(fbins.binCenter(fbin))
        ## Add the low boundary to the right group.
        boundaries[groupindex].append(fbins.binLow(fbin))
        ## Check if the high boundary has to be added.
        if fbin == fbins.numBins() - 1:
            ## This is the last bin.  Have to add the high boundary to the
            ## current group.
            boundaries[groupindex].append(fbins.binHigh(fbin))
            continue
        if fbin == 0:
            ## This is the first bin.  There is no previous bin, so that's it.
            continue
        if len(boundaries[groupindex]) == 1:
            ## This is the first bin in this group.  Add the boundary also
            ## to the previous group.
            boundaries[groupindex-1].append(fbins.binLow(fbin))
    ## End of loop over boundaries.
    names = []
    for i, iboundaries in enumerate(boundaries):
        barray = array.array('d', iboundaries)
        nbins = len(barray) - 1
        name = '%s_%d' % (fine, i)
        names.append(name)
        binning = ROOT.RooBinning(nbins, barray, name)
        x.setBinning(binning, name)
    return names
## End of partition_binning().

##------------------------------------------------------------------------------

x = ROOT.RooRealVar('x', 'x', 0, -5, 5)
x.setBins(10, 'cache')
x.setBins(3, 'ref')
names = partition_binning(x, 'cache', 'ref')

for name in names:
    if x.hasBinning(name):
        x.getBinning(name).Print()

if __name__ == '__main__':
    import user
