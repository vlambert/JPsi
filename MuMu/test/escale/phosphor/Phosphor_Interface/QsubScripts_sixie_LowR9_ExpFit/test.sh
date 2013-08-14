#!/bin/sh

QSUBDIR=/home/cmorgoth/phosphor/CMSSW_4_2_8_patch7/src/JPsi/MuMu/test/escale/phosphor/Phosphor_Interface/QsubScripts_yyv3_LowR9_ExpFit


NEWDIR=`date | gawk '{ print $1 $2 $3"_" $6 }'`
RESULTS=.
LOGS=.
TreeVer="yyv3"

qsub -j y -o $QSUBDIR -q all.q@compute-0-1.local,all.q@compute-0-2.local,all.q@compute-0-6.local,all.q@compute-0-14.local,all.q@compute-1-0.local,all.q@compute-1-4.local,all.q@compute-1-7.local,all.q@compute-1-3.local,all.q@compute-1-2.local,all.q@compute-1-6.local test.sge  -- $NEWDIR -- $TreeVer;