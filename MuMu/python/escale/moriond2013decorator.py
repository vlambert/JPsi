'''
Provides the class Moriond2013Decorator that facilitates the decoration of the PHOSPHOR
fits for the EGM-11-001 paper.
'''

import os
import socket
import ROOT

import JPsi.MuMu.tools as tools
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.egammastyle as egammastyle

from JPsi.MuMu.common.latex import Latex

_hostname_to_hostpath_map = {
    't3-susy.ultralight.org': '/home/veverka/jobs/outputs/',
    'Jan-Veverkas-MacBook-Pro.local': '/Users/veverka/Work/Data/phosphor'
    }

## Path specific to host
_hostpath = _hostname_to_hostpath_map[socket.gethostname()]

## Initial values are set to MC truth for data only
basepath = os.path.join(_hostpath, 'moriond2013')

## Initial values are set to MC truth for both data and MC
# basepath = os.path.join(_hostpath, 'eg_paper_v2')

## In addition to eg_paper_v2, use dr > 0.1 to reduce muon bias
# basepath = os.path.join(_hostpath, 'eg_paper_dr0p1')

###############################################################################
class Moriond2013Decorator:
    #__________________________________________________________________________
    def __init__(
            self,
            name='data_EB_sixie_R9Low_0.94_R9high_999_PtLow_20_PtHigh_999',
            subdir='noregression'
            ):
        '''
        Initializes the canvas.
        '''
        self.name = name
        self.subdir = subdir
                
        ## Open the file
        filename = 'phosphor5_model_and_fit_' + name + '.root'
        filepath = os.path.join(basepath, subdir, filename)
        rootfile = ROOT.TFile.Open(filepath)
        
        ## Get the workspace from the rootfile and close it again.
        self.workspace = rootfile.Get(name + '_workspace').Clone()
        rootfile.Close()
        
        self.old_canvas = self.get_old_canvas()
        self.new_canvas = self.get_new_canvas()
        self.peak_position = self.get_peak_position()
        self.decorate_canvas(self.new_canvas)
    ## End of __init__()
    
    
    #__________________________________________________________________________
    def get_old_canvas(self):
        '''
        Gets the canvas with the fit stored in the workspace.
        '''
        ## Build the name of the canvas depending on whether this is MC or data
        if 'data' in self.name:
            canvas_name = '_'.join(['c', self.name, 'fitSEB_data'])
        else:
            canvas_name = '_'.join(['c', self.name, 'fit'])
        
        ## Retrieve the canvas from the workspace
        return self.workspace.obj(canvas_name)
    ## End of get_old_canvas()
    
    
    #__________________________________________________________________________
    def get_new_canvas(self):
        '''
        Gets the new canvas for the EGM-11-001.
        '''
        ## Clone the old canvas:
        new_canvas = self.get_old_canvas().Clone()
        new_canvas.SetName(self.get_short_name())
        
        ## Store the color and style of the curve
        curve_color_and_style = {}
        for primitive in new_canvas.GetListOfPrimitives():
            if primitive.InheritsFrom('RooCurve'):
                curve_color_and_style[primitive.GetName()] = (
                    primitive.GetLineColor(),
                    primitive.GetLineStyle(),
                    )
                

        ## Force the E/Gamma style
        new_canvas.UseCurrentStyle()
        new_canvas.SetLeftMargin(0.14)
        new_canvas.SetBottomMargin(0.12)

        ## Clean some of the canvas
        for primitive in new_canvas.GetListOfPrimitives():
            ## Remove all the latex
            if primitive.InheritsFrom('TLatex'):
                new_canvas.RecursiveRemove(primitive)
            ## Remove the frame title
            if 'frame' in primitive.GetName():
                primitive.SetTitle('')
            ## Fix the y-axis title offset
            if hasattr(primitive, 'GetYaxis'):
                primitive.GetYaxis().SetTitleOffset(1.4)
            ## Restore the curve color and style
            if primitive.InheritsFrom('RooCurve'):
                color, style = curve_color_and_style[primitive.GetName()]
                primitive.SetLineColor(color)
                primitive.SetLineStyle(style)
               
        
        ## No Title and Grid
        new_canvas.SetGrid(0, 0)
        
        new_canvas.Modified()
        new_canvas.Update()
        
        return new_canvas
    ## End of get_new_canvas()   
    
    #__________________________________________________________________________
    def decorate_canvas(self, canvas):
        '''
        Decorate the new canvas with the results of the fit and other labels.
        '''
        gpad_save = ROOT.gPad
        canvas.cd()
        
        phoScale = self.workspace.var('phoScale')
        phoRes = self.workspace.var('phoRes')
        
        ## Draw fit results:
        Latex([
            #'Fit Parameters:',
            's = %.2f #pm %.2f %%' % (
                phoScale.getVal(), phoScale.getError()
                ),
            'r = %.2f #pm %.2f %%' % (
                phoRes.getVal(), phoRes.getError()
                ),
            ],
            position=(0.59, 0.8), textsize=22, rowheight=0.07
            ).draw()
        
        ## CMS Preliminary:
        
        ## Data or MC
        if 'data' in self.name:
            Latex(['CMS Preliminary, #sqrt{s} = 8 TeV, #int L dt = 19.6 fb^{-1}'],
                  position=(0.15, 0.93), textsize=22).draw()
        else:
            Latex(['CMS Preliminary, #sqrt{s} = 8 TeV, Simulation'],
                  position=(0.15, 0.93), textsize=22).draw()
        

        labels = []
        ## Data or MC
        #if 'data' in self.name:
            #labels.extend([
                #'Data',
                #])
        #else:
            #labels.append('Simulation')
            
        ## EB or EE
        #if 'EB' in self.name:
            #labels.append('ECAL Barrel')
        #else:
            #labels.append('ECAL Endcaps')
        
        #if 'highR9' in self.name:
            #labels.append('R_{9} > 0.94')
        #labels.append('E_{T}^{#gamma} > 20 GeV')
        
        ## Regression or not
        if 'HggRegression' in self.subdir.split('_'):
            labels.append('Regression')
        else:
            labels.append('No Regression')
            
        Latex(labels, position=(0.2, 0.8), textsize=22, 
              rowheight=0.07
              ).draw()
        
        canvas.Modified()
        canvas.Update()
        
        gpad_save.cd()
    ## End of decorate_new_canvas()
        
    #__________________________________________________________________________
    def get_peak_position(self):
        '''
        Returns the apparent position of the peak of the fitted PDF.
        Preconditions: attribute self.workspace is defined.
        '''
        return tools.pdf_mode(self.workspace.pdf('pm'), 
                              self.workspace.var('mmgMass'))
    ## End of peak_position

    #__________________________________________________________________________
    def get_fit_range_num_events(self):
        if not self.old_canvas:
            return None
        primitives = self.old_canvas.GetListOfPrimitives()
        if 'mc' in self.name.split('_'):
            hist_name = 'h_fitdata1'
        else:
            hist_name = 'h_data'
        return primitives.FindObject(hist_name).getFitRangeNEvt()
    ## End of get_fit_range_num_events
    
    #__________________________________________________________________________
    def draw(self):
        self.new_canvas.Draw()
        self.new_canvas.SetWindowSize(600, 600)
        self.new_canvas.Modified()
        self.new_canvas.Update()
    ## End of draw()
    
    #__________________________________________________________________________
    def get_short_name(self):
        newname = '_'.join([self.subdir, self.name])
        ## Remove fragments of the name
        for fragment in '''
                        Zg_2012ABCD_
                        Hgg
                        _newMuCorr_HighR9
                        _EB_sixie_R9Low_0.94_R9high_999_PtLow_20_PtHigh_999
                        '''.split():
            newname = newname.replace(fragment, '')
        return newname
    ## End of get_short_name
        
## End of Moriond2013Decorator.


###############################################################################
def main():
    '''
    Tests the Moriond2013Decorator class.
    '''
    print 'Entering Moriond2013Decorator test...'
    global decorator
    decorator = Moriond2013Decorator()
    decorator.draw()
    print 'Exiting Moriond2013Decorator test with success!'
## End of main()


if __name__ == '__main__':
    main()
    import user
