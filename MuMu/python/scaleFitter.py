import os
import math
import copy
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *
from JPsi.MuMu.common.plotData import PlotData
from JPsi.MuMu.common.padDivider import residPullDivide
from JPsi.MuMu.common.modalinterval import ModalInterval
from JPsi.MuMu.datadrivenbinning import DataDrivenBinning
from JPsi.MuMu.roochi2calculator import RooChi2Calculator

#------------------------------------------------------------------------------
class Def():
    """ScaleFitter definition that can act on an instance and modify it's
    name, title and labels to reflect a fit performed for events
    in a specific category.  This is a base class for other definitions
    implementing data source (real data/MC), fittig model and cuts."""
    def __init__(self, name, title, labels):
        self.name, self.title, self.labels = name, title, labels

    def __call__(self, fitter):
        if fitter.name:
            fitter.name += '_'
        fitter.name += self.name

        if fitter.title:
            fitter.title += ', '
        fitter.title += self.title

        fitter.labels += self.labels

    def __str__(self):
        args = []
        for attr in dir(self):
            if callable(getattr(self, attr)) or attr[0] == '_':
                continue
            value = getattr(self, attr)
            args.append(''.join([attr, '=', repr(value)]))
        args = ', '.join(args)
        return ''.join([self.__class__.__name__, '(', args, ')'])
## end of class Cut


#------------------------------------------------------------------------------
class Model(Def):
    """ScaleFitter model definition that can act on an instance and modify it's
    name, title, labels and fit model to reflect that the fit is performed
    using the specified model."""
    def __init__(self, name):
        if name == 'gauss':
            Def.__init__(self, name, 'Gauss', ['Gaussian Fit'])
            self.model = 'gauss'
        elif name == 'lognormal':
            Def.__init__(self, name, 'Lognormal', ['Lognormal Fit'])
            self.model = 'lognormal'
        elif name == 'bifurGauss':
            Def.__init__(self, name, 'Bifur.-Gauss', ['Bifur. Gaussian Fit'])
            self.model = 'bifurGauss'
        elif name == 'cbShape':
            Def.__init__(self, name, 'CB', ['Crystal Ball Fit'])
            self.model = 'cbShape'
        elif name == 'gamma':
            Def.__init__(self, name, 'Gamma', ['Gamma Fit'])
            self.model = 'gamma'
        elif name == 'cruijff':
            Def.__init__(self, name, 'Cruijff', ['Cruijff Fit'])
            self.model = 'cruijff'
        elif name == 'bifurGsh':
            Def.__init__(self, name, 'Bifur.-GSH', ['Bifur. GSH Fit'])
            self.model = 'bifurGsh'
        elif name == 'gsh':
            Def.__init__(self, name, 'GSH', ['GSH Fit'])
            self.model = 'gsh'
        elif name == 'bw':
            Def.__init__(self, name, 'Breit-Wigner', ['Breit-Wigner Fit'])
            self.model = 'bw'
        elif name == 'sumGaussGauss':
            Def.__init__(self, name, 'Gauss + Gauss', ['Gauss + Gauss Fit'])
            self.model = name        
        elif name == 'sumCruijffGauss':
            Def.__init__(self, name, 'Cruijff + Gauss', ['Cruijff + Gauss Fit'])
            self.model = name        
        elif name == 'sumBwGauss':
            Def.__init__(self, name, 'BW + Gauss', ['BW + Gauss Fit'])
            self.model = name        
        elif name == 'sumGauss3':
            Def.__init__(self, name, 'Sum of 3 Gaussians', ['#Sigma of 3 Gaussians'])
            self.model = name
        else:
            raise ValueError, 'model %s not supported!' % name

    def __call__(self, fitter):
        Def.__call__(self, fitter)
        fitter.pdf = self.model
## end of class Model

#------------------------------------------------------------------------------
class Source(Def):
    """ScaleFitter source definition that can act on an instance and modify it's
    name, title, labels and data source to reflect that the fit is performed
    using the specified data source."""
    def __init__(self, name, title, labels, source):
        Def.__init__(self, name, title, labels)
        self.source = source

    def __call__(self, fitter):
        Def.__call__(self, fitter)
        fitter.source = self.source
## end of class Source


#------------------------------------------------------------------------------
class Cut(Def):
    """ScaleFitter cut definition that can act on an instance and modify it's
    name, title, labels and cuts to reflect a fit performed for events
    satisfying the cut."""
    def __init__(self, name, title, labels, cuts):
        Def.__init__(self, name, title, labels)
        self.cuts = cuts

    def __call__(self, fitter):
        Def.__call__(self, fitter)
        fitter.cuts += self.cuts

#     def __str__(self):
#         args = ', '.join(repr(arg) for arg in [self.name, self.title,
#                                                self.labels, self.cuts,])
#         return ''.join([self.__class__.__name__, '(', args, ')'])
## end of class Cut


#------------------------------------------------------------------------------
class PhoEtBin(Cut):
    """Can act on a ScaleFitter object and modify it's name,
    title, labels and cuts to reflect a fit performed for photon within the
    given Et bin [low,high) GeV."""
    def __init__(self, low, high):
        bin_range = (low, high)
        self.bin_range = bin_range
        Cut.__init__(self,
            name = 'PhoEt%g-%g' % bin_range,
            title = 'photon Et in [%g, %g) GeV' % bin_range,
            labels = ['E_{T}^{#gamma} #in [%g, %g) GeV' % bin_range],
            cuts = ['%g <= phoPt' % low, 'phoPt < %g' % high],
        )

    def __str__(self):
        return self.__class__.__name__ + '(%g, %g)' % self.bin_range
