#include "RooWorkspace.h"
#include "RooPlot.h"
#include "RooDataSet.h"
#include "RooAbsPdf.h"
#include "RooRealVar.h"
#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif 

using namespace RooFit ;

void ex1var()
{
  // Make an empty workspace that exports its contents to CINT
  RooWorkspace *w = new RooWorkspace("w",kTRUE) ;

  // Fill the workspace with a Gaussian pdf
  w->factory("Gaussian::g(x[-10,10],mean[-10,10],sigma[3,0.1,10])") ;

  // Generate unbinned data from the pdf
  RooAbsData* d = w->pdf("g")->generate(*w->var("x"),10000) ;

  // Fit the pdf to the data
  w->pdf("g")->fitTo(*d) ;

  // Plot data and pdf in a frame
  RooPlot* frame = w->var("x")->frame() ;
  d->plotOn(frame) ;
  w->pdf("g")->plotOn(frame) ;
  frame->Draw() ;

  // Print the fitted values of the parameters
  w->var("mean")->Print() ;
  w->var("sigma")->Print() ;

  // You can access w on the ROOT command line after completion
  // of the macro
  gDirectory->Add(w) ;

  // Print the contents of the workspace
  w->Print() ;
}
