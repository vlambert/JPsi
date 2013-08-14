// #include <map>
// #include <string>
#include <iostream>

#include "TH1.h"
#include "TMath.h"

#include "CommonTools/CandUtils/interface/AddFourMomenta.h"
#include "CommonTools/UtilAlgos/interface/DeltaR.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CondFormats/DataRecord/interface/EcalChannelStatusRcd.h"
#include "CondFormats/EcalObjects/interface/EcalChannelStatus.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/CaloRecHit/interface/CaloCluster.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/Candidate/interface/VertexCompositeCandidate.h"
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/EDMException.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"
#include "RecoLocalCalo/EcalRecAlgos/interface/EcalSeverityLevelAlgo.h"

#include "JPsi/MuMu/interface/MuMuGammaTree.h"

class MuMuGammaTreeMaker : public edm::EDAnalyzer {

public:
  explicit MuMuGammaTreeMaker(const edm::ParameterSet&);
  ~MuMuGammaTreeMaker();

private:
  typedef math::XYZPoint Point;
  typedef math::XYZVector Vector;
  typedef math::XYZTLorentzVector LorentzVector;

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

  MuMuGammaTree tree_;

  // input tags
  edm::InputTag photonSrc_;
  edm::InputTag muonSrc_;
  edm::InputTag dimuonSrc_;
  edm::InputTag beamSpotSrc_;
  edm::InputTag primaryVertexSrc_;
  edm::InputTag ebClusterSrc_;
  edm::InputTag ebRecHitsSrc_;
  edm::InputTag eeRecHitsSrc_;
  edm::InputTag genParticleSrc_;
  bool isMC_;

};

#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

MuMuGammaTreeMaker::MuMuGammaTreeMaker(const edm::ParameterSet& iConfig):
  tree_(),
  photonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("photonSrc")),
  muonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("muonSrc")),
  dimuonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("dimuonSrc")),
  beamSpotSrc_(iConfig.getUntrackedParameter<edm::InputTag>("beamSpotSrc")),
  primaryVertexSrc_(iConfig.getUntrackedParameter<edm::InputTag>("primaryVertexSrc")),
  ebClusterSrc_(iConfig.getUntrackedParameter<edm::InputTag>("ebClusterSrc")),
  ebRecHitsSrc_(iConfig.getUntrackedParameter<edm::InputTag>("ebRecHitsSrc")),
  eeRecHitsSrc_(iConfig.getUntrackedParameter<edm::InputTag>("eeRecHitsSrc")),
  genParticleSrc_(iConfig.getUntrackedParameter<edm::InputTag>("genParticleSrc")),
  isMC_(iConfig.getUntrackedParameter<bool>("isMC"))
{
}

MuMuGammaTreeMaker::~MuMuGammaTreeMaker()
{
}

/// dxy parameter. (This is the transverse impact parameter w.r.t. to beamSpot, see DataFormats/TrackReco/interface/TrackBase.h
double MuMuGammaTreeMaker::dxy(const reco::VertexCompositeCandidate& cand,
                              const Point& beamSpot
                              ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  return (- vx * cand.py() + vy * cand.px() ) / cand.pt();
}


/// dsz parameter, see DataFormats/TrackReco/interface/TrackBase.h
double MuMuGammaTreeMaker::dsz(const reco::VertexCompositeCandidate& cand,
                              const Point& beamSpot
                              ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  double vz = cand.vz() - beamSpot.Z();
  return vz * cand.pt() / cand.p() - (vx * cand.px() + vy * cand.py() ) / cand.pt() * (cand.pz() / cand.p() );
}


/// dz parameter (= dsz/cos(lambda)). This is the track z0 w.r.t beamSpot,
double MuMuGammaTreeMaker::dz(const reco::VertexCompositeCandidate& cand,
                             const Point& beamSpot
                             ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  double vz = cand.vz() - beamSpot.Z();
  return vz - (vx * cand.px() + vy * cand.py() ) / cand.pt() * (cand.pz() / cand.pt() );
}

/// rho parameter = distance in the xy-plane
double MuMuGammaTreeMaker::rho(const reco::VertexCompositeCandidate& cand,
                              const Point& beamSpot
                              ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  return sqrt(vx*vx + vy*vy);
}


void
MuMuGammaTreeMaker::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
//   LogDebug("SegFault") << "Entering analyze ..." << std::endl;

  tree_.initLeafVariables();
  AddFourMomenta addP4;

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

  edm::Handle<edm::View<reco::CaloCluster> > ebClusters;
