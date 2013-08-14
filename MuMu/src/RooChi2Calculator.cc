#include "JPsi/MuMu/interface/RooChi2Calculator.h"
/**
  * Implementation of the RooChi2Calculator calss
  * Jan Veverka, Caltech, 26 October 2011
  */

#include <iostream>

#include "RooCurve.h"
#include "RooMsgService.h"
#include "TMath.h"

using namespace cit;
using namespace std;

/// Make this a ROOT class
ClassImp(RooChi2Calculator)

///----------------------------------------------------------------------------
RooChi2Calculator::RooChi2Calculator(RooPlot const * plot) :
  plot_(plot),
  _nominalBinWidth(1)
{}


///----------------------------------------------------------------------------
RooChi2Calculator::~RooChi2Calculator()
{}


///----------------------------------------------------------------------------
RooHist*
RooChi2Calculator::residHist(const char *histname, const char* curvename,
                             bool normalize, bool renormalize)
const
{
  // Create and return RooHist containing  residuals w.r.t to given curve->
  // If normalize is true, the residuals are normalized by the histogram
  // errors creating a RooHist with pull values


  // Find curve object
  RooCurve* curve = (RooCurve*) plot_->findObject(curvename,
                                                  RooCurve::Class());
  if (!curve) {
    coutE(InputArguments) << "cit::RooChi2Calculator(plotname=" << plot_->GetName()
                          << ")::residHist(..) cannot find curve" << endl ;
    return 0 ;
  }

  // Find histogram object
  RooHist* hist = (RooHist*) plot_->findObject(histname,
                                               RooHist::Class()) ;
  if (!hist) {
    coutE(InputArguments) << "cit::RooChi2Calculator(plotname=" << plot_->GetName()
                          << ")::residHist(..) cannot find histogram" << endl ;
    return 0 ;
  }


  // Copy all non-content properties from hist
  RooHist* ret = new RooHist(_nominalBinWidth) ;
  if (normalize) {
    ret->SetName(Form("pull_%s_%s", hist->GetName(), curve->GetName())) ;
    ret->SetTitle(Form("Pull of %s and %s", hist->GetTitle(),
                       curve->GetTitle())) ;
  } else {
    ret->SetName(Form("resid_%s_%s", hist->GetName(), curve->GetName())) ;
    ret->SetTitle(Form("Residual of %s and %s", hist->GetTitle(),
                       curve->GetTitle())) ;
  }

  // Determine range of curve
  Double_t xstart, xstop, y ;
#if ROOT_VERSION_CODE >= ROOT_VERSION(4,0,1)
  curve->GetPoint(0, xstart, y) ;
  curve->GetPoint(curve->GetN()-1,xstop,y) ;
#else
  const_cast<RooCurve&>(curve).GetPoint(0, xstart, y) ;
  const_cast<RooCurve&>(curve).GetPoint(curve->GetN()-1, xstop, y) ;
#endif
  // cout << "cit::RooChi2Calculator::residHist dumping curve:\n";
  // for (int i=0; i<curve->GetN(); ++i){
  //   Double_t xi, yi;
  //   curve->GetPoint(i, xi, yi);
  //   printf("i=%d x,y: %.3g, %.3g\n", i, xi, yi);
  // }

  // cout << "cit::RooChi2Calculator::residHist  adding bins with error:\n";
  double observedTotal(0), expectedTotal(0);
  if (renormalize) {
    for(Int_t i=0 ; i < hist->GetN() ; i++) {
      // Make sure that expected and observed are normalized to the same
      // number of events
      Double_t x, point;
#if ROOT_VERSION_CODE >= ROOT_VERSION(4,0,1)
      hist->GetPoint(i,x,point) ;
#else
      const_cast<RooHist&>(hist).GetPoint(i,x,point) ;
#endif
      Double_t xl = x - hist->GetErrorXlow(i);
      Double_t xh = x + hist->GetErrorXhigh(i);

      // Only calculate pull for bins inside curve range
      if (xl < xstart || xstop < xh) continue ;

      Double_t norm = (xh - xl) / plot_->getFitRangeBinW();
      Double_t norml = (x - xl) / plot_->getFitRangeBinW();
      Double_t normh = (xh - x) / plot_->getFitRangeBinW();
      point *= norm;

      // Start a hack to work around a bug in RooCurve::interpolate
      // that sometimes gives a wrong result.
      // Correcting the expected number of events in this bin for the non-uniform
      // bin width by multiplying with the norm.
      Double_t yexp  = curve->average(xl, xh) * norm;
      Double_t yexp2 = curve->average(xl, x ) * norml + 
	curve->average(x , xh) * normh;
      if (yexp + yexp2 > 0 &&
	  TMath::Abs((yexp - yexp2) / (yexp + yexp2)) > 0.1) {
	yexp = curve->interpolate(x) * norm;
      }
      // End of hack around the bug in RooCurve::interpolate
      observedTotal += point;
      expectedTotal += yexp;
    } // loop over points
  } // if (renormalize)

  // Add histograms, calculate Poisson confidence interval on sum value
  for(Int_t i=0 ; i < hist->GetN() ; i++) {
    Double_t x, point;
#if ROOT_VERSION_CODE >= ROOT_VERSION(4,0,1)
    hist->GetPoint(i,x,point) ;
#else
    const_cast<RooHist&>(hist).GetPoint(i,x,point) ;
#endif
    Double_t xl = x - hist->GetErrorXlow(i);
    Double_t xh = x + hist->GetErrorXhigh(i);

    // Only calculate pull for bins inside curve range
    if (xl < xstart || xstop < xh) continue ;

    Double_t norm = (xh - xl) / plot_->getFitRangeBinW();
    Double_t norml = (x - xl) / plot_->getFitRangeBinW();
    Double_t normh = (xh - x) / plot_->getFitRangeBinW();
    point *= norm;

    // Start a hack to work around a bug in RooCurve::interpolate
    // that sometimes gives a wrong result.
    // Correcting the expected number of events in this bin for the non-uniform
    // bin width by multiplying with the norm.
    Double_t yexp  = curve->average(xl, xh) * norm;
    Double_t yexp2 = curve->average(xl, x ) * norml + 
                     curve->average(x , xh) * normh;
    if (yexp + yexp2 > 0 &&
	TMath::Abs((yexp - yexp2) / (yexp + yexp2)) > 0.1) {
      yexp = curve->interpolate(x) * norm;
    }
    // End of hack around the bug in RooCurve::interpolate

    Double_t yexpected = yexp;
    if (renormalize & expectedTotal > 0) {
      yexpected = observedTotal / expectedTotal * yexpected;
    }

    Double_t yy = point - yexpected;
    // Normalize to the number of events per bin taking into account
    // variable bin width.
    Double_t dy = TMath::Sqrt(yexpected);
    if (normalize) {
	if (dy==0.) {
	  coutW(Plotting) << "cit::RooChi2Calculator::residHist(histname ="
                          << hist->GetName() << ", ...) WARNING: point "
                          << i << " has zero error, setting residual to zero"
                          << endl ;
	  yy=0 ;
	  dy=0 ;
	} else {
	  yy /= dy;
	  dy = 1.;
	}
    }
    // printf("bin=%3d n=%5.3g nu=%5.3g x=%5.3g .. %5.3g y=%5.3g +/- %5.3g "
    //	   "norm=%5.3g\n", i, point, yexpected, xl, xh, yy, dy, norm);
    ret->addBinWithError(x,yy,dy,dy);
  }

  return ret;
}


