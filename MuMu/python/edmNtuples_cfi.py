import FWCore.ParameterSet.Config as cms

############ Muons #############
# {tag: quantity}
# Tag is set to a TTree alias.
# Quantity is interpreted by the PhysicsCutParser and resulting value is stored.
muonQuantities = {
  "Pt"                       : "pt",
  "Eta"                      : "eta",
  "Phi"                      : "phi",
  "P"                        : "p",
  "Charge"                   : "charge",
  "InnerTrackNormalizedChi2" : "innerTrack.normalizedChi2",
  "InnerTrackD0"             : "innerTrack.d0",
  "InnerTrackDZ"             : "innerTrack.dz",
  "SiliconHits"              : "innerTrack.found",
  "PixelHits"                : "innerTrack.hitPattern.numberOfValidPixelHits",
  "IsGlobalMuon"             : "isGlobalMuon",
  "IsTrackerMuon"            : "isTrackerMuon",
  "IsTMLastStationAngTight"  : "muonID('TMLastStationAngTight')",
  "IsTrackerMuonArbitrated"  : "muonID('TrackerMuonArbitrated')",
  "TrackIso"                 : "trackIso",
  "EcalIso"                  : "ecalIso",
  "HcalIso"                  : "hcalIso",
}

# globalMuonQuantities = {
#   "GlobalTrackNormalizedChi2" : "globalTrack.normalizedChi2",
# }

muonVariables = cms.VPSet() + [
  cms.PSet(
    tag = cms.untracked.string(t),
    quantity = cms.untracked.string(muonQuantities[t])
  )
  for t in muonQuantities.keys()
]

muonNtp = cms.EDProducer("CandViewNtpProducer",
  src = cms.InputTag("goodMuons"),
  lazyParser = cms.untracked.bool(True),
  prefix = cms.untracked.string("muon"),
  variables = muonVariables
)

## Auxiliary string descibing the scalar product of daghter momenta
DaughterPDot = "+".join("""daughter(0).px*daughter(1).px
                           daughter(0).py*daughter(1).py
                           daughter(0).pz*daughter(1).pz""".split()
                       )
DaughterPDot = "(" + DaughterPDot + ")"


############ Dimuons #############
# Define the composite quantities

dimuonQuantities = {
  "Mass"       : "mass",
  "Pt"         : "pt",
  "Eta"        : "eta",
  "Phi"        : "phi",
  "Y"          : "y",
  "P"          : "p",
  "Charge"     : "charge",
  "VertexChi2" : "vertexChi2",
  "VertexNdof" : "vertexNdof",
  "CosTheta"   : DaughterPDot + " / (daughter(0).p * daughter(1).p)",
  "VertexR"   : "sqrt(vx*vx + vy*vy)",
  "VertexZ"   : "vz",
}

# Add the daughter quantities same as for muons
for x in muonQuantities.keys():
  dimuonQuantities["Dau1" + x] = "daughter(0).masterClone." + muonQuantities[x]
  dimuonQuantities["Dau2" + x] = "daughter(1).masterClone." + muonQuantities[x]

dimuonVariables = cms.VPSet() + [
  cms.PSet(
    tag = cms.untracked.string(t),
    quantity = cms.untracked.string(dimuonQuantities[t])
  )
  for t in dimuonQuantities.keys()
]

dimuonNtp = cms.EDProducer("CandViewNtpProducer",
  src = cms.InputTag("vertexedDimuons"),
  lazyParser = cms.untracked.bool(True),
  prefix = cms.untracked.string(""),
  variables = dimuonVariables
)

## Add few more event hypotheses
jpsiNtp = dimuonNtp.clone(src = "jpsis", prefix = "jpsi")
psi2SNtp = dimuonNtp.clone(src = "psis2S", prefix = "psi2S")

# ggssJPsiEdmNtuple = ggosJPsiEdmNtuple.clone(src = "dimuonsGGSS", prefix = "ggssJPsi")
#
# gtosJPsiEdmNtuple = ggosJPsiEdmNtuple.clone(src = "dimuonsGTOS", prefix = "gtosJPsi")
# gtssJPsiEdmNtuple = ggosJPsiEdmNtuple.clone(src = "dimuonsGTSS", prefix = "gtssJPsi")
#
# ttosJPsiEdmNtuple = ggosJPsiEdmNtuple.clone(src = "dimuonsTTOS", prefix = "ttosJPsi")
# ttssJPsiEdmNtuple = ggosJPsiEdmNtuple.clone(src = "dimuonsTTSS", prefix = "ttssJPsi")
#
# jpsiEdmNtuple = ggosJPsiEdmNtuple.clone(src = "jpsis", prefix = "jpsi")

