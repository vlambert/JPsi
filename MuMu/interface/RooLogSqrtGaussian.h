//--*-C++-*--
/**
  PDF of X = log(sqrt(Y)) where Y has the Gaussian density.
  Author: Jan Veverka, Caltech
  9 November 2011
*/
#ifndef JPSI_MUMU_ROOLOGSQRTGAUSSIAN_H
#define JPSI_MUMU_ROOLOGSQRTGAUSSIAN_H

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"
#include "RooCBShape.h"
#include "TMath.h"
#include "RooMath.h"


class RooRealVar;


///-----------------------------------------------------------------------------
class RooLogSqrtGaussian : public RooAbsPdf {
public:
  RooLogSqrtGaussian() {};
  RooLogSqrtGaussian(const char *name, const char *title, RooAbsReal& _y,
		     RooAbsReal& _m0, RooAbsReal& _sigma);

  RooLogSqrtGaussian(const RooLogSqrtGaussian& other, const char* name = 0);

  virtual TObject* clone(const char* newname) const
  {
    return new RooLogSqrtGaussian(*this,newname);
  }

  inline virtual ~RooLogSqrtGaussian() { }

protected:

  RooRealProxy y;
  RooRealProxy m0;
  RooRealProxy sigma;

  Double_t evaluate() const;

private:

  ClassDef(RooLogSqrtGaussian,1) // (log)o(sqrt)-Transformed Gaussian
};

#endif
