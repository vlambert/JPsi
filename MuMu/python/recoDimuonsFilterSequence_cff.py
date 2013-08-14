import FWCore.ParameterSet.Config as cms

goodRecoMuons = cms.EDFilter("MuonSelector",
  src = cms.InputTag("muons"),
  cut = cms.string("""
    pt > 10 &
    abs(eta) < 2.4 &
    (
      (
        isGlobalMuon &
        globalTrack.ndof > 0
      ) ||
      (
        !isGlobalMuon &
        isTrackerMuon &
        numberOfMatches('SegmentAndTrackArbitration')>0
      )
    )
    """
  )
)

recoDimuons = cms.EDProducer("CandViewShallowCloneCombiner",
    cut = cms.string('15 < mass'),
    checkCharge = cms.bool(False),
    decay = cms.string('goodRecoMuons goodRecoMuons')
)

recoDimuonsFilter = cms.EDFilter("CandViewRefSelector",
    src = cms.InputTag("recoDimuons"),
    cut = cms.string("daughter(0).pt > 15 | daughter(1).pt > 15"),
    filter = cms.bool(True)
)


recoDimuonsFilterSequence = cms.Sequence(
  goodRecoMuons *
  recoDimuons *
  recoDimuonsFilter
  )