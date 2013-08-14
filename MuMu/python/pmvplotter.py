import os
import JPsi.MuMu.tools as tools
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.pmvTrees as pmvTrees

from array import array
from ROOT import *
from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.legend import Legend

## Format <variable>_<subdetector>
## Supported values of variable: sihih, r9
## Supported values of subdetector: EB, EE
name = 'sihih_EE'

realData = "data"
mcSamples = "z qcd w tt".split()

cweight = {
    "data": 1.,
    ## Fall 11 MC weights
    'z'  :  0.258663958360874,
    'qcd': 64.4429447069508,
    'w'  :  1.77770452633322,
    'tt' :  0.046348624723768,
}


puWeight = {
    'data': '1.',

    'z'  : 'pileup.weight',
    'tt' : 'pileup.weight',
    'w'  : 'pileup.weight',
    'qcd': 'pileup.weight',
}

colors = {
    "z"     : kAzure - 9,
    'zj'    : kSpring + 5,
    "qcd"   : kYellow - 7,
    "tt"    : kOrange - 2,
    "w"     : kRed -3,
}

legendTitles = {
    "z"   : "FSR",
    'zj'  : 'Z+jets',
    "qcd" : "QCD",
    "tt"  : "t#bar{t}",
    "w"   : "W",
}

histograms = {}

## gStyle.SetPadRightMargin(0.05)
#print 'PadTopMargin:', gStyle.GetPadTopMargin()
#gStyle.SetPadTopMargin(0.15)
#print 'PadTopMargin:', gStyle.GetPadTopMargin()

latexLabel = TLatex()
latexLabel.SetNDC()

chains = pmvTrees.getChains('v19')
tree = {}
for tag in 'data z qcd w tt'.split():
  tree[tag] = chains[tag]

#______________________________________________________________________________
def get_selection():
    '''
    Return the TTree selection expression based on the name.
    '''
    tags = name.split('_')

    cuts = [
        'phoPt > 25',
        'scEt > 10',
        'phoHoE < 0.5',
        ]
    
    if 'EB' in tags:
        cuts.append('phoIsEB')
    elif 'EE' in tags:
        cuts.append('!phoIsEB')
    
    ## Muon bias removal for sihih in EB
    if 'EB' in tags and 'sihih' in tags:
        cuts.append('abs(abs(muNearIEtaX - phoIEtaX) - 2) > 1')

    ## Apply the high R9 based on the subdetector
    if 'highR9' in tags:
        if 'EE' in tags:
            cuts.append('phoR9 > 0.95')
        else:
            cuts.append('phoR9 > 0.94')

    return '&'.join(cuts)
## End of get_selection(..)


#______________________________________________________________________________
def get_plotted_variable_in_mc_and_data():
    '''
    Returns a pair of RooRealVars defining the plotted variable in MC and data.
    Plotted expression is in the name, title, ranges in number of bins for 
    the histogram are taken from the RooRealVar    
    '''
    tags = name.split('_')

    if 'sihih' in tags:
        if 'EB' in tags:
            ## Shifting for Barrel from AN 11/251 Vg
            if 'nocorrection' in tags: 
                var = RooRealVar("1000*phoSigmaIetaIeta",
                                 "Photon #sigma_{i#etai#eta} #times 10^{3}", 3, 15)
            else:
                var = RooRealVar("1000*phoSigmaIetaIeta - 0.11",
                                 "Photon #sigma_{i#etai#eta} #times 10^{3}", 3, 15)
            varData = RooRealVar("1000*phoSigmaIetaIeta",
                                "Photon #sigma_{i#etai#eta} #times 10^{3}", 3, 15)
            var.setBins(48)
            
        else:
            ## Shifting for Endcap from AN 11/251 Vg
            #var = RooRealVar("1000*phoSigmaIetaIeta - 0.16",
                            #"Photon #sigma_{i#etai#eta} #times 10^{3}", 10, 40)
            #varData = RooRealVar("1000*phoSigmaIetaIeta",
                                #"Photon #sigma_{i#etai#eta} #times 10^{3}", 10, 40)
            ## Same binning as Poter
            if 'nocorrection' in tags: 
                var = RooRealVar("1000*phoSigmaIetaIeta",
                                 "Photon #sigma_{i#etai#eta} #times 10^{3}", 9.5, 39.5)
            else:
                var = RooRealVar("1000*phoSigmaIetaIeta - 0.16",
                                 "Photon #sigma_{i#etai#eta} #times 10^{3}", 9.5, 39.5)
            varData = RooRealVar("1000*phoSigmaIetaIeta",
                                "Photon #sigma_{i#etai#eta} #times 10^{3}", 9.5, 39.5)
            var.setBins(40)
    
    elif 'r9' in tags:
        if 'zoom' in tags:
            if 'nocorrection' in tags: 
                var = RooRealVar("phoR9", "photon R_{9}", 0.85, 1.)
            else:
                var = RooRealVar("1.0035*phoR9", "photon R_{9}", 0.85, 1.)
            varData = RooRealVar("phoR9", "photon R_{9}", 0.85, 1.)
            var.setBins(60)
        else:
            if 'nocorrection' in tags:
                var = RooRealVar("phoR9", "photon R_{9}", 0.3, 1.1)
            else:
                var = RooRealVar("1.0035*phoR9", "photon R_{9}", 0.3, 1.1)              
            varData = RooRealVar("phoR9", "photon R_{9}", 0.3, 1.1)
            var.setBins(80)
    
    return var, varData
    
