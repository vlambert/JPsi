#include "JPsi/MuMu/interface/DimuonsTree.h"

#include <algorithm>
#include <iostream>
#include <vector>

#include "TLorentzVector.h"

DimuonsTree::DimuonsTree(TTree *tree):
  tree_(0x0)
{
  initLeafVariables();
  if (tree) init(tree);
}

DimuonsTree::~DimuonsTree() {}

/// auxiliary for DimuonsTree::apply*Selection
namespace dimuonstree {

  namespace jpsi {

    typedef struct {
      unsigned dimuonIndex;
      unsigned numberOfGlobalMuons;
      float    pt;
    } ArbitrationData;

    bool
    compareDimuons(ArbitrationData a, ArbitrationData b)
    {
      if (a.numberOfGlobalMuons != b.numberOfGlobalMuons)
        return a.numberOfGlobalMuons > b.numberOfGlobalMuons;
      else
        return a.pt > b.pt;
    } // compareDimuons

  } // namespace jpsi

  namespace upsilon {

    typedef struct {
      unsigned dimuonIndex;
      float    vProb;
    } ArbitrationData;

    bool
    compareDimuons(ArbitrationData a, ArbitrationData b)
    { return a.vProb > b.vProb; } // compareDimuons

  } // namespace upsilon

} // namespace dimuonstree

/// J/psi PAS BPH-10-002
void
DimuonsTree::applyJPsiSelection() {
  /// loop over muons
  for (int i=0; i<nMuons; ++i) {
    muPassJPsiId[i] = 0;
    if (!muIsTrackerMuon[i]) continue;
    if (muIsGlobalMuon[i] & (muStations[i] < 2) ) continue;
    if (muIsGlobalMuon[i] & (muGlobalNormalizedChi2[i] > 20) ) continue;
    if (!muIsGlobalMuon[i] & !muIsTMLastStationAngTight[i]) continue;
    if (muSiHits[i] < 12) continue;
    if (muPixelHits[i] < 2) continue;
    if (muSiNormalizedChi2[i] > 4) continue;
    if (TMath::Abs(muSiD0PV[i]) > 3.) continue;
    if (TMath::Abs(muSiDzPV[i]) > 30.) continue;
    if (TMath::Abs(muEta[i]) > 2.4) continue;
    muPassJPsiId[i] = 1;
  } // loop over muons

  /// container for arbitration data
  typedef dimuonstree::jpsi::ArbitrationData Candidate;
  std::vector<Candidate> candidates(maxDimuons);
  candidates.clear();

  /// loop over dimuons
  for (int i=0; i<nDimuons; ++i) {
    isJPsiCand[i] = 0;
    if (!muPassJPsiId[dau1[i]] || !muPassJPsiId[dau2[i]]) continue;
//     if (charge[i] != 0) continue;
//     if (mass[i] < 2.6 || mass[i] > 3.5) continue;
    if (vProb[i] < 0.001) continue;
    /// store arbitration data
    Candidate cand = {i, 0, pt[i]};
    if (muIsGlobalMuon[dau1[i]]) ++cand.numberOfGlobalMuons;
    if (muIsGlobalMuon[dau2[i]]) ++cand.numberOfGlobalMuons;
    candidates.push_back(cand);
  } // loop over dimuons

  /// arbitration
  if (candidates.size() > 0) {
    std::sort(candidates.begin(), candidates.end(), dimuonstree::jpsi::compareDimuons);
    isJPsiCand[ candidates[0].dimuonIndex ] = 1;
  }
}  // DimuonsTree::applyJPsiSelection


