# minimalistic config file to copy / merge cmssw datasets
# veverka@caltech.edu, 2008-12-16

import FWCore.ParameterSet.Config as cms

process = cms.Process('MERGE')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(
   )
)
form JPsi.MuMu.Mu_Run2010A_PromptReco_v4_DimuonPhotonSkim_v1_json137437_139375_cff import \
  as promptReco_v4
pathPrefix = "rfio://" + promptReco_v4.crabOutputPath
i = 7
process.source.fileNames = [pathPrefix + file for file in prompReco_v4.crabOutputFileList[(i-1)*10:i*10] ]

process.output = cms.OutputModule("PoolOutputModule",
   fileName = cms.untracked.string("file:test_%d.root" % i)
)

process.endpath = cms.EndPath(process.output)

