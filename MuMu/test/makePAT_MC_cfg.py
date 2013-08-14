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

######################################################################
### Add island basic clusters
######################################################################
process.load("RecoEcal.EgammaClusterProducers.islandBasicClusters_cfi")

######################################################################
### PAT
######################################################################
from PhysicsTools.PatAlgos.tools.coreTools import *
removeAllPATObjectsBut(process, ["Muons", "Photons"])
removeMCMatching(process)

# load the coreTools of PAT
#from PhysicsTools.PatAlgos.tools.pfTools import *
#addPFCandidates(process, allHadronicPfCandidates)

process.load("JPsi.MuMu.dimuons_cfi")
process.load("JPsi.MuMu.dimuonsFilter_cfi")
process.dimuonsSequence = cms.Sequence(
  process.dimuons * process.dimuonsFilter
)

process.p = cms.Path(
  process.cleanedCollisionData *
  process.islandBasicClusters  *
  process.patDefaultSequence   *
  process.dimuonsSequence
)

# process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
# from PhysicsTools.PatAlgos.tools.trigTools import *
# switchOnTrigger( process )
# switchOnTriggerMatchEmbedding( process )

process.GlobalTag.globaltag = "START3X_V26::All" # Spring10 MC

#import JPsi.MuMu.filesAtFnal_CS_Onia_June9thSkim_v1_cff as June9thSkim
# from JPsi.MuMu.filesAtFnal_Jun14thReReco_v1_cff import fileNames
from JPsi.MuMu.filesAtFnal_CS_Onia_Jun14thSkim_v1_cff import fileNames
process.source.fileNames = cms.untracked.vstring(fileNames[:50])

# process.maxEvents.input = 2000
# process.maxEvents = cms.untracked.PSet(output = cms.untracked.int32(10))
# process.out.fileName = "pat_test.root"
#process.out.fileName = "/uscms/home/veverka/nobackup/CS_Onia_June9thSkim_v1_PAT.root"
process.out.fileName = "DimuonPhotonSkim.root"

## Add extra photon / ECAL event content
from ElectroWeakAnalysis.MultiBosons.Skimming.VgEventContent import vgExtraPhotonEventContent
vgExtraPhotonEventContent += ["keep *_islandBasicClusters_*_*"]
process.out.outputCommands.extend(vgExtraPhotonEventContent)

process.options.wantSummary = False
process.MessageLogger.cerr.FwkReport.reportEvery = 100

## Same muon selection as in the CS Onia
process.selectedPatMuons.cut = "isGlobalMuon || (isTrackerMuon && numberOfMatches('SegmentAndTrackArbitration')>0)"

## Embed tracker tracks
process.patMuons.embedTrack = True

