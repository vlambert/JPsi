## //////////////////////////////////////////////////////////////////////////
## //
## // 'BASIC FUNCTIONALITY' RooFit tutorial macro #109
## //
## // Calculating chi^2 from histograms and curves in RooPlots,
## // making histogram of residual and pull distributions
## //
## //
## //
## // 07/2008 - Wouter Verkerke
## //
## /////////////////////////////////////////////////////////////////////////
##
## #ifndef __CINT__
## #include "RooGlobalFunc.h"
## #endif
## #include "RooRealVar.h"
## #include "RooDataSet.h"
## #include "RooGaussian.h"
## #include "RooConstVar.h"
## #include "TCanvas.h"
## #include "TAxis.h"
## #include "RooPlot.h"
## #include "RooHist.h"
from ROOT import *
## using namespace RooFit ;

import re
import sys
_titlePattern = re.compile("^[A-Z]")

for method in dir(RooFit):
    if callable(getattr(RooFit, method)) and re.search(_titlePattern, method):
        if hasattr(sys.modules[__name__], method):
            print "% not imported since it already exists!" % method
        else:
            setattr(sys.modules[__name__], method, getattr(RooFit, method))

##
##
## void rf109_chi2residpull()

def rf109_chi2residpull():
## {
##
##   // S e t u p   m o d e l
##   // ---------------------
##
##   // Create observables
##   RooRealVar x("x","x",-10,10) ;
    x = RooRealVar ("x","x",-10,10)
##
##   // Create Gaussian
##   RooRealVar sigma("sigma","sigma",3,0.1,10) ;
##   RooRealVar mean("mean","mean",0,-10,10) ;
##   RooGaussian gauss("gauss","gauss",x,RooConst(0),sigma) ;
    sigma = RooRealVar("sigma","sigma",3,0.1,10)
    mean = RooRealVar("mean","mean",0,-10,10)
    gauss = RooGaussian("gauss","gauss",x,RooConst(0),sigma)
##
##   // Generate a sample of 1000 events with sigma=3
##   RooDataSet* data = gauss.generate(x,10000) ;
    data = gauss.generate(RooArgSet(x), 10000)
##
##   // Change sigma to 3.15
##   sigma=3.15 ;
    sigma.setVal(3.15)
##
##
##   // P l o t   d a t a   a n d   s l i g h t l y   d i s t o r t e d   m o d e l
##   // ---------------------------------------------------------------------------
##
##   // Overlay projection of gauss with sigma=3.15 on data with sigma=3.0
##   RooPlot* frame1 = x.frame(Title("Data with distorted Gaussian pdf"),Bins(40)) ;
##   data->plotOn(frame1,DataError(RooAbsData::SumW2)) ;
##   gauss.plotOn(frame1) ;
    frame1 = x.frame(Title("Data with distorted Gaussian pdf"),Bins(40))
    data.plotOn(frame1, DataError(RooAbsData.SumW2) )
    gauss.plotOn(frame1)
##
##
##   // C a l c u l a t e   c h i ^ 2
##   // ------------------------------
##
##   // Show the chi^2 of the curve w.r.t. the histogram
##   // If multiple curves or datasets live in the frame you can specify
##   // the name of the relevant curve and/or dataset in chiSquare()
##   cout << "chi^2 = " << frame1->chiSquare() << endl ;
    print 'chi^2 =', frame1.chiSquare()
##
##
##   // S h o w   r e s i d u a l   a n d   p u l l   d i s t s
##   // -------------------------------------------------------
##
##   // Construct a histogram with the residuals of the data w.r.t. the curve
##   RooHist* hresid = frame1->residHist() ;
    hresid = frame1.residHist()
##
##   // Construct a histogram with the pulls of the data w.r.t the curve
##   RooHist* hpull = frame1->pullHist() ;
    hpull = frame1.pullHist()
##
##   // Create a new frame to draw the residual distribution and add the distribution to the frame
##   RooPlot* frame2 = x.frame(Title("Residual Distribution")) ;
##   frame2->addPlotable(hresid,"P") ;
    frame2 = x.frame(Title("Residual Distribution"))
    frame2.addPlotable(hresid,"P")
##
##   // Create a new frame to draw the pull distribution and add the distribution to the frame
##   RooPlot* frame3 = x.frame(Title("Pull Distribution")) ;
##   frame3->addPlotable(hpull,"P") ;
    frame3 = x.frame(Title("Pull Distribution"))
    frame3.addPlotable(hpull,"P")
##
##
##
##   TCanvas* c = new TCanvas("rf109_chi2residpull","rf109_chi2residpull",900,300) ;
##   c->Divide(3) ;
##   c->cd(1) ; gPad->SetLeftMargin(0.15) ; frame1->GetYaxis()->SetTitleOffset(1.6) ; frame1->Draw() ;
##   c->cd(2) ; gPad->SetLeftMargin(0.15) ; frame2->GetYaxis()->SetTitleOffset(1.6) ; frame2->Draw() ;
##   c->cd(3) ; gPad->SetLeftMargin(0.15) ; frame3->GetYaxis()->SetTitleOffset(1.6) ; frame3->Draw() ;
    global c
    c = TCanvas("rf109_chi2residpull","rf109_chi2residpull",900,300)
    c.Divide(3)
    c.cd(1); gPad.SetLeftMargin(0.15); frame1.GetYaxis().SetTitleOffset(1.6); frame1.Draw()
    c.cd(2); gPad.SetLeftMargin(0.15); frame2.GetYaxis().SetTitleOffset(1.6); frame2.Draw()
    c.cd(3); gPad.SetLeftMargin(0.15); frame3.GetYaxis().SetTitleOffset(1.6); frame3.Draw()
##
## }

if __name__ == '__main__':
    rf109_chi2residpull()
    import user
