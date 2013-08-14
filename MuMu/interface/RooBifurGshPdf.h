//--*-C++-*--
/**
  Author: Jan Veverka, Caltech

  The Bifurcated Generalized Secant Hyperbolic distribution PDF
  f(x| mu, sigmaL, tL, sigmaR, tR)
  x - observable ranging (-infinity, infinity)
  mu - mean ranging (-infinity, infinity)
  sigma - sqrt(variance) ranging (0, infinity)
    bifurcated in left (L) and right (R) at x = mu
  t - kurtosis parameter ranging (-Pi, infinity)
    bifurcated in left (L) and right (R) at x = mu
    low t - high kurtosis and vice versa
    t = -Pi/2 gives the hyperbolic secant density,
    t = 0 gives the logistic distribution
*/
#ifndef JPSI_MUMU_ROOBIFURGSHPDF_H
#define JPSI_MUMU_ROOBIFURGSHPDF_H

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"
#include "TMath.h"
#include "RooMath.h"

class RooRealVar;

class RooBifurGshPdf : public RooAbsPdf {
public:
  RooBifurGshPdf() {};
  RooBifurGshPdf(const char *name, const char *title, RooAbsReal& _x,
	     RooAbsReal& _mean, RooAbsReal& _sigmaL, RooAbsReal& _tL,
             RooAbsReal& _sigmaR, RooAbsReal& _tR);

  RooBifurGshPdf(const RooBifurGshPdf& other, const char* name = 0);

  virtual TObject* clone(const char* newname) const
  {
    return new RooBifurGshPdf(*this,newname);
  }

  inline virtual ~RooBifurGshPdf() { }

protected:

  RooRealProxy x;
  RooRealProxy mean;
  RooRealProxy sigmaL;
  RooRealProxy tL;
  RooRealProxy sigmaR;
  RooRealProxy tR;

  Double_t evaluate() const;

private:

  ClassDef(RooBifurGshPdf,1) // Generalized Secant Hyperbolic PDF
};

#endif