//   iEvent.getByLabel(ebClusterSrc_, ebClusters);

  edm::Handle<EcalRecHitCollection> eeRecHits;
  edm::Handle<EcalRecHitCollection> ebRecHits;
  edm::Handle<pat::TriggerEvent> triggerEvent;
  edm::ESHandle<EcalChannelStatus> channelStatus;

  edm::Handle<reco::GenParticleCollection> genParticles;

//   iEvent.getByLabel(ebRecHitsSrc_, ebRecHits);
//   iEvent.getByLabel(eeRecHitsSrc_, eeRecHits);
  iEvent.getByLabel("patTriggerEvent", triggerEvent);
//   iSetup.get<EcalChannelStatusRcd>().get(channelStatus);

//   EcalClusterLazyTools lazyTools(iEvent, iSetup, ebRecHitsSrc_, eeRecHitsSrc_);

  iEvent.getByLabel(genParticleSrc_, genParticles);


//   LogDebug("SegFault") << "Setting event variables ..." << std::endl;

  tree_.run   = iEvent.run();
  tree_.lumi  = iEvent.id().luminosityBlock();
  tree_.event = iEvent.id().event();

  // TODO: ADD THE HLT BITS
  if ( triggerEvent->path("L1_DoubleMuOpen") != 0 )
    tree_.L1DoubleMuOpen = triggerEvent->path("L1_DoubleMuOpen")->wasAccept();

  if ( triggerEvent->path("HLT_Mu3") != 0 )
    tree_.HLT_Mu3 = triggerEvent->path("HLT_Mu3")->wasAccept();

  if ( triggerEvent->path("HLT_Mu9") != 0 )
    tree_.HLT_Mu9 = triggerEvent->path("HLT_Mu9")->wasAccept();

  if ( triggerEvent->path("HLT_Mu11") != 0 )
    tree_.HLT_Mu11 = triggerEvent->path("HLT_Mu11")->wasAccept();

  LogDebug("SegFault") << "Setting HLT_Mu15_v1 ..." << std::endl;
  if ( triggerEvent->path("HLT_Mu15_v1") != 0x0 )
    tree_.HLT_Mu15_v1 = triggerEvent->path("HLT_Mu15_v1")->wasAccept();
  else
    tree_.HLT_Mu15_v1 = 0;

  LogDebug("SegFault") << "Setting nDimuons ..." << std::endl;

  tree_.nDimuons = dimuons->size();
  if (tree_.nDimuons > MuMuGammaTree::maxDimuons)
    tree_.nDimuons = MuMuGammaTree::maxDimuons;

  tree_.nMuons = muons->size();
  if (tree_.nMuons > MuMuGammaTree::maxMuons)
    tree_.nMuons = MuMuGammaTree::maxMuons;

  tree_.nVertices = primaryVertices->size();

