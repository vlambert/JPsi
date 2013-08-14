// -- CLASS DESCRIPTION [PDF] --
/**
  PDF of X = log(sqrt(Y)) where Y has the Crystal-Ball density.
  Author: Jan Veverka, Caltech
  8 November 2011
*/


#include <iostream>
#include <math.h>

#include "JPsi/MuMu/interface/RooLogSqrtCBShape.h"

ClassImp(RooLogSqrtCBShape)

RooLogSqrtCBShape::RooLogSqrtCBShape(const char *name, const char *title,
				     RooAbsReal& _y, RooAbsReal& _m0,
				     RooAbsReal& _sigma, RooAbsReal& _alpha,
				     RooAbsReal& _n) :
  RooAbsPdf(name, title),
  y("y", "Dependent", this, _y),
  m0("m0", "m0", this, _m0),
  sigma("sigma", "sigma", this, _sigma),
  alpha("alpha", "alpha", this, _alpha),
  n("n", "n", this, _n)
{
}

RooLogSqrtCBShape::RooLogSqrtCBShape(const RooLogSqrtCBShape& other, const char* name) :
  RooAbsPdf(other, name),
  y("y", this, other.y),
  m0("m0", this, other.m0),
  sigma("sigma", this, other.sigma),
  alpha("alpha", this, other.alpha),
  n("n", this, other.n)
{
}

Double_t RooLogSqrtCBShape::evaluate() const
{
  // Calculate the corresponding value of X, given Y = 1/2 log(X)
  Double_t m = TMath::Exp(2.*y);

  Double_t t = (m-m0)/sigma;
  if (alpha < 0) t = -t;

  Double_t absAlpha = fabs((Double_t)alpha);

  if (t >= -absAlpha) {
    return 2.*m*exp(-0.5*t*t);
  } else {
    Double_t a =  TMath::Power(n/absAlpha,n)*exp(-0.5*absAlpha*absAlpha);
    Double_t b= n/absAlpha - absAlpha; 

    return 2*m*a/TMath::Power(b - t, n);
  }
}

