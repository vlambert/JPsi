// -- CLASS DESCRIPTION [PDF] --
// Generalized Secant Hyperbolic (GSH) PDF


#include <iostream>
#include <math.h>

#include "JPsi/MuMu/interface/RooBifurGshPdf.h"
#include "JPsi/MuMu/interface/Math.h"

ClassImp(RooBifurGshPdf)

RooBifurGshPdf::RooBifurGshPdf(const char *name, const char *title,
                               RooAbsReal& _x, RooAbsReal& _mean,
                               RooAbsReal& _sigmaL, RooAbsReal& _tL,
                               RooAbsReal& _sigmaR, RooAbsReal& _tR) :
  RooAbsPdf(name, title),
  x("x", "Dependent", this, _x),
  mean("mean", "Mean", this, _mean),
  sigmaL("sigmaL", "SigmaLeft", this, _sigmaL),
  tL("tL", "TLeft", this, _tL),
  sigmaR("sigmaR", "SigmaRight", this, _sigmaR),
  tR("tR", "TRight", this, _tR)
{
}

RooBifurGshPdf::RooBifurGshPdf(const RooBifurGshPdf& other, const char* name) :
  RooAbsPdf(other, name),
  x("x", this, other.x),
  mean("mean", this, other.mean),
  sigmaL("sigmaL", this, other.sigmaL),
  tL("tL", this, other.tL),
  sigmaR("sigmaR", this, other.sigmaR),
  tR("tR", this, other.tR)
{
}

Double_t RooBifurGshPdf::evaluate() const
{
  double aL, c1L, c2L;
  double aR, c1R, c2R;
  cit::math::gsh_a_c1_c2(tL, aL, c1L, c2L);
  cit::math::gsh_a_c1_c2(tR, aR, c1R, c2R);

  double xstar, t, sigma, A;
  double numL = c1L * sigmaR * (1. + aR);
  double denL = c1R * sigmaL * (1. + aL);
  if (x < mean) {
    xstar = (x - mean) / sigmaL;
    t = tL;
    A = 2. / (1. + numL/denL);
    sigma = sigmaL;
  } else {
    xstar = (x - mean) / sigmaR;
    t = tR;
    A = 2. / (1. + denL/numL);
    sigma = sigmaR;
  }

  return A * cit::math::gsh(xstar, t) / sigma;
}

