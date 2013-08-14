#------------------------------------------------------------------------------
class BinEdges():
    'Takes a list of bin boundaries and iterates over bin low and high edges.'

    def __init__(self, binning):
        self.binning = binning
        self.bin = 0

    def __iter__(self):
        return self

    def next(self):
        self.bin += 1
        try:
            return (self.binning[self.bin-1],
                    self.binning[self.bin])
        except IndexError:
            raise StopIteration
## end of BinEdges
