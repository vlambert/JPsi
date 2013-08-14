// -- CLASS DESCRIPTION [PDF] --
// Generalized Secant Hyperbolic (GSH) PDF


#include <iostream>
#include <math.h>

#include "JPsi/MuMu/interface/RooGshPdf.h"
#include "JPsi/MuMu/interface/Math.h"

ClassImp(RooGshPdf)

RooGshPdf::RooGshPdf(const char *name, const char *title, RooAbsReal& _x,
                     RooAbsReal& _mean, RooAbsReal& _sigma, RooAbsReal& _t) :
  RooAbsPdf(name, title),
  x("x", "Dependent", this, _x),
  mean("mean", "Mean", this, _mean),
  sigma("sigma", "Sigma", this, _sigma),
  t("t", "T", this, _t)
{
}

RooGshPdf::RooGshPdf(const RooGshPdf& other, const char* name) :
  RooAbsPdf(other, name),
  x("x", this, other.x),
  mean("mean", this, other.mean),
  sigma("sigma", this, other.sigma),
  t("t", this, other.t)
{
}

Double_t RooGshPdf::evaluate() const
{
  // build the functional form
  double dx = (x - mean) / sigma;
  return cit::math::gsh(dx, t) / sigma;
}

