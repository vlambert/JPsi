import copy

'''Holds data specifying a plot based on a TTree'''
## ----------------------------------------------------------------------------
class PlotData:
    def __init__( self, name, title, source, xExpression, cuts, labels,
                  **kwargs ):
        ## string used as a key in various dictionaries
        self.name = name
        ## string used in human-readable output
        self.title = title
        ## TLaltex string list that is included on the graphics
        self.labels = labels
        ## TTree providing source of data
        self.source = source
        ## TTree::Draw xExpression string of variable subject to fittin
        self.xExpression = xExpression
        ## TTree::Draw selection string applied to data source
        self.cuts = cuts
        self._configuration = ('name title labels source xExpression'.split() +
                               ['cuts'] + kwargs.keys())

        for arg, value in kwargs.items():
            setattr( self, arg, value )

    def clone(self, **kwargs):
        newPlot = copy.deepcopy(self)
        for argName, argValue in kwargs.items():
            setattr( newPlot, argName, argValue )
        return newPlot

    def pydump(self):
        lines = [self.__class__.__name__ + '(']
        for field in self._configuration:
            lines.append("    %s = %s," % (field, repr(getattr(self, field))))
        lines.append(')')
        return '\n'.join(lines)
## end of PlotData
