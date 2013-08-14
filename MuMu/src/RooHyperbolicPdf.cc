// -- CLASS DESCRIPTION [PDF] --
// Generalized Secant Hyperbolic (GSH) PDF


#include <iostream>
#include <math.h>

#include "JPsi/MuMu/interface/RooHyperbolicPdf.h"
#include "JPsi/MuMu/interface/Math.h"

ClassImp(RooHyperbolicPdf)

RooHyperbolicPdf::RooHyperbolicPdf(const char *name, const char *title,
                               RooAbsReal& _x, RooAbsReal& _mean,
                               RooAbsReal& _alpha, RooAbsReal& _beta,
                               RooAbsReal& _delta) :
  RooAbsPdf(name, title),
  x("x", "Dependent", this, _x),
  mean("mean", "Mean", this, _mean),
  alpha("alpha", "Alpha", this, _alpha),
  beta("beta", "Asymmetry Parameter", this, _beta),
  delta("delta", "Scale Parameter", this, _delta)
{
}

RooHyperbolicPdf::RooHyperbolicPdf(const RooHyperbolicPdf& other, const char* name) :
  RooAbsPdf(other, name),
  x("x", this, other.x),
  mean("mean", this, other.mean),
  alpha("alpha", this, other.alpha),
  beta("beta", this, other.beta),
  delta("delta", this, other.delta)
{
}

Double_t RooHyperbolicPdf::evaluate() const
{
  Double_t t = x - mean;
  return exp(-alpha * sqrt(delta*delta + t*t) + beta * t);
}

