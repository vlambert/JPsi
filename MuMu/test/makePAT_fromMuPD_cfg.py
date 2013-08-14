import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.patTemplate_cfg import *

##########################################################
# VARIOUS FILTERS TO CLEAN UP COLLISION DATA
##########################################################

## Physics Declared bit selection
## https://twiki.cern.ch/twiki/bin/view/CMS/Collisions2010Recipes#Physics_Declared_bit_selection
process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'

## Removal of Beam Scraping Events
## https://twiki.cern.ch/twiki/bin/view/CMS/Collisions2010Recipes#Removal_of_Beam_Scraping_Events
process.noScraping = cms.EDFilter("FilterOutScraping",
  applyfilter = cms.untracked.bool(True),
  debugOn = cms.untracked.bool(True),
  numtrack = cms.untracked.uint32(10),
  thresh = cms.untracked.double(0.25)
)

## Good vertex selection
## https://twiki.cern.ch/twiki/bin/view/CMS/Collisions2010Recipes#Good_Vertex_selection
process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
  vertexCollection = cms.InputTag('offlinePrimaryVertices'),
  minimumNDOF = cms.uint32(4),
  maxAbsZ = cms.double(15),
  maxd0 = cms.double(2)
)

process.cleanedCollisionData = cms.Sequence(
  process.hltPhysicsDeclared  +
  process.noScraping          +
  process.primaryVertexFilter
)

##########################################################
# SNIPPETS FROM CS_Onia
##########################################################
process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*")

### Onia skim CS
process.goodMuons = cms.EDFilter("MuonRefSelector",
    src = cms.InputTag("muons"),
    cut = cms.string("isGlobalMuon || (isTrackerMuon && numberOfMatches('SegmentAndTrackArbitration')>0)"),
)
process.diMuons = cms.EDProducer("CandViewShallowCloneCombiner",
    decay       = cms.string("goodMuons goodMuons"),
    checkCharge = cms.bool(False),
    cut         = cms.string("mass > 2"),
)
process.diMuonFilter = cms.EDFilter("CandViewCountFilter",
    src       = cms.InputTag("diMuons"),
    minNumber = cms.uint32(1),
)
process.Skim_diMuons = cms.Sequence(
  process.goodMuons    *
  process.diMuons      *
  process.diMuonFilter
)


##########################################################
# PAT
##########################################################

from PhysicsTools.PatAlgos.tools.coreTools import *
removeAllPATObjectsBut(process, ["Muons"])
removeMCMatching(process)

# process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
# from PhysicsTools.PatAlgos.tools.trigTools import *
# switchOnTrigger( process )
# switchOnTriggerMatchEmbedding( process )

process.load("JPsi.MuMu.dimuons_cfi")
process.load("JPsi.MuMu.dimuonsFilter_cfi")
process.dimuonsSequence = cms.Sequence(
  process.dimuons * process.dimuonsFilter
)

process.p = cms.Path(
  process.cleanedCollisionData *
  process.Skim_diMuons         *
  process.patDefaultSequence   *
  process.dimuonsSequence
)

process.GlobalTag.globaltag = "GR_R_36X_V12A::All" # taken from CS_Onia-June14th
# process.GlobalTag.globaltag = "GR_R_37X_V6A::All"

import JPsi.MuMu.CS_Onia_June9thSkim_v1_FilesAtFnal_cff as June9thSkim
process.source.fileNames = cms.untracked.vstring(June9thSkim.fileNames[:])

import JPsi.MuMu.PromptReco_v4_FilesAtFnal_cff as PromptReco_v4
process.source.fileNames = cms.untracked.vstring(PromptReco_v4.fileNames[50:])

process.maxEvents = cms.untracked.PSet(output = cms.untracked.uint32(10) )
process.out.fileName = "DimuonSkim_fromMuPD.root"
process.options.wantSummary = False
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.selectedPatMuons.cut = process.goodMuons.cut.value()

## Deal with JSON: require run > 137632
process.source.firstRun = cms.untracked.uint32(137633)