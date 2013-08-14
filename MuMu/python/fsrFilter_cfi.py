import FWCore.ParameterSet.Config as cms

leadingPhoton = cms.EDFilter("LargestPtPatPhotonSelector",
  src = cms.InputTag("cleanPatPhotons"),
  maxNumber = cms.uint32(1)
)

fsrFilter = cms.EDFilter("PATPhotonSelector",
  src = cms.untracked.InputTag("leadingPhoton"),
  cut = cms.untracked.string("""
    genParticlesSize > 0 &
    genParticle.pdgId = 22 &
    abs(genParticle.mother.pdgId) = 13
    """),
  filter = cms.untracked.bool(True),
  )