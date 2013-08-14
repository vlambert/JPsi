import os
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *
from JPsi.MuMu.common.plotData import PlotData

class ScaleFitterGauss(PlotData):
    '''Fits the Crystal Ball line shape to s = Ereco / Ekin - 1'''
    def __init__(self, name, title, source, expression, cuts, labels):
        PlotData.__init__(self, name, title, source, expression, cuts, labels)
        self.xTitle = 's_{true} = E_{RECO}/E_{GEN} - 1'
        self.nBins = 40
        self.xRange = (-20, 30)
        self.fitRange = (-20, 30)
    ## <-- __init__

    def getData(self, workspace):
        ## Check if the workspace already has the data
        self.data = workspace.data( 'data_' + self.name )
        if self.data:
            ## Use the data from the workspace
            return

        ## Pull fitted variable x, its weight w, the model
        ## and its parameters from the workspace
        x = workspace.var('s')
        w = workspace.var('w')

        x.SetTitle( self.expression )
        self.data = dataset.get(
            tree = self.source,
            variable = x,
            weight = w,
            cuts = self.cuts + [
                '%s > %f' % (self.expression, self.xRange[0]),
                '%s < %f' % (self.expression, self.xRange[1]),
            ]
        )
        self.data.SetName( 'data_' + self.name )
        workspace.Import(self.data)
    ## <-- getData

    def fit(self, workspace, *args):
        ## Pull fitted variable x, its weight w, the model
        ## and its parameters from the workspace
        x = workspace.var('s')
        w = workspace.var('w')
        model = workspace.pdf('model')
        parameters = workspace.set('parameters')

        ## Initialize latex label
        latexLabel = TLatex()
        latexLabel.SetNDC()
        latexLabel.SetTextSize(0.045)

        if not hasattr(self, 'data'):
            self.getData(workspace)

        if self.data.GetName() != self.name:
            self.getData(workspace)

        x.setRange( 'fit_' + self.name, *self.fitRange )

        ## Fit data
        self.fitResult = model.fitTo(
            self.data, Save(), SumW2Error(kTRUE), PrintLevel(-1),
            Range('fit_' + self.name), *args
        )
        workspace.saveSnapshot( self.name, parameters, True )

        ## Make a frame
        x.SetTitle(self.xTitle)
        x.setBins(self.nBins)
        frame = x.frame( Range( *self.xRange ) )

        ## Add the data and model to the frame
        self.data.SetTitle( self.title )
        self.data.plotOn( frame )
        model.plotOn( frame, Range('fit_' + self.name) )
        model.paramOn( frame,
                       Format('NEU', AutoPrecision(2) ),
                       Parameters( parameters ),
                       Layout(.57, 0.92, 0.92) )

        ## Get a canvas
        self.canvas = gROOT.GetListOfCanvases().FindObject( self.name )
        if not self.canvas:
            ## Make the canvas
            self.canvas = TCanvas( self.name, self.title )
            i = len( gROOT.GetListOfCanvases() )
            self.canvas.SetWindowPosition( 20*i, 20*i )

        ## Customize
        frame.SetTitle('')

        ## Draw the frame
        frame.Draw()

        ## Add labels
        for i in range( len( self.labels ) ):
            latexLabel.DrawLatex( 0.59, 0.6 - i * 0.055, self.labels[i] )

        ## Save the plot
        self.canvas.Print( 'sFit_' + self.name + '.png' )
    ## <-- fit
## <-- ScaleFitter

if __name__ == "__main__": import user
