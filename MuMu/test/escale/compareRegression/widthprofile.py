import array
import os
import ROOT
import FWLite.Tools.canvases as canvases
import FWLite.Tools.dataset as dataset
import FWLite.Tools.roofit as roo
from FWLite.Tools.modalinterval import ModalInterval
from FWLite.Tools.legend import Legend
from FWLite.Tools.resampler import Resampler

#==============================================================================
class Source:
    '''
    Facilitates the analysis
    '''    
    ROOT.gROOT.ProcessLine('''
        struct leafs_t {
          UInt_t RunNumber;
          UInt_t EventNumber;
          Float_t Mass;
        };
        '''.replace('\n', '')
        )
    #__________________________________________________________________________
    def __init__(self, name, title, filename, cuts):
        self.name = name
        self.title = title
        self.filename = filename
        self.cuts = cuts
        self.setup_tree()
    
    #__________________________________________________________________________
    def setup_tree(self):
        self.source = ROOT.TFile.Open(self.filename)
        self.tree = self.source.Get('ZmumuGammaEvent')
        self.setbranchstatus(mode='cuts')
        self.tree = self.tree.CopyTree(
            '&'.join(['(%s)' % c for c in self.cuts])
            )
        self.setbranchstatus(mode='brief')
        self.tree = self.tree.CopyTree('1')
        self.tree.BuildIndex('RunNumber', 'EventNumber')
        ## Create leaf buffers
        self.leafs = ROOT.leafs_t()
        for leaf in 'RunNumber EventNumber Mass'.split():
            self.tree.SetBranchAddress(leaf, 
                                       ROOT.AddressOf(self.leafs, leaf))
    #__________________________________________________________________________
    def setbranchstatus(self, mode='cuts'):
        self.tree.SetBranchStatus("*", 0)
        if mode == 'cuts':
            for branch in '''
                          RunNumber
                          EventNumber
                          Mass
                          DileptonMass
                          MinDeltaR
                          Mu1Pt
                          Mu2Pt
                          PhotonIsEB
                          PhotonPt
                          PhotonR9
                          Mu1Eta
                          Mu2Eta
                          PhotonEta
                          '''.split():
                self.tree.SetBranchStatus(branch, 1)
        elif mode == 'brief':
            for branch in '''
                          RunNumber
                          EventNumber
                          Mass
                          '''.split():
                self.tree.SetBranchStatus(branch, 1)            
## End of Source



#==============================================================================
class Merger:
    #__________________________________________________________________________
    def __init__(self, variable, sources):
        self.variable = variable
        self.sources = sources
        self.tree = ROOT.TTree('merged', 'merged')
        self.merge()
        self.get_merged_dataset()
    #__________________________________________________________________________
    def merge(self):
        for src in self.sources:
            self.tree.Branch(src.name,
                             ROOT.AddressOf(src.leafs, self.variable.GetName()),
                             src.name + '/F')
        for entry in range(self.sources[0].tree.GetEntries()):
            self.sources[0].tree.GetEntry(entry)
            run   = self.sources[0].leafs.RunNumber
            event = self.sources[0].leafs.EventNumber
            bytes = self.sources[1].tree.GetEntryWithIndex(run, event)
            if bytes < 0:
                # print 'Run', run, 'Event', event, 'not in', 
                # print self.source2.name
                continue
            self.tree.Fill()
    #__________________________________________________________________________
    def report(self):
        common = self.tree.GetEntries()
        total = sum(map(lambda x: x.tree.GetEntries(), self.sources)) - common
        percent = 100 * float(common) / total
        print 'Total events:', total
        print 'Overlap:', common, '(%.3g %%)' % percent
        for src in self.sources:
            total = src.tree.GetEntries()
            unique = total - common
            percent = 100 * float(unique) / total
            print 'Unique for %s:' % src.name, unique, '(%.2g %%)' % percent

    #__________________________________________________________________________
    def get_merged_dataset(self):
        self.merged_variables = []
        for src in self.sources:
            new_variable = self.variable.Clone(src.name)
            new_variable.SetTitle(src.name)
            self.merged_variables.append(new_variable)
        self.merged_dataset = dataset.get(tree = self.tree,
                                          variables = self.merged_variables)
        for src, var in zip(self.sources, self.merged_variables):
            var.SetTitle(src.title)

