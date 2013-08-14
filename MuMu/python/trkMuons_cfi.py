import FWCore.ParameterSet.Config as cms

trkMuons = cms.EDFilter("PATMuonSelector",
  src = cms.InputTag("goodMuons"),
  cut = cms.string(" ".join("""
    !isGlobalMuon &
    isTrackerMuon &
    innerTrack.ndof > 0 &
    innerTrack.chi2 / innerTrack.ndof < 5.0 &
    muonID("TMLastStationAngTight")
                            """.split())
  )
)