/// Selection from the Upsilon PAS BPH-10-003
void
DimuonsTree::applyYSelection() {
  /// loop over muons
  for (int i=0; i<nMuons; ++i) {
    muPassYId[i] = 0;
    if (!muIsTrackerMuon[i]) continue;
    if (!muIsGlobalMuon[i] & !muIsTMLastStationAngTight[i]) continue;
    if (muSiHits[i] < 12) continue;
    if (muPixelHits[i] < 2) continue;
    if (muSiNormalizedChi2[i] > 5) continue;
    if (TMath::Abs(muSiD0PV[i]) > 0.2) continue;
    if (TMath::Abs(muSiDzPV[i]) > 25.) continue;
    if (TMath::Abs(muEta[i]) > 2.4) continue;
    if (muPt[i] < 2.5) continue;
    if (TMath::Abs(muEta[i]) < 1.6 && muPt[i] < 3.5) continue;
    muPassYId[i] = 1;
  } // loop over muons

  /// container for arbitration data
  typedef dimuonstree::upsilon::ArbitrationData Candidate;
  std::vector<Candidate> candidates(maxDimuons);
  candidates.clear();

  /// loop over dimuons
  for (int i=0; i<nDimuons; ++i) {
    isYCand[i] = 0;
    if (!muPassYId[dau1[i]] || !muPassYId[dau2[i]]) continue;
//     if (charge[i] != 0) continue;
//     if (mass[i] < 8. || mass[i] > 12.) continue;
    if (vProb[i] < 0.001) continue;
    if (TMath::Abs(muVz[dau1[i]] - muVz[dau2[i]]) > 2) continue;
    if (y[i] > 2.0) continue;
    /// store arbitration data
    Candidate cand = {i, vProb[i]};
    candidates.push_back(cand);
  } // loop over dimuons

  /// arbitration
  if (candidates.size() > 0) {
    std::sort(candidates.begin(), candidates.end(), dimuonstree::upsilon::compareDimuons);
    isYCand[ candidates[0].dimuonIndex ] = 1;
  }
}  // DimuonsTree::applyYSelection

/// Selection from the W and Z VBTF PAS EWK-10-002
void
DimuonsTree::applyZSelection() {
  /// loop over muons
  for (int i=0; i<nMuons; ++i) {
    muPassZId[i] = muPassZIdTight[i] = 0;
    if (!muIsTrackerMuon[i]) continue;
    if (muSiHits[i] < 10) continue;
    if (muPt[i] < 10.) continue;
    if (TMath::Abs(muEta[i]) > 2.4) continue;
    if (muTrackIso[i] > 3.0) continue;

    muPassZId[i] = 1;

    /// more cuts for the tight selection
    if (!muIsGlobalMuon[i]) continue;
    if (muGlobalNormalizedChi2[i] > 10.) continue;
    if (muStations[i] < 2) continue;
    if (muSiHits[i] < 11) continue;
    if (muPixelHits[i] < 1) continue;
    if (TMath::Abs(muSiD0BS[i]) > 0.2) continue;

    muPassZIdTight[i] = 1;
  } // loop over muons

  /// container for arbitration data
  typedef dimuonstree::upsilon::ArbitrationData Candidate;
  std::vector<Candidate> candidates(maxDimuons);
  candidates.clear();

  /// loop over dimuons
  for (int i=0; i<nDimuons; ++i) {
    isZCand[i] = 0;
//     if (charge[i] != 0) continue;
    if (!muPassZId[dau1[i]] || !muPassZId[dau2[i]]) continue;
    if (!muPassZIdTight[dau1[i]] && !muPassZIdTight[dau2[i]]) continue;
//     if (mass[i] < 60. || mass[i] > 120.) continue;
    if (TMath::Abs(muEta[dau1[i]]) > 2.1 &&
        TMath::Abs(muEta[dau2[i]]) > 2.1) continue;
    if (muPt[dau1[i]] < 15. &&
        muPt[dau1[i]] < 15. ) continue;  // at least 1 muon above 15 GeV
    isZCand[i] = 1;
  } // loop over dimuons

}  // DimuonsTree::applyZSelection

