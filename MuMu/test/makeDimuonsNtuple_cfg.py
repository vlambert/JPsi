import FWCore.ParameterSet.Config as cms

process = cms.Process("DimuonNtuple")

import FWCore.ParameterSet.VarParsing as VarParsing

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

# register more options
options.register("castorPath",
  "/castor/cern.ch/user/v/veverka/data/DimuonPhotonSkim_v2", # default value
  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
  VarParsing.VarParsing.varType.string,          # string, int, or float
  "Castor path with a subdirectory for each dataset with root files."
)

options.register("dataset",
  "MinimumBias_Commissioning10-SD_Mu-Jun14thSkim_v1_132440-137028", # default value
  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
  VarParsing.VarParsing.varType.string,          # string, int, or float
  "Name of a directory under castorPath containing data"
)

options.register("datasetNumber",
  -1, # default value
  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
  VarParsing.VarParsing.varType.int,          # string, int, or float
  "Number of dataset to process. Overrides dataset unless equal -1."
)

# setup any defaults you want
options.outputFile = 'dimuonsNtuple.root'
pathPrefix = "rfio:" + options.castorPath + "/" + options.dataset + "/"
fileList = """
DimuonPhotonSkim_v2_100_1_8dM.root     DimuonPhotonSkim_v2_110_1_82b.root
DimuonPhotonSkim_v2_101_1_mf2.root     DimuonPhotonSkim_v2_111_1_HfJ.root
DimuonPhotonSkim_v2_102_1_mbO.root     DimuonPhotonSkim_v2_112_1_ffj.root
DimuonPhotonSkim_v2_103_1_acY.root     DimuonPhotonSkim_v2_113_1_QwL.root
DimuonPhotonSkim_v2_104_1_4ff.root     DimuonPhotonSkim_v2_114_1_24v.root
""".split()
options.inputFiles = tuple([pathPrefix + f for f in fileList])
options.maxEvents = 100 # -1 means all events

## get and parse the command line arguments
options.parseArguments()

## get the file list from CASTOR
if options.datasetNumber > 0:
  import os
  datasets = os.popen("nsls " + options.castorPath).read().split()
  datasetNumber = options.datasetNumber
  if datasetNumber > len(datasets):
    print "Illegal datasetNumber =", datasetNumber
  exit
  dataset = options.dataset = datasets[datasetNumber - 1]
  datasetDir = options.castorPath + "/" + dataset
  pathPrefix = "rfio:" + datasetDir + "/"
  fileNames = os.popen("nsls " + datasetDir).read().split()
  print "Processing %d files of %s (%d/%d)" % (len(fileNames),
    dataset, datasetNumber, len(datasets))
  del options.inputFiles[:]
  options.inputFiles = [pathPrefix + f for f in fileNames]
  
if options.maxEvents < 0:
  options.outputFile = options.outputFile.split(".")[0] + "_" + options.dataset

## Message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 100

## Geometry, Detector Conditions and Pythia Decay Tables (needed for the vertexing)
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "GR_R_36X_V12A::All"
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(options.maxEvents)
)


process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(options.inputFiles)
)

process.TFileService = cms.Service("TFileService",
  fileName = cms.string(options.outputFile)
)

process.load("JPsi.MuMu.goodMuons_cfi")
process.load("JPsi.MuMu.glbMuons_cfi")
process.load("JPsi.MuMu.trkMuons_cfi")
process.load("JPsi.MuMu.dimuons_cfi")
process.load("JPsi.MuMu.dimuonsCountFilters_cfi")

process.goodDimuons.cut = "mass > 0"

process.goodDimuonsCountFilter = process.dimuonsCountFilter.clone(src = "goodDimuons")

process.dimuonsNtuple = cms.EDAnalyzer("DimuonsNtupelizer",
  photonSrc   = cms.untracked.InputTag("selectedPatPhotons"),
  muonSrc     = cms.untracked.InputTag("goodMuons"),
  dimuonSrc   = cms.untracked.InputTag("vertexedDimuons"),
  beamSpotSrc = cms.untracked.InputTag("offlineBeamSpot"),
  primaryVertexSrc = cms.untracked.InputTag("offlinePrimaryVertices"),
)


process.p = cms.Path(
  process.goodMuons *
  process.goodDimuons *
  process.goodDimuonsCountFilter *
  process.vertexedDimuons *
  process.dimuonsNtuple
)

if __name__ == "__main__": import user