//   LogDebug("SegFault") << "Looping over dimuons ..." << std::endl;

  // loop over dimuons
  reco::VertexCompositeCandidateView::const_iterator dimuon;
  int i;
  for(dimuon = dimuons->begin(), i=0;
      i < tree_.nDimuons; ++dimuon, ++i) {


    tree_.mass[i]              = dimuon->mass();
    tree_.pt[i]                = dimuon->pt();
    tree_.eta[i]               = dimuon->eta();
    tree_.phi[i]               = dimuon->phi();
    tree_.y[i]                 = dimuon->y();
    tree_.p[i]                 = dimuon->p();
    tree_.charge[i]            = dimuon->charge();

    tree_.vProb [i] = TMath::Prob(dimuon->vertexChi2(),
                                      dimuon->vertexNdof()
                                      );
    tree_.vrho  [i] = rho(*dimuon);
    tree_.vrhoBS[i] = rho(*dimuon, beamSpot->position() );
    tree_.vrhoPV[i] = rho(*dimuon, primaryVertices->at(0).position() );
    tree_.vx    [i] = dimuon->vx();
    tree_.vxBS  [i] = dimuon->vx() - (beamSpot->position().X());
    tree_.vxPV  [i] = dimuon->vx() - (primaryVertices->at(0).position().X());
    tree_.vy    [i] = dimuon->vy();
    tree_.vyBS  [i] = dimuon->vy() - (beamSpot->position().Y());
    tree_.vyPV  [i] = dimuon->vy() - (primaryVertices->at(0).position().Y());
    tree_.vz    [i] = dimuon->vz();
    tree_.vzBS  [i] = dimuon->vz() - (beamSpot->position().Z());
    tree_.vzPV  [i] = dimuon->vz() - (primaryVertices->at(0).position().Z());

    tree_.d0   [i] = - dxy(*dimuon);
    tree_.d0BS [i] = - dxy(*dimuon, beamSpot->position() );
    tree_.d0PV [i] = - dxy(*dimuon, primaryVertices->at(0).position() );
    tree_.dz   [i] = dz(*dimuon);
    tree_.dzBS [i] = dz(*dimuon, beamSpot->position() );
    tree_.dzPV [i] = dz(*dimuon, primaryVertices->at(0).position() );
    tree_.dsz  [i] = dsz(*dimuon);
    tree_.dszBS[i] = dsz(*dimuon, beamSpot->position() );
    tree_.dszPV[i] = dsz(*dimuon, primaryVertices->at(0).position() );
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
        tree_.pdgId[i] = pdgIdJPsi;
      else if ( dimuon->mass() > (1. - epsilon) * pdgMassPsi2S &&
                dimuon->mass() < (1. + epsilon) * pdgMassPsi2S )
        tree_.pdgId[i] = pdgIdPsi2S;
      else if ( dimuon->mass() > (1. - epsilon) * pdgMassY1S &&
                dimuon->mass() < (1. + epsilon) * pdgMassY1S )
        tree_.pdgId[i] = pdgIdY1S;
      else if ( dimuon->mass() > (1. - epsilon) * pdgMassY2S &&
                dimuon->mass() < 0.5 * (pdgMassY2S + pdgMassY3S) )
        tree_.pdgId[i] = pdgIdY2S;
      else if ( dimuon->mass() >= 0.5 * (pdgMassY2S + pdgMassY3S) &&
                dimuon->mass() < (1. + epsilon) * pdgMassY3S)
        tree_.pdgId[i] = pdgIdY3S;
      else if ( dimuon->mass() > (1. - epsilon) * pdgMassZ &&
                dimuon->mass() < (1. + epsilon) * pdgMassZ)
        tree_.pdgId[i] = pdgIdZ;
    } else {
      tree_.pdgId[i] = 0;
    }


    // Jump through 3 hoops to get pointers to the daughters.
    const reco::Candidate * dau1 = dimuon->daughter(0);
    const reco::Candidate * dau2 = dimuon->daughter(1);
    if (dau1 == 0 || dau2 == 0)
      throw edm::Exception(edm::errors::InvalidReference) <<
        "One of the dimuon daughters does not exist.\n";
    // Jump through the 2nd hoop - get the master of the shallow clones.
    if (dau1->hasMasterClone() && dau2->hasMasterClone() ) {
      dau1 = dau1->masterClone().get();
      dau2 = dau2->masterClone().get();
    } else {
      throw edm::Exception(edm::errors::InvalidReference) <<
        "One of the dimuon daughters is not a shallow clone.\n";
    }
    // Jump throught the 3rd hoop - cast up the pointers.
    const pat::Muon * mu1 = dynamic_cast<const pat::Muon*>(dau1);
    const pat::Muon * mu2 = dynamic_cast<const pat::Muon*>(dau2);
    if (mu1 == 0 || mu2 == 0)
      throw edm::Exception(edm::errors::InvalidReference) <<
        "One of the dimuon daughters is not a pat::Muon.\n";

    // The back-to-back cut
    double cosOpeningAngle = dau1->momentum().Dot(dau2->momentum()) /
                             ( dau1->p() * dau2->p() );
    tree_.backToBack[i] = 0.5 * (1. - cosOpeningAngle);

    // use pointer arithmetics to retreive the daughter indices
    const pat::Muon * muBegin = &*muons->begin();
    tree_.dau1[i] = mu1 - muBegin;
    tree_.dau2[i] = mu2 - muBegin;

    if ( isMC_ &&
         mu1->genParticle(0) &&
         mu2->genParticle(0) )
    {
      reco::CompositeCandidate mmGen;
      mmGen.addDaughter(*mu1, "muon1");
      mmGen.addDaughter(*mu2, "muon2");
      addP4.set(mmGen);
      tree_.massGen[i] = mmGen.mass();
    }
    else
    {
      tree_.massGen[i] = 0;
    }

    reco::CompositeCandidate mmVanilla;
    mmVanilla.addDaughter( * mu1 );
    mmVanilla.addDaughter( * mu2 );
    addP4.set(mmVanilla);
    tree_.massVanilla[i]       = mmVanilla.mass();
  } // loop over dimuons

