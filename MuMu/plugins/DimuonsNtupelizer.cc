// #include <map>
// #include <string>
#include <iostream>

#include "TH1.h"
#include "TMath.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/Candidate/interface/VertexCompositeCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"


#include "JPsi/MuMu/interface/DimuonsTree.h"

class DimuonsNtupelizer : public edm::EDAnalyzer {

public:
  explicit DimuonsNtupelizer(const edm::ParameterSet&);
  ~DimuonsNtupelizer();
  
private:
  typedef math::XYZPoint Point;

  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  double dxy(const reco::VertexCompositeCandidate&,
             const Point& beamSpot = Point(0,0,0)
             ) const;
  double dz(const reco::VertexCompositeCandidate&,
            const Point& beamSpot = Point(0,0,0)
            ) const;
  double dsz(const reco::VertexCompositeCandidate&,
             const Point& beamSpot = Point(0,0,0)
             ) const;
  double rho(const reco::VertexCompositeCandidate&,
             const Point& beamSpot = Point(0,0,0)
             ) const;
  
  DimuonsTree dimuonsTree_;

  // input tags  
  edm::InputTag photonSrc_;
  edm::InputTag muonSrc_;
  edm::InputTag dimuonSrc_;
  edm::InputTag beamSpotSrc_;
  edm::InputTag primaryVertexSrc_;

};

#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

DimuonsNtupelizer::DimuonsNtupelizer(const edm::ParameterSet& iConfig):
  dimuonsTree_(),
  photonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("photonSrc")),
  muonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("muonSrc")),
  dimuonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("dimuonSrc")),
  beamSpotSrc_(iConfig.getUntrackedParameter<edm::InputTag>("beamSpotSrc")),
  primaryVertexSrc_(iConfig.getUntrackedParameter<edm::InputTag>("primaryVertexSrc"))
{
}

DimuonsNtupelizer::~DimuonsNtupelizer()
{
}

/// dxy parameter. (This is the transverse impact parameter w.r.t. to beamSpot, see DataFormats/TrackReco/interface/TrackBase.h
double DimuonsNtupelizer::dxy(const reco::VertexCompositeCandidate& cand,
                              const Point& beamSpot
                              ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  return (- vx * cand.py() + vy * cand.px() ) / cand.pt();
}


/// dsz parameter, see DataFormats/TrackReco/interface/TrackBase.h
double DimuonsNtupelizer::dsz(const reco::VertexCompositeCandidate& cand,
                              const Point& beamSpot
                              ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  double vz = cand.vz() - beamSpot.Z();
  return vz * cand.pt() / cand.p() - (vx * cand.px() + vy * cand.py() ) / cand.pt() * (cand.pz() / cand.p() );
}


/// dz parameter (= dsz/cos(lambda)). This is the track z0 w.r.t beamSpot, 
double DimuonsNtupelizer::dz(const reco::VertexCompositeCandidate& cand,
                             const Point& beamSpot
                             ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  double vz = cand.vz() - beamSpot.Z();
  return vz - (vx * cand.px() + vy * cand.py() ) / cand.pt() * (cand.pz() / cand.pt() );
}

/// rho parameter = distance in the xy-plane
double DimuonsNtupelizer::rho(const reco::VertexCompositeCandidate& cand,
                              const Point& beamSpot
                              ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  return sqrt(vx*vx + vy*vy);
}


void
DimuonsNtupelizer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  dimuonsTree_.initLeafVariables();

  // get muon collection
  edm::Handle<edm::View<pat::Muon> > muons;
  iEvent.getByLabel(muonSrc_,muons);

  // get photon collection  
  edm::Handle<edm::View<pat::Photon> > photons;
  iEvent.getByLabel(photonSrc_,photons);

  // get dimuon collection
  edm::Handle<reco::VertexCompositeCandidateView> dimuons;
  iEvent.getByLabel(dimuonSrc_,dimuons);

  edm::Handle<reco::BeamSpot> beamSpot;
  iEvent.getByLabel(beamSpotSrc_, beamSpot);
  
  edm::Handle<edm::View<reco::Vertex> > primaryVertices;
  iEvent.getByLabel(primaryVertexSrc_, primaryVertices);

  dimuonsTree_.run   = iEvent.run();
  dimuonsTree_.lumi  = iEvent.id().luminosityBlock();
  dimuonsTree_.event = iEvent.id().event();

  // TODO: ADD THE HLT BITS
