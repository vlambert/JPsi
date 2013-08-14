// -- CLASS DESCRIPTION [PDF] --
// Cruijff function PDF


#include <iostream>
#include <math.h>

#include "JPsi/MuMu/interface/RooSechPdf.h"

ClassImp(RooSechPdf)

RooSechPdf::RooSechPdf(const char *name, const char *title,
		       RooAbsReal& _x, RooAbsReal& _mean, RooAbsReal& _sigma) :
  RooAbsPdf(name, title),
  x("x", "Dependent", this, _x),
  mean("mean", "Mean", this, _mean),
  sigma("sigma", "Sigma", this, _sigma)
{
}

RooSechPdf::RooSechPdf(const RooSechPdf& other, const char* name) :
  RooAbsPdf(other, name),
  x("x", this, other.x),
  mean("mean", this, other.mean),
  sigma("sigma", this, other.sigma)
{
}

Double_t RooSechPdf::evaluate() const
{
  // build the functional form
  double dx = (x - mean) / sigma;
  // argument of the sech function
  double arg = 0.5 * TMath::Pi() * dx;
  // 0.5 * sech(arg)
  return 1. / (TMath::Exp(arg) + TMath::Exp(-arg));
}
