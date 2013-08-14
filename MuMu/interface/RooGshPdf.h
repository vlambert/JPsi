//--*-C++-*--
/**
  Author: Jan Veverka, Caltech

  The Generalized Secant Hyperbolic distribution PDF
  f(x| mu, sigma, t)
  x - observable ranging (-infinity, infinity)
  mu - mean ranging (-infinity, infinity)
  sigma - sqrt(variance) ranging (0, infinity)
  t - kurtosis parameter ranging (-Pi, infinity)
    low t - high kurtosis and vice versa
    t = -Pi/2 gives the hyperbolic secant density,
    t = 0 gives the logistic distribution
*/
#ifndef JPSI_MUMU_ROOGSHPDF_H
#define JPSI_MUMU_ROOGSHPDF_H

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"
#include "TMath.h"
#include "RooMath.h"

class RooRealVar;

class RooGshPdf : public RooAbsPdf {
public:
  RooGshPdf() {};
  RooGshPdf(const char *name, const char *title, RooAbsReal& _x,
	     RooAbsReal& _mean, RooAbsReal& _sigma, RooAbsReal& _t);

  RooGshPdf(const RooGshPdf& other, const char* name = 0);
  virtual TObject* clone(const char* newname) const { return new RooGshPdf(*this,newname); }

  inline virtual ~RooGshPdf() { }

protected:

  RooRealProxy x;
  RooRealProxy mean;
  RooRealProxy sigma;
  RooRealProxy t;

  Double_t evaluate() const;

private:

  ClassDef(RooGshPdf,1) // Generalized Secant Hyperbolic PDF
};

#endif