## End of get_plotted_variable_in_mc_and_data()


#______________________________________________________________________________
def get_histograms():
    '''
    Returns the data histogram and the list of MC histogram stacks.
    '''
    (var, varData) = get_plotted_variable_in_mc_and_data()    
    selection = get_selection()
    
    h_temp = TH1F("h_temp", "", var.getBins(), var.getMin(), var.getMax() )
    h_temp.GetXaxis().SetTitle( var.GetTitle() )
    if 'EB' in name.split('_'):
        h_temp.GetYaxis().SetTitle("Events / 0.25")
    else:
        h_temp.GetYaxis().SetTitle("Events / 0.5")
    h_temp.SetTitle("")
    h_temp.SetStats(0)
    histos = {}
    for tag, t in tree.items():
        sel = '(%s)' % (selection,)
        if tag == 'z':
            sel += ' && isFSR'
        if tag == 'data':
            continue
        sel = '%s * %f * (%s) ' % (puWeight[tag], cweight[tag], sel,)
        print tag, ':', sel
        t.Draw(var.GetName() + '>>h_temp', sel )
        hname = '_'.join(['h', name, tag])
        histos[tag] = h_temp.Clone(hname)

    sel = "%s * %f * ( (%s) && !isFSR )" % (puWeight['z'], cweight['z'], selection)
    tree['z'].Draw(var.GetName() + '>>h_temp', sel)
    hname = '_'.join(['h', name, 'zj'])
    histos['zj'] = h_temp.Clone(hname)

    tree['data'].Draw(varData.GetName() + '>>h_temp', selection )
    hname = '_'.join(['h', name, 'data'])
    hdata = h_temp.Clone(hname)

    for tag in mcSamples + ['zj']:
        histos[tag].SetFillColor( colors[tag] )
        histos[tag].SetLineColor( colors[tag] )


    ## Sort histos
    sortedHistos = histos.values()
    sortedHistos.sort( key=lambda h: h.Integral() )

    ## Make stacked histos (THStack can't redraw axis!? -> roottalk)
    hstacks = []
    for h in sortedHistos:
        hstemp = h.Clone( h.GetName().replace("h_", "hs_") )
        if hstacks:
            hstemp.Add( hstacks[-1] )
        hstacks.append( hstemp )

    ## Draw
    hstacks.reverse()

    return hdata, hstacks
## End of get_histograms()


#______________________________________________________________________________
def normalize_mc_to_data(hdata, hstacks):
    '''
    Normalizes MC to data.
    '''
    nbins = hstacks[0].GetXaxis().GetNbins()
    mcIntegral = hstacks[0].Integral( 1, nbins )
    scale = hdata.Integral(1, nbins ) / mcIntegral
    #scale = 1.0
    print "Scaling MC by: ", scale
    for hist in hstacks:
        hist.Scale( scale )
## End of normalize_mc_to_data()