## end of class PhoEtBin


#------------------------------------------------------------------------------
class DimuonMassMax(Cut):
    """Can act on a ScaleFitter object and modify it's name,
    title, labels and cuts to reflect a fit performed for dimuons below the
    given mass in GeV."""
    def __init__(self, max):
        self.max = max
        Cut.__init__(self,
            name = 'mmMass%g' % max,
            title = 'mmMass < %g GeV' % max,
            labels = ['m_{#mu^{+}#mu^{-}} < %g GeV' % max],
            cuts = ['mmMass <= %g' % max],
        )

    def __str__(self):
        return self.__class__.__name__ + '(%g)' % self.max
## end of class PhoEtBin


#------------------------------------------------------------------------------
class DimuonPlusDimuonGammaMassSumMax(Cut):
    """Can act on a ScaleFitter object and modify it's name,
    title, labels and cuts to reflect a fit performed for the sum of dimuon
    and gammadimuon masses below the given mass value in GeV.
    """
    def __init__(self, max):
        self.max = max
        Cut.__init__(self,
            name = 'mmPlusMmgMass%g' % max,
            title = 'mmMass + mmgMass < %g GeV' % max,
            labels = ['m_{#mu^{+}#mu^{-}} + m_{#mu^{+}#mu^{-}#gamma} < %g GeV' %
                      max],
            cuts = ['mmMass + mmgMass <= %g' % max],
        )

    def __str__(self):
        return self.__class__.__name__ + '(%g)' % self.max
## end of class DimuonPlusDimuonGammaMassSumMax


#------------------------------------------------------------------------------
class ICut():
    """Iterator over instances of Cut. The constructor arguments are
      * names - list of strings to form filenames
      * titles - list of strings for log files and ASCII reports
      * labels - list of lists of latex strings for canvases and latex reports
      * cuts - list of lists of TTree::Draw expression strings."""
    def __init__(self, names, titles, labels, cuts):
        self.name, self.title = iter(names), iter(titles)
        self.labels, self.cuts = iter(labels), iter(cuts)

    def __iter__(self):
        return self

    def next(self):
        return Cut(self.name.next(), self.title.next(),
                   self.labels.next(), self.cuts.next())
## end of ICut


