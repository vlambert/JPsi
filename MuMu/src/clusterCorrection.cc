#include <math.h>
#include <iostream>
#include "JPsi/MuMu/interface/clusterCorrection.h"
#include "JPsi/MuMu/interface/fCorrs.h"
#include "JPsi/MuMu/interface/fCorr_testNewCorrsPhotons.h"
#include "JPsi/MuMu/interface/fCorr_EE_testNewCorrsPhotons.h"

using namespace std;

// ----------------------------------------------------------------------------
float
corrE( float /*supercluster*/ rawEnergyWithPS,
       float /*supercluster*/ eta,
       float /*supercluster*/ brem,
       int /*correction*/ level /*= 3 (default)*/ )
{
  if (level < 1 || level > 3) {
    cout << "ERROR in corrE: Level must be one of 1, 2, 3!\n";
    throw 1;
  }

  float absEta = fabs(eta);

  // C(eta) for EB only
  if (absEta < 1.5){
    int ieta = int( absEta * (5 / 0.087) );
    float phoCetaCorrE  = rawEnergyWithPS / fcorrs::f5x5(ieta);
    if (level == 1) return phoCetaCorrE;

    // f(brem)-corrected energy
    float phoBremCorrE  = fcorrs::fBrem( brem, phoCetaCorrE );
    if (level == 2) return phoBremCorrE;

    // fully-corrected energy
    float phoFullCorrEt = fcorrs::fullCorr( phoBremCorrE / cosh(eta), absEta );
    return phoFullCorrEt * cosh(eta);

  } else {
    // Endcaps have no C(eta)
    float phoCetaCorrE  = rawEnergyWithPS;
    if (level == 1) return phoCetaCorrE;

    // f(brem)-corrected energies
    float phoBremCorrE  = fcorrs::fBrem_ee( brem, phoCetaCorrE );
    if (level == 2) return phoBremCorrE;

    // fully-corrected energies
    float phoFullCorrEt = fcorrs::fullCorr_ee( phoBremCorrE / cosh(eta),
                                               absEta );
    return phoFullCorrEt * cosh(eta);
  } // Endcaps

  // This should never get executed
  cout << "ERROR in corrE: This should never happen!\n";
  throw 2;
} // corr E


// ----------------------------------------------------------------------------
float
newCorrE( float /*supercluster*/ rawEnergyWithPS,
          float /*supercluster*/ eta,
          float /*supercluster*/ brem,
          int /*correction*/ level /*= 3 (default)*/ )
{
  if (level < 1 || level > 3) {
    cout << "ERROR in corrE: Level must be one of 1, 2, 3!\n";
    throw 1;
  }

  float absEta = fabs(eta);

  // C(eta) for EB only
  if (absEta < 1.5){
    int ieta = int( absEta * (5 / 0.087) );
    float phoCetaCorrE  = rawEnergyWithPS / fcorrs::f5x5(ieta);
    if (level == 1) return phoCetaCorrE;

    // f(brem)-corrected energy
    float phoBremCorrE  = fcorr::electron_br1( brem, phoCetaCorrE );
    if (level == 2) return phoBremCorrE;

    // fully-corrected energy
    float phoFullCorrEt = fcorr::electron_br1_complete(
                            phoBremCorrE / cosh(eta),
                            absEta
                          );
    return phoFullCorrEt * cosh(eta);

  } else {
    // Endcaps have no C(eta)
    float phoCetaCorrE  = rawEnergyWithPS;
    if (level == 1) return phoCetaCorrE;

    // f(brem)-corrected energies
    float phoBremCorrE  = fcorr_ee::electron_br1( brem, phoCetaCorrE );
    if (level == 2) return phoBremCorrE;

    // fully-corrected energies
    float phoFullCorrEt = fcorr_ee::electron_br1_complete(
                            phoBremCorrE / cosh(eta),
                            absEta
                          );
    return phoFullCorrEt * cosh(eta);
  } // Endcaps

  // This should never get executed
  cout << "ERROR in corrE: This should never happen!\n";
  throw 2;
} // corr E
