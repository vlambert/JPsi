'''
Given a selection and data for Zmmg events, build a parametrized KEYS PDF
for the photon resolution shape (Ereco/Etrue - 1) * 100 (in %).  The
shape of the PDF is taken from the RooKeysPdf trained on the simulated
data.  The parametrization introduces dependence on the location
and scale x -> (x-m)/s.  Here, the location and scale parameters are named
m and s.  They are named phoScale and phoRes in the code and they
bear the meaning of the mode and effective sigma of the shape.
The test checks that the PDF shifts and scales correctly as a function
of m and s.
'''
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.cmsstyle as cmsstyle

from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf

##------------------------------------------------------------------------------
## Here starts the meat.
def main():
    define_cuts()
    define_workspace_and_variables()
    #get_data()
    get_saved_data()
    build_model()
    beautify_response_title_and_unit()
    make_scale_dependence_plot()
    make_resolution_scan_plot()
    #plot_multiple_models()
    #plot_shape_and_fit()
    canvases.update()
## End of main()


##------------------------------------------------------------------------------
def define_cuts():
    '''
    Defines selection cuts
    '''
    global cuts, cutlabels
    
    cuts = ['phoIsEB',
            'phoR9 > 0.94',
            '20 < phoPt',
            #'phoPt < 25',
            'mmMass + mmgMass < 190',
            'isFSR',
            'phoGenE > 0',
            ]
    cutlabels = [
        'Barrel',
        'R_{9} > 0.94',
        'E_{T}^{#gamma} #in [20, 25] GeV',
        'm_{#mu#mu} + m_{#mu#mu#gamma} < 190 GeV',
        'FSR'
        ]
## End of define_cuts()        


##------------------------------------------------------------------------------
def define_workspace_and_variables():
    '''
    Creates the default workspace
    '''
    global w, mmgMass, mmMass, phoERes, weight, phoScale, phoRes
    global colors, linestyles
    
    w = ROOT.RooWorkspace('w')

    ## Define data variables
    mmgMass = w.factory('mmgMass[40, 140]')
    mmMass = w.factory('mmMass[10, 140]')
    #phoERes = w.factory('phoERes[-70, 100]')
    phoERes = w.factory('phoERes[-20, 20]')
    weight = w.factory('weight[1]')
    ## Define model parameters
    phoScale = w.factory('phoScale[0,-20,20]')
    phoRes = w.factory('phoRes[5,0.01,50]')

    colors = [
        ROOT.kRed + 1,
        ROOT.kGreen + 2,
        #ROOT.kCyan + 1,
        ROOT.kBlue + 1,
        ROOT.kMagenta + 2,
        ROOT.kBlack,
        ]

## End of define_workspace_and_variables()


##------------------------------------------------------------------------------
def get_data():
    global weight, phoERes
    global data
    ## The TFormula expression defining the data is given in the titles.
    weight.SetTitle('pileup.weight')
    phoERes.SetTitle('100 * phoERes')

    ## Create a preselected tree
    zchain = getChains('v11')['z']
    tree = zchain.CopyTree('&'.join(cuts))
    ## Have to copy aliases by hand
    for a in zchain.GetListOfAliases():
        tree.SetAlias(a.GetName(), a.GetTitle())

    ## Get the nominal dataset
    data = dataset.get(tree=tree, weight=weight, cuts=cuts,
                      variables=[mmgMass, mmMass, phoERes,])

## End of get_data()


##------------------------------------------------------------------------------
def get_saved_data(sourcename='pkeyspdfdemo.root'):
    global data
    sourcefile = ROOT.TFile.Open(sourcename)
    data = sourcefile.Get('demo').data('data').Clone()
    sourcefile.Close()
## End of get_saved_data()
  
##------------------------------------------------------------------------------
def build_model(rho=1.5):
    global phoERes, phoScale, phoRes, data
    global phoEResPdf
    range_save = (phoERes.getMin(), phoERes.getMax())
    ## Enlarge the range of the observable to get vanishing tails.
    #phoERes.setRange(-90, 150)
    phoERes.setRange(-20, 20)
    phoEResPdf = ParametrizedKeysPdf('phoEResPdf', 'phoEResPdf',
                                     phoERes, phoScale, phoRes, data,
                                     ROOT.RooKeysPdf.NoMirror, rho)
    phoERes.setRange(*range_save)
