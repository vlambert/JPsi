'''
Facilitate adding latex labels to ROOT plots.
Usage:
from JPsi.MuMu.common.latex import Latex
labels = get_list_of_labels_from_somewhere()
latexlabels = Latex(labels [, position = (x1, y1))
latexlabels.draw()
'''

import ROOT

class Latex(ROOT.TLatex):
    def __init__(self, labels, position = (0.2, 0.9), **kwargs):
        '__init__(self, labels, position = (0.2, 0.9), **kwargs)'
        ROOT.TLatex.__init__(self)
        ## Remove empty labels
        while '' in labels:
            labels.remove('')
        ## Init data
        self.labels = labels
        self.position = position
        self.textsize = 18
        self.rowheight = 0.055
        self.primitives = []
        self.color = ROOT.kBlack
        self.textfont = self.GetTextFont()
        for arg, val in kwargs.items():
            setattr(self, arg, val)

        ## Customize behavior
        self.SetNDC()
        ## Font size in pixels
        self.SetTextFont(10*(self.textfont/10) + 3)
        self.SetTextSize(self.textsize)
        self.SetTextColor(self.color)
    ## end of __init__

    def draw(self):
        'Draw all labels appending them to the list of primitives.'
        x1, y1 = self.position
        for i, l in enumerate(self.labels):
            self.primitives.append(
                self.DrawLatex(x1, y1 - i * self.rowheight, l)
            )
    ## end of draw
## end of Latex