//   LogDebug("SegFault") << "Looping over muons..." << std::endl;

  // loop over muons
  edm::View<pat::Muon>::const_iterator mu;
  for(mu = muons->begin(), i=0; i < tree_.nMuons; ++mu, ++i) {
    // set the daughter leafs
    tree_.muPt[i]                      = mu->pt();
    tree_.muEta[i]                     = mu->eta();
    tree_.muPhi[i]                     = mu->phi();
    tree_.muVtx[0][i]                  = mu->vx();
    tree_.muVtx[1][i]                  = mu->vy();
    tree_.muVtx[2][i]                  = mu->vz();
    // gen info
    if (isMC_ && mu->genParticle(0)) {
      // found gen match
      tree_.muGenPt    [i] = mu->genParticle(0)->pt();
      tree_.muGenEta   [i] = mu->genParticle(0)->eta();
      tree_.muGenPhi   [i] = mu->genParticle(0)->phi();
      tree_.muGenVtx[0][i] = mu->genParticle(0)->vx();
      tree_.muGenVtx[1][i] = mu->genParticle(0)->vy();
      tree_.muGenVtx[2][i] = mu->genParticle(0)->vz();
    }

    tree_.muP[i]                       = mu->p();
    tree_.muCharge[i]                  = mu->charge();
    if ( mu->globalTrack().isNonnull() && mu->isGlobalMuon() ) {
      tree_.muDxyBS[i]     = mu->globalTrack()->dxy( beamSpot->position() );
      tree_.muDxyPV[i]     = mu->globalTrack()->dxy( primaryVertices->at(0).position() );
      tree_.muPixelHits[i] = mu->globalTrack()->hitPattern().numberOfValidPixelHits();
      tree_.muStripHits[i] = mu->globalTrack()->hitPattern().numberOfValidStripHits();
      tree_.muMuonHits[i]  = mu->globalTrack()->hitPattern().numberOfValidMuonHits();
    }
    tree_.muSiNormalizedChi2[i]        = mu->innerTrack()->normalizedChi2();
    tree_.muSiD0[i]                    = mu->innerTrack()->d0();
    tree_.muSiD0BS[i]                  = - mu->innerTrack()->dxy( beamSpot->position() );
    tree_.muSiD0PV[i]                  = - mu->innerTrack()->dxy( primaryVertices->at(0).position() );
    tree_.muSiDz[i]                    = mu->innerTrack()->dz();
    tree_.muSiDzBS[i]                  = mu->innerTrack()->dz( beamSpot->position() );
    tree_.muSiDzPV[i]                  = mu->innerTrack()->dz( primaryVertices->at(0).position() );
    tree_.muSiDsz[i]                   = mu->innerTrack()->dsz();
    tree_.muSiDszBS[i]                 = mu->innerTrack()->dsz( beamSpot->position() );
    tree_.muSiDszPV[i]                 = mu->innerTrack()->dsz( primaryVertices->at(0).position() );
    tree_.muSiHits[i]                  = mu->innerTrack()->found();
    // count stations
    unsigned nStations = 0, stationMask = mu->stationMask();
    for (; stationMask; nStations++)
      stationMask &= stationMask - 1; // clear the least significant bit set
    tree_.muStations[i]                = nStations;
    tree_.muVz[i]                      = mu->vz();
    tree_.muIsGlobalMuon[i]            = mu->isGlobalMuon();
    tree_.muIsTrackerMuon[i]           = mu->isTrackerMuon();
    tree_.muIsTMLastStationAngTight[i] = mu->muonID("TMLastStationAngTight");
    tree_.muIsTrackerMuonArbitrated[i] = mu->muonID("TrackerMuonArbitrated");
    tree_.muTrackIso[i]                = mu->trackIso();
    tree_.muEcalIso[i]                 = mu->ecalIso();
    tree_.muHcalIso[i]                 = mu->hcalIso();
    tree_.muHltMu9Match[i] = mu->triggerObjectMatchesByPath("HLT_Mu9").size() ? 1 : 0;
    tree_.muHltMu11Match[i] = mu->triggerObjectMatchesByPath("HLT_Mu11").size() ? 1 : 0;
    tree_.muHltMu15v1Match[i] = mu->triggerObjectMatchesByPath("HLT_Mu15_v1").size() ? 1 : 0;
  } // loop over muons

