//--*-C++-*--
/*
Author: Jan Veverka, Caltech

The Bifurcated Hyperbolic Secant Distribution PDF
Based on Wikipedia's article:
http://en.wikipedia.org/wiki/Hyperbolic_secant_distribution

                                 1           pi * (x - mean)
The form is basically f(x) = --------- sech( --------------- )
                             2 * sigma          2 * sigma

where the parameters mean and sigma are the mean and is the square root 
of the variance of the distribution.

The hyperbolic secant function is defined as:
              1
sech(x) = ---------
           cosh(x)

and the hyperboli cosine function as:
           1       
cosh(x) = --- [exp(x) + exp(-x)]
           2
*/
#ifndef JPSI_MUMU_ROOBIFURSECHPDF_H
#define JPSI_MUMU_ROOBIFURSECHPDF_H

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"
#include "TMath.h"
#include "RooMath.h"

class RooRealVar;

class RooBifurSechPdf : public RooAbsPdf {
public:
  RooBifurSechPdf() {};
  RooBifurSechPdf(const char *name, const char *title, RooAbsReal& _x,
	          RooAbsReal& _mean, RooAbsReal& _sigmaL, RooAbsReal& _sigmaR);

  RooBifurSechPdf(const RooBifurSechPdf& other, const char* name = 0);
  virtual TObject* clone(const char* newname) const 
  {
    return new RooBifurSechPdf(*this,newname);
  }

  inline virtual ~RooBifurSechPdf() { }

protected:

  RooRealProxy x;
  RooRealProxy mean;
  RooRealProxy sigmaL;
  RooRealProxy sigmaR;

  Double_t evaluate() const;

private:

  ClassDef(RooBifurSechPdf,1) // Bifurcated Hyperbolic Secant PDF
};

#endif
