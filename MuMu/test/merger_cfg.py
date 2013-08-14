# minimalistic config file to copy / merge cmssw datasets
# veverka@caltech.edu, 2008-12-16
import os
import sys
import glob
import re
import FWCore.ParameterSet.Config as cms

srcPath = "/mnt/hadoop/user/veverka/VGammaSkims_v3b/DimuonSkim"
outPath = "/wntmp/veverka/merged"
datasetName = "135821-144114_Sept17ReReco_FNAL"

def jobNumber(filename,
  pattern=re.compile(r"VGammaPAT_DimuonSkim_(\d+)_\d+_.*\.root")
  ):
  basename = os.path.split(filename)[1]
  match = re.search(pattern, basename)
  if match: return int(match.groups()[0])
  else: return -1

process = cms.Process('MERGER')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

## datasetName can be passed as an argument
if len(sys.argv) >= 2 and os.path.isdir(os.path.join(srcPath, sys.argv[-1])):
    datasetName = sys.argv[-1]

datasetName = datasetName.replace("/", "")

fileMask = os.path.join(srcPath, datasetName, "*.root")

## TODONE: sort files by the job index
files = sorted(glob.glob(fileMask), key=jobNumber)

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring()
)
process.source.fileNames = ["file:" + f for f in files][256:]

process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string(
#       '%s.root' % datasetName
        os.path.join(outPath, '%s_2.root' % datasetName)
    )
)

options = cms.PSet(wantSummary = cms.untracked.bool(True))

process.endpath = cms.EndPath(process.output)

if __name__ == "__main__": import user