//   LogDebug("SegFault") << "Applying selections ..." << std::endl;

  tree_.applyJPsiSelection();
  tree_.applyYSelection();
  tree_.applyZSelection();
  tree_.applyVbtfBaselineSelection();
  tree_.applyBaselineSelection();

  tree_.setOrderByMuQAndPt();
  tree_.setOrderByVProb();

  tree_.setCorrectedMassJPsi();
  tree_.setCorrectedMassY();

  // choose a primary dimuon
  int primaryDimuon = -1;
  for (i=0; i < tree_.nDimuons && primaryDimuon < -1; ++i)
    if (tree_.isZCand[i] && 60. < tree_.mass[i])
      primaryDimuon = i;
  for (i=0; i < tree_.nDimuons && primaryDimuon < -1; ++i)
    if (tree_.isYCand[i] && 8. < tree_.mass[i] && tree_.mass[i] < 12.)
      primaryDimuon = i;
  for (i=0; i < tree_.nDimuons && primaryDimuon < -1; ++i)
    if (tree_.isJPsiCand[i] && 2.6 < tree_.mass[i] && tree_.mass[i] < 3.5)
      primaryDimuon = i;
  for (i=0; i < tree_.nDimuons && primaryDimuon < -1; ++i)
    if (tree_.orderByVProb[i] == 0)
      primaryDimuon = i;
  if (primaryDimuon < 0) // this should never happen
    primaryDimuon = 0;

  // set the photon vertex to the vertex of the primary dimuon
  Point phoVertex = (*dimuons)[primaryDimuon].vertex();

