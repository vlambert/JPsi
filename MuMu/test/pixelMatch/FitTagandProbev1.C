#include <iomanip>
#include <fstream>
#include "TH1.h"
#include "TH2.h"
#include "TString.h"
#include "TFile.h"
#include "TMath.h"
#include "TBranch.h"
#include "TChain.h"
#include <iostream>
#include <algorithm>
#include <map>
#include "TLorentzVector.h"
#include "TVector3.h"
#include "TApplication.h"
#include "TSystem.h"
#include "TF1.h"
#include "TGraphErrors.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TRandom.h"
#include "TRandom3.h"
#include "TMultiLayerPerceptron.h"
#include "TMLPAnalyzer.h"
#include "TMatrixD.h"
#include "TMatrix.h"
#include "TMatrixDSymEigen.h"
#include "TMatrixDSym.h"
#include "TMatrixTSym.h"
#include <vector>
#include "TArrow.h"
#include "TLegend.h"
#include "TROOT.h"
#include <stdlib.h>
#include "TStyle.h"
#include "TLatex.h"
#include "TGraphAsymmErrors.h"
#include "TLegendEntry.h"
#include "THStack.h"
#include "TMultiGraph.h"

#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "RooSimultaneous.h"
#include "RooCategory.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "RooHistPdf.h"
#include "RooExponential.h"
#include "RooFitResult.h"
#include "RooDataHist.h"
#include "RooGenericPdf.h"

#include "RooBreitWigner.h"
#include "RooCBShape.h"
#include "RooFFTConvPdf.h"


using namespace RooFit ;

using namespace std;


// #include "/home/yongy/backup/plot_stack.cc"

/**
    \brief Tag and Probe fitter from Yong
      Originally from t3-susy:/home/raid2/yangyong/data/analysis1/
      How to run:

.L FitTagandProbev1.C+()

FitTagAndProbev1(
  "resTP/testTagProbe.trkmtoid.dm1.dflag4.mT1.cha1.mt30.pass.ptbin0.etabin0",
  "resTP/testTagProbe.trkmtoid.dm1.dflag4.mT1.cha1.mt30.fail.ptbin0.etabin0",
  "res/testTagProbe.dm2.dflag3.mT1.cha1.mt30.pu0.mc3.root",
  "hh_Mtagtrkmtoid_pteta_0_0",
  "hh_Mtagtrkmtoidf_pteta_0_0",
  60, 120, true, false
)
*/

float LUMINOSITY = 3;


double ErrorInProduct(double x, double errx, double y,
                      double erry, double corr) {
  double xFrErr = errx/x;
   double yFrErr = erry/y;
   return sqrt(xFrErr*xFrErr +yFrErr*yFrErr + 2.0*corr*xFrErr*yFrErr)*x*y;
}

