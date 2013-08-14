import FWCore.ParameterSet.Config as cms

process = cms.Process("DimuonsNtuple")

pathPrefix = "rfio:/castor/cern.ch/user/v/veverka/data/DimuonPhotonSkim_v2/Mu_Run2010A-PromptReco-v4_140400-140401_NoJson/"
process.FWLiteParams = cms.PSet(
  input   = cms.string(pathPrefix + "DimuonPhotonSkim_v2_1_1_eyA.root"),
  muonSrc = cms.InputTag('selectedPatMuons')
)

