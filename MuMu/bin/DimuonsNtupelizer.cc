#include <memory>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>
#include <iostream>

#include <TH1F.h>
#include <TTree.h>
#include <TROOT.h>
#include <TFile.h>
#include <TSystem.h>

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"

#include "JPsi/MuMu/interface/DimuonsTree.h"


int main(int argc, char* argv[]) 
{
  // ----------------------------------------------------------------------
  // First Part: 
  //
  //  * enable the AutoLibraryLoader 
  //  * book the histograms of interest 
  //  * open the input file
  // ----------------------------------------------------------------------

  // load framework libraries
  gSystem->Load( "libFWCoreFWLite" );
  AutoLibraryLoader::enable();

  // only allow one argument for this simple example which should be the
  // the python cfg file
  if ( argc < 2 ) {
    std::cout << "Usage : " << argv[0] << " [parameters.py]" << std::endl;
    return 0;
  }

  // get the python configuration
  PythonProcessDesc builder(argv[1]);
  const edm::ParameterSet& fwliteParameters = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("FWLiteParams");

  // now get each parameter
  std::string   input_( fwliteParameters.getParameter<std::string  >("input"  ) );
  edm::InputTag muon_ ( fwliteParameters.getParameter<edm::InputTag>("muonSrc") );
  edm::InputTag dimuonsSrc_ ( fwliteParameters.getParameter<edm::InputTag>("dimuonsSrc") );

  
  // book a set of histograms
  fwlite::TFileService fs = fwlite::TFileService("analyzePatBasics.root");
  TFileDirectory theDir = fs.mkdir("analyzeBasicPat");
  TH1F* muonPt_  = theDir.make<TH1F>("muonPt", "pt",    100,  0.,300.);
  TH1F* muonEta_ = theDir.make<TH1F>("muonEta","eta",   100, -3.,  3.);
  TH1F* muonPhi_ = theDir.make<TH1F>("muonPhi","phi",   100, -5.,  5.);

  // book a tree
//   TFileDirectory treeDir = fs.mkdir("muons");
  DimuonsTree muonsTree( fs.make<TTree>("muons", "muons tree") );
  
  // open input file (can be located on castor)
  TFile* inFile = TFile::Open(input_.c_str());

  // ----------------------------------------------------------------------
  // Second Part: 
  //
  //  * loop the events in the input file 
  //  * receive the collections of interest via fwlite::Handle
  //  * fill the histograms
  //  * after the loop close the input file
  // ----------------------------------------------------------------------

  // loop the events
  unsigned int iEvent=0;
  fwlite::Event ev(inFile);
  for(ev.toBegin(); !ev.atEnd(); ++ev, ++iEvent){
    edm::EventBase const & event = ev;

    // break loop after end of file is reached 
    // or after 1000 events have been processed
    if( iEvent==1000 ) break;
    
    // simple event counter
    if(iEvent>0 && iEvent%1==0){
      std::cout << "  processing event: " << iEvent << std::endl;
    }

    // Handle to the muon collection
    edm::Handle<std::vector<pat::Muon> > muons;
    event.getByLabel(muon_, muons);

    // Handle to the dimuon collection
    edm::Handle<std::vector<pat::Muon> > dimuons;
    event.getByLabel(dimuonsSrc_, dimuons);

  
    
    // loop muon collection and fill histograms
    for(unsigned i=0; i<muons->size(); ++i){
      muonPt_ ->Fill( (*muons)[i].pt()  );
      muonEta_->Fill( (*muons)[i].eta() );
      muonPhi_->Fill( (*muons)[i].phi() );
      muonsTree.pt[i] = (*muons)[i].pt();
      muonsTree.Fill();
    }
  }  
  // close input file
  inFile->Close();

  // ----------------------------------------------------------------------
  // Third Part: 
  //
  //  * never forget to free the memory of objects you created
  // ----------------------------------------------------------------------

  // in this example there is nothing to do 
  
  // that's it!
  return 0;
}