/*  dimuonsTree_.L1DoubleMuOpen    = dimuon->L1DoubleMuOpen();
  dimuonsTree_.HLT_Mu3           = dimuon->HLT_Mu3();
  dimuonsTree_.HLT_Mu9           = dimuon->HLT_Mu9();*/

  dimuonsTree_.nDimuons = dimuons->size();
  if (dimuonsTree_.nDimuons > DimuonsTree::maxDimuons)
    dimuonsTree_.nDimuons = DimuonsTree::maxDimuons;

  dimuonsTree_.nMuons = muons->size();
  if (dimuonsTree_.nMuons > DimuonsTree::maxMuons)
    dimuonsTree_.nMuons = DimuonsTree::maxMuons;
  

  // loop over dimuons
  reco::VertexCompositeCandidateView::const_iterator dimuon;
  int i;
  for(dimuon = dimuons->begin(), i=0;
      i < dimuonsTree_.nDimuons; ++dimuon, ++i) {

  
    dimuonsTree_.mass[i]              = dimuon->mass();
    dimuonsTree_.pt[i]                = dimuon->pt();
    dimuonsTree_.eta[i]               = dimuon->eta();
    dimuonsTree_.phi[i]               = dimuon->phi();
    dimuonsTree_.y[i]                 = dimuon->y();
    dimuonsTree_.p[i]                 = dimuon->p();
    dimuonsTree_.charge[i]            = dimuon->charge();

    dimuonsTree_.vProb [i] = TMath::Prob(dimuon->vertexChi2(),
                                      dimuon->vertexNdof()
                                      );
    dimuonsTree_.vrho  [i] = rho(*dimuon);
    dimuonsTree_.vrhoBS[i] = rho(*dimuon, beamSpot->position() );
    dimuonsTree_.vrhoPV[i] = rho(*dimuon, primaryVertices->at(0).position() );
    dimuonsTree_.vx    [i] = dimuon->vx();
    dimuonsTree_.vxBS  [i] = dimuon->vx() - beamSpot->position().X();
    dimuonsTree_.vxPV  [i] = dimuon->vx() - primaryVertices->at(0).position().X();
    dimuonsTree_.vy    [i] = dimuon->vy();
    dimuonsTree_.vyBS  [i] = dimuon->vy() - beamSpot->position().Y();
    dimuonsTree_.vyPV  [i] = dimuon->vy() - primaryVertices->at(0).position().Y();
    dimuonsTree_.vz    [i] = dimuon->vz();
    dimuonsTree_.vzBS  [i] = dimuon->vz() - beamSpot->position().Z();
    dimuonsTree_.vzPV  [i] = dimuon->vz() - primaryVertices->at(0).position().Z();

    dimuonsTree_.d0   [i] = - dxy(*dimuon);
    dimuonsTree_.d0BS [i] = - dxy(*dimuon, beamSpot->position() );
    dimuonsTree_.d0PV [i] = - dxy(*dimuon, primaryVertices->at(0).position() );
    dimuonsTree_.dz   [i] = dz(*dimuon);
    dimuonsTree_.dzBS [i] = dz(*dimuon, beamSpot->position() );
    dimuonsTree_.dzPV [i] = dz(*dimuon, primaryVertices->at(0).position() );
    dimuonsTree_.dsz  [i] = dsz(*dimuon);
    dimuonsTree_.dszBS[i] = dsz(*dimuon, beamSpot->position() );
    dimuonsTree_.dszPV[i] = dsz(*dimuon, primaryVertices->at(0).position() );
    const double pdgMassJPsi  =  3.097,
                 pdgMassPsi2S =  3.686,
                 pdgMassY1S   =  9.460,
                 pdgMassY2S   = 10.023,
                 pdgMassY3S   = 10.355,
                 pdgMassZ     = 91.187;
    const int pdgIdJPsi  =    443,
              pdgIdPsi2S = 100443,
              pdgIdY1S   =    553,
              pdgIdY2S   = 100553,
              pdgIdY3S   = 200553,
              pdgIdZ     =     23;

    const double epsilon = 0.025;
    if ( dimuon->charge() == 0 ) {
      if ( dimuon->mass() > (1. - epsilon) * pdgMassJPsi &&
           dimuon->mass() < (1. + epsilon) * pdgMassJPsi )
        dimuonsTree_.pdgId[i] = pdgIdJPsi;
      else if ( dimuon->mass() > (1. - epsilon) * pdgMassPsi2S &&
                dimuon->mass() < (1. + epsilon) * pdgMassPsi2S )
        dimuonsTree_.pdgId[i] = pdgIdPsi2S;
      else if ( dimuon->mass() > (1. - epsilon) * pdgMassY1S &&
                dimuon->mass() < (1. + epsilon) * pdgMassY1S )
        dimuonsTree_.pdgId[i] = pdgIdY1S;
      else if ( dimuon->mass() > (1. - epsilon) * pdgMassY2S &&
                dimuon->mass() < 0.5 * (pdgMassY2S + pdgMassY3S) )
        dimuonsTree_.pdgId[i] = pdgIdY2S;
      else if ( dimuon->mass() >= 0.5 * (pdgMassY2S + pdgMassY3S) &&
                dimuon->mass() < (1. + epsilon) * pdgMassY3S)
        dimuonsTree_.pdgId[i] = pdgIdY3S;
      else if ( dimuon->mass() > (1. - epsilon) * pdgMassZ &&
                dimuon->mass() < (1. + epsilon) * pdgMassZ)
        dimuonsTree_.pdgId[i] = pdgIdZ;
    } else {
      dimuonsTree_.pdgId[i] = 0;
    }

    // get the daughters
    const reco::CandidateBaseRef dau1 = dimuon->daughter(0)->masterClone();
    const reco::CandidateBaseRef dau2 = dimuon->daughter(1)->masterClone();
    double cosOpeningAngle = dau1->momentum().Dot(dau2->momentum()) /
                             ( dau1->p() * dau2->p() );
    dimuonsTree_.backToBack[i] = 0.5 * (1. - cosOpeningAngle);

    dimuonsTree_.dau1[i] = dau1.key();
    dimuonsTree_.dau2[i] = dau2.key();
  } // loop over dimuons

  // loop over muons
  edm::View<pat::Muon>::const_iterator mu;
  for(mu = muons->begin(), i=0; i < dimuonsTree_.nMuons; ++mu, ++i) {
    // set the daughter leafs
    dimuonsTree_.muPt[i]                      = mu->pt();
    dimuonsTree_.muEta[i]                     = mu->eta();
    dimuonsTree_.muPhi[i]                     = mu->phi();
    dimuonsTree_.muP[i]                       = mu->p();
    dimuonsTree_.muCharge[i]                  = mu->charge();
    dimuonsTree_.muSiNormalizedChi2[i]        = mu->innerTrack()->normalizedChi2();
    dimuonsTree_.muSiD0[i]                    = mu->innerTrack()->d0();
    dimuonsTree_.muSiD0BS[i]                  = - mu->innerTrack()->dxy( beamSpot->position() );
    dimuonsTree_.muSiD0PV[i]                  = - mu->innerTrack()->dxy( primaryVertices->at(0).position() );
    dimuonsTree_.muSiDz[i]                    = mu->innerTrack()->dz();
    dimuonsTree_.muSiDzBS[i]                  = mu->innerTrack()->dz( beamSpot->position() );
    dimuonsTree_.muSiDzPV[i]                  = mu->innerTrack()->dz( primaryVertices->at(0).position() );
    dimuonsTree_.muSiDsz[i]                   = mu->innerTrack()->dsz();
    dimuonsTree_.muSiDszBS[i]                 = mu->innerTrack()->dsz( beamSpot->position() );
    dimuonsTree_.muSiDszPV[i]                 = mu->innerTrack()->dsz( primaryVertices->at(0).position() );
    dimuonsTree_.muSiHits[i]                  = mu->innerTrack()->found();
    dimuonsTree_.muPixelHits[i]               = mu->innerTrack()->hitPattern().numberOfValidPixelHits();
    // count stations
    unsigned nStations = 0, stationMask = mu->stationMask();
    for (; stationMask; nStations++) 
      stationMask &= stationMask - 1; // clear the least significant bit set
    dimuonsTree_.muStations[i]                = nStations;
    dimuonsTree_.muVz[i]                      = mu->vz();
    dimuonsTree_.muIsGlobalMuon[i]            = mu->isGlobalMuon();
    dimuonsTree_.muIsTrackerMuon[i]           = mu->isTrackerMuon();
    dimuonsTree_.muIsTMLastStationAngTight[i] = mu->muonID("TMLastStationAngTight");
    dimuonsTree_.muIsTrackerMuonArbitrated[i] = mu->muonID("TrackerMuonArbitrated");
    dimuonsTree_.muTrackIso[i]                = mu->trackIso();
    dimuonsTree_.muEcalIso[i]                 = mu->ecalIso();
    dimuonsTree_.muHcalIso[i]                 = mu->hcalIso();
//     dimuonsTree_.muHltMu9Match[i]             = mu->hltMu9Match();
  } // loop over muons

  dimuonsTree_.applyJPsiSelection();
  dimuonsTree_.applyYSelection();
  dimuonsTree_.applyZSelection();

  dimuonsTree_.setOrderByMuQAndPt();
  dimuonsTree_.setOrderByVProb();

  dimuonsTree_.setCorrectedMassJPsi();
  dimuonsTree_.setCorrectedMassY();

  dimuonsTree_.Fill();
}

void 
DimuonsNtupelizer::beginJob()
{
  // register to the TFileService
  edm::Service<TFileService> fs;
  
  // book the tree:
  dimuonsTree_.init( fs->make<TTree>("dimuons", "dimuons tree") );
}

void 
DimuonsNtupelizer::endJob() 
{
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(DimuonsNtupelizer);
