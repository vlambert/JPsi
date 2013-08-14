//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Jun  1 02:49:06 2011 by ROOT version 5.25/04
// from TTree pmv/pixel match veto TreeMaker tree
// found on file: /home/veverka/Work/data/pmv/pmvTree_G_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_Summer11_AOD_42X-v4_V6_numEvent80k.root
//////////////////////////////////////////////////////////

#ifndef PmvTree_h
#define PmvTree_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

#define MAX_PHOTONS 50

class PmvTree {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   UInt_t          id_run;
   UInt_t          id_luminosityBlock;
   UInt_t          id_event;
   Int_t           pileup_size;
   UInt_t          pileup_numInteractions[3];   //[pileup.size]
   Int_t           pileup_bunchCrossing[3];   //[pileup.size]
   Float_t         pileup_weight;
   Float_t         pileup_weightOOT;
   Int_t           nPhotons;
   Float_t         phoPt[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoEta[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoPhi[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoR9[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoIsEB[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoHoE[MAX_PHOTONS];   //[nPhotons]
   Float_t         scEt[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoDeltaRToTrack[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoPassElectronVeto[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoHasMatchedConversion[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoHasPixelMatch[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoSigmaIetaIeta[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoTrackIso[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoEcalIso[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoHcalIso[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoMomPdgId[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoMomStatus[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoGMomPdgId[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoGMomStatus[MAX_PHOTONS];   //[nPhotons]
   Float_t         phoPdgId[MAX_PHOTONS];   //[nPhotons]

   // List of branches
   TBranch        *b_id;   //!
   TBranch        *b_pileup_size;   //!
   TBranch        *b_pileup_numInteractions;   //!
   TBranch        *b_pileup_bunchCrossing;   //!
   TBranch        *b_pileup_weight;   //!
   TBranch        *b_pileup_weightOOT;   //!
   TBranch        *b_nPhotons;   //!
   TBranch        *b_phoPt;   //!
   TBranch        *b_phoEta;   //!
   TBranch        *b_phoPhi;   //!
   TBranch        *b_phoR9;   //!
   TBranch        *b_phoIsEB;   //!
   TBranch        *b_phoHoE;   //!
   TBranch        *b_scEt;   //!
   TBranch        *b_phoDeltaRToTrack;   //!
   TBranch        *b_phoPassElectronVeto;   //!
   TBranch        *b_phoHasMatchedConversion;   //!
   TBranch        *b_phoHasPixelMatch;   //!
   TBranch        *b_phoSigmaIetaIeta;   //!
   TBranch        *b_phoTrackIso;   //!
   TBranch        *b_phoEcalIso;   //!
   TBranch        *b_phoHcalIso;   //!
   TBranch        *b_phoMomPdgId;   //!
   TBranch        *b_phoMomStatus;   //!
   TBranch        *b_phoGMomPdgId;   //!
   TBranch        *b_phoGMomStatus;   //!
   TBranch        *b_phoPdgId;   //!

   PmvTree(TTree *tree=0);
   virtual ~PmvTree();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef PmvTree_cxx
PmvTree::PmvTree(TTree *tree)
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("/home/veverka/Work/data/pmv/pmvTree_G_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_Summer11_AOD_42X-v4_V6_numEvent80k.root");
      if (!f) {
         f = new TFile("/home/veverka/Work/data/pmv/pmvTree_G_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_Summer11_AOD_42X-v4_V6_numEvent80k.root");
      }
      tree = (TTree*)gDirectory->Get("pmv");

   }
   Init(tree);
}

PmvTree::~PmvTree()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t PmvTree::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t PmvTree::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (!fChain->InheritsFrom(TChain::Class()))  return centry;
   TChain *chain = (TChain*)fChain;
   if (chain->GetTreeNumber() != fCurrent) {
      fCurrent = chain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void PmvTree::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("id", &id_run, &b_id);
   fChain->SetBranchAddress("pileup.size", &pileup_size, &b_pileup_size);
   fChain->SetBranchAddress("pileup.numInteractions", pileup_numInteractions, &b_pileup_numInteractions);
   fChain->SetBranchAddress("pileup.bunchCrossing", pileup_bunchCrossing, &b_pileup_bunchCrossing);
   fChain->SetBranchAddress("pileup.weight", &pileup_weight, &b_pileup_weight);
   fChain->SetBranchAddress("pileup.weightOOT", &pileup_weightOOT, &b_pileup_weightOOT);
   fChain->SetBranchAddress("nPhotons", &nPhotons, &b_nPhotons);
   fChain->SetBranchAddress("phoPt", phoPt, &b_phoPt);
   fChain->SetBranchAddress("phoEta", phoEta, &b_phoEta);
   fChain->SetBranchAddress("phoPhi", phoPhi, &b_phoPhi);
   fChain->SetBranchAddress("phoR9", phoR9, &b_phoR9);
   fChain->SetBranchAddress("phoIsEB", phoIsEB, &b_phoIsEB);
   fChain->SetBranchAddress("phoHoE", phoHoE, &b_phoHoE);
   fChain->SetBranchAddress("scEt", scEt, &b_scEt);
   fChain->SetBranchAddress("phoDeltaRToTrack", phoDeltaRToTrack, &b_phoDeltaRToTrack);
   fChain->SetBranchAddress("phoPassElectronVeto", phoPassElectronVeto, &b_phoPassElectronVeto);
   fChain->SetBranchAddress("phoHasMatchedConversion", phoHasMatchedConversion, &b_phoHasMatchedConversion);
   fChain->SetBranchAddress("phoHasPixelMatch", phoHasPixelMatch, &b_phoHasPixelMatch);
   fChain->SetBranchAddress("phoSigmaIetaIeta", phoSigmaIetaIeta, &b_phoSigmaIetaIeta);
   fChain->SetBranchAddress("phoTrackIso", phoTrackIso, &b_phoTrackIso);
   fChain->SetBranchAddress("phoEcalIso", phoEcalIso, &b_phoEcalIso);
   fChain->SetBranchAddress("phoHcalIso", phoHcalIso, &b_phoHcalIso);
   fChain->SetBranchAddress("phoMomPdgId", phoMomPdgId, &b_phoMomPdgId);
   fChain->SetBranchAddress("phoMomStatus", phoMomStatus, &b_phoMomStatus);
   fChain->SetBranchAddress("phoGMomPdgId", phoGMomPdgId, &b_phoGMomPdgId);
   fChain->SetBranchAddress("phoGMomStatus", phoGMomStatus, &b_phoGMomStatus);
   fChain->SetBranchAddress("phoPdgId", phoPdgId, &b_phoPdgId);
   Notify();
}

Bool_t PmvTree::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void PmvTree::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t PmvTree::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef PmvTree_cxx
