import FWCore.ParameterSet.Config as cms

process = cms.Process("NTUPLEDUMP")

## Message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 100

##################################################################
## CUSTOMIZE THIS
## These are defualts that are overridden by command line options.
jobNumber = 3 # 1 .. N
filesPerJob = 20
##################################################################

## Geometry, Detector Conditions and Pythia Decay Tables (needed for the vertexing)
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "GR_R_36X_V12A::All"
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")


process.maxEvents = cms.untracked.PSet(output = cms.untracked.int32(100) )
# process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring("file:/tmp/veverka/DimuonPhotonSkim.root")
)

##################################################################
## CUSTOMIZE THIS
# import JPsi.MuMu.castorFiles_MinimumBias_Commissioning10_CS_Onia_Jun14thSkim_v1_DimuonPhotonSkim_cff as inputFiles
# import JPsi.MuMu.castorFiles_Mu_Run2010A_CS_Onia_Jun14thSkim_v1_135803_137436_WithJson_cff as inputFiles
# import JPsi.MuMu.castorFiles_Mu_Run2010A_PromptReco_v4_137437_139375_WithJson_cff as inputFiles
#import JPsi.MuMu.castorFiles_Mu_Run2010A_PromptReco_v4_139376_139529_NoJson_cff as inputFiles
# import JPsi.MuMu.castorFiles_Mu_Run2010A_PromptReco_v4_139376_139790_WithJson_DimuonPhotonSkim_cff as inputFiles
import JPsi.MuMu.castorFiles_Mu_Run2010A_PromptReco_v4_139791_140156_NoJson_DimuonPhotonSkim_cff as inputFiles
##################################################################

fmin = filesPerJob*(jobNumber-1)
fmax = min(fmin + filesPerJob - 1, len(inputFiles.fileList) )
print ">>>>>> %s" % inputFiles.pathPrefix.split("/")[-2]
print ">>>>>> This is job %d of %d" % (jobNumber, len(inputFiles.fileList)/filesPerJob+1)
process.source.fileNames = [inputFiles.pathPrefix + file for file
                            in inputFiles.fileList[fmin:fmax]
                            ]

process.load("JPsi.MuMu.goodMuons_cfi")
process.load("JPsi.MuMu.glbMuons_cfi")
process.load("JPsi.MuMu.trkMuons_cfi")
process.load("JPsi.MuMu.dimuons_cfi")
process.load("JPsi.MuMu.dimuonsCountFilters_cfi")
process.load("JPsi.MuMu.edmNtuples_cfi")
process.load("JPsi.MuMu.dimuonsFilter_cfi")

process.dimuonsFilter.src = "goodDimuons"

process.p = cms.Path(
  process.goodMuons *
  process.goodDimuons *
  process.dimuonsFilter *
  (process.vertexedDimuons + process.jpsis + process.psis2S) *
  (process.dimuonNtp + process.jpsiNtp + process.psi2SNtp)
)


process.out = cms.OutputModule("PoolOutputModule",
  outputCommands = cms.untracked.vstring('drop *',
    "keep *_*Ntp_*_*",
  ),
  SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring(
      'p',
    )
  ),
  fileName = cms.untracked.string("file:/tmp/veverka/ntuple_%s_%d.root" %
    (inputFiles.pathPrefix.split("/")[-2].replace("-", "_"), jobNumber)
  )
#   fileName = cms.untracked.string("minimumBiasNtuples.root")
)

process.out.fileName = "test.root"

process.outPath= cms.EndPath(process.out)

if __name__ == "__main__": import user