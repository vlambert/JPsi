'''
Facilitates the plotting of ynames versus the the fit range iteration.
    Usage: python -i plotScaleVsFitRangeIter.py
'''
from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *

gSystem.Load('libJPsiMuMu')
from ROOT import RooCruijff
import math

class FitResultPlotter():
    def __init__(self, sources, getters, xtitle='x', ytitle='y', title='', 
                 **kwargs):
        ## Initialize data
        ## List of 3-tuples (filename, workspace name, parameter snapshot)
        self.sources = sources

        ## List of functions acting on workspace returning x, y, ex, ey
        self.getters = getters

        ##
        self.xtitle = xtitle
        self.ytitle = ytitle
        self.title = title

        self.labels = []
        self.graphs = []
        ## Used for legends when plotting multiple graphs
        self.titles = []
        ## Line and marker colors for multiple graphs
        self.colors = [ROOT.kBlue, ROOT.kRed, ROOT.kBlack, ROOT.kGreen]
        ## Marker styles for multiple graphs
        self.styles = range(20,27)

        self.logy = False
        self.yasymmerrors = False
        self.xasymmerrors = False

        for name, value in kwargs.items():
            setattr(self, name, value)

# #------------------------------------------------------------------------------
# def init():
#     '''Initialize private data members.'''
#     global _file, _filename, _workspace, _wsname, xname, _xvar, yname, _yvar
#
#     ## Check if we need to update the file
#     if not _file or _file.GetName() != _filename:
#         _file = ROOT.TFile(_filename)
#         _workspace = _file.Get(_wsname)
#         if xname:
#             _xvar = _workspace.var(xname)
#         if yname:
#             _yvar = _workspace.var(yname)
#     ## Do we need to update the workspace?
#     elif not _workspace or _workspace.GetName() != _wsname:
#         _workspace = _file.Get(_wsname)
#         if xname:
#             _xvar = _workspace.var(xname)
#         if yname:
#             _yvar = _workspace.var(yname)
#     ## Do we need to update the x and y variables?
#     else:
#         if xname and (not _xvar or _xvar.GetName() != xname):
#             _xvar = _workspace.var(xname)
#         if yname and (not _yvar or _yvar.GetName() != yname):
#             _yvar = _workspace.var(yname)
## end of init()

    #--------------------------------------------------------------------------
    def getdata(self, sources=None, getters=None):
        if not sources:
            sources = self.sources
        if not getters:
            getters = self.getters
        data = []
        for fname, wsname, snapshot in sources:
            if 'file' in vars() and file.GetName() == fname:
                pass
            else:
                file = ROOT.TFile(fname)
                wspace = None

            if 'wspace' in vars() and wspace and wspace.GetName() == wsname:
                pass
            else:
                wspace = file.Get(wsname)

            if snapshot:
                wspace.loadSnapshot(snapshot)

            x = []
            for f in getters:
                x.append(f(wspace))

            data.append(x)
        if self.xasymmerrors == True:
            if self.yasymmerrors == True:
                self.x, self.y, self.exl, self.exh, self.eyl, self.eyh = zip(*data)
            else:
                self.x, self.y, self.exl, self.exh, self.ey = zip(*data)
        else:
            if self.yasymmerrors == True:
                self.x, self.y, self.ex, self.eyl, self.eyh = zip(*data)
            else:
                self.x, self.y, self.ex, self.ey = zip(*data)
        
        return zip(*data)
    ## end of getData

    #--------------------------------------------------------------------------
    def makegraph(self):
        '''Makes a graph using the current workspace and yname.'''
        if self.xasymmerrors == True:
            if self.yasymmerrors == True:
                x, exl, exh, y, eyl, eyh = (
                    array('d', self.x), array('d', self.exl), array('d', self.exh),
                    array('d', self.y), array('d', self.eyl), array('d', self.eyh),
                    )
            else:
                x, exl, exh, y, eyl, eyh = (
                    array('d', self.x), array('d', self.exl), array('d', self.exh),
                    array('d', self.y), array('d', self.ey ), array('d', self.ey ),
                    )
            self.graph = TGraphAsymmErrors(len(x), x, y, exl, exh, eyl, eyh)
        else:
            if self.yasymmerrors == True:
                x, exl, exh, y, eyl, eyh = (
                    array('d', self.x), array('d', self.ex ), array('d', self.ex ),
                    array('d', self.y), array('d', self.eyl), array('d', self.eyh),
                    )
                self.graph = TGraphAsymmErrors(len(x), x, y, exl, exh, eyl, eyh)
            else:
                x, ex = array('d', self.x), array('d', self.ex)
                y, ey = array('d', self.y), array('d', self.ey)
                self.graph = TGraphErrors(len(x), x, y, ex, ey)
        if self.title:
            self.graph.SetTitle(self.title)
        self.titles.append(self.title)
        self.graphs.append(self.graph)
        return self.graph
    ## end of makeGraph()

    #--------------------------------------------------------------------------
    def plot(self):
        '''Plots the current graph with appropriate ranges and labels.'''

        graph = self.graph
        n = graph.GetN()
        
        if self.xasymmerrors == True or self.yasymmerrors == True:
            xmin = min([graph.GetX()[i] - graph.GetEXlow()[i] 
                        for i in range(n)])
            xmax = max([graph.GetX()[i] + graph.GetEXhigh()[i] 
                        for i in range(n)])

            ymin = min([graph.GetY()[i] - graph.GetEYlow()[i] 
                        for i in range(n)])
            ymax = max([graph.GetY()[i] + graph.GetEYhigh()[i] 
                        for i in range(n)])
        else:
            xmin = min([graph.GetX()[i] - graph.GetEX()[i] for i in range(n)])
            xmax = max([graph.GetX()[i] + graph.GetEX()[i] for i in range(n)])

            ymin = min([graph.GetY()[i] - graph.GetEY()[i] for i in range(n)])
            ymax = max([graph.GetY()[i] + graph.GetEY()[i] for i in range(n)])


        dx = xmax - xmin
        dy = ymax - ymin

        graph.SetTitle('%s;%s;%s' % (self.title, self.xtitle, self.ytitle))
        graph.GetXaxis().SetLimits(xmin - 0.1 * dx, xmax + 0.1 * dx)
        graph.GetHistogram().SetMinimum(ymin - 0.1 * dy)
        graph.GetHistogram().SetMaximum(ymax + 0.1 * dy)
        graph.Draw("ap")

    ## end of plot()


    #--------------------------------------------------------------------------
    def get_auto_range(self, mode, logy=False):
        '''
        Get the automatic range for all graphs.  Works for both x- and
        y-axis depending on the value of mode = "x" or "y".
        '''
        if not mode in 'x y'.split():
            raise ValueError('mode = %s' % mode)

        ## Calculate the range of the y axis depending on the logy flag.
        ## Add a 10% margin on top of the (min, max) range.
        if logy:
            auto_yrange = lambda ymin, ymax: (ymin / pow(ymax / ymin, 0.1),
                                              ymax * pow(ymax / ymin, 0.1))
        else:        
            auto_yrange = lambda ymin, ymax: (ymin - 0.1 * (ymax - ymin),
                                              ymax + 0.1 * (ymax - ymin))
            
        ## Find the axis ranges
        xlo, xhi, ylo, yhi = [], [], [], []
        for graph in self.graphs:
            n = graph.GetN()
            
            if self.xasymmerrors == True or self.yasymmerrors == True:
                xlo.extend([graph.GetX()[i] - graph.GetEXlow()[i] 
                            for i in range(n)])
                xhi.extend([graph.GetX()[i] + graph.GetEXhigh()[i] 
                            for i in range(n)])

                ylo.extend([graph.GetY()[i] - graph.GetEYlow()[i] 
                            for i in range(n)])
                yhi.extend([graph.GetY()[i] + graph.GetEYhigh()[i] 
                            for i in range(n)])
            else:
                xlo.extend([graph.GetX()[i] - graph.GetEX()[i] 
                            for i in range(n)])
                xhi.extend([graph.GetX()[i] + graph.GetEX()[i] 
                            for i in range(n)])

                ylo.extend([graph.GetY()[i] - graph.GetEY()[i] 
                            for i in range(n)])
                yhi.extend([graph.GetY()[i] + graph.GetEY()[i] 
                            for i in range(n)])
              

        if logy:
            ## Only keep positive y values.
            ytoremove = [y for y in ylo if y <= 0.]
            for y in ytoremove:
                ylo.remove(y)
            ytoremove = [y for y in yhi if y <= 0.]
            for y in ytoremove:
                yhi.remove(y)

        ## Check if all lists of low and high x- and y-values are not empty.
        if not (xlo and xhi and ylo and yhi):
            raise RuntimeError, 'Cannot estimate axis ranges!'
        
        xmin, xmax = min(xlo), max(xhi)
        ymin, ymax = min(ylo), max(yhi)

        # dy = ymax - ymin
        dx = xmax - xmin

        ## Add the margin to the y axis range
        ymin, ymax = auto_yrange(ymin, ymax)
        xmin, xmax = xmin - 0.1 * dx, xmax + 0.1 * dx
        
        if mode == 'x':
            return (xmin, xmax)
        else:
            return (ymin, ymax)

    ## end of get_auto_range(..)

    
    #--------------------------------------------------------------------------
    def plotall(self, logy = False, legend_position='default',
                xrange='auto', yrange='auto', **kwargs):
        '''
        Plots the current graphs with appropriate ranges and labels. Input
        parameters:
            logy: Set y-axis to log scale if True
            legend_position: One of 'default', 'topright', tuple(x1, y1, x2, y2)
            xrange: Either 'auto' or a 2-tuple specifying the range.
            yrange: Either 'auto or a 2-tuple specifying the range.
        '''
        ## Use optional arguments to update instance data
        for name, value in kwargs.items():
            setattr(self, name, value)

        ## Check if legend_position has a sane value
        if (not legend_position in 'default topright'.split() and
            not (type(legend_position) == tuple and 
                 len(legend_position) == 4)):
            raise ValueError('legend_positon = %s' % legend_position) 

        ## Get the axis ranges.
        if xrange == 'auto':
            (xmin, xmax) = self.get_auto_range('x', logy)
        else:
            (xmin, xmax) = xrange
            
        if yrange == 'auto':
            (ymin, ymax) = self.get_auto_range('y', logy)
        else:
            (ymin, ymax) = yrange  
            
        graph = self.graphs[0]
        graph.SetTitle('%s;%s;%s' % (self.title, self.xtitle, self.ytitle))
        graph.GetXaxis().SetLimits(xmin, xmax)
        graph.GetHistogram().SetMinimum(ymin)
        graph.GetHistogram().SetMaximum(ymax)

        ## Draw the graphs
        for i, graph in enumerate(self.graphs):
            ## Cycle through colors and styles in case there are many graphs
            color = self.colors[i % len(self.colors)]
            style = self.styles[i % len(self.styles)]

            graph.SetLineColor(color)
            graph.SetMarkerColor(color)
            graph.SetMarkerStyle(style)

            if i==0:
                graph.Draw("ap")
            else:
                graph.Draw("p")

        ## Make the legend
        if type(legend_position) == tuple:
            legend_coordinates = legend_position
        else:
            legend_coordinates = (0.6, 0.3 + 0.075 * len(self.graphs),
                                  0.9, 0.3)

        if legend_position == 'topright':
            legend_coordinates = (0.68, 0.98, 0.98, 0.98 - 0.075 * len(self.graphs))
            
        self.legend = legend = TLegend(*legend_coordinates)
        legend.SetFillColor(0)
        legend.SetShadowColor(0)
        legend.SetBorderSize(0)

        ## Default titles if no titles are provided
        default_titles = ['graph %d' % (i+1) for i in range(len(self.graphs))]
        if not self.titles:
            self.titles = default_titles

        for graph, title, dtitle in zip(self.graphs,
                                        self.titles,
                                        default_titles):
            if not title:
                 title = dtitle
            legend.AddEntry(graph, title, "pl")

        legend.Draw()
        gPad.Update()
    ## end of plot()

    #--------------------------------------------------------------------------
    def plotlogy(self, graph):
        '''Plots the current graph with appropriate ranges and labels.'''

        graph = self.graph
        n = graph.GetN()
        ymin = min([graph.GetY()[i] - graph.GetEY()[i] for i in range(n)])
        ymax = max([graph.GetY()[i] + graph.GetEY()[i] for i in range(n)])
        dlogy = math.log(ymax) - math.log(ymin)

        graph.SetTitle(';%s;%s' % (xtitle, ytitle))
        graph.GetXaxis().SetLimits(-0.5, n + 0.5)
        graph.GetHistogram().SetMinimum(ymin / math.exp(0.1 * dlogy))
        graph.GetHistogram().SetMaximum(ymax * math.exp(0.1 * dlogy))
        graph.Draw("ap")
    ## end of plot()

    #--------------------------------------------------------------------------
    def dump(self):
        graph = self.graph
        print '         x         ex          y         ey'
        for i in range(graph.GetN()):
            print '%10.3g' % graph.GetX()[i],
            print '%10.3g' % graph.GetEX()[i],
            print '%10.3g' % graph.GetY()[i],
            print '%10.3g' % graph.GetEY()[i]
    ## end of dump()

    #------------------------------------------------------------------------------
    def histogramall(self,
                     name = 'h_yvalues',
                     title = ';graph y values; Entries',
                     nbins = 5, xlow = 0, xhigh = 1,
                     getter = lambda graph, i: graph.GetY()[i]):
        if '%s' in title:
            title = title % self.title
        hist = ROOT.TH1F(name, title, nbins, xlow, xhigh)
        for g in self.graphs:
            for i in range(g.GetN()):
                hist.Fill(getter(g, i))
        hist.SetStats(0)
        hist.SetMinimum()
        return hist
    ## end of histogramall                

    #------------------------------------------------------------------------------
    def main(self, **kwargs):
        '''Initializes private members and makes and plots the graph.
        Takes configuration from the current values of the customizeable data
        members.'''

        for name, value in kwargs.items():
            setattr(self, name, value)

        self.getdata()
        self.makegraph()

        if self.logy:
            self.plotlogy()
        else:
            self.plot()

        gPad.Update()
    ## end of main()
## end of class FitResultPlotter


if __name__ == '__main__':

    ## Defaults for customizeable data
    filenames = ('/home/veverka/cmssw/CMSSW_4_2_3/src/JPsi/MuMu/test/escale/'
                 '11-09-21/mc_mmMass85_EB_lowR9_PhoEt12-15.root',) * 8
    wsnames = ('ws1',) * 8

    snapshots = ['sFit_strue_mc_mmMass85_EB_lowR9_PhoEt12-15_gamma_iter%d' % i
                 for i in range(8)]

    frp = FitResultPlotter(
        sources = zip(filenames, wsnames, snapshots),
        getters = (
            lambda ws, i = iter(range(8)): i.next(),    #x
            lambda ws: ws.var('#Deltas').getVal(),        #y
            lambda ws, i = iter([0]*8): i.next(), #ex
            lambda ws: ws.var('#Deltas').getError(),      #ey
            ),
        xtitle = 'Fit Range Iteration',
        ytitle = '#Deltas (%)',
        )


    labels = ['Barrel', 'R_{9}^{#gamma} < 0.94',
              'E_{T}^{#gamma} #in [10,12] GeV', 'Powheg S4', 'CB']

    frp.main()
    import user
