import re
import os
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
from FWCore.Utilities.FileUtils import sectionNofTotal

process = cms.Process("NTPMAKER")

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

# register more options
options.register("datasetPath",
  "/mnt/hadoop/user/veverka/DimuonVGammaSkim_v3", # default value
  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
  VarParsing.VarParsing.varType.string,          # string, int, or float
  "Castor path with a subdirectory for each dataset with root files."
)

options.register("dataset",
  "", # default value
  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
  VarParsing.VarParsing.varType.string,          # string, int, or float
  "Name of a directory under datasetPath containing data"
)

#options.register("datasetNumber",
  #-1, # default value
  #VarParsing.VarParsing.multiplicity.singleton, # singleton or list
  #VarParsing.VarParsing.varType.int,          # string, int, or float
  #"Number of dataset to process. Overrides dataset unless equal -1."
#)

options.register("reportEvery",
  100, # default value
  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
  VarParsing.VarParsing.varType.int,          # string, int, or float
  "Frequency of ouput."
)

options.register("globalTag",
                 "GR_R_36X_V12A::All", # default value
                 VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                 VarParsing.VarParsing.varType.string,         # string, int, or float
                 "Global tag to be used."
                 )

options.register("isMC",
                 "no", # default value
                 VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                 VarParsing.VarParsing.varType.string,         # string, int, or float
                 "Is this MC."
                 )

#options.register("firstFile",
  #1, # default value
  #VarParsing.VarParsing.multiplicity.singleton, # singleton or list
  #VarParsing.VarParsing.varType.int,          # string, int, or float
  #"Number of the first input file from the list to be processed."
#)

#options.register("lastFile",
  #0, # default value
  #VarParsing.VarParsing.multiplicity.singleton, # singleton or list
  #VarParsing.VarParsing.varType.int,          # string, int, or float
  #"Number of the last input file from the list to be processed."
#)

options.register("splitZMC",
  0, # default value
  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
  VarParsing.VarParsing.varType.int,          # string, int, or float
  "Set to 1 to split the Zmumu MC sample into three outputs: ISR, FSR and fakes."
)

options.register("jsonFile",
  "", # default value
  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
  VarParsing.VarParsing.varType.string,          # string, int, or float
  "JSON file to be applied."
)

options.setupTags(tag = "of%d",
                  ifCond = "totalSections != 0",
                  tagArg = "totalSections")

options.setupTags(tag = "job%d",
                  ifCond = "section != 0",
                  tagArg = "section")

options.setupTags(tag = "%s",
                  ifCond = "maxEvents < 0",
                  tagArg = "dataset")

# setup any defaults you want
#options.datasetPath = "/raid1/veverka/datafiles"
options.outputFile = 'MuMuGammaTree.root'
#pathPrefix = "file:" + options.datasetPath + "/" + options.dataset + "/"
#fileList = """
#ZGammaSkim_v1_100_1_Ce8.root  ZGammaSkim_v1_147_1_NQd.root  ZGammaSkim_v1_193_1_4sr.root  ZGammaSkim_v1_239_1_Z1l.root  ZGammaSkim_v1_57_1_lsw.root
#ZGammaSkim_v1_101_1_M9q.root  ZGammaSkim_v1_148_1_7em.root  ZGammaSkim_v1_194_1_9hq.root  ZGammaSkim_v1_23_1_BY2.root   ZGammaSkim_v1_58_1_LRW.root
#ZGammaSkim_v1_102_1_c9j.root  ZGammaSkim_v1_149_1_UOy.root  ZGammaSkim_v1_195_1_N8c.root  ZGammaSkim_v1_240_1_VnV.root  ZGammaSkim_v1_59_1_RIs.root
#ZGammaSkim_v1_103_1_ZdB.root  ZGammaSkim_v1_14_1_E9g.root   ZGammaSkim_v1_196_1_AXZ.root  ZGammaSkim_v1_241_1_NYy.root  ZGammaSkim_v1_5_1_lWF.root
#ZGammaSkim_v1_104_1_23M.root  ZGammaSkim_v1_150_1_J1y.root  ZGammaSkim_v1_197_1_z4W.root  ZGammaSkim_v1_242_1_jeq.root  ZGammaSkim_v1_60_1_hNo.root
#""".split()
#options.inputFiles = tuple([pathPrefix + f for f in fileList])
options.maxEvents = 100 # -1 means all events

## get and parse the command line arguments
options.parseArguments()

import os
## get the file list from CASTOR
#if options.datasetNumber > 0:
  #datasets = os.popen("ls " + options.datasetPath).read().split()
  #datasetNumber = options.datasetNumber
  #if datasetNumber > len(datasets):
    #print "Illegal datasetNumber =", datasetNumber
  #exit
  #dataset = options.dataset = datasets[datasetNumber - 1]
  #datasetDir = options.datasetPath + "/" + dataset
  #pathPrefix = "file:" + datasetDir + "/"
  #fileNames = os.popen("ls " + datasetDir).read().split()
  #print "Processing dataset %s (%d/%d)" % (dataset, datasetNumber,
                                           #len(datasets)
                                           #)
  #del options.inputFiles[:]
  #options.inputFiles = [pathPrefix + f for f in fileNames]
