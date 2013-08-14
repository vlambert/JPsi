// -- CLASS DESCRIPTION [PDF] --
/**
  PDF of X = log(sqrt(Y)) where Y has the Gaussian density.
  Author: Jan Veverka, Caltech
  9 November 2011
*/


#include <iostream>
#include <math.h>

#include "JPsi/MuMu/interface/RooLogSqrtGaussian.h"

ClassImp(RooLogSqrtGaussian)

RooLogSqrtGaussian::RooLogSqrtGaussian(const char *name, const char *title,
				       RooAbsReal& _y, RooAbsReal& _m0,
				       RooAbsReal& _sigma) :
  RooAbsPdf(name, title),
  y("y", "Dependent", this, _y),
  m0("m0", "m0", this, _m0),
  sigma("sigma", "sigma", this, _sigma)
{
}

RooLogSqrtGaussian::RooLogSqrtGaussian(const RooLogSqrtGaussian& other, const char* name) :
  RooAbsPdf(other, name),
  y("y", this, other.y),
  m0("m0", this, other.m0),
  sigma("sigma", this, other.sigma)
{
}

Double_t RooLogSqrtGaussian::evaluate() const
{
  // Calculate the corresponding value of X, given Y = 1/2 log(X)
  Double_t m = TMath::Exp(2.*y);

  Double_t t = (m-m0)/sigma;
  return 2.*m*exp(-0.5*t*t);
}

