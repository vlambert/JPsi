//--*-C++-*--
/**
  PDF of X = log(sqrt(Y)) where Y has the Crystal-Ball density.
  Author: Jan Veverka, Caltech
  8 November 2011
*/
#ifndef JPSI_MUMU_ROOLOGSQRTCBSHAPE_H
#define JPSI_MUMU_ROOLOGSQRTCBSHAPE_H

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"
#include "RooCBShape.h"
#include "TMath.h"
#include "RooMath.h"


class RooRealVar;


///-----------------------------------------------------------------------------
class RooLogSqrtCBShape : public RooAbsPdf {
public:
  RooLogSqrtCBShape() {};
  RooLogSqrtCBShape(const char *name, const char *title, RooAbsReal& _y,
		    RooAbsReal& _m0, RooAbsReal& _sigma, RooAbsReal& _alpha,
		    RooAbsReal& _n);

  RooLogSqrtCBShape(const RooLogSqrtCBShape& other, const char* name = 0);

  virtual TObject* clone(const char* newname) const
  {
    return new RooLogSqrtCBShape(*this,newname);
  }

  inline virtual ~RooLogSqrtCBShape() { }

protected:

  RooRealProxy y;
  RooRealProxy m0;
  RooRealProxy sigma;
  RooRealProxy alpha;
  RooRealProxy n;

  Double_t evaluate() const;

private:

  ClassDef(RooLogSqrtCBShape,1) // (log)o(sqrt)-Transformed CBShape
};

#endif
