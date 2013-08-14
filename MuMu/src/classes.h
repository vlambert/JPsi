#include "JPsi/MuMu/interface/DummyRootClass.h"
#include "JPsi/MuMu/interface/DataDrivenBinning.h"
#include "JPsi/MuMu/interface/EffectiveSigmaCalculator.h"
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
#include "JPsi/MuMu/interface/RooPhosphorPdf.h"
#include "JPsi/MuMu/interface/RooRelativisticBreitWigner.h"
#include "JPsi/MuMu/interface/RooSechPdf.h"
#include "JPsi/MuMu/interface/RooTruncatedExponential.h"
#include "JPsi/MuMu/interface/RooTransformPdf.h"

namespace cit {
  struct toolDict {
    DataDrivenBinning _ddb;
    ModalInterval     _mi;
    DummyRootClass    _drc;
    RooChi2Calculator _rcc;
    EffectiveSigmaCalculator _esc;
  };
}

namespace jpsimumu {
  struct pdfDict {
    RooBetaCauchy _betacauchy;
    RooBetaGshPdf _betagshpdf;
    RooBifurGshPdf  _bgsh;
    RooBifurSechPdf _bsech;
    RooCruijff      _cruijff;
    RooGshPdf       _gsh;
    RooHyperbolicPdf _hyperbolic;
    RooSechPdf      _sech;
    RooLogSqrtCBShape _lscb;
    RooLogSqrtGaussian   _lsg;
    RooPhosphorPdf _phosphor;
    RooRelativisticBreitWigner _rbw;
    RooTruncatedExponential _te;
    RooTransformPdf _tpdf;
  };
}