class ScaleFitter(PlotData):
    """Fits the Crystal Ball line shape to s = Ereco / Ekin - 1"""
    #--------------------------------------------------------------------------
    def __init__( self, name, title, source, xExpression, cuts, labels,
                  **kwargs ):
        self.xName = 's'
        self.xTitle = 's = E_{RECO}/E_{KIN} - 1'
        self.nBins = 40
        self.nBinsZoom = 20
        self.xRange = (-30, 50)
        self.xRangeZoom = (-10, 10)
        self.xUnit = '%'
        self.fitRange = (-30, 30)
        self.massWindow = None
        self.massWindowScale = 2
        self.fitResults = []
        self.canvases = []
        self.pads = []
        self.pdf = 'model'
        self.chi2s = []
        self.definitions = []
        self.paramLayout = (.57, 0.92, 0.92)
        self.labelsLayout = (0.61, 0.6)
        self.canvasStyle = 'compact'

        ## Chi2 statistic follows the chi2 PDF (and one can trust the p-value
        ## from ROOT if int(f(x), x in bin_i) = nu_i > 5, see explanation
        ## near (33.34) on page 13 of the 2011 PDG Statistics Review
        ## http://pdg.lbl.gov/2011/reviews/rpp2011-rev-statistics.pdf
        ## Use bin content n_i >= 10 to be on the safe side (nu_i != n_i)
        self.binContentMin = 10
        self.binContentMax = 100
        self.doAutoBinning = False
        
        self.xRangeMode = 'SigmaLevel'
        self.xRangeSigmaLevel = 5
        self.xRangeFraction = 1.
        self.xRangeNumberOfEntries = 5000

        self.xRangeModeZoom = 'SigmaLevel'
        self.xRangeSigmaLevelZoom = 2
        self.xRangeFractionZoom = .9
        self.xRangeNumberOfEntries = 5000

        self.fitRangeMode = 'SigmaLevel'
        self.fitRangeSigmaLevel = 5
        self.fitRangeFraction = 1.
        self.fitRangeNumberOfEntries = 5000
        
        self.doAutoXRange = False
        self.doAutoXRangeZoom = False
        self.doAutoFitRange = False

        self.useCustomChi2Calculator = False

        self.pullRangeMode = 'fitRange'
        self.residRangeMode = 'fitRange'
        
        PlotData.__init__( self, name, title, source, xExpression, cuts,
                           labels, **kwargs )

        ## Initialize latex label
        latexLabel = TLatex()
        latexLabel.SetNDC()
        ## Font size in pixels
        latexLabel.SetTextFont( 10*(latexLabel.GetTextFont()/10) + 3)
        latexLabel.SetTextSize(18)
        self.latex = latexLabel

    ## <-- __init__ -----------------------------------------------------------

    #--------------------------------------------------------------------------
    def applyDefinitions(self, definitions=[]):
        """Applies definitions."""
        self.definitions.extend(definitions)
        ## The definitions are applied in the same order as they appear in the
        ## list.  They will be `pop'-ped from the tail of the reversed list.
        self.definitions.reverse()
        ## Unfinite loop
        while True:
            try:
                ## Get the next definition and remove it from the list.
                definition = self.definitions.pop()
                ## Apply the definition.
                definition(self)
            except IndexError:
                ## The list of definitions is empty.
                break
        ## end of unfinite while loop
        return self
    ## end of applyDefinitions

    #--------------------------------------------------------------------------
    def getMassCut(self, workspace):
        """Uses the mmg invariant mass distribution to center the invariant
        mass window and adust its size. Appends the invariant mass cut to
        the list of cuts."""

        ## Check if mass window is explicitly given
        if self.massWindow:
            ## Append the given mass window to the list of cuts
            mean = 0.5 * (self.massWindow[0] + self.massWindow[1])
            width = 0.5 * (self.massWindow[1] - self.massWindow[0])
            self.cuts.append( 'abs(mmgMass-%.2f) < %.2f' % (mean, width) )
            ## Return without making the fit
            return

        mean = 91.2
        width = 4.
        mmgMass = workspace.var('mmgMass')
        mmgMass.SetTitle('mmgMass')
        data = dataset.get(
            tree = self.source,
            variable = mmgMass,
            weight = workspace.var('w'),
            cuts = self.cuts
        )
        m3Model = workspace.pdf('m3Model')
        m3Model.fitTo(data, SumW2Error(kTRUE))
        workspace.saveSnapshot( 'm3_' + self.name,
                                workspace.set('m3Model_params') )
        canvas = TCanvas( 'm3_' + self.name, 'Mass fit, ' + self.title )
        self.canvases.append( canvas )
        i = len(gROOT.GetListOfCanvases())
        canvas.SetWindowPosition(20*(i%50), 20*(i%5))
        canvas.SetGrid()

        ## Extract the approximate mass cut and append it to the current cuts
        center = workspace.var('mZ').getVal() + workspace.var('#Deltam').getVal()
        sigmaCB = workspace.var('#sigmaCB').getVal()
        sigmaBW = workspace.var('#GammaZ').getVal()
        oplus = lambda x, y: math.sqrt(x*x + y*y)
        width = self.massWindowScale * oplus(sigmaCB, sigmaBW)

        ## Tune the position of the mass window by sample the signal pdf
        nsamples = 1000
        xlo, dx = center - width, 2*width/(nsamples-1)
        signal = workspace.pdf('signal')
        xmax, ymax = -1, -1
        for x in [xlo + i*dx for i in range(nsamples)]:
            mmgMass.setVal(x)
            y = signal.getVal()
            if y > ymax:
                xmax, ymax = x, y
        self.cuts.append( 'abs(mmgMass-%.2f) < %.2f' % (xmax, width) )
        self.massWindow = (xmax - width, xmax + width)

        ## Plot the fit result
        mmgMass.SetTitle('m_{#mu#mu#gamma}')
        plot = mmgMass.frame(Range(60,120))
        plot.SetTitle('')
        data.plotOn(plot)
        m3Model.paramOn( plot,
                         Format('NEU', AutoPrecision(2) ),
                         Layout(.65, 0.92, 0.92) )
        m3Model.plotOn(plot)
        plot.Draw()

        ## Initialize latex label
        latexLabel = TLatex()
        latexLabel.SetNDC()
        ## Font size in pixels
        latexLabel.SetTextFont(10*(latexLabel.GetTextFont()/10) + 3)
        latexLabel.SetTextSize(18)

        ## Add mass window label
        latexLabel.DrawLatex( 0.65, 0.6 - 5 * 0.055,
                              '%.2f #pm %.2f GeV' % (xmax, width) )

        ## Plot the mass window
        canvas.Update()
        mmgMass.setVal(center)
        xlo = xmax - width
        xhi = xmax + width
        ylo = 0.
        yhi = 0.8 * canvas.GetY2()
        line1 = ROOT.TLine(xlo, ylo, xlo, yhi)
        line2 = ROOT.TLine(xhi, ylo, xhi, yhi)
        arrow1 = ROOT.TArrow(xlo, 0.5*yhi, xhi, 0.5*yhi, 0.01, '<>')
        for piece in [line1, line2, arrow1]:
            try:
                self.primitives.append(piece)
            except AttributeError:
                self.primitives = []
                self.primitives.append(piece)
            piece.Draw()

        ## Save the plot
        if hasattr(self, 'graphicsExtensions'):
            for ext in self.graphicsExtensions:
                canvas.Print( 'massFit_' + self.name + '.' + ext )
    ## <-- getMassCut ---------------------------------------------------------

    #--------------------------------------------------------------------------
    def getData(self, workspace):
        """Gets the data and imports it in the workspace."""
        ## Pull fitted variable x, its weight w, the model
        ## and its parameters from the workspace
        self.x = workspace.var(self.xName)
        self.x.Print()
        self.w = workspace.var('w')

        self.x.SetTitle( self.xExpression )
        self.data = dataset.get(
            tree = self.source,
            variable = self.x,
            weight = self.w,
            cuts = self.cuts
        )
        self.data.SetName( 'data_' + self.name )
        self.data.SetTitle( self.title )
        workspace.Import(self.data)
    ## <-- getData ------------------------------------------------------------

    #--------------------------------------------------------------------------
    def fitToData(self, workspace, saveName = ''):
        self._updateRanges()
        # print "+++ Entering scaleFitter.fitToData(..)"
        self.model = workspace.pdf(self.pdf).Clone( 'model_' + self.name )
        workspace.Import( self.model )
        self.parameters = workspace.set(self.pdf + '_params')
        # print "+++ Parameters:"
        #self.parameters.Print()
        ## Fit data
