//--*-C++-*--
/**
  Author: Jan Veverka, Caltech
  24 November 2011
  The Hyperbolic distribution PDF
  http://en.wikipedia.org/wiki/Hyperbolic_distribution
  f(x| mu, alpha, beta, delta, gamma = sqrt(alpha^2 - beta^2))
  x - observable ranging (-infinity, infinity)
  mu - mean ranging (-infinity, infinity)
  alpha - related to how pointy it is(?), (0, infinity)
  beta - asymmetry parameter, (-alpha, alpha)
  delta - scale parameter
  gamma - auxiliary paramter depending on alpha and beta (0, infinity)
*/
#ifndef JPSI_MUMU_ROOHYPERBOLICPDF_H
#define JPSI_MUMU_ROOHYPERBOLICPDF_H

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"
#include "TMath.h"
#include "RooMath.h"

class RooRealVar;

class RooHyperbolicPdf : public RooAbsPdf {
public:
  RooHyperbolicPdf() {};
  RooHyperbolicPdf(const char *name, const char *title, RooAbsReal& _x,
	     RooAbsReal& _mean, RooAbsReal& _alpha, RooAbsReal& _beta,
             RooAbsReal& _delta);

  RooHyperbolicPdf(const RooHyperbolicPdf& other, const char* name = 0);

  virtual TObject* clone(const char* newname) const
  {
    return new RooHyperbolicPdf(*this,newname);
  }

  inline virtual ~RooHyperbolicPdf() { }

protected:

  RooRealProxy x;
  RooRealProxy mean;
  RooRealProxy alpha;
  RooRealProxy beta;
  RooRealProxy delta;

  Double_t evaluate() const;

private:

  ClassDef(RooHyperbolicPdf,1) // Hyperbolic PDF
};

#endif
