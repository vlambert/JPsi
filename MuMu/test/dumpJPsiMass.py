import ROOT

## Configuration
# inputFiles = ["muNtuples.root", "minimumBiasNtuples.root"]
inputFiles = ["ntuplePromptReco.root"]
minJMass = 0.
maxJMass = 15.
chargeValue = 2
categoriesToDump = ["gg", "gt", "tt"]
chargeLabel = "ss" # os = opposite sign, ss = same sign
maxEventsInput = 99999999

chain = ROOT.TChain("Events")
for f in inputFiles: chain.Add(f)
chain.SetScanField(0)

## Build the selection
for category in categoriesToDump:
  massExpression = category + chargeLabel + "JPsiMass"
  chargeExpression = category + chargeLabel + "JPsiCharge"
  selection = "%g < %s & %s < %g & %s == %d" % (minJMass,
                                                massExpression,
                                                massExpression,
                                                maxJMass,
                                                chargeExpression,
                                                chargeValue
                                                )
  print "Dumping `%s' for `%s' ..." % (massExpression, selection)
  chain.Scan(massExpression, selection, "", maxEventsInput)
