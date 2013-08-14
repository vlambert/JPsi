#! /usr/bin/env python

from makeEdmNtuples_cfg import *

import sys, getopt

def usage():
  print """
Usage: %s [OPTIONS]

OPTIONS:
  -f --filesPerJob
    Number of input files for this job. Has to be a positive integer.
    Only one of filesPerJob and totalNumberOfJobs can be specified.

  -h --help
    Print this help and exit.

  -j --jobNumber
    Number of the current job.  Has to be a positive integer.
    This determines what input files will be used.
    Job number 1 will process certain number of files defined by the splitting
    parameters `filesPerJob' and `totalNumberOfJobs'. Job 2 will skip the files
    processed by job 1 and so on.

  -t --totalNumberOfJobs
    Total number of jobs to be created.  Has to be a positive integer.
    Only one of filesPerJob and totalNumberOfJobs can be specified.

  """ % (sys.argv[0], )

def illegalArgumentExit(opt, arg):
  print "Illegal argument of option `%s': `%s'" % (opt, arg)
  sys.exit(3)

def main(argv):
  shortFlags = "f:hj:t:"
  longFlags = ["filesPerJob=",
               "help",
               "jobNumber=",
               "totalNumberOfJobs=",
               ]
  filesPerJob = 0
  jobNumber = 0
  totalNumberOfJobs = 0

  try:
    opts, args = getopt.getopt(argv, shortFlags, longFlags)
  except getopt.GetoptError:
    usage()
    sys.exit(2)

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit()
    elif opt in ("-f", "--filesPerJob"):
      try:
        filesPerJob = int(arg)
      except ValueError:
        illegalArgumentExit(opt, arg)
      if filesPerJob <= 0:
        illegalArgumentExit(opt, arg)
    elif opt in ("-j", "--jobNumber"):
      try:
        jobNumber = int(arg)
      except ValueError:
        illegalArgumentExit(opt, arg)
      if jobNumber <= 0:
        illegalArgumentExit(opt, arg)
    elif opt in ("-t", "--totalNumberOfJobs"):
      try:
        totalNumberOfJobs = int(arg)
      except ValueError:
        illegalArgumentExit(opt, arg)
      if totalNumberOfJobs <= 0:
        illegalArgumentExit(opt, arg)
    ## end loop over opts

  numberOfInputFiles = len(inputFiles.fileList)
  numberOfLongerJobs = 0

  ## Make sure filesPerJob is set correctly
  if filesPerJob == 0 and totalNumberOfJobs == 0:
    ## use default value
    filesPerJob = 20
  elif filesPerJob != 0 and totalNumberOfJobs != 0:
    print "Illegal options:", str(opts)
    sys.exit(4)
  elif filesPerJob == 0:
    filesPerJob = numberOfInputFiles / totalNumberOfJobs
    numberOfLongerJobs = numberOfInputFiles - filesPerJob * totalNumberOfJobs
  else:
    totalNumberOfJobs = (numberOfInputFiles - 1) / filesPerJob + 1

  print "number of input files:", numberOfInputFiles
  print "files per job for first %d jobs:" % numberOfLongerJobs, filesPerJob + 1
  print "files per job for last %d jobs:" % (totalNumberOfJobs-numberOfLongerJobs,),  filesPerJob
  print "job number:", jobNumber
  print "total number of jobs:", totalNumberOfJobs

  if jobNumber > 0:
    beginInputFileIndex = filesPerJob*(jobNumber - 1) + min(numberOfLongerJobs, jobNumber - 1)
    endInputFileIndex = beginInputFileIndex + filesPerJob
    if jobNumber <= numberOfLongerJobs: endInputFileIndex += 1
    endInputFileIndex = min(endInputFileIndex, numberOfInputFiles)
    print "Job %d processes input files: %d-%d" % (jobNumber, beginInputFileIndex + 1, endInputFileIndex)

  else:
    for j in range(totalNumberOfJobs):
      beginInputFileIndex = filesPerJob*j + min(numberOfLongerJobs, j)
      if j < numberOfLongerJobs:
        filesPerThisJob = filesPerJob + 1
      else:
        filesPerThisJob = filesPerJob
      endInputFileIndex = beginInputFileIndex + filesPerThisJob
      endInputFileIndex = min(endInputFileIndex, numberOfInputFiles)
      filesPerThisJob = endInputFileIndex - beginInputFileIndex
      print "Job %d processes %d input files: %d-%d" % \
        (j + 1, filesPerThisJob, beginInputFileIndex + 1, endInputFileIndex)

#   if filesPerJob > 0 and jobNumber
## RUN CMSSW FROM WITHIN THE CONFIG
# import os
# outFile = open("tmpConfig.py","w")
# outFile.write("import FWCore.ParameterSet.Config as cms\n")
# outFile.write(process.dumpPython())
# outFile.close()
# os.system("cmsRun tmpConfig.py")

if __name__ == "__main__":
  import user
  main(sys.argv[1:])