///----------------------------------------------------------------------------
Double_t
RooChi2Calculator::chiSquare(const char* pdfname, const char* histname,
			     int nFitParam, bool renormalize) const
{
  // Calculate the chi^2/NDOF of this curve with respect to the histogram
  // 'hist' accounting nFitParam floating parameters in case the curve
  // was the result of a fit

  // Find curve object
  RooCurve* curve = (RooCurve*) plot_->findObject(pdfname,
                                                  RooCurve::Class());
  if (!curve) {
    coutE(InputArguments) << "cit::RooChi2Calculator(plotname=" << plot_->GetName()
                          << ")::chiSquare(..) cannot find curve" << endl ;
    return 0 ;
  }

  // Find histogram object
  RooHist* hist = (RooHist*) plot_->findObject(histname,
                                               RooHist::Class()) ;
  if (!hist) {
    coutE(InputArguments) << "cit::RooChi2Calculator(plotname=" << plot_->GetName()
                          << ")::chiSquare(..) cannot find histogram" << endl ;
    return 0 ;
  }


  Int_t i,np = hist->GetN() ;
  Double_t x,y,/*eyl,eyh,*/ xl,xh ;

  // Find starting and ending bin of histogram based on range of RooCurve
  Double_t xstart,xstop ;

#if ROOT_VERSION_CODE >= ROOT_VERSION(4,0,1)
  curve->GetPoint(0,xstart,y) ;
  curve->GetPoint(curve->GetN()-1,xstop,y) ;
#else
  const_cast<RooCurve*>(curve)->GetPoint(0,xstart,y) ;
  const_cast<RooCurve*>(curve)->GetPoint(curve->GetN() - 1,xstop,y) ;
#endif

  double observedTotal(0), expectedTotal(0);
  if (renormalize) {
    for(Int_t i=0 ; i < hist->GetN() ; i++) {
      // Make sure that expected and observed are normalized to the same
      // number of events
      Double_t x, point;
#if ROOT_VERSION_CODE >= ROOT_VERSION(4,0,1)
      hist->GetPoint(i,x,point) ;
#else
      const_cast<RooHist&>(hist).GetPoint(i,x,point) ;
#endif
      Double_t xl = x - hist->GetErrorXlow(i);
      Double_t xh = x + hist->GetErrorXhigh(i);

      // Only calculate pull for bins inside curve range
      if (xl < xstart || xstop < xh) continue ;

      Double_t norm = (xh - xl) / plot_->getFitRangeBinW();
      Double_t norml = (x - xl) / plot_->getFitRangeBinW();
      Double_t normh = (xh - x) / plot_->getFitRangeBinW();
      point *= norm;

      // Start a hack to work around a bug in RooCurve::interpolate
      // that sometimes gives a wrong result.
      // Correcting the expected number of events in this bin for the non-uniform
      // bin width by multiplying with the norm.
      Double_t yexp  = curve->average(xl, xh) * norm;
      Double_t yexp2 = curve->average(xl, x ) * norml + 
	curve->average(x , xh) * normh;
      if (yexp + yexp2 > 0 &&
	  TMath::Abs((yexp - yexp2) / (yexp + yexp2)) > 0.1) {
	yexp = curve->interpolate(x) * norm;
      }
      // End of hack around the bug in RooCurve::interpolate
      observedTotal += point;
      expectedTotal += yexp;
    } // loop over points
  } // if (renormalize)

  Int_t nbin(0) ;
  Double_t chisq(0) ;
  for (i=0 ; i<np ; i++) {   

    // Retrieve histogram contents
    hist->GetPoint(i,x,y) ;
    xl = x - hist->GetEXlow()[i] ;
    xh = x + hist->GetEXhigh()[i] ;
    // eyl = hist->GetEYlow()[i] ;
    // eyh = hist->GetEYhigh()[i] ;

    // Check if the whole bin is in range of curve
    if (xl < xstart || xstop < xh) continue ;

    nbin++ ;
 
    // JV: Adjust observed and expected number of events for bin width to represent
    // number of events.
    Double_t norm  = (xh - xl) / plot_->getFitRangeBinW();
    Double_t norml = (x - xl) / plot_->getFitRangeBinW();
    Double_t normh = (xh - x) / plot_->getFitRangeBinW();
    y *= norm;

    // Integrate function over this bin.

    // Start a hack to work around a bug in RooCurve::interpolate
    // that sometimes gives a wrong result.
    // Correcting the expected number of events in this bin for the non-uniform
    // bin width by multiplying with the norm.
    Double_t yexp  = curve->average(xl, xh) * norm;
    Double_t yexp2 = curve->average(xl, x ) * norml + 
                     curve->average(x , xh) * normh;
    if (yexp + yexp2 > 0 &&
        TMath::Abs((yexp - yexp2) / (yexp + yexp2)) > 0.1) {
      yexp = curve->interpolate(x) * norm;
      coutW(InputArguments) << "cit::RooChi2Calculator(plotname=" 
                            << plot_->GetName()
                            << ")::chiSquare(..) Interpolating bin "
                            << i << " for " << xl << "-" << xh << endl ;
    }
    // End of hack around the bug in RooCurve::interpolate

    Double_t avg = yexp;
    if (renormalize & expectedTotal > 0) {
      avg = observedTotal / expectedTotal * avg;
    }

    if (avg < 5.) {
      coutW(InputArguments) << "cit::RooChi2Calculator(plotname=" << plot_->GetName()
                            << ")::chiSquare(..) expectation in bin "
                            << i << " is " << avg << " < 5!" << endl ;
    }

    // cout << "chi2 calculator i, obs, exp: " << i << ", "
    // 	 << y << ", " << avg << endl;

    // JV: Use the expected number of events for the y uncertainty,
    // See (33.34) of http://pdg.lbl.gov/2011/reviews/rpp2011-rev-statistics.pdf
    
    // Add pull^2 to chisq
    if (avg != 0) {      
      Double_t resid = y - avg;
      chisq += (resid * resid / avg) ;
    }
  }

  // Return chisq/nDOF 
  return chisq / (nbin - nFitParam) ;
}



