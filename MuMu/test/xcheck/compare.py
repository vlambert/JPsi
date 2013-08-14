import caltech
import lyon
import ROOT
from ROOT import *

caltechFile = "mmgEvents_LyonSelection_Nov4ReReco_v5.dat"
lyonFile = "Selected_hadEt-noDeltaRmin-relaxedMuEta.txt"

tree = TTree("compare", "compare Lyon and Caltech events")
canvases = []
gROOT.LoadMacro("../tdrstyle.C")
ROOT.setTDRStyle()
TGaxis.SetMaxDigits(3)
gStyle.SetPadRightMargin(0.15)

## Process Lyon events
lines = file(lyonFile).readlines()
eventList = [lyon.Event(line) for line in lines if line.strip()[0] != "#"]
lyonEvents = {}
for e in eventList:
    lyonEvents[e.eid] = e

gROOT.ProcessLine( e.cppStruct("LyonLeafs") )
lleafs = ROOT.LyonLeafs()
e.makeBranches(tree, lleafs, "lyon_")

## Process Caltech events
lines = file(caltechFile).readlines()
eventList = [caltech.Event(line) for line in lines if line.strip()[0] != "#"]
caltechEvents = {}
for e in eventList:
    caltechEvents[e.eid] = e

gROOT.ProcessLine( e.cppStruct("CaltechLeafs") )
cleafs = ROOT.CaltechLeafs()
e.makeBranches(tree, cleafs, "caltech_")

## Iterate over all events and fill the tree
gROOT.ProcessLine("struct Presence {Int_t hasCaltech, hasLyon;};")
presence = ROOT.Presence()
tree.Branch("hasCaltech", AddressOf(presence, "hasCaltech"), "hasCaltech/I")
tree.Branch("hasLyon"   , AddressOf(presence, "hasLyon"   ), "hasLyon/I")

for eid in set( caltechEvents.keys() + lyonEvents.keys() ):
    presence.hasCaltech = 0
    presence.hasLyon = 0
    caltech.Event.initLeafs(cleafs)
    lyon.Event.initLeafs(lleafs)
    if eid in caltechEvents.keys():
        presence.hasCaltech = 1
        caltechEvents[eid].setLeafs(cleafs)
    if eid in lyonEvents.keys():
        presence.hasLyon = 1
        lyonEvents[eid].setLeafs(lleafs)
    tree.Fill()

## Get the overlap statistics
print "Total events:", tree.GetEntries()
print "Caltech-Lyon overlap:", tree.Draw(">>list",  "hasCaltech && hasLyon")
tree.SetScanField(0)
print "== Unique Caltech events =="
tree.Scan("caltech_run:caltech_lumi:caltech_eid",  "hasCaltech && !hasLyon", "col=6d:4d:10ld")
print "== Unique Lyon events =="
tree.Scan("lyon_run:lyon_lumi:lyon_eid",           "!hasCaltech && hasLyon", "col=6d:4d:10ld")

## Make difference and ratio plots for common events
for xname in caltech.Event.varNames:
    if not xname in lyon.Event.varNames: continue
    canvases.append(TCanvas(xname + "Ratio", xname + "Ratio"))
    tree.Draw("lyon_%s / caltech_%s - 1" % (xname, xname), "hasCaltech && hasLyon")
    #gDirectory.Get("htemp").GetXaxis().SetTitle("xname (IPN/CIT - 1)")
    canvases.append(TCanvas(xname + "Difference", xname + "Difference"))
    tree.Draw("lyon_%s - caltech_%s" % (xname, xname), "hasCaltech && hasLyon")
    #gDirectory.Get("htemp").GetXaxis().SetTitle("xname (IPN - CIT)")
    
for c in canvases:
    i = canvases.index(c)
    c.SetWindowPosition(10+20*i, 10+20*i)
    #c.Print("plots_Nov4Rereco_caltechMasses/" + c.GetName() + ".png")


if __name__ == "__main__": import user
