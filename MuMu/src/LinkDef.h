#pragma GCC diagnostic ignored "-Wwrite-strings" //needed to get rid of pesky "deprecated conversion from string constant to char *" compilation error
// #include "PhysicsTools/TagAndProbe/interface/RooCBExGaussShape.h"
// #include "PhysicsTools/TagAndProbe/interface/ZGeneratorLineShape.h"
// #include "PhysicsTools/TagAndProbe/interface/RooCMSShape.h"
#include "JPsi/MuMu/interface/DummyRootClass.h"
#include "JPsi/MuMu/interface/DataDrivenBinning.h"
#include "JPsi/MuMu/interface/ModalInterval.h"
#include "JPsi/MuMu/interface/RooBetaCauchy.h"
#include "JPsi/MuMu/interface/RooBetaGshPdf.h"
#include "JPsi/MuMu/interface/RooBifurGshPdf.h"
#include "JPsi/MuMu/interface/RooBifurSechPdf.h"
#include "JPsi/MuMu/interface/RooChi2Calculator.h"
#include "JPsi/MuMu/interface/RooCruijff.h"
#include "JPsi/MuMu/interface/RooGshPdf.h"
#include "JPsi/MuMu/interface/RooHyperbolicPdf.h"
#include "JPsi/MuMu/interface/RooLogSqrtCBShape.h"
#include "JPsi/MuMu/interface/RooLogSqrtGaussian.h"
#include "JPsi/MuMu/interface/RooSechPdf.h"
#include "JPsi/MuMu/interface/RooPhosphorPdf.h"
#include "JPsi/MuMu/interface/RooRelativisticBreitWigner.h"
#include "JPsi/MuMu/interface/RooTruncatedExponential.h"
#include "JPsi/MuMu/interface/RooTransformPdf.h"
#include "JPsi/MuMu/interface/EffectiveSigmaCalculator.h"
#include "JPsi/MuMu/interface/tools.h"
#include "TVirtualFFT.h"
#include "TH1.h"

#ifdef __CINT__

//never even gets here...
#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;
//#pragma GCC diagnostic ignored "-Wformat"
// #pragma GCC diagnostic warning "-Wwrite-strings"

#pragma link C++ class cit::DummyRootClass;

#pragma link C++ class cit::DataDrivenBinning;
#pragma link C++ class cit::EffectiveSigmaCalculator;
#pragma link C++ class cit::ModalInterval;
#pragma link C++ class cit::RooChi2Calculator;

#pragma link C++ class RooBetaCauchy;
#pragma link C++ class RooBetaGshPdf;
#pragma link C++ class RooBifurGshPdf;
#pragma link C++ class RooBifurSechPdf;
#pragma link C++ class RooCruijff;
#pragma link C++ class RooGshPdf;
#pragma link C++ class RooHyperbolicPdf;
#pragma link C++ class RooLogSqrtCBShape;
#pragma link C++ class RooLogSqrtGaussian;
#pragma link C++ class RooSechPdf;
#pragma link C++ class RooPhosphorPdf;
#pragma link C++ class RooRelativisticBreitWigner;
#pragma link C++ class RooTruncatedExponential;
#pragma link C++ class RooTransformPdf;

#pragma link C++ global gROOT;
#pragma link C++ global gEnv;


#pragma link C++ function effSigma(TH1*);
#pragma link C++ function zMassPdg();
#pragma link C++ function Oplus(Double_t, Double_t);
#pragma link C++ function Oplus(Double_t, Double_t, Double_t);
#pragma link C++ function muonSigmaPtOverPt(Double_t, Double_t);
#pragma link C++ function photonSigmaEOverE(Double_t, Double_t);
#pragma link C++ function photonSigmaPtOverPt(Double_t, Double_t);
#pragma link C++ function phoEtrue(Double_t);
#pragma link C++ function phoEmeas(Double_t, Double_t);
#pragma link C++ function kRatio(Double_t, Double_t);
#pragma link C++ function inverseK(Double_t, Double_t);
#pragma link C++ function scaledMmgMass10(Double_t, Double_t, Double_t,\
                                          Double_t, Double_t, Double_t,\
                                          Double_t, Double_t, Double_t,\
                                          Double_t);
#pragma link C++ function smearingFabrice(Double_t, Double_t);                                        
#pragma link C++ function scaledMmgMass3(Double_t, Double_t, Double_t);
#pragma link C++ function mmgMassPhoFabriceSmearE(Double_t, Double_t,\
                                                  Double_t, Double_t);
#pragma link C++ function scaledDimuonPhotonMass(Double_t, Double_t, Double_t,\
                                                 Double_t, Double_t, Double_t,\
                                                 Double_t, Double_t);
#pragma link C++ function twoBodyMass(Double_t, Double_t, Double_t, Double_t,\
		                      Double_t, Double_t, Double_t, Double_t);
#pragma link C++ function threeBodyMass(Double_t, Double_t, Double_t, Double_t,\
		                        Double_t, Double_t, Double_t, Double_t,\
                                        Double_t, Double_t, Double_t, Double_t);
#pragma link C++ function phoSmearE(Double_t, Double_t, Double_t, Double_t,\
				    Double_t, Double_t)
#pragma link C++ function phoSmearF(Double_t, Double_t, Double_t, Double_t,\
				    Double_t, Double_t)
#pragma link C++ function mmgMassPhoSmearE(Double_t, Double_t, Double_t,\
					   Double_t, Double_t, Double_t,\
					   Double_t, Double_t)
#pragma link C++ function deltaR(Double_t, Double_t, Double_t, Double_t)
/// TODO: add all functions from tools.h
#endif
