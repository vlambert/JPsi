#!/bin/sh

QSUBDIR=/home/cmorgoth/phosphor/CMSSW_4_2_8_patch7/src/JPsi/MuMu/test/escale/phosphor/Phosphor_Interface/QsubScripts

for qfiles in $QSUBDIR/*.sge; do
    pwd; echo $qfiles; SGEFILE=$qfiles; echo $SGEFILE    
    if [ -a $SGEFILE ] 
	then 
	echo "QSUB"
	#qsub -j y -o `pwd` -q all.q $SGEFILE;
	#qsub -j y -o `pwd` -q all.q@compute-1-6.local,all.q@compute-0-1.local,all.q@compute-0-3.local,all.q@compute-1-7.local,all.q@compute-1-8.local,all.q@compute-1-9.local,all.q@compute-0-14.local,all.q@compute-0-2.local,all.q@compute-0-4.local,all.q@compute-0-6.local $SGEFILE;
	
	#qsub -j y -o `pwd` -q all.q@compute-1-5.local,all.q@compute-1-8.local,all.q@compute-1-9.local,all.q@compute-1-6.local,all.q@compute-1-0.local  $SGEFILE;
	qsub -j y -o `pwd` -q all.q $SGEFILE;
    else

	echo "FILE $SGEFILE DOES NOT EXIT, DOING NOTHING"
    fi
    #cd $INITIALTOPDIR;
done



