'''
Get the Et bin centers and asymmetric errors for the plots
of resolution versus Et.

Jan Veverka, Caltech, 12 September 2012

Modified: Increased pT bins and changed tree_version
Valere Lambert, Caltech, 14 August 2013
'''
import array
import ROOT
import JPsi.MuMu.common.roofit as roo
from JPsi.MuMu.common.energyScaleChains import getChains


#______________________________________________________________________________
## Configuration
tree_version = 'sixie'

## For EGM-11-001 to help with regression
cuts = [
    'mmMass + mmgMass < 180',
    'minDeltaR < 1.5',
    'minDeltaR > 0.1',
    'isFSR',
    ]

bin_edges = [10, 12, 15, 20, 25, 35, 999]
# cuts = ['mmMass + mmgMass < 180', 'minDeltaR < 1.5']
# cuts = ['mmMass + mmgMass < 180']
bin_low, bin_center, bin_high = [], [], []
  
#______________________________________________________________________________
def main():
    '''
    Main entry point for execution.
    '''
    global reduced_tree
    tree = getChains(tree_version)['z']
    reduced_tree = tree.CopyTree('(' + ')&('.join(cuts) + ')')
    
    for a in tree.GetListOfAliases():
        reduced_tree.SetAlias(a.GetName(), a.GetTitle())
        
    p = ROOT.RooStats.SignificanceToPValue(1)
    quantilex = array.array('d', [p, 0.5, 1. - p])
    quantiley = array.array('d', [1., 2., 3.])
    
    for lo, hi in zip(bin_edges[:-1], bin_edges[1:]):
        selection = '%d <= phoPt & phoPt < %d' % (lo, hi)
        tree.Draw('phoPt', 'pileup.weight * (%s)' % selection, 'goff')
        htemp = ROOT.gROOT.FindObject('htemp')
        htemp.GetQuantiles(3, quantiley, quantilex)
        bin_low   .append(quantiley[1] - quantiley[0])
        bin_center.append(quantiley[1])
        bin_high  .append(quantiley[2] - quantiley[1])
    
    print 'center:', bin_center
    print 'low:', bin_low
    print 'high:', bin_high
## End of main().


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user

