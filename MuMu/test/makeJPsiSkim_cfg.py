import FWCore.ParameterSet.Config as cms

from JPsi.MuMu.makeJPsiSkim_cfi import *

pathPrefix = "file:/uscms_data/d1/veverka/data/"
fileNames = ["Mu_Run2010A-CS_Onia-Jun14thSkim_v1_DimuonSkimPAT.root"]

process.maxEvents.input = 1000
process.MessageLogger.cerr.FwkReport.reportEvery = 10

process.TFileService.fileName = "jpsiSkimHistos_%devts.root" % process.maxEvents.input.value()

process.out.fileName = "jpsiSkim_%devts.root" % process.maxEvents.input.value()
process.options.wantSummary = True