#______________________________________________________________________________
def get_yrange():
    '''
    Returns the y-axis range based on name.
    '''
    tags = name.split('_')
    
    if 'sihih' in tags:
        if 'EB' in tags:
            if 'highR9' in tags:
                yrange = (1e-4, 450.)
            else:
                yrange = (1e-4, 700.)
        else:
            if 'highR9' in tags:
                yrange = (1e-4, 140.)
            else:
                yrange = (1e-4, 375.)
    elif 'r9' in name.split('_'):
        if 'zoom' in name.split('_'):
            if 'EB' in name:
                yrange = (1e-4, 325.)
            else:
                yrange = (1e-4, 100.)
        else:
            if 'EB' in name:
                yrange = (1e-4, 1200.)
            else:
                yrange = (1e-4, 300.)
                
    return yrange
## End of get_yrange()


#______________________________________________________________________________
def get_canvas():
    '''
    Returns the canvas based on the name.
    '''
    c1 = canvases.next(name, name)
    c1.SetTopMargin(0.1)
    return c1
## End of get_canvas()


#______________________________________________________________________________
def draw_histograms(hdata, hstacks):
    '''
    Draws histograms on the current canvas.
    '''
    ## Draw MC
    yrange = get_yrange()
    for h in hstacks:
        h.GetYaxis().SetRangeUser(*yrange)
        if hstacks.index(h) == 0: 
            h.Draw()
        else:
            h.Draw("same")

    ## Draw data
    hdata.Draw("e1 same")
## End of draw_histograms()


#______________________________________________________________________________
def decorate_canvas():
    '''
    Writes various Latex labels on the current canvas.
    '''
    tags = name.split('_')
  
    ## CMS Preliminary:
    Latex(['CMS Preliminary 2011,  #sqrt{s} = 7 TeV'], 
          position=(0.17, 0.93), textsize=22).draw()

    labels = [
        'L = 4.9 fb^{-1}',
        'E_{T}^{#gamma} > 25 GeV',
        ]

    ## EB or EE
    if 'EB' in tags:
        if 'highR9' in tags:
            labels.append('R_{9} > 0.94')
        labels.append('ECAL Barrel')
    elif 'EE' in tags:
        if 'highR9' in tags:
            labels.append('R_{9} > 0.95')
        labels.append('ECAL Endcaps')

    if 'nocorrection' in tags:
        labels.append('No MC Correction')

    Latex(labels, position=(0.22, 0.8), textsize=22, 
          rowheight=0.07
          ).draw()
## End of decorate_canvas()
     

#______________________________________________________________________________
def get_legend(hdata, hstacks):
    '''
    Returns legend for the histograms.
    '''
    tags = name.split('_')

    if 'sihih' in tags:
        layout = (0.65, 0.55, 0.9, 0.85)
    elif 'r9' in tags:
        if 'zoom' in tags:
            layout = (0.22, 0.3, 0.47, 0.6)          
        else:
            layout = (0.22, 0.3, 0.47, 0.6)
    
    legend = Legend([hdata] + hstacks[:3],
                    ['Data', 'Z #rightarrow #mu#mu#gamma',
                    'Z #rightarrow #mu#mu + jets', 't#bar{t}'],
                    position = layout,
                    optlist = ['pl', 'f', 'f', 'f']
                    )
            
    return legend
## End of get_legend()


#______________________________________________________________________________
def print_yields_and_purities(hdata, hstacks):
    '''
    Prints yields and purities.
    '''
    nbins = hstacks[0].GetXaxis().GetNbins()
    ## Print yields:
    print "--++ Yields and Purities"
    for i in range( len(hstacks) ):
        if i < len(hstacks) - 1:
            res = hstacks[i].Integral() - hstacks[i+1].Integral()
        else:
            res = hstacks[i].Integral()
        print "%10s %10.2f %10.4g%%" % ( 
                hstacks[i].GetName().replace('hs_', ''),
                res,
                100. * res/hdata.Integral(1, nbins) 
                )


#______________________________________________________________________________
def make_plot(newname = None):
    global name
    
    if newname:
        name = newname
    
    c1 = get_canvas()    

    global hdata, hstacks
    (hdata, hstacks) = histograms[name] = get_histograms()
    normalize_mc_to_data(hdata, hstacks)
    draw_histograms(hdata, hstacks)
    
    legend = get_legend(hdata, hstacks)
    legend.draw()

    decorate_canvas()

    c1.RedrawAxis()
    c1.Update()

    print_yields_and_purities(hdata, hstacks)
## End of make_plot()
    

#______________________________________________________________________________
if __name__ == '__main__':
    make_plot()
    import user
    
