from ROOT import *

t = TTree("t", "t")
t.ReadFile("dummy_to_sort.txt", "run/i:lumi:event:gPt/F:nmuPt:fmuPt:gEta:nmuEta:fmuEta:gPhi:nmuPhi:fmuPhi:m2:m3:dr:k")
