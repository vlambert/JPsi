#!/bin/bash
## 
## Test SGE submission script for the PHOSPHOR Fit.
## USAGE:
## qsub $CMSSW_BASE/src/JPsi/MuMu/scripts/phosphor-job-test.sh
## Jan Veverka, Caltech, 10 April 2012

# request Bourne shell as shell for job
#$ -S /bin/sh
# Name of the job will be
#$ -N sgetest_data_EE_highR9_pt30to999_v15
# Name of the log file will be
#$ -o /raid2/veverka/jobs/test/sgetest_data_EE_highR9_pt30to999_v15.log
# Combine output/error messages into one file
#$ -j y

echo 'Entering PHOSHPOR OSG job test.'

CMSSW_SETUP_SCRIPT=/home/veverka/bin/fsr-apr12-cmssw42x-osg.sh
JOB_DIR=/wntmp/veverka/sgetest_data_EE_highR9_pt30to999_v15
JOB_SCRIPT=JPsi/MuMu/test/escale/phosphormodel5_test9.py
JOB_ARGS=( -b sgetest_data_EE_highR9_pt30to999_v15 )
OUTPUT_DIR=/raid2/veverka/jobs/test

## Setup CMSSW
. $CMSSW_SETUP_SCRIPT || { 
    echo "Cannot source $CMSSW_SETUP_SCRIPT" >2
    exit 1 
}

## Create work area
if [[ ! -d $JOB_DIR ]]; then
    mkdir -p $JOB_DIR
fi

## Move to work area
cd $JOB_DIR || { 
    echo "Cannot cd to $JOB_DIR" >2
    exit 2
}

## Run the script
python $CMSSW_BASE/src/$JOB_SCRIPT ${JOB_ARGS[@]}

## Create PDF files for EPS figures
for EPS in $JOB_DIR/*.eps; do
    ps2pdf -dEPSCrop $EPS
done

## Copy the outputs
echo "Results in $JOB_DIR:"
ls -l $JOB_DIR
cp -r $JOB_DIR $OUTPUT_DIR || { 
    echo "Cannot copy \`$JOB_DIR' to \`$OUTPUT_DIR'" >2
    exit 2
}

## Clean up
rm -rf $JOB_DIR

echo 'Exitting PHOSHPOR OSG job test with success!'
exit 0

