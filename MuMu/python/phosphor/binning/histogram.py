import array
import ROOT
import JPsi.MuMu.common.canvases as canvases

##=============================================================================
class Histogram(ROOT.TH1F):
    '''
    Manages and filling a single histogram
    '''
    ##_________________________________________________________________________
    def __init__(self, name, title, nbins, xstart, xstop, quantity, weight=''):
        '''
        Initializes the class.
        '''
        ROOT.TH1F.__init__(self, name, title, nbins, xstart, xstop)
        self.quantity = quantity
        self.weight = weight
     ## End of Histogram.__init__(...)
    
    ##_________________________________________________________________________
    def clone(self, newname=''):
        if not newname:
            newname = self.GetName()
        newhist =  Histogram(
            newname, 
            self.GetTitle(),
            self.GetXaxis().GetNbins(),
            self.GetXaxis().GetXmin(),
            self.GetXaxis().GetXmax(),
            self.quantity,
            self.weight
            )
        self.Copy(newhist)
        newhist.SetName(newname)
        
        return newhist
    ## End of Histogram.clone()
    
    ##_________________________________________________________________________
    def __deepcopy__(self, memo):
        return self.clone()
    ## End of Histogram.__deepcopy__(...)
    
    ##_________________________________________________________________________
    def fill_with(self, tree, max_events=int(1e10)):
        '''
        Fills the histogram with the data in the tree.
        '''
        expression = '%s >> %s' % (self.quantity, self.GetName())
        tree.Draw(expression, self.weight, 'goff', max_events)
        
    ## End of Histogram.fill_with(...)

    ##_________________________________________________________________________
    def make_plot(self):
        '''
        Creates a canvas and draws the histogram on it.
        '''
        canvases.next(self.GetName())
        self.DrawCopy()
        canvases.update()
    ## End of Histogram.make_plot(..)

    ##_________________________________________________________________________
    def get_quantiles(self, granularity=100):
        '''
        Creates a graphs with a number of equidistant quantiles equal to 
        granularity.  The distance between quantiles is 1/granularity.
        '''
        if granularity <= 0:
            raise RuntimeError, 'granularity must be positive!'
        ## We want to include the 0- and 1-quantile.
        qn = granularity + 1
        probabilities = [float(i) / (qn - 1) for i in range(qn)]
        qx = array.array('d', probabilities)
        qy = array.array('d', [0.] * qn)
        self.GetQuantiles(qn, qy, qx)
        ## Transform the fraction of events to percentage.
        for i in range(qn):
            qx[i] = 100. * qx[i]
        self.quantiles = ROOT.TGraph(qn, qx, qy)
    ## End of Histogram.make_plot(..)
    
    ##_________________________________________________________________________
    def plot_quantiles(self, granularity=100):
        '''
        Plots the quantile curve.
        '''
        ## Calculate the quantiles if need be
        if not hasattr(self, 'quantiles'):
            self.get_quantiles(granularity)
        canvas = canvases.next(self.GetName() + '_quant')
        canvas.SetGrid()
        self.quantiles.Draw('al')
        ## Decorate the axis
        self.quantiles.GetXaxis().SetTitle(
            'Fraction of %s (%%)' % self.GetYaxis().GetTitle()
            )
        self.quantiles.GetYaxis().SetTitle(self.GetXaxis().GetTitle())
        self.quantiles.GetYaxis().SetRangeUser(10., self.quantiles.Eval(95.))
        canvases.update()
    ## End of Histogram.plot_quantiles(..)
    
    ##_________________________________________________________________________
    def get_bin_edges(self, nbins=5):
        edges = []
        for x in [i * 100. / nbins for i in range(nbins + 1)]:
            edges.append(self.quantiles.Eval(x))
        return edges
    ## End of Histogram.get_bin_edges(..)

## End of class Histogram

