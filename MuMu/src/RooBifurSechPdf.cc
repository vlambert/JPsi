// -- CLASS DESCRIPTION [PDF] --
// Bifurcated hyperbolic secant PDF


#include <iostream>
#include <math.h>

#include "JPsi/MuMu/interface/RooBifurSechPdf.h"
#include "JPsi/MuMu/interface/Math.h"

ClassImp(RooBifurSechPdf)

RooBifurSechPdf::RooBifurSechPdf(const char *name, const char *title,
		                 RooAbsReal& _x, RooAbsReal& _mean, 
				 RooAbsReal& _sigmaL, RooAbsReal& _sigmaR) :
  RooAbsPdf(name, title),
  x("x", "Dependent", this, _x),
  mean("mean", "Mean", this, _mean),
  sigmaL("sigmaL", "SigmaL", this, _sigmaL),
  sigmaR("sigmaR", "SigmaR", this, _sigmaR) 
{
}

RooBifurSechPdf::RooBifurSechPdf(const RooBifurSechPdf& other, const char* name) :
  RooAbsPdf(other, name),
  x("x", this, other.x),
  mean("mean", this, other.mean),
  sigmaL("sigmaL", this, other.sigmaL),
  sigmaR("sigmaR", this, other.sigmaR)
{
}

Double_t RooBifurSechPdf::evaluate() const
{
  // build the functional form
  double xstar;
  if (x < mean) {
    xstar = (x - mean) / sigmaL;
  } else {
    xstar = (x - mean) / sigmaR;
  }
    
  // argument of the sech function
  double arg = 0.5 * TMath::Pi() * xstar;
  // sech(arg) / sigma
  return cit::math::sech(arg) / (sigmaL + sigmaR);
  //1. / (sigma * (TMath::Exp(arg) + TMath::Exp(-arg)));
}
