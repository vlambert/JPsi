from ROOT import *
import re
import sys
_titlePattern = re.compile("^[A-Z]")

for method in dir(RooFit):
    if callable(getattr(RooFit, method)) and re.search(_titlePattern, method):
        if hasattr(sys.modules[__name__], method):
            print "% not imported since it already exists!" % method
        else:
            setattr(sys.modules[__name__], method, getattr(RooFit, method))

gStyle.SetOptTitle(0)

#------------------------------------------------------------------------------
def customizeAxis(axis, labelOffset=0.005, titleOffset=1):
    ## Switch to fixed pixel size fonts
    precision = axis.GetLabelFont() % 10
    axis.SetLabelFont( axis.GetLabelFont() - precision + 3 )
    axis.SetLabelSize(18)
    precision = axis.GetTitleFont() % 10
    axis.SetTitleFont( axis.GetTitleFont() - precision + 3)
    axis.SetTitleSize(18)
    ## Scale offsets
    axis.SetLabelOffset(labelOffset )
    axis.SetTitleOffset( titleOffset )
# end of customize axis

#------------------------------------------------------------------------------
def customPadDivide(pad, topMargin = 0.025, bottomMargin = 0.1,
                    leftMargin = 0.2, rightMargin = 0.05):
    ''' Divides the given pad in 3 sub-pads that are on top of each other
    w/o spaces, share the x-axis and the sizes of their plot area
    along y are in the ratio 2:1:1. This is meant to show a fit to data
    on top, residuals in the middle and pulls in the bottom.
    The optional arguments are margins as fractions of the original pad
    and are recomputed and applied to the sub-pads. The three sub-pads
    given on return have to be assign to a variable in order for the pads
    not to be destroyed by python's garbage collector.'''

    y1 = 0.5*(1 - topMargin + bottomMargin)
    y2 = 0.25 * (1 - topMargin + 3*bottomMargin)

    padsav = gPad
    pad.cd()

    name = pad.GetName() + '_1'
    pad1 = TPad(name, name, 0, y1, 1, 1)
    pad1.SetNumber(1)
    pad1.SetTopMargin( topMargin / (1. - y1) )
    pad1.SetBottomMargin(0)
    pad1.SetLeftMargin(leftMargin)
    pad1.SetRightMargin(rightMargin)
    pad1.Draw()

    name = pad.GetName() + '_2'
    pad2 = TPad(name, name, 0, y2, 1, y1)
    pad2.SetNumber(2)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0)
    pad2.SetLeftMargin(leftMargin)
    pad2.SetRightMargin(rightMargin)
    pad2.Draw()

    name = pad.GetName() + '_3'
    pad3 = TPad(name, name, 0, 0, 1, y2)
    pad3.SetNumber(3)
    pad3.SetTopMargin(0)
    pad3.SetBottomMargin(bottomMargin/y2)
    pad3.SetLeftMargin(leftMargin)
    pad3.SetRightMargin(rightMargin)
    pad3.Draw()

    # Clean up and exit
    pad.Modified()
    if padsav:
        padsav.cd()
    return pad1, pad2, pad3
## end of customPadDivide


def main():
    ## S e t u p   m o d e l
    ## ---------------------
    ## Create observables
    x = RooRealVar ("x","x",-10,10)

    ## Create Gaussian
    sigma = RooRealVar("sigma","sigma",3,0.1,10)
    mean = RooRealVar("mean","mean",0,-10,10)
    gauss = RooGaussian("gauss","gauss",x,RooConst(0),sigma)

    ## Generate a sample of 1000 events with sigma=3
    data = gauss.generate(RooArgSet(x), 10000)

    ## Change sigma to 3.15
    # sigma.setVal(3.15)

    ## Fit the model to the data
    gauss.fitTo(data)


    ## P l o t   d a t a   a n d   s l i g h t l y   d i s t o r t e d   m o d e l
    ## ---------------------------------------------------------------------------
    ##
    ## Overlay projection of gauss with sigma=3.15 on data with sigma=3.0
    frame1 = x.frame(Title("Data with distorted Gaussian pdf"),Bins(40))
    data.plotOn(frame1, DataError(RooAbsData.SumW2) )
    gauss.plotOn(frame1)


    ## C a l c u l a t e   c h i ^ 2
    ## ------------------------------
    ##
    ## Show the chi^2 of the curve w.r.t. the histogram
    ## If multiple curves or datasets live in the frame you can specify
    ## the name of the relevant curve and/or dataset in chiSquare()
    print 'chi^2 =', frame1.chiSquare()


    ## S h o w   r e s i d u a l   a n d   p u l l   d i s t s
    ## -------------------------------------------------------
    ##
    ## Construct a histogram with the residuals of the data w.r.t. the curve
    hresid = frame1.residHist()

    ## Construct a histogram with the pulls of the data w.r.t the curve
    hpull = frame1.pullHist()

    ## Create a new frame to draw the residual distribution and
    ## add the distribution to the frame
    frame2 = x.frame(Title("Residual Distribution"))
    frame2.addPlotable(hresid,"P")
    frame2.GetYaxis().SetTitle("Residuals")

    ## Create a new frame to draw the pull distribution and
    ## add the distribution to the frame
    frame3 = x.frame(Title("Pull Distribution"))
    frame3.addPlotable(hpull,"P")
    frame3.GetYaxis().SetTitle("Pulls")


    customizeAxis(frame1.GetYaxis(), 0.01, 2.7)
    customizeAxis(frame2.GetYaxis(), 0.01, 2.5)
    customizeAxis(frame3.GetYaxis(), 0.01, 2.3)
    customizeAxis(frame3.GetXaxis(), 0.01, 3)

    topMargin = 0.025
    bottomMargin = 0.1
    leftMargin = 0.2
    rightMargin = 0.05

    global c, pads

    c = TCanvas("chi2residpull","chi2residpull",300, 600)

    gStyle.SetPadBorderMode(0)
    gStyle.SetOptStat(0)
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)

    pads = customPadDivide(c, topMargin, bottomMargin, leftMargin, rightMargin)

    for p, f in [ (pads[0], frame1),
                  (pads[1], frame2),
                  (pads[2], frame3), ]:
        p.cd()
        p.SetGrid()
        f.GetYaxis().CenterTitle()
        f.Draw()

    c.Update()
## end of `main'

if __name__ == '__main__':
    main()
    import user
