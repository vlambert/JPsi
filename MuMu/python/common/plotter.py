'''
Facilitate making ROOT plots.
'''
import copy
import ROOT

from JPsi.MuMu.common.legend import Legend
from JPsi.MuMu.common.latex import Latex

##-----------------------------------------------------------------------------
class Plotter:
    def __init__(self, trees, expression, **kwargs):
        ## Init mandatory configuration data
        self.trees = trees
        n = len(trees)
        self.expression = expression
        ## Init other configuration data with defaults
        self.name = 'h'
        if 'cuts' in kwargs:
            self.title = ' & '.join(kwargs['cuts'])
        else:
            self.title = ''
        self.binning = ''
        self.cuts = []
        self.xtitle = expression
        self.ytitle = 'a.u.'
        self.normalize_to_unit_area = True
        self.labels = []
        ## By default, use palette colors
        self.colors = [ROOT.TColor.GetColorPalette(5*i) for i in range(n)]
        self.ltitles = [''] * n
        self.drawopts = [''] * n
        self.markerstyles = [range(20, 20+n)]
        self.legendkwargs = dict(position = (0.7, 0.95, 0.95, 0.8))
        self.labels_layout = (0.2, 0.9)
        ## Apply optional configuration from ctor kwargs
        for attr, val in kwargs.items():
            setattr(self, attr, val)
    ## end of __init__

    def draw(self):
        ## Make auxiliary lists of indices and hitogram names
        indices = range(len(self.trees))
        hnames = ['h_%s_%d' % (self.name, i) for i in indices]
        ## Make the histograms
        for t, hname in zip(self.trees, hnames):
            expr = '%s>>%s' % (self.expression, hname)
            sel = '&'.join(['(%s)' % c for c in self.cuts if c.strip()])
            if self.binning:
                expr += '(%s)' % self.binning
                t.Draw(expr, sel, 'goff')
            else:
                ## No binning is specified.
                ## Take extra care to use the same binning for all.
                ## Use automatic binning fro the first tree and apply it
                ## to all others.
                if id(t) == id(self.trees[0]):
                    ## This is the first tree, use auto-binning.
                    t.Draw(expr, sel)
                else:
                    ## This is no the first tree, use same binning as
                    ## for the first one
                    t.Draw(expr, sel, 'same')

        ## Retrieve the histograms in put them in a list
        self.histos = [ROOT.gDirectory.Get(hn) for hn in hnames]
        ## Customize histos
        for h, c, ms in zip(self.histos, self.colors, self.markerstyles):
            h.Sumw2()
            if self.normalize_to_unit_area:
                nbins = h.GetXaxis().GetNbins()
                area = h.GetBinWidth(1) * h.Integral(1, nbins)
                h.Scale(1./area)
            h.GetXaxis().SetTitle(self.xtitle)
            h.GetYaxis().SetTitle(self.ytitle)
            h.SetTitle(self.title)
            h.SetStats(0)
            h.SetLineColor(c)
            h.SetMarkerColor(c)
            h.SetMarkerStyle(ms)
        ## Find the histogram with greatest y range
        maxima = [h.GetMaximum() for h in self.histos]
        highest = max(maxima)
        imax = maxima.index(highest)
        ## Draw the "highest" histo first to guarantee nice the y-range.
        self.histos[imax].Draw(self.drawopts[imax])
        ## Draw all histograms
        for h, opt in zip(self.histos, self.drawopts):
            h.Draw(opt + 'same')
        ## Add the legend
        legend = Legend(self.histos, self.ltitles, **self.legendkwargs)
        legend.draw()
        ## Add latex labels
        latex = Latex(self.labels, self.labels_layout)
        latex.draw()

    def clone(self, **kwargs):
        'Returns a deep copy of itself upating attributes to optional kwargs.'
        new = copy.deepcopy(self)
        for attr, val in kwargs.items():
            setattr(new, attr, val)
        return new
    ## end of clone
## end of Plotter
