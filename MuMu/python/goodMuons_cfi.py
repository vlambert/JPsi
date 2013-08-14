import FWCore.ParameterSet.Config as cms

goodMuons = cms.EDFilter("PATMuonSelector",
  src = cms.InputTag("selectedPatMuons"),
  cut = cms.string(" ".join("""
    abs(eta) < 2.4 &
    (
      isGlobalMuon &
      globalTrack.ndof > 0
    )
    ||
    (
      !isGlobalMuon &
      isTrackerMuon
    )
                            """.split())
  )
)

