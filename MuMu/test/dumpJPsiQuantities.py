import ROOT

## Configuration
# inputFiles = ["muNtuples.root", "minimumBiasNtuples.root"]
inputFiles = ["ntuplePromptReco.root"]
quantitiesToDump = ["Mass", "Charge"]
minJMass = 0.
maxJMass = 15.
categoriesToDump = ["gg", "gt", "tt"]
maxEventsInput = 10

chain = ROOT.TChain("Events")
for f in inputFiles: chain.Add(f)
chain.SetScanField(0)

## Build the selection
for category in categoriesToDump:
  scanExpression = ":".join([category + chargeLabel + "JPsi" + x
                             for x in quantitiesToDump] + [category]
                             )
  print "Dumping `%s' ..." % (scanExpression,)
  chain.Scan(scanExpression, "", "", maxEventsInput)