# End of class Merger


#==============================================================================
class SubsampleWidthCalculator:
    '''
    Calculates subsample width(s) for given data and sabsample sizes given as
    fractions of the full sample.
    '''
    #__________________________________________________________________________
    def __init__(self, data, fractions=[0.1 * i for i in range(1,10)]):
        self.data = data
        self.fractions = fractions
        self.makegraph()
        
    #__________________________________________________________________________
    def makegraph(self):
        row = self.data.get()
        if row.getSize() < 1:
            raise RuntimeError, 'Dataset must contain at least one variable!'
        variable = row.first()
        self.data.tree().Draw(variable.GetName(), '', 'goff')
        size = self.data.tree().GetSelectedRows()
        first = self.data.tree().GetV1()
        modalinterval = ModalInterval(size, first)
        widths = []
        for x in self.fractions:
            modalinterval.setFraction(x)
            widths.append(modalinterval.length())
        xvalues = array.array('d', self.fractions)
        yvalues = array.array('d', widths)
        self.graph = ROOT.TGraph(len(self.fractions), xvalues, yvalues)
        ## Decorate the graph
        self.graph.SetName(variable.GetName())
        self.graph.SetTitle(variable.GetTitle())
        self.graph.GetXaxis().SetTitle('Sample Fraction')
        ytitle = 'Subsample Width'
        if variable.getUnit():
            ytitle += ' (%s)' % variable.getUnit()
        self.graph.GetYaxis().SetTitle(ytitle)
        
## End of class SubsampleWidthCalculator