// https://twiki.cern.ch/twiki/bin/view/CMS/VbtfZMuMuBaselineSelection
void
DimuonsTree::applyVbtfBaselineSelection() {
  /// loop over muons
  for (int i=0; i<nMuons; ++i) {
    muPassVbtfBaseline[i] = muPassVbtfBaselineTight[i] = 0;

    if (!muIsGlobalMuon[i]) continue;
    if (muStripHits[i] + muPixelHits[i] < 10) continue;
    if (muTrackIso[i] > 3.0) continue;
    if (muPt[i] < 10.) continue;
    if (TMath::Abs(muEta[i]) > 2.4) continue;

    muPassVbtfBaseline[i] = 1;

    /// more cuts for the tight selection
    if (TMath::Abs(muDxyBS[i]) > 0.2) continue;
 if (muGlobalNormalizedChi2[i] > 10.) continue;
    if (muPixelHits[i] < 1) continue;
    if (muStations[i] < 2) continue;
    if (muMuonHits[i] < 1) continue;
    if (!muIsTrackerMuon[i]) continue;
    if (!muHltMu9Match[i] &&
        !muHltMu11Match[i] &&
        !muHltMu15v1Match[i]) continue;
    if (TMath::Abs(muEta[i]) > 2.1) continue;

    if (muHltMu15v1Match[i])    muPassVbtfBaselineTight[i] = 3;
    else if (muHltMu11Match[i]) muPassVbtfBaselineTight[i] = 2;
    else                        muPassVbtfBaselineTight[i] = 1;
  } // loop over muons

  /// loop over dimuons
  for (int i=0; i<nDimuons; ++i) {
    isVbtfBaselineCand[i] = 0;
    if (!HLT_Mu9 && !HLT_Mu11 && !HLT_Mu15_v1) continue;
    if (charge[i] != 0) continue;
    if (!muPassVbtfBaseline[dau1[i]] || !muPassVbtfBaseline[dau2[i]]) continue;
    if (!muPassVbtfBaselineTight[dau1[i]] && !muPassVbtfBaselineTight[dau2[i]]) continue;
    if (muPt[dau1[i]] < 15. &&
        muPt[dau1[i]] < 15. ) continue;  // at least 1 muon above 15 GeV
    if (HLT_Mu15_v1 &
         (
           muPassVbtfBaselineTight[dau1[i]] == 3 ||
           muPassVbtfBaselineTight[dau2[i]] == 3
         )
       )
    {
      isVbtfBaselineCand[i] = 3;
    }
    else if (HLT_Mu11 &
              (
                muPassVbtfBaselineTight[dau1[i]] == 2 ||
                muPassVbtfBaselineTight[dau2[i]] == 2
              )
            )
    {
      isVbtfBaselineCand[i] = 1;
    }
    else
    {
      isVbtfBaselineCand[i] = 3;
    }
  } // loop over dimuons

}  // DimuonsTree::applyVbtfBaselineSelection


// https://twiki.cern.ch/twiki/bin/view/CMS/VbtfZMuMuBaselineSelection
// without any trigger requirement
void
DimuonsTree::applyBaselineSelection() {
  /// loop over muons
  for (int i=0; i<nMuons; ++i) {
    muPassVbtfBaseline[i] = muPassBaselineTight[i] = 0;

    if (!muIsGlobalMuon[i]) continue;
    if (muStripHits[i] + muPixelHits[i] < 10) continue;
    if (muTrackIso[i] > 3.0) continue;
    if (muPt[i] < 10.) continue;
    if (TMath::Abs(muEta[i]) > 2.4) continue;

    muPassVbtfBaseline[i] = 1;

    /// more cuts for the tight selection
    if (TMath::Abs(muDxyBS[i]) > 0.2) continue;
    if (muGlobalNormalizedChi2[i] > 10.) continue;
    if (muPixelHits[i] < 1) continue;
    if (muStations[i] < 2) continue;
    if (muMuonHits[i] < 1) continue;
    if (!muIsTrackerMuon[i]) continue;
    if (TMath::Abs(muEta[i]) > 2.1) continue;

    muPassBaselineTight[i] = 1;
  } // loop over muons

  /// loop over dimuons
  for (int i=0; i<nDimuons; ++i) {
    isBaselineCand[i] = 0;
    if (charge[i] != 0) continue;
    if (!muPassVbtfBaseline[dau1[i]] || !muPassVbtfBaseline[dau2[i]]) continue;
    if (!muPassBaselineTight[dau1[i]] && !muPassBaselineTight[dau2[i]]) continue;
    if (muPt[dau1[i]] < 15. &&
        muPt[dau1[i]] < 15. ) continue;  // at least 1 muon above 15 GeV
    isBaselineCand[i] = 1;
  } // loop over dimuons

}  // DimuonsTree::applyBaselineSelection