//   LogDebug("SegFault") << "Looping over photons..." << std::endl;

  // loop over photons
  int nPhotons = photons->size();
  if ( nPhotons <= MuMuGammaTree::maxPhotons)
    tree_.nPhotons = nPhotons;
  else
    tree_.nPhotons = MuMuGammaTree::maxPhotons;

  tree_.nMuMuGammas = tree_.nPhotons; // use primary dimuons only

  // loop over photons
  edm::View<pat::Photon>::const_iterator pho;
  for (pho = photons->begin(), i=0; i < tree_.nPhotons; ++i, ++pho) {
    tree_.phoPt[i] = pho->pt();
    tree_.phoEta[i] = pho->eta();
    tree_.phoScEta[i] = pho->superCluster()->eta();
    tree_.phoPhi[i] = pho->phi();
    tree_.phoCaloPosition[0][i] = pho->caloPosition().x();
    tree_.phoCaloPosition[1][i] = pho->caloPosition().y();
    tree_.phoCaloPosition[2][i] = pho->caloPosition().z();
    tree_.phoVtx[0][i] = pho->vx();
    tree_.phoVtx[1][i] = pho->vy();
    tree_.phoVtx[2][i] = pho->vz();
    tree_.phoEcalIso[i] = pho->ecalIso();
    tree_.phoHcalIso[i] = pho->hcalIso();
    tree_.phoTrackIso[i] = pho->trackIso();
    tree_.phoHadronicOverEm[i] = pho->hadronicOverEm();
    tree_.phoSigmaIetaIeta[i] = pho->sigmaIetaIeta();
    tree_.phoHasPixelSeed[i] = pho->hasPixelSeed();
    tree_.phoMaxEnergyXtal[i] = pho->maxEnergyXtal();
    tree_.phoE3x3[i] = pho->e3x3();

    tree_.phoGenMatchPdgId[i]  = 0;
    tree_.phoGenMatchStatus[i] = 0;
    tree_.phoGenMatchMomPdgId[i]  = 0;
    tree_.phoGenMatchMomStatus[i] = 0;

    if (isMC_ && pho->genParticle(0)) {
      // found gen match
      tree_.phoGenMatchPdgId[i]  = pho->genParticle(0)->pdgId();
      tree_.phoGenMatchStatus[i] = pho->genParticle(0)->status();

      tree_.phoGenPt [i]    = pho->genParticle(0)->pt ();
      tree_.phoGenEta[i]    = pho->genParticle(0)->eta();
      tree_.phoGenPhi[i]    = pho->genParticle(0)->phi();
      tree_.phoGenVtx[0][i] = pho->genParticle(0)->vx();
      tree_.phoGenVtx[1][i] = pho->genParticle(0)->vy();
      tree_.phoGenVtx[2][i] = pho->genParticle(0)->vz();

      // look for the gen match in the (pruned) gen particle collection
      reco::GenParticleCollection::const_iterator genMatch;
      for (genMatch = genParticles->begin(); genMatch != genParticles->end(); ++genMatch) {
        if (genMatch->pdgId()  == pho->genParticle(0)->pdgId() &&
            genMatch->status() == pho->genParticle(0)->status() &&
            genMatch->p4()     == pho->genParticle(0)->p4()
            )
        {
          // found the gen match in gen particles.
          if (genMatch->numberOfMothers() > 0) {
              tree_.phoGenMatchMomPdgId[i]  = genMatch->mother(0)->pdgId();
              tree_.phoGenMatchMomStatus[i] = genMatch->mother(0)->status();
          }
          break;
        } // if found the gen match in gen particles.
      } // for loop over genParticles
    } // if found gen match

    tree_.phoR9    [i] = pho->r9();
    tree_.phoESC   [i] = pho->superCluster()->energy();
    tree_.phoESCRaw[i] = pho->superCluster()->rawEnergy();
    tree_.phoE5x5  [i] = pho->e5x5();

/*    DetId seedId = pho->superCluster()->seed()->seed();
    if (pho->isEB() && EBDetId::validHashIndex(EBDetId(seedId).hashedIndex()))
    {
        // We are in the EB and have a valid det id
      tree_.phoIEta  [i] = EBDetId(seedId).ieta();
      tree_.phoIPhi  [i] = EBDetId(seedId).iphi();
    }*/

    /*
    const reco::CaloCluster &phoSeed = *( pho->superCluster()->seed() );
    DetId seedId = lazyTools.getMaximum(phoSeed).first;
    const EcalRecHitCollection & recHits = ( pho->isEB() ?
      *ebRecHits :
      *eeRecHits
      );
    EcalRecHitCollection::const_iterator rh = recHits.find(seedId);
    if (rh != recHits.end()) {
      tree_.phoSeedRecoFlag[i]      = rh->recoFlag();
      tree_.phoSeedSeverityLevel[i] = EcalSeverityLevelAlgo::severityLevel(
                                        seedId, recHits, *channelStatus
                                        );
      tree_.phoSeedSwissCross[i]    = EcalSeverityLevelAlgo::swissCross(seedId, recHits);
      tree_.phoSeedE1OverE9[i]      = EcalSeverityLevelAlgo::E1OverE9(seedId, recHits);
    } else {
      edm::LogWarning("SpikeCleaningVariables") << "Didn't find seed rechit!"
                                                << std::endl;
      tree_.phoSeedRecoFlag[i]      = -999;
      tree_.phoSeedSeverityLevel[i] = -999;
      tree_.phoSeedSwissCross[i]    = -999;
      tree_.phoSeedE1OverE9[i]      = -999;
    }
    */
    tree_.phoSeedRecoFlag[i]      = pho->userInt("photonUserData:seedRecoFlag");
    tree_.phoSeedSeverityLevel[i] = pho->userInt("photonUserData:seedSeverityLevel");
    tree_.phoSeedSwissCross[i]    = pho->userFloat("photonUserData:seedSwissCross");
    tree_.phoSeedE1OverE9[i]      = pho->userFloat("photonUserData:seedE1OverE9");

    reco::CompositeCandidate dimuon = (*dimuons)[primaryDimuon];
    reco::CompositeCandidate mmg;
    mmg.addDaughter(dimuon, "dimuon");
    mmg.addDaughter(*pho, "photon");
    addP4.set(mmg);
    tree_.mmgMass[i] = mmg.mass();


    // Jump through 3 hoops to get pointers to the daughters.
    const reco::Candidate * dau1 = dimuon.daughter(0);
    const reco::Candidate * dau2 = dimuon.daughter(1);
    if (dau1 == 0 || dau2 == 0)
      throw edm::Exception(edm::errors::InvalidReference) <<
        "One of the mmg dimuon daughters does not exist.\n";
    // Jump through the 2nd hoop - get the master of the shallow clones.
    if (dau1->hasMasterClone() && dau2->hasMasterClone() ) {
      dau1 = dau1->masterClone().get();
      dau2 = dau2->masterClone().get();
    } else {
      throw edm::Exception(edm::errors::InvalidReference) <<
        "One of the mmg dimuon daughters is not a shallow clone.\n";
    }
    // Jump throught the 3rd hoop - cast up the pointers.
    const pat::Muon * mu1 = dynamic_cast<const pat::Muon*>(dau1);
    const pat::Muon * mu2 = dynamic_cast<const pat::Muon*>(dau2);
    if (mu1 == 0 || mu2 == 0)
      throw edm::Exception(edm::errors::InvalidReference) <<
        "One of the mmg dimuon daughters is not a pat::Muon.\n";

    if ( isMC_ &&
         mu1->genParticle(0) &&
         mu2->genParticle(0) &&
         pho->genParticle(0) )
    {
      reco::CompositeCandidate mmgGen;
      mmgGen.addDaughter(*mu1->genParticle(0), "muon1");
      mmgGen.addDaughter(*mu2->genParticle(0), "muon2");
      mmgGen.addDaughter(*pho->genParticle(0), "photon");
      addP4.set(mmgGen);
      tree_.mmgMassGen[i] = mmgGen.mass();
    }
    else
    {
      tree_.mmgMassGen[i] = 0;
    }

    reco::CompositeCandidate mmgVanilla;
    mmgVanilla.addDaughter( *dimuon.daughter(0), "muon1" );
    mmgVanilla.addDaughter( *dimuon.daughter(1), "muon2" );
    mmgVanilla.addDaughter( *pho               , "photon");
    addP4.set(mmgVanilla);
    tree_.mmgMassVanilla[i] = mmgVanilla.mass();

    pat::Photon *phoVCorr = pho->clone();
    Point dimuonVtx( dimuon.vx(), dimuon.vy(), dimuon.vz() );
    phoVCorr->setVertex(dimuonVtx);
    reco::CompositeCandidate mmgVCorr;
    mmgVCorr.addDaughter( dimuon, "dimuon");
    mmgVCorr.addDaughter(*phoVCorr, "photon");
    addP4.set(mmgVCorr);
    tree_.mmgMassVCorr[i] = mmgVCorr.mass();

    tree_.mmgDimuon[i] = primaryDimuon;
    tree_.mmgPhoton[i] = i;

    DeltaR<pat::Photon, reco::Candidate> deltaR;
    double dr1 = deltaR( *pho, *dimuon.daughter(0) );
    double dr2 = deltaR( *pho, *dimuon.daughter(1) );
    if (dr1 < dr2) {
      tree_.mmgDeltaRNear[i] = dr1;
      tree_.mmgMuonNear[i] = tree_.dau1[primaryDimuon];
      tree_.mmgMuonFar[i]  = tree_.dau2[primaryDimuon];
    } else {
      tree_.mmgDeltaRNear[i] = dr2;
      tree_.mmgMuonNear[i] = tree_.dau2[primaryDimuon];
      tree_.mmgMuonFar[i]  = tree_.dau1[primaryDimuon];
    } // if (dr1 < dr2)

  } // loop over photons


  // loop over ebclusters
/*  edm::View<reco::CaloCluster>::const_iterator cluster;
  for(cluster = ebClusters->begin(), i=0; i < tree_.nPhotons; ++cluster, ++i) {

    Vector phoDirection = cluster->position() - phoVertex;
    Vector phoP = cluster->energy() * phoDirection.unit();
    LorentzVector phoP4( phoP.x(), phoP.y(), phoP.z(), cluster->energy() );
    reco::LeafCandidate pho(0, phoP4, phoVertex);

    tree_.phoPt[i] = pho.pt();
  }*/

//   LogDebug("SegFault") << "Filling the tree..." << std::endl;

  // only store interesting events
  tree_.Fill();

  LogDebug("SegFault") << "Exiting analyze..." << std::endl;

}

void
MuMuGammaTreeMaker::beginJob()
{
  // register to the TFileService
  edm::Service<TFileService> fs;

  // book the tree:
  std::cout << "MuMuGammaTreeMaker: booking tree" << std::endl;
  TTree * tree = fs->make<TTree>("mmg", "MuMuGamma tree");
  tree_.init(tree);
  tree_.initGamma(tree);
}

void
MuMuGammaTreeMaker::endJob()
{
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MuMuGammaTreeMaker);