#==============================================================================
class WidthComparator:
    '''
    Compares the width of two different variables for given data.
    '''
    #__________________________________________________________________________
    def __init__(self, name, title, data, granularity=40, nboot=500):
        self.name = name
        self.title = title
        self.data = data
        self.granularity = granularity
        self.nboot = nboot
        self.setup()

    #__________________________________________________________________________
    def setup(self):
        self.fractions = self.get_fractions()

        self.variables = self.data.get().pylist()
        if len(self.variables) != 2:
            message = 'Data must contain exactly 2 variables! Found %d.'
            raise RuntimeError, message % len(self.variables)

        self.widths = [self.get_width(x) for x in self.variables]
        self.width_ratio = self.divide_graphs(self.widths[0].graph,
                                              self.widths[1].graph)
        errors =  self.bootstrap(self.nboot)
        (self.errors_rms, self.errors_mi1, self.errors_mi2) = errors
    #__________________________________________________________________________
    def get_fractions(self):
        '''
        Returns the list of boundaries spliting (0, 1) into equidistant bins
        whose number is given by self.granualrity. The first and last 
        boundaries 0 and 1 are excluded from the returned list.
        '''
        dx = 1./self.granularity
        return [dx * i for i in range(1, self.granularity)]

    #__________________________________________________________________________
    def get_width(self, variable):
        reduced_data = self.data.reduce(ROOT.RooArgSet(variable))
        return SubsampleWidthCalculator(reduced_data, self.fractions)
        
    #__________________________________________________________________________
    def divide_graphs(self, graph1, graph2):
        ratio_graph = ROOT.TGraph(graph1.GetN())
        for i in range(ratio_graph.GetN()):
            x = graph1.GetX()[i]
            y = graph1.GetY()[i] / graph2.GetY()[i]
            ratio_graph.SetPoint(i, x, y)
        ratio_graph.GetXaxis().SetTitle('Sample Fraction')
        ratio_graph.GetYaxis().SetTitle(
            'Width Ratio %s/%s' % (graph1.GetTitle(),
                                   graph2.GetTitle())
            )
        return ratio_graph
        
    #__________________________________________________________________________
    def get_width_ratio(self, data, fractions):
        widths = []
        for variable in self.variables:
            reduced_data = data.reduce(ROOT.RooArgSet(variable))
            widths.append(SubsampleWidthCalculator(reduced_data, fractions))
        return self.divide_graphs(widths[0].graph, widths[1].graph)
      
    #__________________________________________________________________________
    def bootstrap(self, repeat=10):
        nbinsx = len(self.fractions)
        xlow = 0.5 * self.fractions[0]
        xup = self.fractions[-1] + xlow
        errors_rms = ROOT.TProfile(self.name + '_errors_rms', self.title, 
                                   nbinsx, xlow, xup, 's')
        errors_mi1 = ROOT.TGraphAsymmErrors(nbinsx)
        errors_mi2 = ROOT.TGraphAsymmErrors(nbinsx)
        for graph in [errors_mi1, errors_mi2]:
            graph.SetTitle(self.title)
        resampler = Resampler(self.data)
        bootdata = {}
        for iteration in range(repeat):
            replica = resampler.bootstrap()
            boot = self.get_width_ratio(replica, self.fractions)
            for i in range(boot.GetN()):
                x = boot.GetX()[i]
                y = boot.GetY()[i]
                #y = boot.GetY()[i] - self.width_ratio.GetY()[i]
                errors_rms.Fill(x, y)
                bootdata.setdefault(x, []).append(y)
        for i, (x, ydist) in enumerate(sorted(bootdata.items())):
            ysize = len(ydist)
            yarray = array.array('d', ydist)
            y = ROOT.TMath.Median(ysize, yarray)
            errors_mi1.SetPoint(i, x, y)
            errors_mi2.SetPoint(i, x, y)
            exh = exl = 0.
            mi = ModalInterval(ysize, yarray)
            mi.setSigmaLevel(1)
            eyl = y - mi.lowerBound()
            eyh = mi.upperBound() - y
            errors_mi1.SetPointError(i, exl, exh, eyl, eyh)
            mi.setSigmaLevel(2)
            eyl = y - mi.lowerBound()
            eyh = mi.upperBound() - y
            errors_mi2.SetPointError(i, exl, exh, eyl, eyh)
        return errors_rms, errors_mi1, errors_mi2
        
    #__________________________________________________________________________
    def make_plots(self):
        #self.make_width_profiles_plot()
        #self.make_width_ratio_plot()        
        self.make_width_ratio_booterrors_plot()

    #__________________________________________________________________________
    def make_width_profiles_plot(self):
        canvases.next(self.name + '_width_profiles').SetGrid()
        self.widths[0].graph.SetLineColor(ROOT.kRed)
        self.widths[0].graph.Draw('al')
        self.widths[1].graph.Draw('l')
        graphs = [w.graph for w in self.widths]
        titles = [x.GetTitle() for x in self.variables]
        Legend(graphs, titles, opt = 'l').draw()

    #__________________________________________________________________________
    def make_width_ratio_plot(self):
        canvases.next(self.name + '_width_ratio').SetGrid()        
        self.copy_axes_titles(self.width_ratio, self.errors_rms)
        #self.errors_rms.GetXaxis().SetTitle(self.width_ratio.GetXaxis().GetTitle())
        #self.errors_rms.GetYaxis().SetTitle(self.width_ratio.GetYaxis().GetTitle())
        self.errors_rms.SetFillColor(ROOT.kGreen)
        #self.errors_rms.GetYaxis().SetRangeUser(0.9, 1.1)
        #self.errors_rms.GetXaxis().SetRangeUser(0.05, 0.95)
        self.errors_rms.DrawCopy('E4')
        self.errors_rms.SetFillColor(ROOT.kWhite)
        self.errors_rms.DrawCopy('HIST L SAME')
        self.width_ratio.SetLineColor(ROOT.kRed)
        self.width_ratio.Draw('L')        

    #__________________________________________________________________________
    def make_width_ratio_booterrors_plot(self):
        canvas = canvases.next(self.name + '_width_ratio_booterrors')
        canvas.SetGrid()
        self.copy_axes_titles(self.width_ratio, self.errors_mi1)
        self.copy_axes_titles(self.width_ratio, self.errors_mi2)
        self.errors_mi1.SetFillColor(ROOT.kYellow)
        self.errors_mi2.SetFillColor(ROOT.kGreen)
        # self.errors_mi2.GetYaxis().SetRangeUser(0.9, 1.1)
        self.errors_mi2.Draw('3a')
        self.errors_mi1.Draw('3')
        self.errors_mi1.Draw('lx')
        self.width_ratio.SetLineColor(ROOT.kRed)
        self.width_ratio.Draw('l')
        ## Some ROOT Voodoo to make the grid lines appear above the bands
        self.errors_mi2.GetHistogram().Draw('sameaxig')
        canvas.RedrawAxis('g')

    #__________________________________________________________________________
    def copy_axes_titles(self, source, destination):
        self.copy_title(source.GetXaxis(), destination.GetXaxis())
        self.copy_title(source.GetYaxis(), destination.GetYaxis())
        
    #__________________________________________________________________________
    def copy_title(self, source, destination):
        destination.SetTitle(source.GetTitle())

    #__________________________________________________________________________
    def save_plots(self):
        canvases.make_plots(['root'])
        canvases.make_pdf_from_eps()
