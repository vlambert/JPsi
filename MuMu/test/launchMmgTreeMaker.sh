# DATASET=Mu
# TOTALSECTIONS=4
# # SECTION=3
# for SECTION in `seq $TOTALSECTIONS`; do
#   nohup cmsRun makeMuMuGammaTree_cfg.py print \
#     outputFile=MuMuGammaTree_${DATASET} \
#     inputFiles_clear \
#     inputFiles_load=files_Mu_Run2010A-Dec22ReReco_v1.dat \
#     inputFiles_load=files_Mu_Run2010B-DiLeptonMu-Dec22ReReco_v2.dat \
#     maxEvents=-1 \
#     reportEvery=100 \
#     isMC=no \
#     globalTag=GR_R_39X_V6::All \
#     jsonFile=Cert_136033-149442_7TeV_Dec22ReReco_Collisions10_JSON_v3.txt \
#     totalSections=$TOTALSECTIONS \
#     section=$SECTION \
#   >& mmgTree_${DATASET}_${SECTION}of${TOTALSECTIONS}.out &
# done

# DATASET=DYToMuMu-powheg-Winter10-v1
# INPUT_FILES=files_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1-DimuonVGammaSkim_v4.dat

# DATASET=DYToMuMu-powheg-Winter10-v2
# INPUT_FILES=files_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v2-DimuonVGammaSkim_v4.dat

DATASET=DYToMuMu-powheg-Winter10-v2
INPUT_FILES=files_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v2-DimuonVGammaSkim_v4.dat

# DATASET=QCD
# INPUT_FILES=files_QCD_Pt-20_MuEnrichedPt-15_Winter10.dat

# DATASET=TTJets
# INPUT_FILES=files_TTJets_TuneZ2-madgraph-Winter10.dat

# DATASET=WJets
# INPUT_FILES=files_WJetsToLNu_TuneZ2_7TeV-madgraph_Winter10.dat 

# DATASET=GJets_TuneD6T_HT-40To100_7TeV-madgraph_Winter10_JetVGammaSkim_v4_noDimuonFilter
# INPUT_FILES=files_GJets_TuneD6T_HT-40To100_7TeV-madgraph_Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1-JetVGammaSkim_v4.dat

# DATASET=GluGluToHToGG_M-120_7TeV-powheg-pythia6_Winter10_InclusiveVGammaSkim_v4
# INPUT_FILES=files_GluGluToHToGG_M-120_7TeV-powheg-pythia6_Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1-InclusiveVGammaSkim_v4.dat

TOTALSECTIONS=32
# SECTION=3
# for SECTION in `seq $TOTALSECTIONS`; do
for SECTION in `seq 25 32`; do
  nohup cmsRun makeMuMuGammaTree_cfg.py print \
    inputFiles_clear \
    inputFiles_load=$INPUT_FILES \
    maxEvents=-1 \
    reportEvery=1000 \
    outputFile=/wntmp/veverka/MuMuGammaTree_${DATASET} \
    isMC=yes \
    globalTag=START39_V8::All \
    totalSections=$TOTALSECTIONS \
    section=$SECTION \
  >& mmgTree_${DATASET}_${SECTION}of${TOTALSECTIONS}.out &
done
