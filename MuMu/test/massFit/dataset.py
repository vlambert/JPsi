'''Utility to extract RooDataSet from a TTree.

Data:
  - tree: source TTree
  - variable: RooRealVar in dataset rows defined by TTree.Draw expression
              in it's title.
  - weight: RooRealVar defining dataset weights
  - categories: RooCategory list included in dataset.
                Expression evaluating to index is defined by their titles.
  - cuts: List of strings defining cuts that extracted rows pass.
  - dataset: RooDataSet extracted after call to dataset.get()
  (- canvases: optional auxiliary TCanvas list used for testing)

Functions:
  - set: Set data values. Helper function of get.
  - get: Takes optional tree, variable, categories, cuts.
         Updates data with given args using set and extracts dataset from tree
         given configuration held in variable, categories and cuts.
         Updates dataset data and returns it.
  - plot: Plot the dataset on variable's frame.
  - main:
Takes a tree, a RooRealVar variable, a list of categories and a list of cuts.
Returns a RooDataSet extracted from the tree given the expressions in
variable and categories titles.
'''

import os
import sys
import ROOT
import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *

gROOT.LoadMacro( 'datasetUtilities.cc+' )

## Configuration
tree = esChains.getChains('v4')['data']
variable = RooRealVar( 's', '100*(1/kRatio-1)', 0, -50, 50, "%" )
weight = RooRealVar( 'w', '1', 0, 999 )

## Default/example categories
_r9 = RooCategory( 'r9', 'isHighR9(phoIsEB, phoR9)' )
_r9.defineType( 'High', 1 )
_r9.defineType( 'Low', 0 )

_subdet = RooCategory( 'subdet', 'phoIsEB' )
_subdet.defineType( 'Barrel' , 1 )
_subdet.defineType( 'Endcaps', 0 )

# categories = [ _r9, _subdet ]
categories = []

cuts = []

# cuts = [
#     '87.2 < mmgMass && mmgMass < 95.2',
# ]

## Data extracted from tree
dataset = RooDataSet()

#------------------------------------------------------------------------------
def set(**kwargs):
    global tree, variable, weight, cuts, categories, dataset
    for arg in 'tree variable weight cuts categories dataset'.split():
        if arg in kwargs.keys():
            setattr( sys.modules[__name__], arg, kwargs[arg] )
            del kwargs[arg]
    if kwargs.keys():
        raise RuntimeError, "Unknown argument(s): %s" % repr( kwargs.keys() )
## set

#------------------------------------------------------------------------------
def get(**kwargs):
    global tree, variable, weight, cuts, categories, dataset

    ## Initialize
    set(**kwargs)
    varSet = RooArgSet( variable, weight, *categories )
    dataset = RooDataSet( 'data', 'data', varSet, WeightVar( weight.GetName() ) )
    #dataset.setWeightVar( weight )
    #dataset = RooDataSet('data', 'data', varSet )

    ## Build list expressions for variables
    varExpressions = [ variable.GetTitle(), weight.GetTitle() ]

    for cat in categories:
        varExpressions.append( cat.GetTitle() )

    ## Auxiliary function to build the selection string
    andCuts = lambda(cuts): " & ".join( "(%s)" % cut for cut in cuts )
    joinExpressions = lambda(expressions): ":".join( expressions )

    ## Get the data from the tree
    tree.Draw( joinExpressions(varExpressions), andCuts(cuts), 'goff para' )

    ## Fill the dataset
    for i in range( tree.GetSelectedRows() ):
        variable.setVal( tree.GetV1()[i] )
        weight.setVal( tree.GetV2()[i] )
        for icat in range( len(categories) ):
            cat = categories[icat]
            x = tree.GetVal(icat+2)[i]
            cat.setIndex( int(x) )
        dataset.add( varSet, weight.getVal() )
    ## Close the file with source tree

    return dataset
## get

#------------------------------------------------------------------------------
def plot():
    frame = variable.frame()
    dataset.plotOn(frame)
    frame.Draw()
    return frame
# plot

#------------------------------------------------------------------------------
def main():
    'test the get function'
    global canvases
    canvases = []

    #gROOT.Set

    get()
    canvases.append( TCanvas('s', 's') )
    plot()

    get( variable = RooRealVar('k', 'kRatio', 0.5, 1.5) )
    canvases.append( TCanvas('k_noweights', 'k_noweights') )
    frame = plot()
    dataset.plotOn( frame, Cut('subdet==subdet::Barrel'), MarkerColor(kBlue),
                    LineColor(kBlue) )
    dataset.plotOn( frame, Cut('subdet==subdet::Endcaps'), MarkerColor(kRed),
                    LineColor(kRed) )
    frame.Draw()

    canvases.append( TCanvas('k_withweights', 'k_withweights') )
    frame = plot()
    dataset.plotOn( frame, Cut('subdet==subdet::Barrel'), MarkerColor(kBlue),
                    LineColor(kBlue), DataError(RooAbsData.SumW2) )
    dataset.plotOn( frame, Cut('subdet==subdet::Endcaps'), MarkerColor(kRed),
                    LineColor(kRed) )
    frame.Draw()

    get( variable = RooRealVar('logik', '-log(kRatio)', -0.5, 0.5) )
    canvases.append( TCanvas() )
    frame = plot()
    dataset.plotOn( frame, Cut('r9==r9::High'), MarkerColor(kBlue),
                    LineColor(kBlue) )
    dataset.plotOn( frame, Cut('r9==r9::Low'), MarkerColor(kRed),
                    LineColor(kRed) )
    frame.Draw()
## main

if __name__ == "__main__":
    main()
    import user