void
DimuonsTree::setOrderByMuQAndPt() {
  /// container for arbitration / sorting data
  typedef dimuonstree::jpsi::ArbitrationData Candidate;
  std::vector<Candidate> candidates(maxDimuons);
  candidates.clear();
  /// loop over dimuons to fill the container
  for (int i=0; i<nDimuons; ++i) {
    Candidate cand = {i, 0, pt[i]};
    if (muIsGlobalMuon[dau1[i]]) ++cand.numberOfGlobalMuons;
    if (muIsGlobalMuon[dau2[i]]) ++cand.numberOfGlobalMuons;
    candidates.push_back(cand);
  } /// loop over dimuons
  /// arbitration
  std::sort(candidates.begin(), candidates.end(), dimuonstree::jpsi::compareDimuons);
  /// loop over dimuons again
  for (unsigned i = 0; i < candidates.size(); ++i) {
    /// store arbitration data
    orderByMuQAndPt[ candidates[i].dimuonIndex ] = i;
  } /// loop over dimuons
} // DimuonsTree::setOrderByMuQAndPt()


void
DimuonsTree::setOrderByVProb() {
  /// container for arbitration / sorting data
  typedef dimuonstree::upsilon::ArbitrationData Candidate;
  std::vector<Candidate> candidates(maxDimuons);
  candidates.clear();
  /// loop over dimuons to fill the container
  for (int i=0; i<nDimuons; ++i) {
    Candidate cand = {i, vProb[i]};
    candidates.push_back(cand);
  } /// loop over dimuons
  /// arbitration
  std::sort(candidates.begin(), candidates.end(), dimuonstree::upsilon::compareDimuons);
  /// loop over dimuons again
  for (unsigned i = 0; i < candidates.size(); ++i) {
    /// store arbitration data
    orderByVProb[ candidates[i].dimuonIndex ] = i;
  } /// loop over dimuons
} // DimuonsTree::setOrderByVProb()


void
DimuonsTree::setCorrectedMassJPsi()
{
  TLorentzVector p1, p2;
  const double muMass = 0.105658369; /// GeV / c^2
  int i, d1, d2;
  for (i=0, d1=dau1[i], d2=dau2[i]; i < nDimuons; ++i, d1=dau1[i], d2=dau2[i]) {
    p1.SetPtEtaPhiM(1.0009 * muPt[d1], muEta[d1], muPhi[d1], muMass);
    p2.SetPtEtaPhiM(1.0009 * muPt[d2], muEta[d2], muPhi[d2], muMass);
    correctedMassJPsi[i] = (p1+p2).M();
  }
} /// DimuonsTree::setCorrectedMassJPsi


void
DimuonsTree::setCorrectedMassY()
{
  const double a[] = {0.002, -0.002, 0.001, -0.0001};
  const double muMass = 0.105658369; /// GeV / c^2
  int i, d1, d2;
  TLorentzVector p1, p2;
  for (i=0, d1=dau1[i], d2=dau2[i]; i < nDimuons; ++i, d1=dau1[i], d2=dau2[i]) {
    double corr1 = a[0] + a[1]*TMath::Abs(muEta[d1]) + a[2]*muEta[d1]*muEta[d1] + a[3]*muPt[d1];
    double corr2 = a[0] + a[1]*TMath::Abs(muEta[d2]) + a[2]*muEta[d2]*muEta[d2] + a[3]*muPt[d2];
    p1.SetPtEtaPhiM( (1. + corr1) * muPt[d1], muEta[d1], muPhi[d1], muMass);
    p2.SetPtEtaPhiM( (1. + corr2) * muPt[d2], muEta[d2], muPhi[d2], muMass);
    correctedMassY[i] = (p1+p2).M();
  }
} /// DimuonsTree::setCorrectedMassY

