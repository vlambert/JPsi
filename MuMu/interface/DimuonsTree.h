#ifndef JPsi_MuMu_DimuonsTree_h
#define JPsi_MuMu_DimuonsTree_h

#include <TTree.h>

class DimuonsTree {
public:
  DimuonsTree(TTree *tree=0);
  ~DimuonsTree();
  int Fill();
  void init(TTree*);
  void initLeafVariables();
  void applyJPsiSelection();
  void applyYSelection();
  void applyZSelection();
  void applyVbtfBaselineSelection();
  void applyBaselineSelection();
  void setOrderByMuQAndPt();
  void setOrderByVProb();
  void setCorrectedMassJPsi();  /// TODO
  void setCorrectedMassY();     /// TODO

  const static unsigned char maxMuons = 10;
  const static unsigned char maxDimuons = 45;

  // event leaf variables
  unsigned      run           ;
  unsigned      lumi          ;
  unsigned      event         ;
  unsigned char L1DoubleMuOpen;
  unsigned char HLT_Mu3       ;
  unsigned char HLT_Mu9       ;
  unsigned char HLT_Mu11      ;
  unsigned char HLT_Mu15_v1   ;
  Int_t         nDimuons      ;
  Int_t         nMuons        ;
  Int_t         nVertices     ;

  // dimuon leaf variables
  float         mass             [maxDimuons];
  float         massGen          [maxDimuons];
  float         massVanilla      [maxDimuons];
  float         pt               [maxDimuons];
  float         eta              [maxDimuons];
  float         phi              [maxDimuons];
  float         y                [maxDimuons];
  float         p                [maxDimuons];
  int           charge           [maxDimuons];
  float         vProb            [maxDimuons];
  float         vrho             [maxDimuons];
  float         vrhoBS           [maxDimuons];
  float         vrhoPV           [maxDimuons];
  float         vx               [maxDimuons];
  float         vxBS             [maxDimuons];
  float         vxPV             [maxDimuons];
  float         vy               [maxDimuons];
  float         vyBS             [maxDimuons];
  float         vyPV             [maxDimuons];
  float         vz               [maxDimuons];
  float         vzBS             [maxDimuons];
  float         vzPV             [maxDimuons];
  float         d0               [maxDimuons];
  float         d0BS             [maxDimuons];
  float         d0PV             [maxDimuons];
  float         dz               [maxDimuons];
  float         dzBS             [maxDimuons];
  float         dzPV             [maxDimuons];
  float         dsz              [maxDimuons];
  float         dszBS            [maxDimuons];
  float         dszPV            [maxDimuons];
  int           pdgId            [maxDimuons];
  float         backToBack       [maxDimuons];
  unsigned char dau1             [maxDimuons];
  unsigned char dau2             [maxDimuons];
  float         correctedMassJPsi[maxDimuons];
  float         correctedMassY   [maxDimuons];
  unsigned char isJPsiCand       [maxDimuons];
  unsigned char isYCand          [maxDimuons];
  unsigned char isZCand          [maxDimuons];
  unsigned char isVbtfBaselineCand[maxDimuons];
  unsigned char isBaselineCand[maxDimuons];
  unsigned char orderByMuQAndPt  [maxDimuons];
  unsigned char orderByVProb     [maxDimuons];

  // muon leaf variables
  float         muPt                     [maxMuons];
  float         muEta                    [maxMuons];
  float         muPhi                    [maxMuons];
  float         muVtx[3]                 [maxMuons];
  float         muGenPt                  [maxMuons];
  float         muGenEta                 [maxMuons];
  float         muGenPhi                 [maxMuons];
  float         muGenVtx[3]              [maxMuons];
  float         muP                      [maxMuons];
  int           muCharge                 [maxMuons];
  float         muDxyBS                  [maxMuons];
  float         muDxyPV                  [maxMuons];
  float         muSiNormalizedChi2       [maxMuons];
  float         muSiD0                   [maxMuons];
  float         muSiD0BS                 [maxMuons];
  float         muSiD0PV                 [maxMuons];
  float         muSiDz                   [maxMuons];
  float         muSiDzBS                 [maxMuons];
  float         muSiDzPV                 [maxMuons];
  float         muSiDsz                  [maxMuons];
  float         muSiDszBS                [maxMuons];
  float         muSiDszPV                [maxMuons];
  unsigned char muSiHits                 [maxMuons];
  unsigned char muPixelHits              [maxMuons];
  unsigned char muStripHits              [maxMuons];
  unsigned char muMuonHits               [maxMuons];
  unsigned char muStations               [maxMuons];
  float         muGlobalNormalizedChi2   [maxMuons];
  float         muVz                     [maxMuons];
  char          muIsGlobalMuon           [maxMuons];
  char          muIsTrackerMuon          [maxMuons];
  char          muIsTMLastStationAngTight[maxMuons];
  char          muIsTrackerMuonArbitrated[maxMuons];
  float         muTrackIso               [maxMuons];
  float         muEcalIso                [maxMuons];
  float         muHcalIso                [maxMuons];
  unsigned char muPassJPsiId             [maxMuons];
  unsigned char muPassYId                [maxMuons];
  unsigned char muPassZId                [maxMuons];
  unsigned char muPassZIdTight           [maxMuons];
  unsigned char muPassVbtfBaseline       [maxMuons];
  unsigned char muPassVbtfBaselineTight  [maxMuons];
  unsigned char muPassBaselineTight      [maxMuons];
  unsigned char muHltMu9Match            [maxMuons];
  unsigned char muHltMu11Match           [maxMuons];
  unsigned char muHltMu15v1Match         [maxMuons];

private:
  TTree *tree_;
};

#endif