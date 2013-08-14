//******************************************//
// author:
//
//  Various utility functions used with 
//  ROOT and TTree::Draw.
//
//  TODO list:
//
//
//
//  Modified by:
//
//******************************************//
#ifndef JPSI_MUMU_TOOLS_H
#define JPSI_MUMU_TOOLS_H

#include "TH1.h"

Double_t zMassPdg();
Double_t Oplus(Double_t a, Double_t b) ;
Double_t Oplus(Double_t a, Double_t b, Double_t c);
Double_t muonSigmaPtOverPt(Double_t pt, Double_t eta);
Double_t photonSigmaEOverE(Double_t E, Double_t eta);
Double_t photonSigmaPtOverPt(Double_t pt, Double_t eta);
Double_t phoEtrue(Double_t mmMass) ;
Double_t phoEmeas(Double_t mmgMass, Double_t mmMass) ;
Double_t kRatio(Double_t mmgMass, Double_t mmMass) ;
Double_t inverseK(Double_t mmgMass, Double_t mmMass) ;
Double_t scaledMmgMass10(Double_t scale3,
			 Double_t pt1, Double_t eta1, Double_t phi1,
			 Double_t pt2, Double_t eta2, Double_t phi2,
			 Double_t pt3, Double_t eta3, Double_t phi3);
Double_t scaledMmgMass3(Double_t sfactor, Double_t mmgMass, Double_t mmMass);
Double_t phoSmearE(Double_t scale, Double_t resolution,
		   Double_t refScale, Double_t refResolution,
		   Double_t phoE, Double_t phoGenE);
Double_t phoSmearF(Double_t scale, Double_t resolution,
                   Double_t refScale, Double_t refResolution,
                   Double_t phoE, Double_t phoGenE);
Double_t phoFabriceSmearE(Double_t phoE, Double_t scEta, Double_t r9);
Double_t smearingFabrice(Double_t scEta, Double_t r9);
Double_t mmgMassPhoSmearE(Double_t scale, Double_t resolution,
                          Double_t refScale, Double_t refResolution,
                          Double_t phoE, Double_t phoGenE,
                          Double_t mmgMass, Double_t mmMass);
Double_t mmgMassPhoFabriceSmearE(Double_t mmgMass, Double_t mmMass,
                                 Double_t scEta, Double_t r9);
Double_t scaledDimuonPhotonMass(Double_t scale2,
				Double_t pt1, Double_t eta1, Double_t phi1, Double_t m1,
				Double_t pt2, Double_t eta2, Double_t phi2);
Double_t twoBodyMass(Double_t pt1, Double_t eta1, Double_t phi1, Double_t m1,
		     Double_t pt2, Double_t eta2, Double_t phi2, Double_t m2);
Double_t threeBodyMass(Double_t pt1, Double_t eta1, Double_t phi1, Double_t m1,
		       Double_t pt2, Double_t eta2, Double_t phi2, Double_t m2,
		       Double_t pt3, Double_t eta3, Double_t phi3, Double_t m3);
Double_t effSigma(TH1 * hist);
Double_t deltaR(Double_t eta1, Double_t phi1, Double_t eta2, Double_t phi2);

#endif