void
DimuonsTree::init(TTree *tree) {
  tree_ = tree;
  if (!tree_) return;
  tree_->Branch("run"              , &run              , "run/i"              );
  tree_->Branch("lumi"             , &lumi             , "lumi/i"             );
  tree_->Branch("event"            , &event            , "event/i"            );
  tree_->Branch("L1DoubleMuOpen"   , &L1DoubleMuOpen   , "L1DoubleMuOpen/b"   );
  tree_->Branch("HLT_Mu3"          , &HLT_Mu3          , "HLT_Mu3/b"          );
  tree_->Branch("HLT_Mu9"          , &HLT_Mu9          , "HLT_Mu9/b"          );
  tree_->Branch("HLT_Mu11"         , &HLT_Mu11         , "HLT_Mu11/b"         );
  tree_->Branch("HLT_Mu15_v1"      , &HLT_Mu15_v1      , "HLT_Mu15_v1/b"      );
  tree_->Branch("nDimuons"         , &nDimuons         , "nDimuons/I"         );
  tree_->Branch("nMuons"           , &nMuons           , "nMuons/I"           );
  tree_->Branch("nVertices"        , &nVertices        , "nVertices/I"        );

  tree_->Branch("mass"             , mass             , "mass[nDimuons]/F"             );
  tree_->Branch("massGen"          , massGen          , "massGen[nDimuons]/F"          );
  tree_->Branch("massVanilla"      , massVanilla      , "massVanilla[nDimuons]/F"      );
  tree_->Branch("pt"               , pt               , "pt[nDimuons]/F"               );
  tree_->Branch("eta"              , eta              , "eta[nDimuons]/F"              );
  tree_->Branch("phi"              , phi              , "phi[nDimuons]/F"              );
  tree_->Branch("y"                , y                , "y[nDimuons]/F"                );
  tree_->Branch("p"                , p                , "p[nDimuons]/F"                );
  tree_->Branch("charge"           , charge           , "charge[nDimuons]/I"           );
  tree_->Branch("vProb"            , vProb            , "vProb[nDimuons]/F"            );
  tree_->Branch("vrho"             , vrho             , "vrho[nDimuons]/F"             );
  tree_->Branch("vrhoBS"           , vrhoBS           , "vrhoBS[nDimuons]/F"           );
  tree_->Branch("vrhoPV"           , vrhoPV           , "vrhoPV[nDimuons]/F"           );
  tree_->Branch("vx"               , vx               , "vx[nDimuons]/F"               );
  tree_->Branch("vxBS"             , vxBS             , "vxBS[nDimuons]/F"             );
  tree_->Branch("vxPV"             , vxPV             , "vxPV[nDimuons]/F"             );
  tree_->Branch("vy"               , vy               , "vy[nDimuons]/F"               );
  tree_->Branch("vyBS"             , vyBS             , "vyBS[nDimuons]/F"             );
  tree_->Branch("vyPV"             , vyPV             , "vyPV[nDimuons]/F"             );
  tree_->Branch("vz"               , vz               , "vz[nDimuons]/F"               );
  tree_->Branch("vzBS"             , vzBS             , "vzBS[nDimuons]/F"             );
  tree_->Branch("vzPV"             , vzPV             , "vzPV[nDimuons]/F"             );
  tree_->Branch("d0"               , d0               , "d0[nDimuons]/F"               );
  tree_->Branch("d0BS"             , d0BS             , "d0BS[nDimuons]/F"             );
  tree_->Branch("d0PV"             , d0PV             , "d0PV[nDimuons]/F"             );
  tree_->Branch("dz"               , dz               , "dz[nDimuons]/F"               );
  tree_->Branch("dzBS"             , dzBS             , "dzBS[nDimuons]/F"             );
  tree_->Branch("dzPV"             , dzPV             , "dzPV[nDimuons]/F"             );
  tree_->Branch("dsz"              , dsz              , "dsz[nDimuons]/F"              );
  tree_->Branch("dszBS"            , dszBS            , "dszBS[nDimuons]/F"            );
  tree_->Branch("dszPV"            , dszPV            , "dszPV[nDimuons]/F"            );
  tree_->Branch("pdgId"            , pdgId            , "pdgId[nDimuons]/I"            );
  tree_->Branch("backToBack"       , backToBack       , "backToBack[nDimuons]/F"       );
  tree_->Branch("dau1"             , dau1             , "dau1[nDimuons]/b"             );
  tree_->Branch("dau2"             , dau2             , "dau2[nDimuons]/b"             );
  tree_->Branch("correctedMassJPsi", correctedMassJPsi, "correctedMassJPsi[nDimuons]/F");
  tree_->Branch("correctedMassY"   , correctedMassY   , "correctedMassY[nDimuons]/F"   );
  tree_->Branch("isJPsiCand"       , isJPsiCand       , "isJPsiCand[nDimuons]/b"       );
  tree_->Branch("isYCand"          , isYCand          , "isYCand[nDimuons]/b"          );
  tree_->Branch("isZCand"          , isZCand          , "isZCand[nDimuons]/b"          );
  tree_->Branch("isVbtfBaselineCand"          , isVbtfBaselineCand          , "isVbtfBaselineCand[nDimuons]/b"          );
  tree_->Branch("isBaselineCand"          , isBaselineCand          , "isBaselineCand[nDimuons]/b"          );
  tree_->Branch("orderByMuQAndPt"  , orderByMuQAndPt  , "orderByMuQAndPt[nDimuons]/b"  );
  tree_->Branch("orderByVProb"     , orderByVProb     , "orderByVProb[nDimuons]/b"     );

  tree_->Branch("muPt"                     , muPt                     , "muPt[nMuons]/F"                     );
  tree_->Branch("muEta"                    , muEta                    , "muEta[nMuons]/F"                    );
  tree_->Branch("muPhi"                    , muPhi                    , "muPhi[nMuons]/F"                    );
  tree_->Branch("muVtx"                    , muVtx                    , "muVtx[3][nMuons]/F"                    );
  tree_->Branch("muGenPt"                  , muGenPt                  , "muGenPt[nMuons]/F"                     );
  tree_->Branch("muGenEta"                 , muGenEta                 , "muGenEta[nMuons]/F"                    );
  tree_->Branch("muGenPhi"                 , muGenPhi                 , "muGenPhi[nMuons]/F"                    );
  tree_->Branch("muGenVtx"                 , muGenVtx                 , "muGenVtx[3][nMuons]/F"                 );
  tree_->Branch("muP"                      , muP                      , "muP[nMuons]/F"                      );
  tree_->Branch("muCharge"                 , muCharge                 , "muCharge[nMuons]/I"                 );
  tree_->Branch("muDxyPV"                  , muDxyPV                  , "muDxyPV[nMuons]/F"                  );
  tree_->Branch("muDxyBS"                  , muDxyBS                  , "muDxyBS[nMuons]/F"                  );
  tree_->Branch("muSiNormalizedChi2"       , muSiNormalizedChi2       , "muSiNormalizedChi2[nMuons]/F"       );
  tree_->Branch("muSiD0"                   , muSiD0                   , "muSiD0[nMuons]/F"                   );
  tree_->Branch("muSiD0BS"                 , muSiD0BS                 , "muSiD0BS[nMuons]/F"                 );
  tree_->Branch("muSiD0PV"                 , muSiD0PV                 , "muSiD0PV[nMuons]/F"                 );
  tree_->Branch("muSiDz"                   , muSiDz                   , "muSiDz[nMuons]/F"                   );
  tree_->Branch("muSiDzBS"                 , muSiDzBS                 , "muSiDzBS[nMuons]/F"                 );
  tree_->Branch("muSiDzPV"                 , muSiDzPV                 , "muSiDzPV[nMuons]/F"                 );
  tree_->Branch("muSiDsz"                  , muSiDsz                  , "muSiDsz[nMuons]/F"                  );
  tree_->Branch("muSiDszBS"                , muSiDszBS                , "muSiDszBS[nMuons]/F"                );
  tree_->Branch("muSiDszPV"                , muSiDszPV                , "muSiDszPV[nMuons]/F"                );
  tree_->Branch("muSiHits"                 , muSiHits                 , "muSiHits[nMuons]/b"                 );
  tree_->Branch("muPixelHits"              , muPixelHits              , "muPixelHits[nMuons]/b"              );
  tree_->Branch("muStripHits"              , muStripHits              , "muStripHits[nMuons]/b"              );
  tree_->Branch("muMuonHits"               , muMuonHits               , "muMuonHits[nMuons]/b"               );
  tree_->Branch("muStations"               , muStations               , "muStations[nMuons]/b"               );
  tree_->Branch("muGlobalNormalizedChi2"   , muGlobalNormalizedChi2   , "muGlobalNormalizedChi2[nMuons]/b"   );
  tree_->Branch("muVz"                     , muVz                     , "muVz[nMuons]/F"                     );
  tree_->Branch("muIsGlobalMuon"           , muIsGlobalMuon           , "muIsGlobalMuon[nMuons]/B"           );
  tree_->Branch("muIsTrackerMuon"          , muIsTrackerMuon          , "muIsTrackerMuon[nMuons]/B"          );
  tree_->Branch("muIsTMLastStationAngTight", muIsTMLastStationAngTight, "muIsTMLastStationAngTight[nMuons]/B");
  tree_->Branch("muIsTrackerMuonArbitrated", muIsTrackerMuonArbitrated, "muIsTrackerMuonArbitrated[nMuons]/B");
  tree_->Branch("muTrackIso"               , muTrackIso               , "muTrackIso[nMuons]/F"               );
  tree_->Branch("muEcalIso"                , muEcalIso                , "muEcalIso[nMuons]/F"                );
  tree_->Branch("muHcalIso"                , muHcalIso                , "muHcalIso[nMuons]/F"                );
  tree_->Branch("muPassJPsiId"             , muPassJPsiId             , "muPassJPsiId[nMuons]/b"             );
  tree_->Branch("muPassYId"                , muPassYId                , "muPassYId[nMuons]/b"                );
  tree_->Branch("muPassZId"                , muPassZId                , "muPassZId[nMuons]/b"                );
  tree_->Branch("muPassZIdTight"           , muPassZIdTight           , "muPassZIdTight[nMuons]/b"           );
  tree_->Branch("muPassVbtfBaseline"       , muPassVbtfBaseline       , "muPassVbtfBaseline[nMuons]/b"       );
  tree_->Branch("muPassVbtfBaselineTight"  , muPassVbtfBaselineTight  , "muPassVbtfBaselineTight[nMuons]/b"  );
  tree_->Branch("muPassBaselineTight"  , muPassBaselineTight  , "muPassBaselineTight[nMuons]/b"  );
  tree_->Branch("muHltMu9Match"            , muHltMu9Match            , "muHltMu9Match[nMuons]/b"            );
  tree_->Branch("muHltMu11Match"           , muHltMu11Match           , "muHltMu11Match[nMuons]/b"           );
  tree_->Branch("muHltMu15v1Match"         , muHltMu15v1Match         , "muHltMu15v1Match[nMuons]/b"         );
}