#         self.x.setRange( 'fitRange_' + self.name, *self.fitRange )
        self.data.SetName( self.name )
        #print "+++ fitting"
        self.fitResults.append(
            self.model.fitTo( self.data, Save(),
                              Range(*self.fitRange),
#                               Range('fitRange_' + self.name),
                              SumW2Error(kTRUE),
                              PrintLevel(-1) )
        )

        ## Get the number of events in the fit range from the dataset
        expr = self.x.GetName()
        sel = "%f <= %s & %s < %f" % (self.fitRange[0], expr,
                                      expr, self.fitRange[1])
        self.fitRangeNumEvents = self.data.tree().Draw(expr, sel, 'goff')

        if saveName == '':
            workspace.saveSnapshot('sFit_' + self.name, self.parameters, True)
        else:
            workspace.saveSnapshot( saveName, self.parameters, True )
    ## <-- fitToData ----------------------------------------------------------

    #--------------------------------------------------------------------------
    def _customizeAxis(self, axis, labelOffset=0.005, titleOffset=1):
        ## Switch to fixed pixel size fonts
        precision = axis.GetLabelFont() % 10
        axis.SetLabelFont( axis.GetLabelFont() - precision + 3 )
        axis.SetLabelSize(18)
        precision = axis.GetTitleFont() % 10
        axis.SetTitleFont( axis.GetTitleFont() - precision + 3)
        axis.SetTitleSize(18)
        ## Scale offsets
        axis.SetLabelOffset( labelOffset )
        axis.SetTitleOffset( titleOffset )
    # end of customize axis

    #--------------------------------------------------------------------------
    def _updateRanges(self):
        tree = self.data.tree()
        n = tree.Draw(self.x.GetName(), '', 'goff')
        mi = ModalInterval(n, tree.GetV1())
        if self.doAutoXRange:
            ## Determine the range as a modal interval
            if self.xRangeMode == 'SigmaLevel':
                mi.setSigmaLevel(self.xRangeSigmaLevel)
            elif self.xRangeMode == 'Fraction':
                mi.setFraction(self.xRangeFraction)
            elif self.xRangeMode == 'NumberOfEntries':
                mi.setNumberOfEntriesToCover(self.xRangeNumberOfEntries)
            else:
                message = "Illegal xRangeMode = '%s'" % self.xRangeMode
                raise RuntimeError, message
            xmargin = 0.1 * mi.length()
            self.xRange = (mi.lowerBound() - xmargin,
                           mi.upperBound() + xmargin)
        else:
            ## If possible, shrink the range to cover the data plus a margin
            mi.setFraction(1.)
            xlo = mi.lowerBound()
            xhi = mi.upperBound()
            xmargin = 0.1 * mi.length()
            self.xRange = (max(xlo - xmargin, self.xRange[0]),
                           min(xhi + xmargin, self.xRange[1]))

        if self.doAutoXRangeZoom:
            mi.setSigmaLevel(self.xRangeSigmaLevelZoom)
            self.xRangeZoom = tuple(mi.bounds())

        if self.doAutoFitRange:
            ## Determine the range as a modal interval
            if self.fitRangeMode == 'SigmaLevel':
                mi.setSigmaLevel(self.fitRangeSigmaLevel)
            elif self.fitRangeMode == 'Fraction':
                mi.setFraction(self.fitRangeFraction)
            elif self.fitRangeMode == 'NumberOfEntries':
                mi.setNumberOfEntriesToCover(self.fitRangeNumberOfEntries)
                print "setting fit range number of entries:", mi.bounds()
            else:
                message = "Illegal fitRangeMode = '%s'" % self.fitRangeMode
                raise RuntimeError, message
            self.fitRange =  tuple(mi.bounds())
            print "++++ fit range changed to:", self.fitRange
        
        self.pullRange = getattr(self, self.pullRangeMode)
        self.residRange = getattr(self, self.residRangeMode)
    # end of _updateRanges


    #--------------------------------------------------------------------------
    def _getBinning(self):
        'Get binning that guaranties at least self.binContentMin events'
        'per bin. This is done by merging neighboring bins with too few evetns.'
        'The obtained binning is useful for calculation of chi2 statistic'
        'that obeys the chi2 PDF, see the PDG chapter on Statistics.'

        ## Histogram the data
        self.x.setBins(self.nBins)
        self.x.SetTitle(self.xTitle)

        plot = self.x.frame(*self.xRange)

        ## Plot the data to obtain the bin frequencies for uniform binning.
        self.data.plotOn(plot)
        hist = plot.getHist()

        ## Determine the range of the binning.
        xstart, xstop = self.xRange

        ## Create the target binning with the merged bins.
        bins = ROOT.RooBinning(xstart, xstop)
        bins.Print()
        boundaries = []
        contents = []

        ## Loop over all the uniform bins forward, copy to the new binning,
        ## merge them if needed.
        binContent = 0.
        for i in range(hist.GetN()):
            xlo = hist.GetX()[i] - hist.GetErrorXlow(i)
            xhi = hist.GetX()[i] + hist.GetErrorXhigh(i)
            binContent += hist.GetY()[i]

            ## Only consider bins inside of the range
            if xlo < xstart or xstop < xhi:
                continue

            if binContent >= self.binContentMin:
                if bins.hasBoundary(xhi):
                    continue
                boundaries.append(xhi)
                contents.append(binContent)
                binContent = 0.
            ## End of forward loop over bins

        ## The last bin may have too low content. Walk over the new bins
        ## backward and remove boundaries as needed.
        ## Create a new histogram with the new bins
        boundaries.reverse()
        contents.reverse()
        for boundary, content in zip(boundaries, contents):
            if binContent >= self.binContentMin:
                break
            binContent += content
            boundaries.remove(boundary)
        ## End of backward loop over the new boundaries

        for boundary in boundaries:
            bins.addBoundary(boundary)

        return bins
    ## end of _getBinning


    #--------------------------------------------------------------------------
    def _getAutoBinning(self):
        'Get binning that is uniform around that peak area and non-uniform\n'
        'in the tails.  It guaranties that the number of entries per bin is\n'
        'in a given range [minEntriesPerBin, maxEntriesPerBin] by merging\n'
        'neighboring bins in the tails. This is useful for calculation of\n'
        'chi2 statistic that obeys the chi2 PDF.\n'
        'Optional features:\n'
        '  * the bin width is a pretty number, e.g. 1, 0.5, 0.2, etc.\n'
        '  * calculate the median for each bin. (->better looking plot)\n'

        ## Get the data as an array of doubles pointed by a tree
        entries = self.data.tree().Draw(self.x.GetName(), '', 'goff')

        ## Create the DataDrivenBinning object
        bins = DataDrivenBinning(entries, self.data.tree().GetV1(),
                                 self.binContentMin, self.binContentMax)

        return bins
    ## end of _getAutoBinning


    #--------------------------------------------------------------------------
    def _makeCompactCanvas(self):
        ## Make a canvas
        canvas = TCanvas( self.name, self.name, 400, 800 )
        latexLabel = self.latex
        self.pads.extend( residPullDivide(canvas) )
        self.model.paramOn(self.plot,
                           Format('NEU', AutoPrecision(2)),
                           Parameters(self.parameters),
                           Layout(*self.paramLayout))
        ## Draw the frames
        for pad, plot in [(canvas.cd(1), self.plot),
                          (canvas.cd(2), self.residPlot),
                          (canvas.cd(3), self.pullPlot),]:
            pad.cd()
            pad.SetGrid()
            plot.GetYaxis().CenterTitle()
            plot.Draw()

        ## Add labels
        # rowsize = 0.055
        rowsize = 0.06
        canvas.cd(1)
        for i in range( len( self.labels ) ):
            latexLabel.DrawLatex(self.labelsLayout[0],
                                 self.labelsLayout[1] - i*rowsize, self.labels[i])

        ## Add the total number of events used
        numLabels = len( self.labels )
        latexLabel.DrawLatex( self.labelsLayout[0],
                              self.labelsLayout[1] - numLabels * rowsize,
                              '%d events' % self.data.numEntries() )
        ## Add the reduced chi2
        latexLabel.DrawLatex( self.labelsLayout[0],
                              self.labelsLayout[1] - (numLabels+1) * rowsize,
                              '#chi^{2}/ndof: %.2g' % self.reducedChi2.getVal() )
        ## Add the chi2 and ndof
        canvas.cd(2)
        chi2Val = self.reducedChi2.getVal() * self.ndof.getVal()
        ndofVal = int( self.ndof.getVal() )
        latexLabel.DrawLatex( self.labelsLayout[0], 0.85, '#chi^{2}: %.2g' % chi2Val)
        latexLabel.DrawLatex( self.labelsLayout[0], 0.75, 'ndof: %d' % ndofVal)

        ## Add the chi2 probability
        canvas.cd(3)
        latexLabel.DrawLatex(self.labelsLayout[0], 0.867,
                             'Prob: %.2g' % self.chi2Prob.getVal())
        return canvas
    ## end of makeCompactCanvas


    #--------------------------------------------------------------------------
    def _makeExtendedCanvas(self, landscape = False):
        ## Make a canvas
        canvas = TCanvas(self.name, self.name)
        if landscape:
            canvas.SetWindowSize(1200, 600)
            canvas.Divide(3,2)
            plots = [self.plot, self.plotZoom, self.pullDistPlot,
                     self.pullPlot, self.residPlot]
        else:
            canvas.SetWindowSize(800, 900 )
            canvas.Divide(2,3)
            plots = [self.plot, self.plotZoom, 
                     self.pullPlot, self.residPlot,
                     self.pullDistPlot]


        for i in range(1, 7):
            self.pads.append(canvas.cd(i))
            
        canvas.cd(1).SetLogy()

        self.model.paramOn(self.plot,
                           Format('NEU', AutoPrecision(2)),
                           Parameters(self.parameters),
                           Layout(*self.paramLayout))

        ## Draw the frames
        for i, plot in enumerate(plots):
            pad = canvas.cd(i+1)
            pad.SetGrid()
            #plot.GetYaxis().CenterTitle()
            plot.Draw()

        ## Extend labels to include more information
        chi2Val = self.reducedChi2.getVal() * self.ndof.getVal()
        ndofVal = int(self.ndof.getVal())
        labels = self.labels
        ## Add the total number of events used
        labels.append('%d events' % self.data.numEntries())
        ## Add the reduced chi2
        #labels.append('#chi^{2}/ndof: %.2g' % self.reducedChi2.getVal())
        ## Add the chi2 and ndof
        labels.append('#chi^{2}/ndof: %.3g/%d' % (chi2Val, ndofVal))
        ## Add the chi2 probability
        labels.append('p-value: %.2g' % self.chi2Prob.getVal())

        ## Draw labels
        canvas.cd(6)
        for index, label in enumerate(labels):
            self.latex.DrawLatex(gStyle.GetPadLeftMargin(),
                                 1. - gStyle.GetPadTopMargin() - index*0.08,
                                 label)

        return canvas
    ## end of makeExtendedCanvas


    #--------------------------------------------------------------------------
    def makePlot(self, workspace):
        self._updateRanges()

        if self.doAutoBinning:
            ## Get the DataDrivenBinning object
            ddbins = self._getAutoBinning()

            ## Get custom binning with at least self.binContentMin events per bin.
            self.bins = ddbins.binning(ROOT.RooBinning())
            self.bins.SetName('chi2')

            ## Get the corresponding unfiorm binning that is it's smallest superset
            self.uniformBins = ddbins.uniformBinning(ROOT.RooUniformBinning())
            self.uniformBins.SetName('normalization')
        else:
            self.uniformBins = ROOT.RooUniformBinning(self.xRange[0],
                                                      self.xRange[1],
                                                      self.nBins)
            self.bins = self.uniformBins
        self.x.SetTitle(self.xTitle)
        self.x.setBins(self.nBins)

        ## Make frames
        self.plot = self.x.frame(Range(*self.xRange))
        self.pullPlot = self.x.frame(Range(*self.pullRange))

        ## Make zoom frames
