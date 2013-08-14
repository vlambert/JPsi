import FWCore.ParameterSet.Config as cms

jpsisGGOS = cms.EDFilter("CandViewRefSelector",
  src = cms.InputTag("dimuonsGGOS"),
  cut = cms.string("mass > 0"),
  filter = cms.bool(True)
)

jpsisGGSS = jpsisGGOS.clone( src = "dimuonsGGSS" )

jpsisGTOS = jpsisGGOS.clone( src = "dimuonsGTOS" )
jpsisGTSS = jpsisGGOS.clone( src = "dimuonsGTSS" )

jpsisTTOS = jpsisGGOS.clone( src = "dimuonsTTOS" )
jpsisTTSS = jpsisGGOS.clone( src = "dimuonsTTSS" )
