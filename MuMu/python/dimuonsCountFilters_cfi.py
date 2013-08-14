import FWCore.ParameterSet.Config as cms

dimuonsCountFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("dimuons"),
    minNumber = cms.uint32(1)
)

dimuonsOSCountFilter = dimuonsCountFilter.clone(src = "dimuonsOS")
dimuonsSSCountFilter = dimuonsCountFilter.clone(src = "dimuonsSS")

dimuonsGGOSCountFilter = dimuonsCountFilter.clone(src = "dimuonsGGOS")
dimuonsGGSSCountFilter = dimuonsCountFilter.clone(src = "dimuonsGGSS")

dimuonsGTOSCountFilter = dimuonsCountFilter.clone(src = "dimuonsGTOS")
dimuonsGTSSCountFilter = dimuonsCountFilter.clone(src = "dimuonsGTSS")

dimuonsTTOSCountFilter = dimuonsCountFilter.clone(src = "dimuonsTTOS")
dimuonsTTSSCountFilter = dimuonsCountFilter.clone(src = "dimuonsTTSS")
