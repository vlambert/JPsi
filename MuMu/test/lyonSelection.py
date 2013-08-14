lyonCuts = [
  # 0. Dummy to have cut index equal to it's number in the notes
  "1",
  # 1. only fraction of data analyzed
  "run <= 143179",
  # 2. SC |eta| < 2.5 not implemented and obsoleted by 14
  "1",
  # 3. EB/EE gab removed
  "abs(phoEta[g]) < 1.4442 | 1.566 < abs(phoEta[g])",
  # 4. Spike rejection with kWeird, kOutOfTime and kBad not implemented yet
  "1",
  # 5.
  "muIsGlobalMuon[mu1] & muIsTrackerMuon[mu1] &" + \
  "muIsGlobalMuon[mu2] & muIsTrackerMuon[mu2]",
  # 6.
  "muSiHits[mu1] > 10 & muSiHits[mu2] > 10",
  # 7.
  "muGlobalNormalizedChi2[mu1] < 10 & muGlobalNormalizedChi2[mu2] < 10",
  # 8.
  "abs(muEta[mu1]) < 2.1 & abs(muEta[mu2]) < 2.1",
  # 9. HLT_Mu9 fired - not implemented yet
  "1",
  # 10. muon |eta| < 2.4 - already covered by 8 which is event tighter
  "1",
  # 11.
  "charge[mm] == 0",
  # 12.
  "muPt[mu1] > 10 & muPt[mu2] > 10",
  # 13.
  "40 < mass[mm] & mass[mm] < 80",
  # 14.
  "abs(phoEta[g]) < 2.5",
  # 15.
  "phoPt[g] > 10",
  # 16.
  "mmgDeltaRNear < 0.8",
  # 17.
  "70 < mmgMass & mmgMass < 110",
  # 18.
  "muEcalIso[far] < 1.0",
  # 19.
  "muPt[far] > 30",
  # 20.
  "muHcalIso[near] <= 1.0 | muTrackIso[far] <= 3.0",

  ]

lyonSelection = "&".join(["(%s)" % cut for cut in lyonCuts])