///v1 using unbinnned fit
//input data text file
void FitTagAndProbev1(char *datafile_pass, char *datafile_fail, char *mcRootFile, char *mcPassHist, char *mcFailHist, float xminFit, float xmaxFit, bool SetPassBkgZero,bool SetFailBkgZero){


  gROOT->cd();
  gROOT->Reset();

  gSystem->Load("libRooFit") ;
  gSystem->Load("libRooFitCore") ;



  RooRealVar* rooMass_ = new RooRealVar("Mass","m_{#mu#mu}",xminFit, xmaxFit, "GeV/c^{2}");
  RooRealVar Mass = *rooMass_;


  // Make the category variable that defines the two fits,
  // namely whether the probe passes or fails the eff criteria.
  RooCategory sample("sample","") ;
  sample.defineType("Pass", 1) ;
  sample.defineType("Fail", 2) ;

  ///////// convert Histograms into RooDataHists
  //RooDataHist* data_pass = new RooDataHist("data_pass","data_pass",
  //RooArgList(Mass), hist_pass);

  RooDataSet *data_pass = RooDataSet::read(datafile_pass,RooArgSet(Mass));
  //RooDataHist* data_fail = new RooDataHist("data_fail","data_fail",
  //RooArgList(Mass), hist_fail);
  RooDataSet *data_fail = RooDataSet::read(datafile_fail,RooArgSet(Mass));

  cout<<data_pass->sumEntries()<<" " <<data_fail->sumEntries()<<endl;



  //  RooDataHist* data = new RooDataHist( "fitData","fitData",
  //				       RooArgList(Mass),RooFit::Index(sample),
  //				       RooFit::Import("Pass",*hist_pass), RooFit::Import("Fail",*hist_fail) );

  RooDataSet* data = new RooDataSet( "fitData","fitData",RooArgList(Mass),RooFit::Index(sample),RooFit::Import("Pass",*data_pass),RooFit::Import("Fail",*data_fail) );


  // Signal pdf

  //TFile *Zeelineshape_file =  new TFile("res/testTagProbe.dm2.dflag2.mT1.root","read");

  //  TFile *Zeelineshape_file =  new TFile("res/testTagProbe.dm2.dflag2.mT1.cha1.mt30.root","read");
  //res/testTagProbe.dm2.dflag2.mT1.cha1.mt30.root

  //TFile *Zeelineshape_file =  new TFile("res/testTagProbe.dm2.dflag3.mT1.cha0.mt-1.pu1.root","read");




    TFile *Zeelineshape_file =  new TFile(mcRootFile,"read");

  TH1F *th1 = (TH1F*)Zeelineshape_file->Get(mcPassHist);

 //  ///int nbins = th1->GetNbinsX();
//   int nbins = int( (xmaxFit - xminFit+0.1) / th1->GetBinWidth(1));
//   int rebin = 2;
//   nbins = nbins/ rebin;

//   cout<<"nbins: "<< nbins <<endl;


//   th1->Rebin(rebin);

  int nbins = 60;



  RooDataHist* rdh = new RooDataHist("rdh","", Mass, th1);
  TH1 *th1f = (TH1F*)Zeelineshape_file->Get(mcFailHist);
  RooDataHist* rdhf = new RooDataHist("rdh","", Mass, th1f);



  const char *passHistName = th1->GetName();
  const char *failHistName = th1f->GetName();

  const char *passHistTitle = th1->GetTitle();
  const char *failHistTitle = th1->GetTitle();

  float xlowMC = th1->GetXaxis()->GetXmin();
  float xmaxMC = th1->GetXaxis()->GetXmax();
  if( xminFit < xlowMC  || xmaxFit > xmaxMC ){
    cout<<"FitRangeNotMC "<< xlowMC <<"to"<< xmaxMC <<" MC "<<endl;
    return;
  }
  int startbin = int((xminFit-xlowMC+0.001)/th1->GetBinWidth(1)) + 1;
  int endbin = int((xmaxFit-xlowMC+0.001)/th1->GetBinWidth(1));
  float passMC = th1->Integral(startbin,endbin);
  float allMC = th1->Integral(startbin,endbin) +  th1f->Integral(startbin,endbin);
  float effTP_MC =  passMC / allMC;
  float effTP_MCerr = sqrt( effTP_MC * (1- effTP_MC)/ allMC);
  //  float effTP_MC =  th1->Integral() / ( th1->Integral() + th1f->Integral());




  //RooRealVar* rooMass1_ = new RooRealVar("Mass","m_{#mu#mu}",xminFit, xmaxFit, "GeV/c^{2}");
  //RooRealVar Mass1 = *rooMass1_;

  // RooRealVar* massShift = new RooRealVar("massShift","massShift",0.,-2,2);
  //RooFormulaVar* rooMass1_ = new RooFormulaVar("Mass1", "(1-massShift)*Mass", RooArgList(*massShift,Mass));
  //RooFormulaVar Mass1 = *rooMass1_;

  RooHistPdf* signalShapePdfPass = new RooHistPdf("signalShapePdf", "",
						  RooArgSet(Mass), *rdh,1);

  RooHistPdf* signalShapePdfFail = new RooHistPdf("signalShapePdf", "",
						  RooArgSet(Mass), *rdhf,1);


  RooRealVar  cbBias ("#Deltam_{CB}", "CB Bias", 0.05, -2, 2,"GeV/c^{2}");
  RooRealVar  cbSigma("#sigma_{CB}","CB Width", 1.38, 0.01, 10.0,"GeV/c^{2}");
  RooRealVar  cbCut  ("a_{CB}","CB Cut", 1.5, 0.1, 2.0);
  RooRealVar  cbPower("n_{CB}","CB Power", 1.3, 0.1, 20.0);
  RooRealVar bwMean("m_{Z}","BW Mean", 91.1876, "GeV/c^{2}");
  RooRealVar bwWidth("#Gamma_{Z}", "BW Width", 2.4952, "GeV/c^{2}");
  RooBreitWigner bw("bw", "bw", Mass, bwMean, bwWidth);
  RooCBShape     cball("cball", "A  Crystal Ball Lineshape", Mass, cbBias, cbSigma, cbCut, cbPower);
  RooFFTConvPdf BWxCB("BWxCB","bw (X) crystall ball", Mass, bw, cball);




  // Background pass PDF

  RooRealVar* bkgShape = new RooRealVar("bkgShape","bkgShape",-0.2,-10.,0.);

  if(SetPassBkgZero){
    bkgShape = new RooRealVar("bkgShape","bkgShape",0.,0.,0.);
  }

  RooExponential* bkgShapePdf = new RooExponential("bkgShapePdf","bkgShapePdf",Mass, *bkgShape);

  // Background fail PDF
  RooRealVar* bkgShapef = new RooRealVar("bkgShapef","bkgShape",-0.2,-10.,0.);
  if(SetFailBkgZero){
    bkgShapef = new RooRealVar("bkgShapef","bkgShape",0.,0.,0.);
  }

  RooExponential* bkgShapePdff = new RooExponential("bkgShapePdff","bkgShapePdff",Mass, *bkgShapef);
  //RooGenericPdf* bkgShapePdff = new RooGenericPdf("bkgShapePdff","bkgShapePdff","pow(Mass,bkgShapef)",RooArgSet(Mass, *bkgShapef));

  // Now define some efficiency/yield variables


  RooRealVar* numSignal = new RooRealVar("numSignal","numSignal", 100, 0.0, 1000000.0);
  RooRealVar* eff = new RooRealVar("eff","eff", 0.9, 0.2, 1.0);
  RooFormulaVar* nSigPass = new RooFormulaVar("nSigPass", "eff*numSignal", RooArgList(*eff,*numSignal));
  RooFormulaVar* nSigFail = new RooFormulaVar("nSigFail", "(1.0-eff)*numSignal", RooArgList(*eff,*numSignal));

  RooRealVar* nBkgPass = new RooRealVar("nBkgPass","nBkgPass", 100, 0.0, 10000000);
  if(SetPassBkgZero){
    nBkgPass = new RooRealVar("nBkgPass","nBkgPass", 0., 0., 0.);
  }


  RooRealVar* nBkgFail = new RooRealVar("nBkgFail","nBkgFail", 100, 0.0, 10000000);
  if(SetFailBkgZero){
    nBkgFail = new RooRealVar("nBkgFail","nBkgFail", 0.,0.,0.);
  }



  RooArgList componentsPass(*signalShapePdfPass,*bkgShapePdf);
  RooArgList yieldsPass(*nSigPass, *nBkgPass);

  RooArgList componentsFail(*signalShapePdfFail,*bkgShapePdff);
  // RooArgList componentsFail(BWxCB,*bkgShapePdff);


  RooArgList yieldsFail(*nSigFail, *nBkgFail);


   RooAddPdf pdfPass("pdfPass","extended sum pdf", componentsPass, yieldsPass);
   RooAddPdf pdfFail("pdfFail","extended sum pdf", componentsFail, yieldsFail);


   // The total simultaneous fit ...
   RooSimultaneous totalPdf("totalPdf","totalPdf", sample);
   totalPdf.addPdf(pdfPass,"Pass");
   totalPdf.Print();
   totalPdf.addPdf(pdfFail,"Fail");
   totalPdf.Print();


   ifstream readinfail(datafile_fail,ios::in);
   float mm;
   int ndataFailPeak = 0;
   while(readinfail.good()){
    if( readinfail.eof()) break;
    readinfail>>mm;

    if( mm> 80 && mm <100){
      ndataFailPeak ++;
    }

   }


   // ********* Do the Actual Fit ********** //

   RooFitResult *fitResult = totalPdf.fitTo(*data,RooFit::Save(true),
					    RooFit::Extended(true), RooFit::PrintLevel(-1));

   fitResult->Print("v");


  double numerator = nSigPass->getVal();
  double nfails    = nSigFail->getVal();
  double denominator = numerator + nfails;

  cout<<"num/den: "<< numerator <<" "<< denominator <<endl;

   RooAbsData::ErrorType errorType = RooAbsData::Poisson;

   TCanvas *can0 = new TCanvas("can0","c000",200,10,550,500);
   setTCanvasNicev1(can0);

   //RooPlot* frame1 = Mass.frame();
   RooPlot* frame1 = Mass.frame(Range(xminFit,xmaxFit),Bins(nbins));

   frame1->SetMinimum(0);
   data_pass->plotOn(frame1,RooFit::DataError(errorType));
   pdfPass.plotOn(frame1,RooFit::ProjWData(*data_pass),
		  RooFit::Components(*bkgShapePdf),RooFit::LineColor(kRed));
   pdfPass.plotOn(frame1,RooFit::ProjWData(*data_pass));
   frame1->Draw("e0");

   char *filename = new char[1000];
   sprintf(filename,"Probe Pass %s",passHistTitle);
   TLatex l;
   l.SetNDC();
   l.SetTextSize(0.04);
   l.SetTextColor(1);
   l.DrawLatex(0.2,0.9,filename);
   double nsig = numSignal->getVal();
   double nErr = numSignal->getError();
   double e = eff->getVal();
   double eErr = eff->getError();
   double corr = fitResult->correlation(*eff, *numSignal);
   double err = ErrorInProduct(nsig, nErr, e, eErr, corr);
   sprintf(filename, "N_{s} = %.2f #pm %.2f", nSigPass->getVal(), err);
   l.DrawLatex(0.62,0.8,filename);
   sprintf(filename, "N_{b} = %.2f #pm %.2f", nBkgPass->getVal(), nBkgPass->getError());
   l.DrawLatex(0.62,0.75,filename);
   sprintf(filename, "#epsilon^{Data}_{s} = %4.3f #pm %4.3f", eff->getVal(), eff->getError());
   l.DrawLatex(0.62,0.7,filename);
   sprintf(filename, "#epsilon^{MC}_{s} = %4.3f", effTP_MC);
   l.DrawLatex(0.62,0.65,filename);


   sprintf(filename,"resTP/hhu_probepass_%s.gif",passHistName);
   can0->Print(filename);
   sprintf(filename,"resTP/hhu_probepass_%s.pdf",passHistName);
   can0->Print(filename);


   //probel fail

   TCanvas *can1 = new TCanvas("can1","c001",200,10,550,500);
   setTCanvasNicev1(can1);
   //RooPlot* frame1f = Mass.frame();
   //RooPlot* frame1f = Mass.frame(Range(xminFit,xmaxFit),Bins(nbins));
   RooPlot* frame1f = Mass.frame(Range(xminFit,xmaxFit),Bins(30));
   frame1f->SetMinimum(0);
   data_fail->plotOn(frame1f,RooFit::DataError(errorType));
   pdfFail.plotOn(frame1f,RooFit::ProjWData(*data_fail),
		  RooFit::Components(*bkgShapePdff),RooFit::LineColor(kRed));
   pdfFail.plotOn(frame1f,RooFit::ProjWData(*data_fail));
   frame1f->Draw("e0");

   sprintf(filename,"Probe Fail %s", failHistTitle);
   l.DrawLatex(0.2,0.9,filename);
   nsig = numSignal->getVal();
   nErr = numSignal->getError();
   e = 1-eff->getVal();
   eErr = eff->getError();
   corr = fitResult->correlation(*eff, *numSignal);
   err = ErrorInProduct(nsig, nErr, e, eErr, corr);
   sprintf(filename, "N_{s} = %.2f #pm %.2f", nSigFail->getVal(), err);
   l.DrawLatex(0.6,0.8,filename);
   sprintf(filename, "N_{b} = %.2f #pm %.2f", nBkgFail->getVal(), nBkgFail->getError());
   l.DrawLatex(0.6,0.75,filename);
   sprintf(filename, "#epsilon^{Data}_{s} = %3.3f #pm %3.3f", eff->getVal(), eff->getError());
   //l.DrawLatex(0.65,0.6,filename);
   sprintf(filename, "#epsilon^{MC}_{s} = %3.3f", effTP_MC);
   //l.DrawLatex(0.6,0.5,filename);

   sprintf(filename,"resTP/hhu_probefail_%s.pdf",failHistName);
   can1->Print(filename);
   sprintf(filename,"resTP/hhu_probefail_%s.gif",failHistName);
   can1->Print(filename);


   cout<<"effMC: "<< effTP_MC <<" +/- " <<effTP_MCerr <<endl;
   cout<<"eff: "<< eff->getVal() <<" +/- " << eff->getError() <<endl;

   cout<<"ndataPeakFail " << ndataFailPeak <<endl;

}