## End of build_model()


##------------------------------------------------------------------------------
def beautify_response_title_and_unit():
    ## Give the titles the original meaning
    phoERes.SetTitle('x = E^{#gamma}/E_{true}^{#gamma} - 1')
    phoERes.setUnit('%')
## End of beautify_response_title_and_unit()


##------------------------------------------------------------------------------
def make_scale_dependence_plot():
    ## Plot the phoEResPdf for various values of the scale
    canvases.next('ShapeScaleScan').SetGrid()
    phoRes.setVal(1)
    plot = phoERes.frame(roo.Range(-6, 8))
    latexlabels = []

    for i, color in enumerate(colors):
        scale = -4 + 2*i
        phoScale.setVal(scale)
        phoEResPdf.plotOn(plot, roo.LineColor(color), roo.Precision(1e-4))
        label = Latex(['s = %d %%' % scale,],
                      position=(0.8, 0.75 - (i+1) * 0.055),
                      textsize=24)
        label.SetTextColor(color)
        latexlabels.append(label)

    # plot.SetTitle('Dependence on Scale')
    plot.SetTitle('')
    plot.GetYaxis().SetTitle('Probability Density f(x|s,r) (1/%)')
    plot.Draw()
    #Latex(cutlabels, position=(0.2, 0.75)).draw()
    Latex(['r = 1 %',], position=(0.8, 0.8), textsize=24).draw()
    for l in latexlabels:
        l.draw()
## Endo fo make_scale_dependence_plot()

##------------------------------------------------------------------------------
def make_resolution_scan_plot():
    ## Plot the phoEResPdf for various values of the effective sigma
    canvases.next('ShapeWidthScan').SetGrid()
    plot = phoERes.frame(roo.Range(-7, 8))
    phoScale.setVal(0)
    latexlabels = []
    for i, color in enumerate(colors):
        res = 1./(1. + 0.25*(2-i))
        phoRes.setVal(res)
        phoEResPdf.plotOn(plot, roo.LineColor(color), roo.Precision(1e-4))
        label = Latex(['r = %.2g %%' % res,],
                      position=(0.75, 0.75 - (i+1) * 0.055),
                      textsize=24)
        label.SetTextColor(color)
        latexlabels.append(label)

    phoScale.setVal(-4)
    for res, color in zip([1./(1. + 0.25*(2-i)) for i in range(5)], colors):
        phoRes.setVal(res)
        phoEResPdf.plotOn(plot, roo.LineColor(color))

    phoScale.setVal(2)
    for res, color in zip([1./(1. + 0.25*(2-i)) for i in range(5)], colors):
        phoRes.setVal(res)
        phoEResPdf.plotOn(plot, roo.LineColor(color))

    #plot.SetTitle('Dependence on Scale and Resolution')
    plot.SetTitle('')
    plot.GetYaxis().SetTitle('Probability Density f(x|s,r) (1/%)')
    plot.Draw()
    # Latex(cutlabels, position=(0.2, 0.75)).draw()
    Latex(['s = -4, 0, 2 %',], position=(0.75, 0.8), textsize=24).draw()
    for l in latexlabels:
        l.draw()
## End of make_resolution_scan_plot()
       
##------------------------------------------------------------------------------
def plot_multiple_models():
    linestyles = [
        ROOT.kDashed,
        ROOT.kSolid,
        ROOT.kDotted,
        #ROOT.kDashDotted,
        #ROOT.kSolid
        ]
    colors = [
        ROOT.kRed + 1,
        ROOT.kBlack,
        ROOT.kBlue + 1,
        ]
    build_multiple_models()
    canvases.next('rho_scan')
    phoERes.setUnit("%")
    plot = phoERes.frame(roo.Range(-5, 5))
    plot.SetTitle("")
    data.plotOn(plot)
    for i, model in enumerate(models):
        model.shape.plotOn(plot, roo.LineColor(colors[i]),
                           roo.LineStyle(linestyles[i]))
    plot.Draw()
