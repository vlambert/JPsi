#!/bin/bash
### CONFIGURATION BEGIN #######################################################
DATA_SOURCE=/mnt/hadoop/user/veverka/esTrees/testSelectionfsr.v3.Data2011.Jul2012ReReco.muid2.phtid1.phtcorr96.datapu0.mcpu0.scale0.rochcor.root
MC_SOURCE=/mnt/hadoop/user/veverka/esTrees/testSelectionfsr.v3.dy2mmpowhegpythias6v02bAODSIM.muid2.phtid1.phtcorr96.datapu6.mcpu1.scale0.rochcor.root
DATA_OUTPUT=mmg_data_2011AB_jul2012rereco_hggv2_rochcor.dat
MC_OUTPUT=mmg_mc_f11s6_hggv2_rochcor_tight.dat
DUMP_COMMAND='Analysis->SetScanField(0);
  Analysis->Scan(
    "runNumber:lumiBlock:evtNumber:mmgcorr:mm:gamscenergycorr:gameta:gamphi:"
      "gametrue:mpt[0]:meta[0]:mphi[0]:mpt[1]:meta[1]:mphi[1]", 
    "mm + mmg < 180 & min(mdrg[0], mdrg[1]) < 0.8 & mpt[0] > 21 & "
      " mpt[1] > 10.5 & mm > 35 & abs(mmg-90) < 30",
    "col=::20d::::::::::::")'
### CONFIGURATION END #######################################################

## The actual script starts here ##############################################

## Run ROOT to make the dumps in temporary files
root -l -b $DATA_SOURCE $MC_SOURCE <<EOF
_file0->cd();
$DUMP_COMMAND; > data_tmp.dat
_file1->cd();
$DUMP_COMMAND; > mc_tmp.dat
.q
EOF

## Echo this script in the head of the dumps for reference
cat $0 > $DATA_OUTPUT
cat $0 > $MC_OUTPUT
sed -i 's/^/## /' $DATA_OUTPUT $MC_OUTPUT

## Attach the dumps cleaning the `*' signs
sed -i '{s/*//g; /entries/d; /^ *$/d; s/^\(.*Row\)/##\1/}' data_tmp.dat
sed -i '{s/*//g; /entries/d; /^ *$/d; s/^\(.*Row\)/##\1/}' mc_tmp.dat
cat data_tmp.dat >> $DATA_OUTPUT
cat mc_tmp.dat >> $MC_OUTPUT

## Clean up temporary files
rm data_tmp.dat mc_tmp.dat

echo "Exiting $0 with success\!"