#         self.x.setBins(int (self.nBins *
#                             (self.xRangeZoom[1] - self.xRangeZoom[0]) /
#                             (self.xRange[1] - self.xRange[0])))
        self.plotZoom = self.x.frame(Range(*self.xRangeZoom))
        self.residPlot = self.x.frame(Range(*self.residRange))

        ## Add the data and model to the frame
        for p in [self.plot, self.plotZoom]:
            if self.doAutoBinning:
                ## This is hack to make RooFit use a nice normaliztion.
                ## First plot the data with uniform binning but don't display it.
                self.data.plotOn(p, Binning(self.uniformBins), Invisible())
            ## Then plot the data with the non-uniform binning.
            self.data.plotOn(p, Binning(self.bins))
            if self.doAutoBinning:
                ## Get the histogram of data and set the bin centers equal
                ## to per-bin medians.
                hist = p.getHist('h_' + self.data.GetName())
                ddbins.applyTo(hist)
            ## ## Find normalization range defined by bin boundaries
            ## xlo, xhi = self.fitRange
            ## binIndexes = range(self.bins.numBins())
            ## for b in binIndexes:
            ##     if self.bins.binLow(b) >= xlo:
            ##         xlo = self.bins.binLow(b)
            ## binIndexes.reverse()
            ## for b in binIndexes:
            ##     if self.bins.binHigh(b) <= xhi:
            ##         xhi = self.bins.binHigh(b)
            ## self.x.setRange('FitNormRange', xlo, xhi)
            
            ## Finally, overlay the fit.
            self.model.plotOn(p, Normalization(self.fitRangeNumEvents,
                                               ROOT.RooAbsReal.NumEvent))

        ## Adjust the y range of the plot
        hist = self.plot.getHist('h_' + self.data.GetName())
        irange = range(hist.GetN())
        ymax = max([hist.GetY()[i] + hist.GetErrorYhigh(i) for i in irange])
        ymin = min([hist.GetY()[i] - hist.GetErrorYlow(i) for i in irange])
        if ymin <= 0.:
            ymin = 0.1
        ymarginf = pow(ymax / ymin, 0.1)
        self.plot.GetYaxis().SetRangeUser(ymin / ymarginf, ymax * ymarginf)

