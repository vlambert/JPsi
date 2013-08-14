"""Utility to extract RooDataSet from a TTree.

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

This module has several design flaws and should be rewritten along these lines:
    - Data and functions should be wrapped into a class.
    - import * should be avoided
    - Some sort of argument check should be implemented **kwargs is too generic.
"""

import os
import sys
import ROOT

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *

## Configuration
## tree = TTree()
## variable = RooRealVar( 'x', '0', 0, -10, 10)

#------------------------------------------------------------------------------
def init():
    '''
    Initializes global variables and sets them to their default values.
    '''
    global tree, variable, variables, weight, name, title, categories, cuts
    tree = None
    variable = None

    ## Default values
    variables = []
    weight = RooRealVar( 'w', '1', 1 )
    name, title = 'data', 'data'

    ## Default/example categories
    categories = []

    cuts = []
    
    global dataset
    dataset = RooDataSet()
## End of init_globals().
    

#------------------------------------------------------------------------------
def set(**kwargs):
    """set(tree, variable, variables, weight, cuts, categories, dataset,
    name, title)"""
    init()
    
    global tree, variable, weight, cuts, categories, dataset, name, title
    global variables
    

    ## require that tree and variable must be set
    if (not (tree or 'tree' in kwargs) or 
        (not (variable or 'variable' in kwargs) and not 'variables' in kwargs) or
        (not (variable or 'variable' in kwargs) and not kwargs['variables'])):
        raise RuntimeError, "Must provide tree and variable."

    for arg in ('tree variable weight cuts categories dataset name '
                'title variables').split():
        if arg in kwargs.keys():
            setattr( sys.modules[__name__], arg, kwargs[arg] )
            del kwargs[arg]
    if kwargs.keys():
        raise RuntimeError, "Unknown argument(s): %s" % repr( kwargs.keys() )

    if name != 'data' and title == 'data':
        title = name

    if variable and not variable in variables:
        variables.append(variable)
      
    if not 'variable' in kwargs:
        variable = variables[0]
## set

#------------------------------------------------------------------------------
def get(**kwargs):
    """RooDataSet get(tree, variable, variables, weight, cuts, categories,
    dataset, name, title)"""
    global tree, variable, weight, cuts, categories, dataset, name, title
    global variables

    ## Initialize
    set(**kwargs)
    # print '+++ DEBUG before varSet ctor:', str(variables + categories + [weight])
    varSet = RooArgSet(*(variables + categories + [weight]))
    # print '+++ DEBUG after varSet ctor: ', 
    varSet.Print()
    dataset = RooDataSet(name, title, varSet, WeightVar( weight.GetName() ) )
    #dataset.setWeightVar( weight )
    #dataset = RooDataSet('data', 'data', varSet )

    ## Build list expressions for variables
    varExpressions = [x.GetTitle() for x in variables + categories + [weight]]

    ## for cat in categories:
    ##     varExpressions.append( cat.GetTitle() )

    ## Auxiliary function to build the selection string
    andCuts = lambda(cuts): " & ".join( "(%s)" % cut for cut in cuts )
    joinExpressions = lambda(expressions): ":".join( expressions )

    ## Set the title for the dataset
    dataset.SetTitle( '%s for %s' % ( joinExpressions(varExpressions),
                                      andCuts(cuts)                    ) )
    ## Select only events within the range of variable.
    ## This is needed to exclude underflows and overflows.
    for x in variables:
        cuts.append('%f<%s & %s<%f' % (x.getMin(), x.GetTitle(),
                                       x.GetTitle(), x.getMax()))
    ## Get the data from the tree
    tree.Draw( joinExpressions(varExpressions), andCuts(cuts), 'goff para' )

    ## get a list of variables for fast adding
    row = dataset.get()
    rowVars = [row[x.GetName()] for x in variables + categories]
    
    ## Fill the dataset
    for i in range( tree.GetSelectedRows() ):
        for j, x in enumerate(rowVars):
            if x in categories:
                x.setIndex(int(tree.GetVal(j)[i]))
            else:
                x.setVal(tree.GetVal(j)[i])
        weight.setVal(tree.GetVal(len(rowVars))[i])
        dataset.addFast(row, weight.getVal())
    ## Close the file with source tree

    return dataset
## get

#------------------------------------------------------------------------------
def plot(variable):
    frame = variable.frame()
    dataset.plotOn(frame)
    frame.Draw()
    return frame
# plot

#------------------------------------------------------------------------------
def main():
    'test the get function'
    import JPsi.MuMu.common.energyScaleChains as chains
    trees = chains.getChains('v11')

    global canvases
    canvases = []

    #gROOT.Set

    w = RooWorkspace('w', 'w')
    #s = w.factory('s[-5,5]')
    kRatio = w.factory('kRatio[-20,20]')
    mmgMass = w.factory('mmgMass[40,140]')
    mmMass = w.factory('mmMass[10,140]')
    # s.SetTitle('1/kRatio - 1')
    get(tree=trees['z'], variables=[kRatio, mmgMass, mmMass])
    canvases.append( TCanvas('kRatio', 'kRatio') )
    plot(kRatio)
    
    canvases.append( TCanvas('mmgMass', 'mmgMass') )
    plot(mmgMass)

    canvases.append( TCanvas('mmMass', 'mmMass') )
    plot(mmMass)

    ## get( variable = RooRealVar('k', 'kRatio', 0.5, 1.5) )
    ## canvases.append( TCanvas('k_noweights', 'k_noweights') )
    ## frame = plot()
    ## dataset.plotOn( frame, Cut('subdet==subdet::Barrel'), MarkerColor(kBlue),
    ##                 LineColor(kBlue) )
    ## dataset.plotOn( frame, Cut('subdet==subdet::Endcaps'), MarkerColor(kRed),
    ##                 LineColor(kRed) )
    ## frame.Draw()

    ## canvases.append( TCanvas('k_withweights', 'k_withweights') )
    ## frame = plot()
    ## dataset.plotOn( frame, Cut('subdet==subdet::Barrel'), MarkerColor(kBlue),
    ##                 LineColor(kBlue), DataError(RooAbsData.SumW2) )
    ## dataset.plotOn( frame, Cut('subdet==subdet::Endcaps'), MarkerColor(kRed),
    ##                 LineColor(kRed) )
    ## frame.Draw()

    ## get( variable = RooRealVar('logik', '-log(kRatio)', -0.5, 0.5) )
    ## canvases.append( TCanvas() )
    ## frame = plot()
    ## dataset.plotOn( frame, Cut('r9==r9::High'), MarkerColor(kBlue),
    ##                 LineColor(kBlue) )
    ## dataset.plotOn( frame, Cut('r9==r9::Low'), MarkerColor(kRed),
    ##                 LineColor(kRed) )
    ## frame.Draw()
## main

if __name__ == "__main__":
    main()
    import user