## End of plot_multiple_models().


##------------------------------------------------------------------------------
def build_multiple_models(rhos = [1.0, 1.5, 2.0]):
    global phoEResPdf
    global models
    if 'phoEResPdf' in locals():
        phoEResPdf_backup = phoEResPdf
    models = []
    for rho in rhos:
        build_model(rho)
        models.append(phoEResPdf)
    if 'phoEResPdf_backup' in locals():
        phoEResPdf = phoEResPdf_backup
## End of build_multiple_models(rhos)


##------------------------------------------------------------------------------
def plot_shape_and_fit():
    # Extract the MC truth scale and resolution from MC
    phoEResPdf.fitTo(data, roo.PrintLevel(-1), roo.SumW2Error(False))
    phoScaleRef = phoScale.getVal()
    phoResRef = phoScale.getVal()

    # mmgMassPhoSmearE = w.factory('mmgMassPhoSmearE[40, 140]')
    # phoEResSmear = w.factory('phoEResSmear[-80, 110]')

    #------------------------------------------------------------------------------
    # Plot the nominal MC data overlayed with the pdf shape and fit
    canvases.next('pkeyspdf_fit')
    phoERes.setUnit("%")
    plot = phoERes.frame(roo.Range(-5, 5))
    plot.SetTitle('')
    data.plotOn(plot)
    phoEResPdf.shape.plotOn(plot)
    phoEResPdf.plotOn(plot, roo.LineColor(ROOT.kRed), roo.LineStyle(ROOT.kDashed))
    plot.Draw()
    Latex([
        's_{0} = %.3f %%' % phoEResPdf.shapemode,
        's_{fit} = %.3f #pm %.3f %%' % (phoScale.getVal(), phoScale.getError()),
        's_{fit} - s_{0} = %.3f #pm %.3f %%' % (
            phoScale.getVal() - phoEResPdf.shapemode,
            phoScale.getError()
            ),
        'r_{0} = %.3f %%' % phoEResPdf.shapewidth,
        'r_{fit} = %.3f #pm %.3f %%' % (phoRes.getVal(), phoRes.getError()),
        'r_{fit}/r_{0} = %.3f #pm %.3f' % (
            phoRes.getVal() / phoEResPdf.shapewidth,
            phoRes.getError() / phoEResPdf.shapewidth),
        ], position=(0.675, 0.82)).draw()
 ##

##------------------------------------------------------------------------------
## Plot the nominal MC data overlayed with a CB fit

#cb = w.factory('''CBShape::cb(phoERes, mcb[0,-50, 50], scb[3, 0.1, 20],
                              #acb[1.5, -10, 10], ncb[1.5, 0.2, 10])''')

#cb.fitTo(data, roo.Range(-40, 20))

#c1 = canvases.next('nominal_data_log')
#c1.SetLogy()
#c1.SetGrid()
#phoERes.setUnit("%")
#plot = phoERes.frame(roo.Range(-40, 20), roo.SumW2Error(True))
#plot.SetTitle(', '.join(cutlabels[:3]))
#data.plotOn(plot)
#cb.plotOn(plot)
#plot.GetYaxis().SetRangeUser(0.01, 1e4)
#plot.Draw()

#canvases.next('nominal_data_zoom').SetGrid()
#phoERes.setUnit("%")
#plot = phoERes.frame(roo.Range(-7.5, 7.5))
#plot.SetTitle(', '.join(cutlabels[:3]))
#data.plotOn(plot)
#cb.plotOn(plot)
#plot.Draw()

##------------------------------------------------------------------------------
def save_data():
    workspace = ROOT.RooWorkspace('demo')
    workspace.Import(data)
    workspace.writeToFile('pkeyspdfdemo.root')
    

##------------------------------------------------------------------------------
## Footer stuff
canvases.update()
if __name__ == "__main__":
    main()
    import user