#         self.model.plotOn(self.plot, Normalization(scale))

        if (hasattr(self, "useCustomChi2Calculator") and
            self.useCustomChi2Calculator == True):
            plotChi2 = RooChi2Calculator(self.plot)
            plotZoomChi2 = RooChi2Calculator(self.plotZoom)
            self.chi2s.append(plotChi2.chiSquare(self.parameters.getSize()))
            ## Get the residual and pull dists
            hresid = plotZoomChi2.residHist()
            hpull = plotChi2.pullHist()
        else:
            self.chi2s.append( self.plot.chiSquare( self.parameters.getSize() ) )
            ## Get the residual and pull dists
            hresid = self.plotZoom.residHist()
            hpull  = self.plot.pullHist()
            
        self.residPlot.SetYTitle('#chi^{2} Residuals')
        self.pullPlot.SetYTitle('#chi^{2} Pulls')
        self.residPlot.addPlotable(hresid, 'P')
        self.pullPlot.addPlotable(hpull, 'P')

        ## Plot the pull spectrum
        standardNormal = workspace.pdf('standardNormal')
        if not standardNormal:
            standardNormal = workspace.factory(
                'Gaussian::standardNormal(pull[-6,6],zero[0],unit[1])'
                )
        pull = workspace.var('pull')
        pull.SetTitle('#chi^{2} Pulls')
        pull.setBins(10)
        self.pullDistPlot = pull.frame()
        self.pullDistPlot.SetYTitle('Bins of %s' % self.xTitle)
        self.pulldata = RooDataSet('pulldata_' + self.name,
                                   'Pulls, ' + self.title, RooArgSet(pull))
        for i in range(hpull.GetN()):
            pull.setVal(hpull.GetY()[i])
            self.pulldata.add(RooArgSet(pull))
        ## entries = pulldata.tree().Draw('pull', '', 'goff')
        ## pullbins = DataDrivenBinning(entries, pulldata.tree().GetV1(), 5, 10)
        ## binning = pullbins.binning(ROOT.RooBinning())
        ## uniformBinning = pullbins.uniformBinning(ROOT.RooUniformBinning())
        ## pulldata.plotOn(self.pullDistPlot, Binning(uniformBinning), Invisible())
        ## pulldata.plotOn(self.pullDistPlot, Binning(binning))
        workspace.Import(self.pulldata)
        self.pulldata.plotOn(self.pullDistPlot)
        standardNormal.plotOn(self.pullDistPlot)#, Normalization(hpull.GetN()))

        ## Customize plot titles and axis
        for p in [self.plot, self.plotZoom, self.residPlot, self.pullPlot,
                  self.pullDistPlot]:
            p.SetTitle('')
            self._customizeAxis(p.GetYaxis(), 0.01, 2.5)
        ## end of loop over plots
        #self._customizeAxis( self.pullPlot.GetXaxis(), 0.01, 3.5 )

        ## Save the chi2 and ndof in the workspace
        if workspace.var('reducedChi2'):
            reducedChi2 = workspace.var('reducedChi2')
            ndof = workspace.var('ndof')
            chi2Prob = workspace.var('chi2Prob')
        else:
            reducedChi2 = RooRealVar( 'reducedChi2', 'fit #chi^{2}/ndof', -1 )
            ndof = RooRealVar( "ndof", "fit n.d.o.f.", -1 )
            chi2Prob = RooRealVar( 'chi2Prob', '#chi^{2} probability', -1 )
            workspace.Import(reducedChi2)
            workspace.Import(ndof)
            workspace.Import(chi2Prob)
        reducedChi2.setVal( self.chi2s[-1] )
        ndof.setVal( self.residPlot.getHist().GetN() - self.parameters.getSize() )
        chi2Prob.setVal( TMath.Prob( reducedChi2.getVal() * ndof.getVal(),
                                    int( ndof.getVal() ) ) )
        chi2 = RooArgSet( reducedChi2, ndof, chi2Prob )
        workspace.saveSnapshot( 'chi2_' + self.name, chi2, True )

        ## Attach chi2 and ndof to self
        self.reducedChi2 = reducedChi2
        self.ndof = ndof
        self.chi2Prob = chi2Prob

        ## Make the canvas
        if self.canvasStyle == 'compact':
            self.canvas = self._makeCompactCanvas()
        elif self.canvasStyle == 'extended':
            self.canvas = self._makeExtendedCanvas()
        elif self.canvasStyle == 'landscape':
            self.canvas = self._makeExtendedCanvas(landscape = True)
        else:
            raise RuntimeError, "Illegal canvasStyle `'!" % self.canvasStyle

        self.canvases.append(self.canvas)
        i = len( gROOT.GetListOfCanvases() )
        self.canvas.SetWindowPosition(20*(i%50), 20*(i%5))
        self.canvas.Update()

        ## Save the plots
        if hasattr(self, 'graphicsExtensions'):
            for ext in self.graphicsExtensions:
                self.canvas.Print( 'sFit_' + self.name + '.' + ext )
    ## <-- makePlot -----------------------------------------------------------

    #--------------------------------------------------------------------------
    def fit(self, workspace, saveName = ''):
        self.getMassCut(workspace)
        self.getData(workspace)
        self._updateRanges()
        self.fitToData(workspace, saveName)
        self.makePlot(workspace)
    ## <-- fit ----------------------------------------------------------------