void
DimuonsTree::initLeafVariables()
{
  run               = 0;
  lumi              = 0;
  event             = 0;
  L1DoubleMuOpen    = 0;
  HLT_Mu3           = 0;
  HLT_Mu9           = 0;
  HLT_Mu11          = 0;
  HLT_Mu15_v1       = 0;
  nDimuons          = 0;
  nMuons            = 0;
  nVertices         = 0;

  for (int i=0; i<nDimuons; ++i) {
    mass[i]              = 0;
    massGen[i]              = 0;
    massVanilla[i]       = 0;
    pt[i]                = 0;
    eta[i]               = 0;
    phi[i]               = 0;
    y[i]                 = 0;
    p[i]                 = 0;
    charge[i]            = 0;
    vProb[i]             = 0;
    vrho[i]              = 0;
    vrhoBS[i]            = 0;
    vrhoPV[i]            = 0;
    vx[i]                = 0;
    vxBS[i]              = 0;
    vxPV[i]              = 0;
    vy[i]                = 0;
    vyBS[i]              = 0;
    vyPV[i]              = 0;
    vz[i]                = 0;
    vzBS[i]              = 0;
    vzPV[i]              = 0;
    d0[i]                = 0;
    d0BS[i]              = 0;
    d0PV[i]              = 0;
    dz[i]                = 0;
    dzBS[i]              = 0;
    dzPV[i]              = 0;
    dsz[i]               = 0;
    dszBS[i]             = 0;
    dszPV[i]             = 0;
    pdgId[i]             = 0;
    backToBack[i]        = 0;
    dau1[i]              = 0;
    dau2[i]              = 0;
    correctedMassJPsi[i] = 0;
    correctedMassY[i]    = 0;
    isJPsiCand[i]        = 0;
    isYCand[i]           = 0;
    isZCand[i]           = 0;
    isVbtfBaselineCand[i] = 0;
    isBaselineCand[i]    = 0;
    orderByMuQAndPt[i]   = 0;
    orderByVProb[i]      = 0;
  }

  for (int i=0; i<maxMuons; ++i) {
    muPt[i]                      = 0;
    muEta[i]                     = 0;
    muPhi[i]                     = 0;
    muGenPt[i]                   = 0;
    muGenEta[i]                  = 0;
    muGenPhi[i]                  = 0;
    muP[i]                       = 0;
    muCharge[i]                  = 0;
    muDxyPV[i]                   = 0;
    muDxyBS[i]                   = 0;
    muSiNormalizedChi2[i]        = 0;
    muSiD0[i]                    = 0;
    muSiD0BS[i]                  = 0;
    muSiD0PV[i]                  = 0;
    muSiDz[i]                    = 0;
    muSiDzBS[i]                  = 0;
    muSiDzPV[i]                  = 0;
    muSiDsz[i]                   = 0;
    muSiDszBS[i]                 = 0;
    muSiDszPV[i]                 = 0;
    muSiHits[i]                  = 0;
    muPixelHits[i]               = 0;
    muStripHits[i]               = 0;
    muMuonHits[i]                = 0;
    muStations[i]                = 0;
    muGlobalNormalizedChi2[i]    = 0;
    muVz[i]                      = 0;
    muIsGlobalMuon[i]            = 0;
    muIsTrackerMuon[i]           = 0;
    muIsTMLastStationAngTight[i] = 0;
    muIsTrackerMuonArbitrated[i] = 0;
    muTrackIso[i]                = 0;
    muEcalIso[i]                 = 0;
    muHcalIso[i]                 = 0;
    muPassJPsiId[i]              = 0;
    muPassYId[i]                 = 0;
    muPassZId[i]                 = 0;
    muPassZIdTight[i]            = 0;
    muPassVbtfBaseline[i]        = 0;
    muPassVbtfBaselineTight[i]   = 0;
    muPassBaselineTight[i]       = 0;
    muHltMu9Match[i]             = 0;
    muHltMu11Match[i]            = 0;
    muHltMu15v1Match[i]          = 0;
    for (int j=0; j<3; ++j) {
      muVtx   [j][i]             = 0;
      muGenVtx[j][i]             = 0;
    }
  }
}

int
DimuonsTree::Fill() {
  return tree_->Fill();
}