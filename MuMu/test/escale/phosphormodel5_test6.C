/*******************************************************************************
 * Test norm value caching in CINT for the PHOSPHOR pdf loaded 
 * from a workspace.
 * Jan Veverka, Caltech, 9 February 2012
 ******************************************************************************/

// void phosphormodel5_test6() {
{
  const char *filename = "phosphor5_model_and_fit_EB_highR9_pt15to20.root";
  TFile file1(filename);
  RooWorkspace *w = (RooWorkspace*) file1.Get("w");
  RooHistPdf *sm = (RooHistPdf*) w->pdf("EB_highR9_pt15to20_signal_model");
  RooWorkspace w2("w2");
  w2.import(*sm);
  w2.Print();
  sm->setNormValueCaching(1);
  RooArgSet oset(*w->var("mmgMass"));
  sm->getVal(&oset);

  RooHistPdf *sm2 = (RooHistPdf*) w2.pdf("EB_highR9_pt15to20_signal_model");
  sm2->getVal(&oset);
  w2.Print();
  }
