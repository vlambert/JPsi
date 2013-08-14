// -- CLASS DESCRIPTION [PDF] --
// PDF through a-posteriori parameter transform.


#include <iostream>
#include <math.h>

#include "JPsi/MuMu/interface/RooTransformPdf.h"

ClassImp(RooTransformPdf)
using namespace std;

RooTransformPdf::RooTransformPdf(const char *name, const char *title,
				 RooAbsRealLValue& _x, RooAbsReal& _xtransform,
				 RooAbsPdf& _motherPdf, 
				 RooArgSet& _motherObservables) :
  RooAbsPdf(name, title),
  x(&_x),
  xtransform("xtransfrom", "Transfrom of x", this, _xtransform),
  motherPdf("motherPdf", "Mother PDF", this, _motherPdf),
  //motherPdf(&_motherPdf),
  motherObservables("motherObservables", "Observables of mother PDF", this)
{
  motherObservables.add(_motherObservables);
}

RooTransformPdf::RooTransformPdf(const RooTransformPdf& other, 
				 const char* name) :
  RooAbsPdf(other, name),
  x(other.x),
  xtransform("xtransform", this, other.xtransform),
  //motherPdf("motherPdf", this, other.motherPdf),
  motherPdf(other.motherPdf),
  motherObservables("motherObservables", this, other.motherObservables)
{
}

Double_t RooTransformPdf::evaluate() const
{
  // Store the value of x
  Double_t xval = x->getVal();
  // const RooAbsPdf &thePdf = (const RooAbsPdf&) motherPdf.arg();
  //RooAbsPdf &thePdf = *motherPdf;

  cout << "x, xtranfrom, mother pdf before substitution: " 
       << x->getVal() << ", " 
       << xtransform.arg().getVal() << ", "
    //       << thePdf.getVal(&motherObservables) << endl;
       << motherPdf << endl;

  // Update the value of x
  // xtransform.syncCache();
  x->setVal(xtransform.arg().getVal());

  cout << "x, xtranfrom, mother pdf after substitution: " 
       << x->getVal() << ", " 
       << xtransform.arg().getVal() << ", "
    //       << thePdf.getVal(&motherObservables) << endl;
       << motherPdf << endl;

  // Evaluate the mother PDF
  // Double_t ret = thePdf.getVal(&motherObservables);
  Double_t ret = motherPdf;
  x->setVal(xval);
  return ret;
}
