'''
Provides the class Decorator that facilitates the decoration of the PHOSPHOR
fits for the EWK-11-009 paper.
'''

import os
import socket
import ROOT

import JPsi.MuMu.tools as tools
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.latex import Latex

_hostname_to_hostpath_map = {
    't3-susy.ultralight.org': '/raid2/veverka/phosphor',
    'Jan-Veverkas-MacBook-Pro.local': '/Users/veverka/Work/Data/phosphor'
    }

## Path specific to host
_hostpath = _hostname_to_hostpath_map[socket.gethostname()]

## Initial values are set to MC truth for data only
basepath = os.path.join(_hostpath, 'sge_correction')

## Initial values are set to MC truth for both data and MC
# basepath = os.path.join(_hostpath, 'eg_paper_v2')

## In addition to eg_paper_v2, use dr > 0.1 to reduce muon bias
# basepath = os.path.join(_hostpath, 'eg_paper_dr0p1')

###############################################################################
class Decorator:
    #__________________________________________________________________________
    def __init__(self, name='sge_data_EB_pt15to20_v13'):
        '''
        Initializes the canvas.
        '''
        self.name = name
        self.latex_labels = []
                
        ## Open the file
        filename = ('phosphor5_model_and_fit_'
                    'test_mc_EE_highR9_pt30to999_v13_evt1of4.root')
        filepath = os.path.join(basepath, name, filename)
        rootfile = ROOT.TFile.Open(filepath)
        
        ## Get the workspace from the rootfile and close it again.
        self.workspace = rootfile.Get(name + '_workspace').Clone()
        rootfile.Close()
        
        self.old_canvas = self.get_old_canvas()
        self.new_canvas = self.get_new_canvas()
        # self.peak_position = self.get_peak_position()
        self.decorate_canvas(self.new_canvas)
    ## End of __init__()
    
    
    #__________________________________________________________________________
    def get_old_canvas(self):
        '''
        Gets the canvas with the fit stored in the workspace.
        '''
        ## Build the name of the canvas depending on whether this is MC or data
        if 'data' in self.name:
            canvas_name = '_'.join(['c', self.name, 'data'])
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
        new_canvas = self.get_old_canvas().Clone(self.name + '_' + 'egm')
        
        ## Clean some of the canvas
        for primitive in new_canvas.GetListOfPrimitives():
            ## Remove all the latex
            if primitive.InheritsFrom('TLatex'):
                new_canvas.RecursiveRemove(primitive)
            ## Remove the frame title
            if 'frame' in primitive.GetName():
                primitive.SetTitle('')
        
        ## No Title and Grid
        new_canvas.SetGrid(0, 0)
        
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
            'Fit Parameters:',
            '#mu(E_{#gamma}) = %.2f #pm %.2f %%' % (
                phoScale.getVal(), phoScale.getError()
                ),
            '#sigma(E_{#gamma}) = %.2f #pm %.2f %%' % (
                phoRes.getVal(), phoRes.getError()
                ),
            ],
            position=(0.65, 0.8), textsize=22, rowheight=0.07,
            textfont=42
            ).draw()
        
        ## CMS Preliminary:
        Latex(['CMS 2011,  #sqrt{s} = 7 TeV'], 
              position=(0.17, 0.93), textsize=22,
              textfont=42).draw()        

        labels = []
        tokens = self.name.split('_')
        
        ## Data or MC
        if 'data' in tokens:
            labels.append('Data, L = 4.89 fb^{-1}')
        else:
            labels.append('Simulation')
            
        ## EB or EE
        if 'EB' in tokens:
            labels.append('ECAL Barrel')
        else:
            labels.append('ECAL Endcaps')
        
        if 'highR9' in tokens:
            labels.append('R_{9} > 0.94')
            
        ## Find the name token with the pt information
        pt_token = ''
        for token in tokens:
            print token
            if ('pt' in token) and ('to' in token):
                pt_token = token
                print 'Pt range:', pt_token
        if pt_token:
            ## We found it.  Parse it to get the pt range
            lo, hi = pt_token.replace('pt', '').split('to')
            labels.append('Photon E_{T} #in [%s, %s) GeV' % (lo, hi))
                
        Latex(labels, position=(0.22, 0.8), textsize=22, 
              rowheight=0.07, textfont = 42
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
    
## End of EgmDecorator.


###############################################################################
def main():
    '''
    Tests the EgmDecorator class.
    '''
    print 'Entering EgmDecorator test...'
    global decorator
    decorator = Decorator()
    decorator.old_canvas.Draw()
    decorator.new_canvas.Draw()
    print 'Exiting EgmDecorator test with success!'
## End of main()


if __name__ == '__main__':
    main()
    import user