///----------------------------------------------------------------------------
/// Returns the number of degrees of freedom.
int
RooChi2Calculator::numDOF(const char* pdfname, const char* histname, 
                          int nFitParam) const
{
  // Calculate the NDOF of this curve with respect to the histogram
  // 'hist' accounting nFitParam floating parameters in case the curve

  // Find curve object
  RooCurve* curve = (RooCurve*) plot_->findObject(pdfname,
                                                  RooCurve::Class());
  if (!curve) {
    coutE(InputArguments) << "cit::RooChi2Calculator(plotname=" 
                          << plot_->GetName()
                          << ")::numDOF(..) cannot find curve" << endl ;
    return 0 ;
  }

  // Find histogram object
  RooHist* hist = (RooHist*) plot_->findObject(histname,
                                               RooHist::Class()) ;
  if (!hist) {
    coutE(InputArguments) << "cit::RooChi2Calculator(plotname=" 
                          << plot_->GetName()
                          << ")::numDOF(..) cannot find histogram" << endl ;
    return 0 ;
  }
  
  Int_t i,np = hist->GetN() ;
  Double_t x,y,/*eyl,eyh,*/ xl,xh ;

  // Find starting and ending bin of histogram based on range of RooCurve
  Double_t xstart,xstop ;

#if ROOT_VERSION_CODE >= ROOT_VERSION(4,0,1)
  curve->GetPoint(0,xstart,y) ;
  curve->GetPoint(curve->GetN()-1,xstop,y) ;
#else
  const_cast<RooCurve*>(curve)->GetPoint(0,xstart,y) ;
  const_cast<RooCurve*>(curve)->GetPoint(curve->GetN() - 1,xstop,y) ;
#endif

  Int_t nbin(0) ;

  for (i=0 ; i<np ; i++) {
    // Retrieve histogram contents
    hist->GetPoint(i,x,y) ;
    xl = x - hist->GetEXlow()[i] ;
    xh = x + hist->GetEXhigh()[i] ;
    // Check if the whole bin is in range of curve
    if (xl < xstart || xstop < xh) continue ;
    nbin++ ;
  }
  // Return nDOF 
  return nbin - nFitParam;
}  // RooChi2Calculator::numDOF(const char* pdfname, const char* histname, 
//                              int nFitParam)