## End of class WidthComparator
    
    
#==============================================================================
class WidthProfile:
    #__________________________________________________________________________
    def __init__(self, name, title, sources, granularity=10, nboot=200):
        self.name = name
        self.title = title
        self.sources = sources
        self.granularity = granularity
        self.nboot = nboot
    
    #__________________________________________________________________________
    def run(self):
        variable = ROOT.RooRealVar('Mass', 'Mass', 60, 120, 'GeV')
        self.merger = Merger(variable, self.sources)
        self.merger.report()
        self.comparator = WidthComparator(self.name,
                                          self.title,
                                          self.merger.merged_dataset,
                                          self.granularity,
                                          self.nboot)
        self.comparator.make_plots()        
## End of class WidthProfile


#==============================================================================
def main():
    '''
    Main entry point of execution of a test.
    '''
    global widthprofile
    basepath = '/home/cmorgoth/scratch/CMSSW_5_2_5/src/UserCode/CPena/src/PhosphorCorrFunctor/SIXIE_LAST_VERSION'

    basecuts = [
        'DileptonMass + Mass < 180',
        #'0.4 < MinDeltaR',
        '0.05 < min(abs(Mu1Eta - PhotonEta), abs(Mu2Eta - PhotonEta)) || 0.3 < MinDeltaR',    
        'MinDeltaR < 1.5', 
        'Mu2Pt > 10.5',
        'Mu1Pt > 21', 
        'DileptonMass > 55',
        ]
        
    catcuts = [
        'PhotonIsEB',
        '25 < PhotonPt && PhotonPt < 99',
        'PhotonR9 >= 0.94',
        #'PhotonR9 < 0.94',
        #'RunNumber >= 197770', ## Beginning of 2012C
        'RunNumber < 197770', ## Beginning of 2012C
        ]

    name = 'EB_highR9_2012CD'
    title = 'Barrel, R9 > 0.94, 2012CD'

    sources = [
        Source(
            name = 'regression',
            title = 'Regression',
            filename = os.path.join(
                basepath, 
                'PhotonRegression/ZmumuGammaNtuple_Full2012_MuCorr.root'
                ),
            cuts = basecuts + catcuts,
            ),
        
        Source(
            name = 'default',
            title = 'Default',
            filename = os.path.join(
                basepath, 
                'NoPhotonRegression/ZmumuGammaNtuple_Full2012_MuCorr.root',
                ),
            cuts = basecuts + catcuts,
            )
        ]

    widthprofile = WidthProfile(name, title, sources, 20, 500)
    widthprofile.run()
    
    canvases.update()
## End of main()


#==============================================================================
if __name__ == '__main__':
    main()
    import user
