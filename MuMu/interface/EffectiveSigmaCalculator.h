//******************************************//
// author:
//  This class is a wrapper around a function 
//  that evaluates the effective 
//  sigma of a histogram. 
//  It's adapted from http://cmsdoc.cern.ch/cms/performance/ecal/effSigma.html
//
//
//  TODO list:
//
//
//
//  Modified by:
//
//******************************************//

#ifndef JPSI_MUMU_EFFECTIVESIGMACALCULATOR_H
#define JPSI_MUMU_EFFECTIVESIGMACALCULATOR_H

#include "TH1.h"

namespace cit {
  // Double_t effSigma(TH1 * hist);
  struct EffectiveSigmaCalculator : public TObject { 
    Double_t operator() (TH1 * hist);
    ClassDef(EffectiveSigmaCalculator,0)
  };

} /// end of namespace cit

#endif