if options.dataset != "":
    #dataset = options.dataset
    print "Processing dataset %s" % (options.dataset,)
    datasetDir = os.path.join(options.datasetPath, options.dataset)
    rootRE = re.compile(".+\.root")
    options.clearList("inputFiles")
    for root, dirs, files in os.walk(datasetDir):
        fileNames = []
        for f in files:
            if rootRE.match(f):
                fileNames.append(os.path.join(root, f))
        if fileNames:
            print "  Added %d files from %s ..." % (len(fileNames), root)
        ## sort by job number
        fileNames.sort(key = lambda f: int(f.split("_")[-3]) )
        options.inputFiles = ["file:" + f for f in fileNames]

    if options._register.has_key('totalSections') and \
        options._register.has_key('section') and \
        options._register.has_key('inputFiles') and \
        options.totalSections and options.section:
        # copy list
        oldInputFiles = options.inputFiles
        # clear list
        options.clearList('inputFiles')
        # used old list to make list
        options.inputFiles = sectionNofTotal(oldInputFiles,
                                             options.section,
                                             options.totalSections)
        print "  Processing %d files (section %d of %d) ... " % \
            (len(options.inputFiles), options.section, options.totalSections)


#if options.maxEvents < 0:
  #options.outputFile = options.outputFile.split(".")[0] + "_" + options.dataset.replace("/", "_")

#if options.firstFile != 1 or options.lastFile != 0:
  #first = options.firstFile - 1
  #last = options.lastFile
  #options.outputFile = options.outputFile.split(".")[0] + "_%d-%d" % (first+1, last)
  #newInputFiles = options.inputFiles[first:last]
  #del options.inputFiles[:]
  #options.inputFiles = newInputFiles[:]
  #print "Processing %d files (%d..%d) of %d available." % \
    #(len(options.inputFiles), first+1, last, len(options.inputFiles))
#else:
  #print "Processing all %d available files." % len(options.inputFiles)

## Message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

## Geometry, Detector Conditions and Pythia Decay Tables (needed for the vertexing)
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = options.globalTag
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

process.goodMuons.src = "cleanPatMuonsTriggerMatch"
process.goodDimuons.cut = "mass > 0"
process.goodDimuonsCountFilter = process.dimuonsCountFilter.clone(src = "goodDimuons")
process.vertexedDimuons.src = "goodDimuons"

process.MuMuGammaTree = cms.EDAnalyzer("MuMuGammaTreeMaker",
    photonSrc   = cms.untracked.InputTag("cleanPatPhotonsTriggerMatch"),
    muonSrc     = cms.untracked.InputTag("goodMuons"),
    dimuonSrc   = cms.untracked.InputTag("vertexedDimuons"),
    beamSpotSrc = cms.untracked.InputTag("offlineBeamSpot"),
    primaryVertexSrc = cms.untracked.InputTag("offlinePrimaryVertices"),
    ebClusterSrc = cms.untracked.InputTag("islandBasicClusters", "islandBarrelBasicClusters"),
    ebRecHitsSrc = cms.untracked.InputTag("ecalRecHit", "EcalRecHitsEB"),
    eeRecHitsSrc = cms.untracked.InputTag("ecalRecHit", "EcalRecHitsEE"),
    genParticleSrc = cms.untracked.InputTag("prunedGenParticles"),
    isMC        = cms.untracked.bool(False),
    )

process.defaultSequence = cms.Sequence(
    process.goodMuons *
    process.goodDimuons *
    process.goodDimuonsCountFilter *
    process.vertexedDimuons
    )

if options.splitZMC == 1:
    process.load("JPsi.MuMu.photonFilters_cff")

    process.MuMuGammaTreeFsr  = process.MuMuGammaTree.clone()
    process.MuMuGammaTreeIsr  = process.MuMuGammaTree.clone()
    process.MuMuGammaTreeFake = process.MuMuGammaTree.clone()

    process.pFsr = cms.Path(
        process.defaultSequence *
        process.fsrFilterSequence *
        process.MuMuGammaTreeFsr
    )

    process.pIsr = cms.Path(
        process.defaultSequence *
        process.isrFilterSequence *
        process.MuMuGammaTreeIsr
    )

    process.pFake = cms.Path(
        process.defaultSequence *
        process.fakeFilterSequence *
        process.MuMuGammaTreeFake
    )

else:
    process.p = cms.Path(
        process.defaultSequence *
        process.MuMuGammaTree
    )


if options.isMC == "yes":
    #process.goodMuons.src = "cleanPatMuons"
    #process.MuMuGammaTree.photonSrc = "cleanPatPhotons"
    process.MuMuGammaTree.isMC = True

process.options.SkipEvent = cms.untracked.vstring('ProductNotFound')

# JSON file
if options.jsonFile != "":
    import FWCore.PythonUtilities.LumiList as LumiList
    import FWCore.ParameterSet.Types as CfgTypes
    myLumis = LumiList.LumiList(
        filename = options.jsonFile
        ).getCMSSWString().split(',')
    process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
    process.source.lumisToProcess.extend(myLumis)
#     process.source.firstRun = cms.untracked.uint32(146240)


## Debugging
## The Tracer service
# process.Tracer = cms.Service('Tracer')

## Enable LogDebug for MuMuGammaTree module
# process.MessageLogger.debugModules = ["MuMuGammaTree"]
# process.MessageLogger.cerr.threshold = "DEBUG"

if __name__ == "__main__": import user

