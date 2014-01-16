'''
This is a PyROOT version of 
rf609_xychi2fit.C: 'LIKELIHOOD AND MINIMIZATION' RooFit tutorial macro #609
combined with
rf610_visualerror.C: 'LIKELIHOOD AND MINIMIZATION' RooFit tutorial macro #610
See originals at:
http:##root.cern.ch/root/html/tutorials/roofit/rf609_xychi2fit.C.html
http://root.cern.ch/root/html/tutorials/roofit/rf610_visualerror.C.html

Jan Veverka, Caltech, 10 September 2012.

USAGE: python -i xychi2fitter.py
'''
import math
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.cmsstyle as cmsstyle
import JPsi.MuMu.common.canvases as canvases
from JPsi.MuMu.common.latex import Latex

## Defaults
_filename  = '/home/veverka/test/resTrueVsPt_HggV2Ression_NoMuonBias_EGMPaperCategories.root'
_graphname = 'regressions_restrue_EB_jan2012rereco'
_name      = 'PhotonResolutionVsEt_MCTruth_Barrel_S0'
_title     = 'Barrel, MC Truth, S = 0 % #sqrt{GeV} Fixed'
_systematics = 0.
_yrange    = None
_noxerrors = True

#==============================================================================
class XYChi2Fitter():
  
    #_________________________________________________________________________
    def __init__(self,
                 filename = _filename,
                 graphname = _graphname,
                 name = _name,
                 title = _title,
                 systematics = _systematics,
                 yrange = _yrange,
                 noxerrors = _noxerrors):
        
        self.filename = filename
        self.graphname = graphname
        self.name = name
        self.title = title
        self.systematics = systematics
        self.yrange = yrange
        self.noxerrors = noxerrors
        
        #self.generate_toy_data()
        #self.define_fit_function_parabola()

        self.read_data_from_graph_in_file()
        self.define_resolution_fit_model()

        #self.S.setVal(0)
        #self.S.setConstant(True)

        #self.N.setVal(0.3)
        #self.N.setConstant(True)
    ## End of __init__(self).


    #_________________________________________________________________________
    def run(self):
        ## P e r f o r m   c h i 2   f i t   t o   X + / - d x   a n d   Y + / - d Y   v a l u e s
        ## ---------------------------------------------------------------------------------------

        if self.noxerrors:
            ## Fit chi^2 using Y errors only
            self.fresult = self.f.chi2FitTo(self.dxy_noxerrors,
                                            roo.YVar(self.y), roo.Save(),
                                            roo.Minos())
        else:
            ## Fit chi^2 using X and Y errors
            self.fresult = self.f.chi2FitTo(self.dxy, roo.YVar(self.y), roo.Save(),
                                            roo.Minos())
        
        self.frame = self.make_plot()                
        self.draw_plot(self.frame)
        self.decorate_plot()
        canvases.update()
    ## End of run(self)

    
    #_________________________________________________________________________
    def read_data_from_graph_in_file(self):
        x = ROOT.RooRealVar('x', 'Photon E_{T}', 5, 70, 'GeV')
        y = ROOT.RooRealVar('y', 'y', 0, 20)
        dxy = ROOT.RooDataSet('dxy', 'dxy', ROOT.RooArgSet(x, y),
                              roo.StoreAsymError(ROOT.RooArgSet(x, y)))
        dxy_noxerrors = ROOT.RooDataSet('dxy_noxerrors', 'dxy_noxerrors',
                                        ROOT.RooArgSet(x, y),
                                        roo.StoreAsymError(ROOT.RooArgSet(y)))
        self.x, self.y, self.dxy = x, y, dxy
        self.dxy_noxerrors = dxy_noxerrors
        rootfile = ROOT.TFile.Open(self.filename)
        graph = rootfile.Get(self.graphname)
        oplus = lambda x, y: ROOT.TMath.Sqrt(x*x + y*y)
        ## Add in quadrature 1% syst. error to the stat. errors
        if graph.InheritsFrom('TGraphAsymmErrors'):
            ex_low  = lambda i: -oplus(graph.GetEXlow ()[i], graph.GetX()[i] * self.systematics)
            ex_high = lambda i:  oplus(graph.GetEXhigh()[i], graph.GetX()[i] * self.systematics)
            ey_low  = lambda i: -oplus(graph.GetEYlow ()[i], graph.GetX()[i] * self.systematics)
            ey_high = lambda i:  oplus(graph.GetEYhigh()[i], graph.GetX()[i] * self.systematics)
        else:
            ex_low  = lambda i: -oplus(graph.GetEX()[i], graph.GetX()[i] * self.systematics)
            ex_high = lambda i:  oplus(graph.GetEX()[i], graph.GetX()[i] * self.systematics)
            ey_low  = lambda i: -oplus(graph.GetEY()[i], graph.GetX()[i] * self.systematics)
            ey_high = lambda i:  oplus(graph.GetEY()[i], graph.GetX()[i] * self.systematics)
        if self.noxerrors:
            # ex_low_orig  = ex_low
            # ex_high_orig = ex_high
            # ex_low  = lambda i: 0.1 * ex_low_orig(i)
            # ex_high = lambda i: 0.1 * ex_high_orig(i)
            # ex_low  = lambda i: 0.1
            # ex_high = lambda i: 0.1
            pass
        for i in range(graph.GetN()):
            self.x.setVal(graph.GetX()[i])
            self.y.setVal(graph.GetY()[i])
            self.x.setAsymError(ex_low(i), ex_high(i))
            self.y.setAsymError(ey_low(i), ey_high(i))
            self.dxy.add(ROOT.RooArgSet(self.x, self.y))
            self.x.removeError()
            self.x.removeAsymError()
            self.dxy_noxerrors.add(ROOT.RooArgSet(self.x, self.y))
        rootfile.Close()
    ## End of read_data_from_graph_in_file()  
    
    
    #_________________________________________________________________________
    def generate_toy_data(self):
        ## C r e a t e   d a t a s e t   w i t h   X   a n d   Y   v a l u e s
        ## -------------------------------------------------------------------

        ## Make weighted XY dataset with asymmetric errors stored
        ## The StoreError() argument is essential as it makes
        ## the dataset store the error in addition to the values
        ## of the observables. If errors on one or more observables
        ## are asymmetric, one can store the asymmetric error
        ## using the StoreAsymError() argument
        
        ## Fill an example dataset with X,err(X),Y,err(Y) values
        x = ROOT.RooRealVar('x', 'x', -11,  11)
        y = ROOT.RooRealVar('y', 'y', -10, 200)
        dxy = ROOT.RooDataSet('dxy', 'dxy', ROOT.RooArgSet(x, y),
                              roo.StoreError(ROOT.RooArgSet(x, y)))
        self.x, self.y, self.dxy = x, y, dxy
        for i in range(11):
          
            ## Set X value and error
            x.setVal(-10 + 2 * i)
            if i < 5:
                x.setError(0.5 / 1.)
            else:
                x.setError(1.0 / 1. )
              
            ## Set Y value and error
            y.setVal(x.getVal() * x.getVal() + 4 * math.fabs(ROOT.gRandom.Gaus()))
            y.setError(math.sqrt(y.getVal()))
            
            dxy.add(ROOT.RooArgSet(x, y))
        ## End of loop over dxy entries
        
    ## End of create_dataset(self)
    
    
    #_________________________________________________________________________
    def define_fit_function_parabola(self):
        ## Make fit function
        self.a = ROOT.RooRealVar('a', 'a', 0.0, -10, 10)
        self.b = ROOT.RooRealVar('b', 'b', 0, -100, 100)
        self.f = ROOT.RooPolyVar('f', 'f', self.x, 
                                 ROOT.RooArgList(self.b, 
                                                 self.a, 
                                                 roo.RooConst(1)))
    ## End of define_fit_function(self)
    

    #_________________________________________________________________________
    def define_resolution_fit_model(self):
        ## Make resolution fit model
        self.S = ROOT.RooRealVar('S', 'Stochastic Term', 0, -100, 100, 
                                 r'% (GeV)^{1/2}')
        self.N = ROOT.RooRealVar('N', 'Noise Term', 0.3, -100, 100,
                                 r'% GeV')
        self.C = ROOT.RooRealVar('C', 'Constant Term', 1, -100, 100, '%')
        self.f = ROOT.RooFormulaVar('f', 'Resolution fit model',
                                    'sqrt(S*S/x + N*N/x/x + C*C)',
                                    ROOT.RooArgList(self.x, 
                                                    self.S, self.N, self.C))
        
    ## End of define_resolution_fit_model(self)
    

    #_________________________________________________________________________
    def make_plot(self):
        frame = self.x.frame(roo.Title(self.title))

        ## Visualize 2- and 1-sigma errors using linear error propagation.
        self.f.plotOn(frame, roo.VisualizeError(self.fresult, 2), 
                      roo.FillColor(ROOT.kGreen))
        self.f.plotOn(frame, roo.VisualizeError(self.fresult, 1), 
                      roo.FillColor(ROOT.kYellow))

        ## Visualize 1-sigma errors using a curve sampling method. 
        #self.f.plotOn(frame, roo.VisualizeError(self.fresult, 1, False),
                      #roo.DrawOption("L"), roo.LineWidth(2),
                      #roo.LineColor(ROOT.kRed))

        ## Plot fitted function
        self.f.plotOn(frame)

        ## Overlay dataset in X-Y interpretation
        self.dxy.plotOnXY(frame, roo.YVar(self.y))

        return frame
      
    ## End of make_plot(self)
    
    
    #_________________________________________________________________________
    def draw_plot(self, frame):
        ## Draw the plot on a canvas
        #print "## Draw the plot on a canvas"
        canvases.wwidth = 600
        canvases.wheight = 600
        canvas = canvases.next(self.name)
        canvas.SetGrid()
        canvas.SetLeftMargin(0.15)
        canvas.SetTopMargin(0.1)
        frame.GetYaxis().SetTitleOffset(1.0)
        frame.GetYaxis().SetTitle('E_{#gamma} Resolution '
                                  '#sigma_{eff}/E (%)')
        if self.yrange:
            frame.GetYaxis().SetRangeUser(*self.yrange)
        frame.Draw()
        canvas.RedrawAxis('g')
        canvases.update()
    ## End of draw_plot()

    #_________________________________________________________________________
    def decorate_plot(self):
        ## Draw the functional form
        Latex(['#frac{#sigma_{eff}}{E} = #frac{S}{#sqrt{E_{T}}} #oplus '
                                        '#frac{N}{E_{T}} #oplus C'],
              position = (0.18, 0.8), textsize = 22).draw()
              
        ## Draw the fit result 
        chi2 = self.fresult.minNll()
        npars = self.fresult.floatParsFinal().getSize()
        ndof = self.dxy.numEntries() - npars
        prob = ROOT.TMath.Prob(chi2, ndof)
        Latex([self.root_latex_for_realvar(self.S, 1),
               self.root_latex_for_realvar(self.N, 1),
               self.root_latex_for_realvar(self.C, 1),
               '#chi^{2} / N_{dof}: %.2g / %d' % (chi2, ndof),
               '#chi^{2} Prob.: %.3g %%' % (100 * prob)],
               position = (0.53, 0.8), textsize = 22).draw()
    ## End of decorate_plot()
    
    
    #_________________________________________________________________________
    def root_latex_for_realvar(self, var, precision=1):
        '''
        Return ROOT Latex string for this variable
        '''
        latex = var.GetName() + ': '
        if var.isConstant():
            latex += (' %.' + '%d' % precision + 'f ') % var.getVal()
        else:
            if var.hasAsymError():
                val = var.getVal()
                lo = var.getVal() + var.getErrorLo()
                hi = var.getVal() + var.getErrorHi()
                bounds = [ROOT.TMath.Abs(x) for x in [lo, val, hi]]
                if lo * hi < 0.0:
                    bounds.append(0.)
                val = ROOT.TMath.Abs(val)
                lo = min(bounds)
                hi = max(bounds)
                elo = val - lo
                ehi = hi - val
                ## Autoprecision
                errors = [e for e in [elo, ehi] if e > 0.001]
                precision = max(0, 1 - int(round(ROOT.TMath.Log10(min(errors)))))
                latex += (' %.' + '%d' % precision + 'f') % val
                latex += ('_{-%.' + '%d' % precision + 'f}') % elo
                latex += ('^{+%.' + '%d' % precision + 'f} ') % ehi
            else:
                latex += (' (%.' + '%d' % precision + 'f') % var.getVal()
                latex += (' #pm %.' + '%d' % precision + 'f) ') % var.getError()
        latex += var.getUnit()
        return latex
        
## End of class XYChi2Fitter      

#==============================================================================
def main():
    '''
    Main entry point of execution.
    '''
    global fitter
    fitter = XYChi2Fitter()
    #fitter.read_data_from_graph_in_file()
    #fitter.dxy.Print()
    fitter.run()
    # canvases.make_plots(['png'])
    # canvases.make_pdf_from_eps()
## End of main()


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
