import FWCore.ParameterSet.Config as cms

process = cms.Process("ANALYSIS")

## Message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    'file:testZMuMuGammaSubskim.root'
  )
)

# pathPrefix = "rfio:/castor/cern.ch/user/g/gpetrucc/7TeV/DATA/"
# pathPrefix = "file:/tmp/veverka/"
pathPrefix = "file:/uscms/home/veverka/work/jpsi/CMSSW_3_7_0_patch3/src/JPsi/MuMu/test/crab/crab_0_100701_095456/res/"

# fileNames = """
# DATA_skimJPsiLoose_fromApr20MuonSkim-v2.root
# DATA_skimJPsiLoose_fromMuonSkimV9_upToApr28-v2.root
# """.split()

fileNames = ["DimuonSkim_merge156.root"]
process.source.fileNames = [pathPrefix + fileName for fileName in fileNames]

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.TFileService = cms.Service("TFileService",
  fileName = cms.string("histos_%devts.root" % process.maxEvents.input.value() )
)

process.load("JPsi.MuMu.testJPsiSkim_cfi")

process.p = cms.Path(process.jpsiSequence)