## <-- ScaleFitter ------------------------------------------------------------

subdet_r9_nv_categories = ICut(
    names = 'EB_sixie_LowNV_R9Low_0_R9High_0.94 EB_sixie_HighNV_R9Low_0_R9High_0.94 EB_sixie_LowNV_R9Low_0.94_R9High_999 EB_sixie_HighNV_R9Low_0.94_R9High_999 EE_sixie_LowNV_R9Low_0_R9High_0.94 EE_sixie_HighNV_R9Low_0_R9High_0.94 EE_sixie_LowNV_R9Low_0.94_R9High_999 EE_sixie_HighNV_R9Low_0.94_R9High_999'.split(),
    titles = ('Barrel, R9 < 0.94, Low Pile Up',
              'Barrel, R9 < 0.94, High Pile Up',
              'Barrel, R9 > 0.94, Low Pile Up',
              'Barrel, R9 > 0.94, High Pile Up',
              'Endcaps, R9 < 0.94, Low Pile Up',
              'Endcaps, R9 < 0.94, High Pile Up',
              'Endcaps, R9 > 0.94, Low Pile Up',
              'Endcaps, R9 > 0.94, High Ple Up'),
    labels = (('Barrel', 'R_{9}^{#gamma} < 0.94', 'Low Pile Up'),
              ('Barrel', 'R_{9}^{#gamma} < 0.94', 'High Pile Up'),
              ('Barrel', 'R_{9}^{#gamma} > 0.94', 'Low Pile Up'),
              ('Barrel', 'R_{9}^{#gamma} > 0.94', 'High Pile Up'),
              ('Endcaps', 'R_{9}^{#gamma} < 0.94', 'Low Pile Up'),
              ('Endcaps', 'R_{9}^{#gamma} < 0.94', 'High Pile Up'),
              ('Endcaps', 'R_{9}^{#gamma} > 0.94', 'Low Pile Up'),
              ('Endcaps', 'R_{9}^{#gamma} > 0.94','High Pile Up' ),),

    cuts = (('phoIsEB' , 'phoR9 < 0.94', 'NV <= 18'),
            ('phoIsEB' , 'phoR9 < 0.94', 'NV > 18'),
            ('phoIsEB' , 'phoR9 > 0.94', 'NV <= 18'),
            ('phoIsEB' , 'phoR9 > 0.94', 'NV > 18'),
            ('!phoIsEB' , 'phoR9 < 0.94', 'NV <= 18'),
            ('!phoIsEB' , 'phoR9 < 0.94', 'NV > 18'),
            ('!phoIsEB' , 'phoR9 > 0.94', 'NV <= 18'),
            ('!phoIsEB' , 'phoR9 > 0.94', 'NV > 18'),)
    )
 
