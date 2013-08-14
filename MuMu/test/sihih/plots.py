from ROOT import *

class Var(RooRealVar):
    """store histogram data related to a variable,
    title holds the selection."""
    def __init__(self, name, title, minValue, maxValue, unit, numBins=0):
        RooRealVar.__init__(self, name, title, minValue, maxValue, unit)
        if numBins > 0:
            self.setBins(numBins)

histos = {}
histos["mass"] = Var("mass", "mass", 30, 130, "GeV", 100)
