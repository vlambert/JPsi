import FWCore.ParameterSet.Config as cms

dimuons = cms.EDProducer("CandViewShallowCloneCombiner",
    cut = cms.string('0 < mass'),
    checkCharge = cms.bool(False),
    decay = cms.string('selectedPatMuons selectedPatMuons')
)

goodDimuons = cms.EDProducer("CandViewShallowCloneCombiner",
    cut = cms.string('0 < mass'),
    checkCharge = cms.bool(False),
    decay = cms.string('goodMuons goodMuons')
)

dimuonsOS = goodDimuons.clone(
    checkCharge = True,
    decay = 'goodMuons@+ goodMuons@-'
)

dimuonsSS = dimuonsOS.clone(decay = 'goodMuons@+ goodMuons@+')

dimuonsGGOS = dimuonsOS.clone(decay = 'glbMuons@+ glbMuons@-' )
dimuonsGGSS = dimuonsOS.clone(decay = 'glbMuons@+ glbMuons@+' )

dimuonsGTOS = dimuonsOS.clone(decay = 'glbMuons@+ trkMuons@-' )
dimuonsGTSS = dimuonsOS.clone(decay = 'glbMuons@+ trkMuons@+' )

dimuonsTTOS = dimuonsOS.clone(decay = 'trkMuons@+ trkMuons@-' )
dimuonsTTSS = dimuonsOS.clone(decay = 'trkMuons@+ trkMuons@+' )

vertexedDimuons = cms.EDProducer("KalmanVertexFitCompositeCandProducer",
  src = cms.InputTag("dimuons"),
)

# jpsis = cms.EDProducer("KinematicVertexFitCompositeCandProducer",
#   src = cms.InputTag("goodDimuons"),
#   setPdgId = cms.int32(443)
# )
#
# psis2S = cms.EDProducer("KinematicVertexFitCompositeCandProducer",
#   src = cms.InputTag("goodDimuons"),
#   setPdgId = cms.int32(553)
# )
#
#
#
#