subdet_r9_categories = ICut(
    names = 'EB_sixie_R9Low_0_R9High_0.94 EB_sixie_R9Low_0.94_R9High_999 EE_sixie_R9Low_0_R9High_0.94 EE_sixie_R9Low_0.94_R9High_999'.split(),
    titles = ('Barrel, R9 < 0.94',
              'Barrel, R9 > 0.94',
              'Endcaps, R9 < 0.95',
              'Endcaps, R9 > 0.95'),
    ## For latex labels on plots
    labels = (('Barrel', 'R_{9}^{#gamma} < 0.94'),
              ('Barrel', 'R_{9}^{#gamma} > 0.94'),
              ('Endcaps', 'R_{9}^{#gamma} < 0.95'),
              ('Endcaps', 'R_{9}^{#gamma} > 0.95'),),
    ## For TTree selection expressions
    cuts = (('phoIsEB' , 'phoR9 < 0.94'),
            ('phoIsEB' , 'phoR9 > 0.94'),
            ('!phoIsEB' , 'phoR9 < 0.95'),
            ('!phoIsEB' , 'phoR9 > 0.95'),)
    )

subdet_nv_categories = ICut(
    names = 'EB_sixie_HighNV_R9Low_0_R9High_999 EB_sixie_LowNV_R9Low_0_R9High_999 EE_sixie_HighNV_R9Low_0_R9High_999 EE_sixie_LowNV_R9Low_0_R9High_999'.split(),
    titles = ('Barrel, High Pile Up',
              'Barrel, Low Pile Up',
              'Endcaps, High Pile Up',
              'Endcaps, Low Pile Up'),
    labels = (('Barrel', 'High Pile Up'),
              ('Barrel', 'Low Pile Up'),
              ('Endcaps', 'High Pile Up'),
              ('Endcaps', 'Low Pile Up'),),
    cuts = (('phosIsEB', 'NV > 18'),
            ('phoIsEB', 'NV <=18'),
            ('!phoIsEB', 'NV > 18'),
            ('!phoIsEB', 'NV <= 18'),)
    )


    
subdet_categories = ICut(
    names = 'EB EE'.split(),
    titles = ('Barrel',
              'Endcaps',),
    ## For latex labels on plots
    labels = (('Barrel',),
              ('Barrel',),),
    ## For TTree selection expressions
    cuts = (('phoIsEB',),
            ('!phoIsEB',),)
    )

## model_names = 'gauss cbShape lognormal curijff gamma'.split()
## model_titles = 'Gauss CB Lognaormal Cruijff Gamma'.split()
## model_labels = [[i] for i in model_titles]
## models = {}
## for args in zip(model_names, model_titles, model_labels, model_names):
##     models[ars[0]] = Model(*args)

if __name__ == "__main__":
    test_fitter = ScaleFitter(
        name = 's',
        title = 's-Fit',
        cuts = ['mmMass < 80'],
        labels = [],
        source = '_chains["z"]',
        xExpression = '100 * (1/kRatio - 1)',
        xRange = (-20, 40),
        nBins = 120,
        fitRange = (-100, 100),
        pdf = 'lognormal',
        graphicsExtensions = [],
        massWindowScale = 1.5,
        fitScale = 2.0,
    )

    print test_fitter.applyDefinitions().pydump()

    eb_lor9, eb_hir9, ee_lor9, ee_hir9 = list(subdet_r9_categories)

    print "Applying", eb_lor9.title
    print test_fitter.applyDefinitions([eb_lor9]).pydump()

    pt10_15 = PhoEtBin(10, 15)
    print "Applying", pt10_15.title
    print test_fitter.applyDefinitions([pt10_15]).pydump()

    import user
