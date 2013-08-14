if [[ -z $jobNumber ]]; then
  echo "Setting jobNumber=1"
  jobNumber=1
fi

if [[ $jobNumber -lt 1 || $jobNumber -gt 6 ]]; then
  echo "Illegal jobNumber: $jobNumber"
else
  nohup cmsRun makeMuMuGammaTree_cfg.py maxEvents=-1 \
                                        datasetNumber=$jobNumber \
                                        >& mmgTree_${jobNumber}.out &
  echo "lanched job $jobNumber"
  ((jobNumber++))
fi