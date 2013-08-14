# minimalistic config file to copy / merge cmssw datasets
# veverka@caltech.edu, 2008-12-16

import re
import os
import FWCore.ParameterSet.Config as cms

process = cms.Process('PICK')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(),
   eventsToProcess = cms.untracked.VEventRange("149294:114")
)

process.output = cms.OutputModule("PoolOutputModule",
   fileName = cms.untracked.string('pick.root')
)

process.endpath = cms.EndPath(process.output)

## Set the input files based on a given path
datasetDir = "/mnt/hadoop/user/veverka/DimuonVGammaSkim_v3/Mu"
rootRE = re.compile(".+\.root")
inputFiles = []
for root, dirs, files in os.walk(datasetDir):
    fileNames = []
    for f in files:
        if rootRE.match(f):
            fileNames.append(os.path.join(root, f))
    if fileNames:
        print "  Added %d files from %s ..." % (len(fileNames), root)
    ## sort by job number
    fileNames.sort(key = lambda f: int(f.split("_")[-3]) )
    inputFiles += ["file:" + f for f in fileNames]

process.source.fileNames = inputFiles

## Delete problematic file with I/O error
# process.source.fileNames = [process.source.fileNames[-8]]
# del process.source.fileNames[-8]

## Set the events to be picked based on the ASCII event dump
events = file("../doc/mmgEvents_sihihSelection_Nov4ReReco.dat").readlines()
## run:event are the first two columns of the ASCII file
for e in events:
    ## Skip comments
    if e.strip()[0] == "#": continue
    pars = e.split()
    run, event = pars[0], pars[2]
    process.source.eventsToProcess.append(run + ":" + event)

if __name__ == "__main__": import user

