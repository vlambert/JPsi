import FWCore.ParameterSet.Config as cms

glbMuons = cms.EDFilter("PATMuonSelector",
  src = cms.InputTag("goodMuons"),
  cut = cms.string(" ".join("""
    isGlobalMuon &
    globalTrack.ndof > 0 &
    globalTrack.chi2 / globalTrack.ndof < 20.0
                            """.split())
  )
)

