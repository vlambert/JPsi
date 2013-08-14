'''Facilitates adding legends to ROOT canvases.
Usage:
from JPsi.MuMu.common.legend import Legend
histos = get_list_of_histograms_from_somewhere()
titles = get_histogram_titles_to_appear_on_legend()
legend = Legend(histos, titles [, position =(x1, y1, x2, y2)])
legend.Draw()
'''

import ROOT

class Legend(ROOT.TLegend):
    def __init__(self, histos, titles,
                 position = (0.7, 0.95, 0.95, 0.8), opt = 'pl',
                 optlist = None):
        ROOT.TLegend.__init__(self, *position)
        self.histos = histos
        self.titles = titles
        self.opt = opt
        if not optlist:
            optlist = [opt] * len(histos)
        self.optlist = optlist
        self.SetFillColor(0)
        self.SetShadowColor(0)
        self.SetBorderSize(0)
        for h, t, opt in zip(histos, titles, optlist):
            self.AddEntry(h, t, opt)
    ## end of __init__

    def draw(self):
        'Just for the heck of it! :-)'
        self.Draw()
    ## end of draw
## end of Legend

