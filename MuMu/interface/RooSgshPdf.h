//--*-C++-*--
/*
Author: Jan Veverka, Caltech

Based on Wikipedia's Hyperbolic secant distribution:
http://en.wikipedia.org/wiki/Hyperbolic_secant_distribution

                                 1           pi * (x - mean)
The form is basically f(x) = --------- sech( --------------- )
                             2 * sigma          2 * sigma

where mean and sigma are the mean and sigma is the sqrt(variance).
*/
#ifndef JPSI_MUMU_ROOSECHPDF_H
#define JPSI_MUMU_ROOSECHPDF_H

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"
#include "TMath.h"
#include "RooMath.h"

class RooRealVar;

class RooSechPdf : public RooAbsPdf {
public:
  RooSechPdf() {};
  RooSechPdf(const char *name, const char *title, RooAbsReal& _x,
	     RooAbsReal& _mean, RooAbsReal& _sigma);

  RooSechPdf(const RooSechPdf& other, const char* name = 0);
  virtual TObject* clone(const char* newname) const { return new RooSechPdf(*this,newname); }

  inline virtual ~RooSechPdf() { }

protected:

  RooRealProxy x;
  RooRealProxy mean;
  RooRealProxy sigma;

  Double_t evaluate() const;

private:

  ClassDef(RooSechPdf,1) // Cruijff function PDF
};

#endif
