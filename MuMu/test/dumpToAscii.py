## Configuration
pathPrefix = "rfio:/castor/cern.ch/user/v/veverka/data/DimuonPhotonSkim/edmNtuples/"
# inputFileNames = [pathPrefix + f for f in """
#   ntuple_MinimumBias_Commissioning10_CS_Onia_Jun14thSkim_v1_1.root
#   ntuple_MinimumBias_Commissioning10_CS_Onia_Jun14thSkim_v1_2.root
#   ntuple_MinimumBias_Commissioning10_CS_Onia_Jun14thSkim_v1_3.root
#   ntuple_MinimumBias_Commissioning10_CS_Onia_Jun14thSkim_v1_4.root
#   ntuple_Mu_Run2010A_CS_Onia_Jun14thSkim_v1_135803_137436_WithJson_1.root
#   ntuple_Mu_Run2010A_PromptReco_v4_137437_139375_WithJson_1.root
#   ntuple_Mu_Run2010A_PromptReco_v4_137437_139375_WithJson_2.root
#   ntuple_Mu_Run2010A_PromptReco_v4_137437_139375_WithJson_3.root
#   ntuple_Mu_Run2010A_PromptReco_v4_139376_139790_WithJson_1.root
#   ntuple_Mu_Run2010A_PromptReco_v4_139376_139790_WithJson_2.root
#   ntuple_Mu_Run2010A_PromptReco_v4_139791_140156_NoJson_1.root
#   ntuple_Mu_Run2010A_PromptReco_v4_139791_140156_NoJson_2.root
#   ntuple_Mu_Run2010A_PromptReco_v4_139791_140156_NoJson_3.root
# """.split()]

inputFileNames = [pathPrefix + f for f in """
  ntuple_MinimumBias_Commissioning10_CS_Onia_Jun14thSkim_v1_1.root
  ntuple_MinimumBias_Commissioning10_CS_Onia_Jun14thSkim_v1_2.root
  ntuple_MinimumBias_Commissioning10_CS_Onia_Jun14thSkim_v1_3.root
  ntuple_MinimumBias_Commissioning10_CS_Onia_Jun14thSkim_v1_4.root
  ntuple_Mu_Run2010A_CS_Onia_Jun14thSkim_v1_135803_137436_WithJson_1.root
  ntuple_Mu_Run2010A_PromptReco_v4_137437_139375_WithJson_1.root
  ntuple_Mu_Run2010A_PromptReco_v4_137437_139375_WithJson_2.root
  ntuple_Mu_Run2010A_PromptReco_v4_137437_139375_WithJson_3.root
  ntuple_Mu_Run2010A_PromptReco_v4_139376_139790_WithJson_2.root
  ntuple_Mu_Run2010A_PromptReco_v4_139791_140156_NoJson_2.root
  ntuple_Mu_Run2010A_PromptReco_v4_139791_140156_NoJson_3.root
""".split()]

selection = " && ".join("""8.0 < Mass && Mass < 12.0
Charge != 0
TMath::Prob(VertexChi2, VertexNdof) > 0.001
abs(Y) < 2.0
abs(Dau1Eta) < 2.4
( (abs(Dau1Eta) < 1.6 && Dau1Pt > 3.5) || (1.6 < abs(Dau1Eta) && Dau1Pt > 2.5) )
Dau1SiliconHits > 11
Dau1PixelHits > 1
Dau1InnerTrackNormalizedChi2 < 5
abs(Dau1InnerTrackD0) < 3
abs(Dau1InnerTrackDZ) < 10
abs(Dau2Eta) < 2.4
( (abs(Dau2Eta) < 1.6 && Dau2Pt > 3.5) || (1.6 < abs(Dau2Eta) && Dau2Pt > 2.5) )
Dau2SiliconHits > 11
Dau2PixelHits > 1
Dau2InnerTrackNormalizedChi2 < 5
abs(Dau2InnerTrackD0) < 3
abs(Dau2InnerTrackDZ) < 10""".split("\n"))
outputExpression = "Mass"
outputFileName = "YMassSS_upto140156.txt"
print "Dumping `%s'" % outputExpression
print "  from `%s' " % "', `".join(inputFileNames)
print "  to `%s'"    % outputFileName
print "  for `%s'"   % selection

print "Switching to batch mode ..."
import sys
sys.argv.append( '-b' )

print "Loading ROOT ..."
import ROOT
chain = ROOT.TChain("Events")
for f in inputFileNames:
  print "Reading `%s'" % f
  chain.Add(f)

print "Going trhough %d input entries ..." % chain.GetEntries()
chain.Draw(outputExpression, selection, "goff")
output = chain.GetV1()
outputSize = chain.GetSelectedRows()

print "Writing to %d entries `%s'" % (outputSize, outputFileName)
outputFile = open(outputFileName, "w")
ascii = "\n".join(["%f" % output[i] for i in range(outputSize)])
outputFile.write(ascii + "\n")
outputFile.close()
print "... Done."
