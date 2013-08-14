import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from PhysicsTools.PatAlgos.patTemplate_cfg import *


##########################################################
# COMMAND LINE OPTIONS
##########################################################

options = VarParsing.VarParsing("analysis")
options.register("globalTag",
                 "START36_V10::All", # default value
                 VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                 VarParsing.VarParsing.varType.string,         # string, int, or float
                 "Global tag to be used."
                 )

# get and parse the command line arguments
#options.parseArguments()

prunedGenParticles = cms.EDProducer("GenParticlePruner",
  src = cms.InputTag("genParticles"),
  select = cms.vstring(
    "++keep+ numberOfMothers > 0 & mother(0).status = 3", # hard scattering
    "++keep+ numberOfMothers > 0 & mother(0).numberOfMothers > 0 & mother(0).mother(0).status = 3", # hard scattering
    "++keep status = 1 & pdgId = 22 & abs(eta) < 3.1 & pt > 0.7",
    "++keep status = 1 & abs(pdgId) = 13 & abs(eta) < 2.5 & pt > 9",
  )
)


process.load("JPsi.MuMu.recoDimuonsFilterSequence_cff")

######################################################################
### Rechit-level spike cleaning
######################################################################
process.load("EGamma.EGammaSkims.cleanReRecoSequence_cff")
process.ecalCleanClustering = cms.Sequence(
  process.cleanedEcalClusters*
  process.cleanedEgammaSkimReco
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
#removeMCMatching(process)
removeCleaning(process)

# load the coreTools of PAT
#from PhysicsTools.PatAlgos.tools.pfTools import *
#addPFCandidates(process, allHadronicPfCandidates)

process.load("JPsi.MuMu.dimuons_cfi")
process.load("JPsi.MuMu.dimuonsFilter_cfi")
process.dimuonsSequence = cms.Sequence(
  process.dimuons *
  process.vertexedDimuons *
  process.dimuonsFilter
)

process.p = cms.Path(
  process.recoDimuonsFilterSequence * ## test
  process.ecalCleanClustering       *
  process.islandBasicClusters       *
  process.patDefaultSequence        *
  process.dimuonsSequence
)

from PhysicsTools.PatAlgos.tools.trigTools import *
from ElectroWeakAnalysis.MultiBosons.tools.skimmingTools import embedTriggerMatches
process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
switchOnTrigger(process)
process.patTrigger.processName = "REDIGI36X"
process.patTriggerEvent.processName = "REDIGI36X"
matchHltPaths = {
  "selectedPatMuons": """
    HLT_L1Mu14_L1ETM30
    HLT_L1Mu14_L1SingleJet6U
    HLT_L1Mu14_L1SingleEG10
    HLT_L1Mu20
    HLT_DoubleMu3
    HLT_Mu3
    HLT_Mu5
    HLT_Mu9
    HLT_L2Mu9
    HLT_L2Mu11
    HLT_L1Mu30
    HLT_Mu7
    HLT_L2Mu15
    """.split()
  }
embedTriggerMatches(process, matchHltPaths)

process.GlobalTag.globaltag = options.globalTag

import os
#path = "/store/mc/Spring10/Zmumu/GEN-SIM-RECO/START3X_V26_S09-v1/0006/"
path = "/store/mc/Summer10/Zmumu_M20_CTEQ66-powheg/GEN-SIM-RECO/START36_V9_S09-v2/0032/"
files = os.popen("ls /pnfs/cms/WAX/11" + path).read().split()
prefix = "dcap://cmsdca.fnal.gov:22125/pnfs/fnal.gov/usr/cms/WAX/11"
fileNames = [prefix + path + f for f in files]
process.source.fileNames = cms.untracked.vstring(fileNames[:5])

#process.maxEvents.input = -1
process.maxEvents.input = 20
#process.maxEvents = cms.untracked.PSet(output = cms.untracked.int32(2))  # test

process.out.fileName = "ZGammaSkim_v1.root"

## Add extra photon / ECAL event content
#from ElectroWeakAnalysis.MultiBosons.Skimming.VgEventContent import vgExtraPhotonEventContent
process.out.outputCommands.extend([
  "drop *_selectedPatMuons_*_*", # duplicated by selectedPatMuonsTriggerMatch
  "keep *_genParticles_*_*",
  "keep *_prunedGenParticles_*_*",
  "keep *_offlinePrimaryVertices_*_*",
  "keep *_offlineBeamSpot_*_*",
  "keep *_ecalPreshowerRecHit_*_*",
  "keep *_ecalRecHit_*_*",
  "keep *_pfElectronTranslator_pf_PAT",  # electron super-/preshower-/calo-clusters
  "keep *_islandBasicClusters_*_PAT", # for soft photons
  "keep *_hybridSuperClusters_*_PAT", # contains the instance hybridBarrelBasicClusters
  "keep *_multi5x5BasicClusters_*_PAT",
  "keep *_correctedHybridSuperClusters_*_PAT",
  "keep *_multi5x5SuperClustersWithPreshower_*_PAT",
  "keep *_correctedMulti5x5SuperClustersWithPreshower_*_PAT",
  "keep *_photonCore_*_PAT",
  "keep *_electronCore_*_PAT",
  "keep *_conversions_*_PAT",
  "keep *_trackerOnlyConversions_*_PAT",
  "keep *_ckfInOutTracksFromConversions_*_PAT",
  "keep *_ckfOutInTracksFromConversions_*_PAT",
  "keep *_patTriggerEvent_*_*"
  ])

process.options.wantSummary = True # test
process.MessageLogger.cerr.FwkReport.reportEvery = 1000 # test

## test
process.selectedPatMuons.cut = """
  pt > 10 &
  abs(eta) < 2.4 &
  (
    (
      isGlobalMuon &
      globalTrack.ndof > 0
    ) ||
    (
      !isGlobalMuon &
      isTrackerMuon &
      numberOfMatches('SegmentAndTrackArbitration')>0
    )
  )
  """

## Embed tracker tracks
process.patMuons.embedTrack = True
process.patElectrons.embedTrack = True

## Loosened photon reco cuts
process.photonCore.minSCEt = 1.0
process.photons.minSCEtBarrel = 1.0
process.photons.minSCEtEndcap = 1.0
process.photons.maxHoverEBarrel = 10.0
process.photons.maxHoverEEndcap = 10.0

## Suppress many warnings about missing prescale tables
process.MessageLogger.categories += ["hltPrescaleTable"]
process.MessageLogger.cerr.hltPrescaleTable = cms.untracked.PSet(
  limit = cms.untracked.int32(5)
  )


## Debug
# process.Tracer = cms.Service("Tracer")

## Add tab completion + history during inspection
if __name__ == "__main__": import user
