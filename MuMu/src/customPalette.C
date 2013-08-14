/**
 * Define custom color palette for 3D plots.
 * Usage: root -l customPalette.C
 * Jan Veverka, Caltech, 5 December 2012
 */

#include "TCanvas.h"
#include "TColor.h"
#include "TH2F.h"
#include "TMath.h"
#include "TRandom.h"
#include "TROOT.h"
#include "TSeqCollection.h"
#include "TStyle.h"
#include "TString.h"

/// Declare functions
void customPalette();
TCanvas* makeCanvas(TH2F* hist, const char* name=0, const char* title=0);
TH2F* makeHistogram();
void setCustomPalette();
void saveAllCanvases(const char *ext = "png");


/**____________________________________________________________________________
 * Main entry point for execution.
 */
void 
customPalette() {
  gROOT->SetStyle("Plain");
  gStyle->SetPadRightMargin(0.15);
  
  /// Grab an example histo for demonstration
  TH2F *hist = makeHistogram();

  /// Default palettes, see
  /// http://root.cern.ch/root/html/TColor.html#TColor:SetPalette
  // int paletteCodes[] = {1, 51, 52, 53, 54, 55};
  /// Only these two default palette codes seem to lead to distinct settings.
  int paletteCodes[] = {1, 51};
  int numPalettes = sizeof(paletteCodes) / sizeof(int);
  
  /// Draw the default palettes
  for (int i=0; i < numPalettes; ++i) {
    int palette = paletteCodes[i];
    gStyle->SetPalette(palette);
    makeCanvas(hist, Form("Default_Palette_%d", palette))->Draw();
  }

  /// Draw the custom palette
  setCustomPalette();
  makeCanvas(hist, "Custom_Palette")->Draw();
  
  saveAllCanvases();
} // customPalette()


/**____________________________________________________________________________
 * Makes the canvas with the plot.
 */
TCanvas*
makeCanvas(TH2F * hist, const char *name, const char *title) {
  if (!title) {
    title = name;
  }
  
  TCanvas *canvas = new TCanvas(name, title, 1200, 400);
  canvas->Divide(2,1);
  
  hist->SetStats(kFALSE);

  canvas->cd(1);
  hist->SetTitle("COLZ Option");
  hist->DrawCopy("colz");
  
  canvas->cd(2);
  hist->SetTitle("SURF1 Option");
  hist->DrawCopy("surf1");

  return canvas;
} // makeCanvas()


/**____________________________________________________________________________
 * Makes a 2D histogram of a bivariate Gaussian density
 */
TH2F*
makeHistogram() {
  TH2F *hist = new TH2F("Test", "Test;x;y", 20, -3, 3, 20, -3, 3);
  /// Correlation coefficient, see
  /// http://www.sitmo.com/article/generating-correlated-random-numbers/
  double rho = 0.3;
  /// Fill the histogram
  for (int i=0; i<100000; ++i) {
    double x1 = gRandom->Gaus(0, 1);
    double x2 = gRandom->Gaus(0, 1);
    double y = rho * x1 + TMath::Sqrt(1 - rho * rho) * x2;
    hist->Fill(x1, y);
  }
  return hist;
} // makeHistogram()


/**____________________________________________________________________________
 * Set the custom palette.
 */
void
setCustomPalette() {
  const Int_t NRGBs = 5;
  const Int_t NCont = 99; //255

  Double_t stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
  Double_t red[NRGBs]   = { 0.00, 0.00, 0.87, 1.00, 0.51 };
  Double_t green[NRGBs] = { 0.00, 0.81, 1.00, 0.20, 0.00 };
  Double_t blue[NRGBs]  = { 0.51, 1.00, 0.12, 0.00, 0.00 };
  TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
  gStyle->SetNumberContours(NCont);
} // customPalette()


/**____________________________________________________________________________
 * Save all canvases as graphic files with the given extension.
 */
void 
saveAllCanvases(const char *ext) {
  TSeqCollection* canvases = gROOT->GetListOfCanvases();
  for (int i = 0; i < canvases->GetSize(); ++i) {
    TCanvas *canvas = (TCanvas*) canvases->At(i);
    canvas->Print(Form("%s.%s", canvas->GetName(), ext));
  }
} // saveAllCanvases()
