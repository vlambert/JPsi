leafs = """
run/i
lumi/i
event/i
L1DoubleMuOpen/b
HLT_Mu3/b
HLT_Mu9/b
nDimuons/b
mass/F
pt/F
eta/F
phi/F
y/F
p/F
charge/I
vProb/F
vrho/F
vrhoBS/F
vrhoPV/F
vx/F
vxBS/F
vxPV/F
vy/F
vyBS/F
vyPV/F
vz/F
vzBS/F
vzPV/F
d0/F
d0BS/F
d0PV/F
dz/F
dzBS/F
dzPV/F
dsz/F
dszBS/F
dszPV/F
pdgId/I
backToBack/F
dau1/b
dau2/b
correctedMassJPsi/F
correctedMassY/F
isJPsiCand/b
isYCand/b
isZCand/b
orderByMuQAndPt/b
orderByVProb/b
""".split()

dauLeafs = """
nMuons/b
pt/F
eta/F
phi/F
p/F
charge/I
innerTrack->normalizedChi2/F
innerTrack->dxy/F
innerTrack->dxyBS/F
innerTrack->dxyPV/F
innerTrack->dz/F
innerTrack->dzBS/F
innerTrack->dzPV/F
innerTrack->dsz/F
innerTrack->dszBS/F
innerTrack->dszPV/F
innerTrack->found/b
innerTrack->hitPattern->numberOfValidPixelHits/b
vz/F
isGlobalMuon/B
isTrackerMuon/B
muonID("TMLastStationAngTight")/B
muonID("TrackerMuonArbitrated")/B
trackIso/F
ecalIso/F
hcalIso/F
stations/b
passJPsiId/b
passYId/b
passZId/b
passZIdTight/b
hltMu9Match/b
""".split()

varTypes = {
  "F": "float",
  "I": "int",
  "D": "double",
  "B": "char",
  "i": "unsigned",
  "b": "unsigned char"
}

while leafs.count("") > 0: leafs.remove("")

def getDauName(var):
  tokens = var.split("/")[0].split("->")
  tokens = [t[0].capitalize() + t[1:] for t in tokens]
  name = "".join(tokens)
  name = name.replace("InnerTrackHitPatternNumberOfValid", "")
  name = name.replace("InnerTrack", "Silicon")
  name = name.replace("Found", "Hits")
  name = name.replace("MuonID", "Is")
  name = name.replace('"', '')
  name = name.replace("(", "")
  name = name.replace(")", "")
  return name

def getDauExpr(var):
  tokens = var.split("/")[0].split("->")
  tokens = [t + "()" for t in tokens]
  return "->".join(tokens)

maxNameLen = 0
for var in leafs:
  name = var.split("/")[0]
  if len(name) > maxNameLen: maxNameLen = len(name)

maxDauNameLen = 0
for var in dauLeafs:
  name = getDauName(var)
  if len(name) > maxDauNameLen: maxDauNameLen = len(name)
  
maxTypeLen = 0
for t in varTypes.values():
  if len(t) > maxTypeLen: maxTypeLen = len(t)

print "interface/DimuonsTree.h snippet"

for var in leafs:
  name = var.split("/")[0]
  typeFlag = var.split("/")[1]
  space1 = (maxTypeLen - len(varTypes[typeFlag])) * " "
  space2 = (maxNameLen - len(name) ) * " "
  print '  %s%s %s%s[maxDimuons];' % (varTypes[typeFlag], space1, name, space2)

for var in dauLeafs:
  name = getDauName(var)
  typeFlag = var.split("/")[1]
  space1 = (maxTypeLen - len(varTypes[typeFlag])) * " "
  space2 = (maxDauNameLen - len(name) ) * " "
  print '  {t}{s1} mu{n}{s2}[maxMuons];'.format(t = varTypes[typeFlag], 
                                       s1 = space1, 
                                       n = name, 
                                       s2 = space2)
print

#print "interface/DimuonsTree.cc ctor snippet"

#for name in [var.split("/")[0] for var in leafs]:
  #space = ( maxNameLen - len(name) ) * " "
  #print '  {n}{s}(0),'.format(n=name, s=space)
#for name in [getDauName(var) for var in dauLeafs]:
  #space = ( maxNameLen - len(name) - 3 ) * " "
  #print '  mu1{n}{s}(0),'.format(n=name, s=space)
  #print '  mu2{n}{s}(0),'.format(n=name, s=space)
#print


print "src/DimuonsTree.cc init snippet"
for var in leafs:
  name = var.split("/")[0]
  typeFlag = var.split("/")[1]
  space = (maxNameLen - len(name)) * " "
  mask = '  tree_->Branch("{n}"{s}, {n}{s}, "{n}[nDimuons]/{t}"{s});'
  print mask.format(n=name, s=space, v=var, t=typeFlag)
for var in dauLeafs:
  name = getDauName(var)
  typeFlag = var.split("/")[1]
  space = (maxDauNameLen - len(name)) * " "
  mask = '  tree_->Branch("mu{n}"{s}, mu{n}{s}, "mu{n}[nMuons]/{t}"{s});'
  print mask.format(n=name, s=space, v=var, t=typeFlag)
print

print "src/DimuonsTree.cc initLeafVariables snippet"
for var in leafs:
  name = var.split("/")[0]
  space = (maxNameLen - len(name)) * " "
  print '    {n}[i]{s} = 0;'.format(n=name, s=space)
print
for var in dauLeafs:
  name = getDauName(var)
  space = (maxDauNameLen - len(name)) * " "
  print '    mu{n}[i]{s} = 0;'.format(n=name, s=space)
print

print "plugins/DimuonsNtupelizer.cc snippet"
for var in leafs:
  name = var.split("/")[0]
  space = (maxNameLen - len(name)) * " "
  print '    dimuonsTree_.{n}[i]{s} = dimuon->{n}();'.format(n=name, s=space)
print
for var in dauLeafs:
  name = getDauName(var)
  expr = getDauExpr(var)
  space = (maxDauNameLen - len(name)) * " "
  print '    dimuonsTree_.mu{n}[i]{s} = mu->{e};'.format(n=name, s=space, e=expr)
print
