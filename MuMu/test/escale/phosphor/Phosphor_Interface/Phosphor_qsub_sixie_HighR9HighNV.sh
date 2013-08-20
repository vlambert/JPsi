#!/Bin/sh

QSUBDIR=/home/vlambert/scratch_phosphor/CMSSW_4_2_8/src/JPsi/MuMu/test/escale/phosphor/Phosphor_Interface/QsubScripts_sixie_HighR9_ExpFit_HNV

NEWDIR=`date | gawk '{ print $1 $2 $3"_" $6 }'`
RESULTS=HighNV_HighR9
LOGS=HighNV_HighR9_Logs
TreeVer="sixie"

RESDIR=Dir_Results

if [ -d $RESDIR/$NEWDIR ]; then
	echo "DIR $RESDIR/$NEWDIR exists."
	if [ -d $RESDIR/$NEWDIR/$RESULTS ]; then
		echo "DIR $RESDIR/$NEWDIR/$RESULTS exists."
	else
		mkdir $RESDIR/$NEWDIR/$RESULTS
		echo "Creating DIR: $RESDIR/$NEWDIR/$RESULTS."
	fi

	if [ -d $RESDIR/$NEWDIR/$LOGS ]; then
		echo "DIR $RESDIR/$NEWDIR/$LOGS exists."
	else
		mkdir $RESDIR/$NEWDIR/$LOGS
		echo "Creating DIR: $RESDIR/$NEWDIR/$LOGS."
	fi

		
else
	mkdir $RESDIR/$NEWDIR
	echo "Creating DIR: $RESDIR/$NEWDIR."
	mkdir $RESDIR/$NEWDIR/$RESULTS
	echo "Creating DIR: $RESDIR/$NEWDIR/$RESULTS."
	mkdir $RESDIR/$NEWDIR/$LOGS
	echo "Creating DIR: $RESDIR/$NEWDIR/$LOGS."
fi


for qfiles in $QSUBDIR/*.sge; do
    pwd; echo $qfiles; SGEFILE=$qfiles; echo $SGEFILE    
    if [ -a $SGEFILE ] 
	then 
	echo "QSUB"
	#For t3-susy
	#qsub -j y -o $RESDIR/$NEWDIR/$LOGS -q all.q@compute-1-5.local,all.q@compute-0-1.local,all.q@compute-0-2.local,all.q@compute-0-6.local,all.q@compute-1-0.local,all.q@compute-1-4.local,all.q@compute-1-7.local,all.q@compute-1-3.local,all.q@compute-1-2.local,all.q@compute-1-6.local $SGEFILE  -- $RESDIR/$NEWDIR/$RESULTS $TreeVer;
	#For t3-higgs
        qsub -j y -o $RESDIR/$NEWDIR/$LOGS -q all.q@compute-3-2.local,all.q@compute-3-3.local,all.q@compute-3-4.local,all.q@compute-3-9.local,all.q@compute-3-10.local,all.q@compute-3-12.local $SGEFILE -- $RESDIR/$NEWDIR/$RESULTS $TreeVer;
#qsub -j y -o $NEWDIR/$LOGS -q all.q@compute-1-5.local,all.q@compute-1-3.local,all.q@compute-0-1.local,all.q@compute-0-0.local $SGEFILE  -- $NEWDIR/$RESULTS $TreeVer;
#qsub -j y -o $NEWDIR/$LOGS -q all.q@compute-1-2.local $SGEFILE  -- $NEWDIR/$RESULTS $TreeVer;
	#sdfdf

    else

	echo "FILE $SGEFILE DOES NOT EXIT, DOING NOTHING"
    fi
    #cd $INITIALTOPDIR;
done



