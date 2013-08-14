#!/bin/sh

QSUBDIR=/home/cmorgoth/phosphor/CMSSW_4_2_8_patch7/src/JPsi/MuMu/test/escale/phosphor/Phosphor_Interface/QsubScripts_yyv3_HighR9_ExpFit


NEWDIR=`date | gawk '{ print $1 $2 $3"_" $6 }'`
RESULTS=Gaussian_yyv3_muon_corr_highR9_exp_SmMCNormalData
LOGS=Gaussian_yyv3_muon_corr_highR9_log_exp_SmMCNormalData
TreeVer="yyv3"

if [ -d $NEWDIR ]; then
	echo "DIR $NEWDIR exists."
	if [ -d $NEWDIR/$RESULTS ]; then
		echo "DIR $NEWDIR/$RESULTS exists."
	else
		mkdir $NEWDIR/$RESULTS
		echo "Creating DIR: $NEWDIR/$RESULTS."
	fi

	if [ -d $NEWDIR/$LOGS ]; then
		echo "DIR $NEWDIR/$LOGS exists."
	else
		mkdir $NEWDIR/$LOGS
		echo "Creating DIR: $NEWDIR/$LOGS."
	fi

		
else
	mkdir $NEWDIR
	echo "Creating DIR: $NEWDIR."
	mkdir $NEWDIR/$RESULTS
	echo "Creating DIR: $NEWDIR/$RESULTS."
	mkdir $NEWDIR/$LOGS
	echo "Creating DIR: $NEWDIR/$LOGS."
fi


for qfiles in $QSUBDIR/*.sge; do
    pwd; echo $qfiles; SGEFILE=$qfiles; echo $SGEFILE    
    if [ -a $SGEFILE ] 
	then 
	echo "QSUB"

	qsub -j y -o $NEWDIR/$LOGS -q all.q@compute-0-1.local,all.q@compute-0-2.local,all.q@compute-0-6.local,all.q@compute-0-14.local,all.q@compute-1-0.local,all.q@compute-1-4.local,all.q@compute-1-7.local,all.q@compute-1-3.local,all.q@compute-1-2.local,all.q@compute-1-6.local $SGEFILE  -- $NEWDIR/$RESULTS $TreeVer;
	#qsub -j y -o $NEWDIR/$LOGS -q all.q@compute-0-5.local,all.q@compute-1-5.local $SGEFILE  -- $NEWDIR/$RESULTS;
	#sdfdf

    else

	echo "FILE $SGEFILE DOES NOT EXIT, DOING NOTHING"
    fi
    #cd $INITIALTOPDIR;
done



