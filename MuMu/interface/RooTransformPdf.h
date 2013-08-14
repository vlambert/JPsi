//--*-C++-*--
/**
  * Jan Veverka, Caltech,  03 December 2011
  * A PDF based on a given PDF through a a-posteriori variable transform.
  */
#ifndef JPSI_MUMU_ROOTRANSFORMPDF_H
#define JPSI_MUMU_ROOTRANSFROMPDF_H

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"
#include "TMath.h"
#include "RooMath.h"
#include "RooSetProxy.h"

class RooRealVar;

class RooTransformPdf : public RooAbsPdf {
public:
  RooTransformPdf() {};
  RooTransformPdf(const char *name, const char *title, 
		  RooAbsRealLValue& _x, RooAbsReal& _xtransform,
		  RooAbsPdf& _motherPdf, RooArgSet& _motherObservables);

  RooTransformPdf(const RooTransformPdf& other, const char* name = 0);
  virtual TObject* clone(const char* newname) const { 
    return new RooTransformPdf(*this,newname); 
  }

  inline virtual ~RooTransformPdf() { }

protected:

  RooAbsRealLValue* x;
  RooRealProxy xtransform;
  RooRealProxy motherPdf;
  //RooAbsPdf* motherPdf;
  RooSetProxy motherObservables;

  Double_t evaluate() const;

private:

  ClassDef(RooTransformPdf,1) // PDF through a-posteriori parameter transform
};

#endif
