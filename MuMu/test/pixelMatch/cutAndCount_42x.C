/*
 * Global Definitions
 */

struct Config {
  enum Host {t3_susy, JansMacBookPro} host;
  enum Analysis {k30Nov2011ReReco, k16Jan2012ReReco} analysis;
  enum Veto {kMvaVeto, kCiCVeto, kPixelMatch, kR9, kCorrR9} veto;
  TFile * outputFile;
  enum Period {k2011AplusB, k2011A, k2011B} period;
  enum Subdetector {EcalBarrel, EcalEndcaps} subdetector;
  enum R9Category {LowR9=0, HighR9, AllR9} r9Category;
  enum EtaCategory {
    Eta1of4=0, Eta2of4, Eta3of4, Eta4of4, 
    Eta1of6, Eta2of6, Eta3of6, Eta4of6, Eta5of6, Eta6of6                    
  } etaCategory;
  enum PtBin {kPt10to12=0, kPt12to15, kPt15to20, kPt20up} ptBin;
  bool do4EtaCategories;
  bool do6EtaCategories;
  bool doR9Categories;
  bool doPtBins;
};

string calculateEfficiencies(const Config &);
string loopOverPeriods(Config &);
string loopOverCategories(Config &);
string loopOverPtBins(Config &);
string latexHeader(Config const&);
string latexFooter(Config const&);

///____________________________________________________________________________
void cutAndCount_42x(){  
  gROOT->LoadMacro("../resolutionErrors.C");
  
  /// Common configuration
  Config cfg;
  cfg.host        = Config::t3_susy;
  // cfg.host       = Config::JansMacBookPro;
  
  cfg.analysis   = Config::k16Jan2012ReReco;
  // cfg.analysis   = Config::k30Nov2011ReReco;
  
  // cfg.veto       = Config::kMvaVeto;
  // cfg.veto       = Config::kPixelMatch;
  // cfg.veto       = Config::kCiCVeto;
  // cfg.veto       = Config::kR9;  
  cfg.veto       = Config::kCorrR9;  
  
  // cfg.doEtaCategories = true;
  // cfg.doR9Categories = true;

  cfg.outputFile = new TFile("cutAndCount_42x_devel.root", "RECREATE");
  cfg.do4EtaCategories = false;
  cfg.do6EtaCategories = false;
  cfg.doR9Categories = false;
  cfg.doPtBins = true;

  cfg.r9Category = Config::AllR9;

  string latex = "";  

  latex += latexHeader(cfg);
  latex += loopOverPeriods(cfg);  
  latex += latexFooter(cfg);

  cout << latex << endl;
} // cutAndCount_42x()


///____________________________________________________________________________
string latexHeader(Config const & cfg) {
  
  string caption;
  
  switch(cfg.veto) {
  case Config::kPixelMatch:
    caption = "Pixel match veto ";
    break;
  case Config::kCiCVeto: 
    caption = "CiC photon ID electron rejection cut "; 
    break;
  case Config::kMvaVeto:
    caption = "MVA photon ID electron rejection cut ";
    break;
  case Config::kR9:
    caption = "High R9 categorization cut ";
    break;
  case Config::kCorrR9:
    caption = "Corrected high R9 categorization cut ";
    break;
  }
  
  caption += "efficiency\n";
  caption += "         for photons in ";

  if (cfg.do4EtaCategories == true && cfg.doR9Categories == true)  {
    caption += "eight different $|eta|\\times R_9$ ";
  } else if (cfg.do4EtaCategories == true && cfg.doR9Categories == false) {
    caption += "four different $|\\eta|$";
  } else if (cfg.do4EtaCategories == false && cfg.doR9Categories == true) {
    caption += "four different subdetector $\\times R_9$";
  } else if (cfg.do6EtaCategories == true){
    caption += "six different $|\\eta|$";
  } else {
    caption += "two different subdetector categories\n";
  }

  caption += " categories\n";
  caption += "         measured for the ";

  switch (cfg.analysis) {
  case Config::k30Nov2011ReReco:
    caption += "30-Nov-2011 re-reco dataset.";
    break;
  case Config::k16Jan2012ReReco:
    caption += "16-Jan-2012 re-reco dataset.";
    break;
  }

  string latex = ("\\begin{table}[htbp]\n"
		  "\\caption{");
  latex += caption;
  latex += ("}\n"
	    "\\begin{center}\n"
	    "\\begin{tabular}{c|c|c|c}\n"
	    "\\hline\n"
	    "\\hline\n"
	    "Category &\n"
	    "    $\\epsilon_{data}$ (\\%) &\n"
	    "        $\\epsilon_{MC}$ (\\%) &\n"
	    "            $\\epsilon_{data}$/$\\epsilon_{MC}$ \\\\\n");
  return latex;
} // latexHeader(..)


///____________________________________________________________________________
string latexFooter(Config const & cfg) {
  string label = "CutAndCount";

  switch(cfg.veto) {
  case Config::kPixelMatch: label += "_PMV"    ; break;
  case Config::kCiCVeto   : label += "_CiCVeto"; break;  
  case Config::kMvaVeto   : label += "_MVAVeto"; break;
  case Config::kR9        : label += "_R9"     ; break;
  case Config::kCorrR9    : label += "_CorrR9" ; break;
  }
  
  switch (cfg.analysis) {
  case Config::k30Nov2011ReReco: label += "_30Nov2011ReReco"; break;
  case Config::k16Jan2012ReReco: label += "_16Jan2012ReReco"; break;
  }

  if (cfg.do4EtaCategories == true) {
    label += "_4EtaCategories";
  }

  if (cfg.do6EtaCategories == true) {
    label += "_6EtaCategories";
  }

  
  // if (cfg.doR9Categories == true) {
  //   label += "_R9Categories";
  // }

  string latex = ("\\hline\n"
		  "\\hline\n"
		  "\\end{tabular}\n"
		  "\\end{center}\n"
		  "\\label{tab:");

  latex += label;

  latex += ("}\n"
	    "\\end{table}\n");

  return latex;
} // latexFooter(..)


///____________________________________________________________________________
string loopOverPeriods(Config &cfg) {
  string latex = "";
  
  latex += ("\\hline\n"
	    "\\multicolumn{4}{|c|}{2011 - all}\\\\\n"
	    "\\hline\n");
  cfg.period = Config::k2011AplusB;
  latex += loopOverCategories(cfg);

  latex += ("\\hline\n"
  	    "\\multicolumn{4}{|c|}{2011A}\\\\\n"
  	    "\\hline\n");
  cfg.period = Config::k2011A;
  latex += loopOverCategories(cfg);
  
  latex += ("\\hline\n"
  	    "\\multicolumn{4}{|c|}{2011B}\\\\\n"
  	    "\\hline\n");
  cfg.period = Config::k2011B;
  latex += loopOverCategories(cfg);

  return latex;
} // loopOverPeriods(..)
  

///____________________________________________________________________________
string loopOverCategories(Config& cfg) {  

  if (cfg.do4EtaCategories == true && cfg.doR9Categories == true) {
    return loopOverEtaR9Categories(cfg);
  }

  if (cfg.do4EtaCategories == true && cfg.doR9Categories == false) {
    cfg.r9Category  = Config::AllR9;
    return loopOver4EtaCategories(cfg);
  }
  
  if (cfg.do6EtaCategories == true) {
    cfg.r9Category  = Config::AllR9;
    return loopOver6EtaCategories(cfg);
  }

  if (cfg.veto == Config::kR9 || cfg.veto == Config::kCorrR9) {
    cfg.r9Category = Config::AllR9;
    return loopOverPtBins(cfg);
  }
  
  
  string row = "";
  string latex = "";
    
  /// Category 1/5
  cfg.subdetector = Config::EcalBarrel;
  cfg.r9Category  = Config::HighR9;
  row = calculateEfficiencies(cfg);
  switch(cfg.veto) {
  case Config::kCiCVeto:    latex += " 1 & "; break;
  case Config::kMvaVeto:    latex += " 5 & "; break;
  case Config::kPixelMatch: latex += "  1 & "; break;
  }
  latex += row + " \\\\\n";
  
  /// Category 2/6
  cfg.subdetector = Config::EcalBarrel;
  cfg.r9Category = Config::LowR9;
  row = calculateEfficiencies(cfg);
  switch(cfg.veto) {
  case Config::kCiCVeto:    latex += " 2 & "; break;
  case Config::kMvaVeto:    latex += " 6 & "; break;
  case Config::kPixelMatch: latex += "  2 & "; break;
  }
  latex += row + " \\\\\n";
  
  /// Category 3/7/9
  cfg.subdetector = Config::EcalEndcaps;
  cfg.r9Category = Config::HighR9;
  row = calculateEfficiencies(cfg);
  switch(cfg.veto) {
  case Config::kCiCVeto:    latex += " 3 & "; break;
  case Config::kMvaVeto:    latex += " 7 & "; break;
  case Config::kPixelMatch: latex += "  9 & "; break;
  }
  latex += row + " \\\\\n";

  /// Category 4/8/10
  cfg.subdetector = Config::EcalEndcaps;
  cfg.r9Category = Config::LowR9;
  row = calculateEfficiencies(cfg);
  switch(cfg.veto) {
  case Config::kCiCVeto:    latex += " 4 & "; break;
  case Config::kMvaVeto:    latex += " 8 & "; break;
  case Config::kPixelMatch: latex += " 10 & "; break;
  }
  latex += row + " \\\\\n";
  
  return latex;
} // loopOverCategories(..)


///____________________________________________________________________________
string loopOver4EtaCategories(Config& cfg) {  
  string row = "";
  string latex = "";
    
  /// Category 11
  cfg.subdetector = Config::EcalBarrel;  
  cfg.etaCategory = Config::Eta1of4;
  row = calculateEfficiencies(cfg);
  latex += " 11 &" + row + " \\\\\n";
  
  /// Category 12
  cfg.subdetector = Config::EcalBarrel;  
  cfg.etaCategory = Config::Eta2of4;
  row = calculateEfficiencies(cfg);
  latex += " 12 &" + row + " \\\\\n";
  
  /// Category 13
  cfg.subdetector = Config::EcalEndcaps;  
  cfg.etaCategory = Config::Eta3of4;
  row = calculateEfficiencies(cfg);
  latex += " 13 &" + row + " \\\\\n";
  
  /// Category 14
  cfg.subdetector = Config::EcalEndcaps;  
  cfg.etaCategory = Config::Eta4of4;
  row = calculateEfficiencies(cfg);
  latex += " 14 &" + row + " \\\\\n";

  return latex;
} // loopOverEtaCategories(..)


///____________________________________________________________________________
string loopOver6EtaCategories(Config& cfg) {  
  string row = "";
  string latex = "";
    
  for (unsigned cat = Config::Eta1of6; cat <= Config::Eta6of6; ++cat) {    
    /// Categories 23-28
    if (cat <= Config::Eta4of6)
      cfg.subdetector = Config::EcalBarrel;
    else
      cfg.subdetector = Config::EcalEndcaps;
    cfg.etaCategory = cat;
    row = calculateEfficiencies(cfg);
    unsigned catNumber = cat + 23 - Config::Eta1of6;
    cout << row << endl;
    string rowWithCatNumber = Form(" %u & %s \\\\\n", catNumber, row.c_str());
    cout << rowWithCatNumber << endl;
    latex += rowWithCatNumber;
  }

  return latex;
} // loopOver6EtaCategories(..)


///____________________________________________________________________________
string loopOverEtaR9Categories(Config& cfg) {  
  string row = "";
  string latex = "";
    
  /// Category 15
  cfg.subdetector = Config::EcalBarrel;  
  cfg.etaCategory = Config::Eta1of4;
  cfg.r9Category  = Config::HighR9;
  row = calculateEfficiencies(cfg);
  latex += " 15 &" + row + " \\\\\n";
  
  /// Category 16
  cfg.subdetector = Config::EcalBarrel;  
  cfg.etaCategory = Config::Eta1of4;
  cfg.r9Category  = Config::LowR9;
  row = calculateEfficiencies(cfg);
  latex += " 16 &" + row + " \\\\\n";
  
  /// Category 17
  cfg.subdetector = Config::EcalBarrel;  
  cfg.etaCategory = Config::Eta2of4;
  cfg.r9Category  = Config::HighR9;
  row = calculateEfficiencies(cfg);
  latex += " 17 &" + row + " \\\\\n";
  
  /// Category 18
  cfg.subdetector = Config::EcalBarrel;  
  cfg.etaCategory = Config::Eta2of4;
  cfg.r9Category  = Config::LowR9;
  row = calculateEfficiencies(cfg);
  latex += " 18 &" + row + " \\\\\n";
  
  /// Category 19
  cfg.subdetector = Config::EcalEndcaps;  
  cfg.etaCategory = Config::Eta3of4;
  cfg.r9Category  = Config::HighR9;
  row = calculateEfficiencies(cfg);
  latex += " 19 &" + row + " \\\\\n";
  
  /// Category 20
  cfg.subdetector = Config::EcalEndcaps;  
  cfg.etaCategory = Config::Eta3of4;
  cfg.r9Category  = Config::LowR9;
  row = calculateEfficiencies(cfg);
  latex += " 20 &" + row + " \\\\\n";
  
  /// Category 21
  cfg.subdetector = Config::EcalEndcaps;  
  cfg.etaCategory = Config::Eta4of4;
  cfg.r9Category  = Config::HighR9;
  row = calculateEfficiencies(cfg);
  latex += " 21 &" + row + " \\\\\n";
  
  /// Category 22
  cfg.subdetector = Config::EcalEndcaps;  
  cfg.etaCategory = Config::Eta4of4;
  cfg.r9Category  = Config::LowR9;
  row = calculateEfficiencies(cfg);
  latex += " 22 &" + row + " \\\\\n";
    
  return latex;
} // loopOverEtaR9Categories(..)

///____________________________________________________________________________
string loopOverPtBins(Config& cfg) {  
  string row = "";
  string latex = "";
    
  cfg.subdetector = Config::EcalBarrel;
  for (unsigned ptBin = Config::kPt10to12; ptBin <= Config::kPt20up; ++ptBin) {
    cfg.ptBin = ptBin;
    row = calculateEfficiencies(cfg);
    unsigned catNumber = 29 + ptBin;
    cout << row << endl;
    string rowWithCatNumber = Form(" %u & %s \\\\\n", catNumber, row.c_str());
    cout << rowWithCatNumber << endl;
    latex += rowWithCatNumber;
  }
  return latex;
} // loopOverPtBins(..)



///____________________________________________________________________________
string calculateEfficiencies(const Config &cfg)
{ 
  
  switch (cfg.host) {
    case Config::t3_susy:
      const char *path = "/mnt/hadoop/user/veverka/pmvTrees/";
      break;
    case Config::JansMacBookPro:
      const char *path = "/Users/veverka/Work/Data/pmvTrees/";
      break;
  }

  // const char *filenameData = "pixelMatch_data_Nov4ReReco_v4.dat";
  // const char *filenameMC   = "pixelMatch_Powheg_Fall10_v4.dat";

  

  /**
      'data' : [ 'pmvTree_V9_Run2010B-ZMu-Apr21ReReco-v1.root',
		'pmvTree_V9_ZMu-May10ReReco-42X-v3.root',
		'pmvTree_V9_PromptReco-v4_FNAL_42X-v3.root', ],
      'z'    : [ 'pmvTree_V9_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
      'qcd'  : [ 'pmvTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V6.root' ],
      'w'    : [ 'pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V6.root' ],
      'tt'   : [ 'pmvTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V6.root' ],
  */

  // const char *filenameData = "pmvTree_V9_ZMu-May10ReReco_plus_PromptReco-v4-42X-v3.root";
  // const char *filenameMC   = "pmvTree_V9_DYToMuMu_pythia6_v2_RECO-42X-v4.root";
  // const char *filenameQCD  = "pmvTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V6.root";
  // const char *filenameW    = "pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V6.root";
  // const char *filenameTT   = "pmvTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V6.root";

  // 2011A+B
  // const char *filenameData = "pmvTree_V15_05Jul2011ReReco_05Aug2011_03Oct2011-v1_PromptReco-v1B.root";
  // 2011A
  // const char *filenameData = "pmvTree_V15_05Jul2011ReReco_05Aug2011_03Oct2011-v1.root";
  // 2011B
  // const char *filenameData = "pmvTree_V15_DoubleMu_Run2011B-PromptReco-v1_condor_Dimuon_AOD-42X-v9.root";
  // 2011A+B PU weights
  // const char *filenameMC   = "pmvTree_V15_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9.root";
  // 2011A PU weights
  // const char *filenameMC   = "pmvTree_V16_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9.root";
  // 2011B PU weights
  // const char *filenameMC   = "pmvTree_V17_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9.root";
  // const char *filenameQCD  = "pmvTree_V15_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_S4-v1_condor_Dimuon_AOD-42X-v9.root";
  // const char *filenameW    = "pmvTree_V15_WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_Summer11-PU_S4_START42_V11-v1_condor_Dimuon_AOD-42X-v9.root";
  // const char *filenameTT   = "pmvTree_V15_TTJets_TuneZ2_7TeV-madgraph-tauola_S4-v2_condor_Dimuon_AOD-42X-v9.root";

  /// Build the label specific to the analysis and period.
  string label = "";

  switch (cfg.veto) {
  case Config::kMvaVeto:    label = "MVAVeto"; break;
  case Config::kCiCVeto:    label = "CiCVeto"; break;
  case Config::kPixelMatch: label = "PMVeto" ; break;
  case Config::kR9:         label = "R9"     ; break;
  }

  switch (cfg.analysis) {
  case Config::k30Nov2011ReReco: label += "_k30Nov2011ReReco"; break;
  case Config::k16Jan2012ReReco: label += "_k16Jan2012ReReco"; break;
  }

  switch (cfg.period) {
  case Config::k2011AplusB: label += "_2011AplusB"; break;
  case Config::k2011A     : label += "_2011A"     ; break;
  case Config::k2011B     : label += "_2011B"     ; break;
  }

  /// Samples
  switch (cfg.period) {

  case Config::k2011AplusB:
    const char *filenameMC   = "pmvTree_V19_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root";
    const char *filenameQCD  = "pmvTree_V19_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root";
    const char *filenameTT   = "pmvTree_V19_TT_TuneZ2_7TeV-powheg-tauola_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root";
    const char *filenameW    = "pmvTree_V19_WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root";

    switch (cfg.analysis) {
    case Config::k30Nov2011ReReco:
      // Datasets for AN 2012/048 Hgg MVA 2011A+B
      const char *filenameData = "pmvTree_V19_DoubleMu_Run2011AB-30Nov2011-v1_condor_Dimuon_AOD-42X-v10_DBS.root";
      break;

    case Config::k16Jan2012ReReco:
      // Datasets for reload 16 Jan 2011A+B
      const char *filenameData = "pmvTree_V21_DoubleMu_Run2011AB-16Jan2012-v1_condor_Dimuon_AOD-42X-v10.root";
      break;
    }
    break;
      
    // Datasets for 2011A
  case Config::k2011A:
    const char *filenameMC   = "pmvTree_V20_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root";
    const char *filenameQCD  = "pmvTree_V20_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root";
    const char *filenameTT   = "pmvTree_V20_TT_TuneZ2_7TeV-powheg-tauola_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root";
    const char *filenameW    = "pmvTree_V20_WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root";
    switch (cfg.analysis) {
    case Config::k30Nov2011ReReco:
      // Datasets for AN 2012/048 Hgg MVA 2011A
      const char *filenameData = "pmvTree_V19_DoubleMu_Run2011A-30Nov2011-v1_condor_Dimuon_AOD-42X-v10_DBS.root";
      break;

    case Config::k16Jan2012ReReco:
      // Datasets for reload 16 Jan 2011A
      const char *filenameData = "pmvTree_V21_DoubleMu_Run2011A-16Jan2012-v1_condor_Dimuon_AOD-42X-v10.root";
      break;
    }
    break;
      
    // Datasets for 2011B
  case Config::k2011B:
    const char *filenameMC   = "pmvTree_V21_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root";
    const char *filenameQCD  = "pmvTree_V21_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root";
    const char *filenameTT   = "pmvTree_V21_TT_TuneZ2_7TeV-powheg-tauola_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root";
    const char *filenameW    = "pmvTree_V21_WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb.root";

    switch (cfg.analysis) {
    case Config::k30Nov2011ReReco:
      // Datasets for AN 2012/048 Hgg MVA 2011B
      const char *filenameData = "pmvTree_V19_DoubleMu_Run2011B-30Nov2011-v1_condor_Dimuon_AOD-42X-v10_DBS.root";
      break;

    case Config::k16Jan2012ReReco:
      // Datasets for reload 16 Jan 2011B
      const char *filenameData = "pmvTree_V21_DoubleMu_Run2011B-16Jan2012-v1_condor_Dimuon_AOD-42X-v10.root";
      break;
    }
    break;
  }

  enum mcSample {z=0, qcd, w, tt};

  // Weights of V15 ntuples for 4.603 / fb
  // double weight[] = {
  //   0.2578237765992,  // Z
  //   15.5412157722089, // QCD
  //   1.77177343641992, // W
  //   0.20516095989489 // tt
  // };
  
  // Weights of V19-21 ntuples for 4.618 / fb
  double weight[] = {
    0.258663958360874,  // Z
    64.4429447069508, // QCD
    1.77770452633322, // W
    0.046348624723768 // tt
  };

  TFile dataFile(Form("%s%s", path, filenameData));
  TFile mcFile(Form("%s%s", path, filenameMC));
  TFile qcdFile(Form("%s%s", path, filenameQCD));
  TFile wFile(Form("%s%s", path, filenameW));
  TFile ttFile(Form("%s%s", path, filenameTT));
  
  /// Read data set
  TTree * tdata  = (TTree*) dataFile.Get("pmvTree/pmv");
  TTree * tmc    = (TTree*) mcFile.Get("pmvTree/pmv");
  TTree * tqcd   = (TTree*) qcdFile.Get("pmvTree/pmv");
  TTree * tw   = (TTree*) wFile.Get("pmvTree/pmv");
  TTree * ttt   = (TTree*) ttFile.Get("pmvTree/pmv");

  TCut drCut("minDeltaR < 1");
  // TCut phoTIsoCut("phoTrackIsoCorr < 2 + 0.001 * phoPt");
  // TCut phoEIsoCut("phoEcalIso < 4.2+0.006*phoPt");
  // TCut phoHIsoCut("phoHcalIso < 2.2+0.0025*phoPt");
  // TCut ebSihihCut("minDTheta<0.05|phoSigmaIetaIeta<0.013");
  TCut ebCut("abs(phoEta) < 1.5");
  TCut eeCut("abs(phoEta) > 1.5");
  TCut signalCut("isFSR");
  TCut backgroundCut("!isFSR");
  TCut mWindowCut("abs(mmgMass-90) < 15");
  TCut mWindowCutUp("abs(mmgMass-90) < 17.5");
  TCut mWindowCutDown("abs(mmgMass-90) < 12.5");
  TCut ubCut("(minDEta > 0.04 | minDPhi > 0.2)");
  TCut nVtx1to2("nVertices<=2");
  TCut phoPt5to10("5 <= phoPt & phoPt < 10");
  TCut phoPt10to20("10 <= phoPt & phoPt < 20");
  TCut phoPt20up("20 <= phoPt");
  TCut etaBin1of4("abs(scEta) < 0.9");
  TCut etaBin2of4("0.9 <= abs(scEta) & abs(scEta) < 1.5");
  TCut etaBin3of4("1.5 <= abs(scEta) & abs(scEta) < 2.1");
  TCut etaBin4of4("2.1 <= abs(scEta) & abs(scEta) < 2.5");
  TCut etaBin1of6("phoIsEB & abs(phoIEtaX) <= 25"); // module 1
  TCut etaBin2of6("phoIsEB & 25 < abs(phoIEtaX) & abs(phoIEtaX) <= 45"); // module 2
  TCut etaBin3of6("phoIsEB & 45 < abs(phoIEtaX) & abs(phoIEtaX) <= 65"); // module 3
  TCut etaBin4of6("phoIsEB & 65 < abs(phoIEtaX) & abs(phoIEtaX) <= 85"); // module 4
  TCut etaBin5of6("!phoIsEB & 1.5 <= abs(scEta) & abs(scEta) < 2.0");
  TCut etaBin6of6("!phoIsEB & 2.0 <= abs(scEta) & abs(scEta) < 2.5");
  TCut pt10to12("10 <= phoPt & phoPt < 12");
  TCut pt12to15("12 <= phoPt & phoPt < 15");
  TCut pt15to20("15 <= phoPt & phoPt < 20");
  TCut pt20up("20 <= phoPt");
  
  TCut vetoCut, ebLowR9, eeLowR9, ebHighR9, eeHighR9, ebSelection, eeSelection;
  TCut vetoCutData, vetoCutEBMC, vetoCutEEMC;
  switch (cfg.veto) {
  case Config::kMvaVeto:
    vetoCut = "phoPassElectronVeto";
    // TCut highR9("0.9 < phoR9");
    ebLowR9 = "0 < phoR9 && phoR9 <= 0.9";
    eeLowR9 = "0 < phoR9 && phoR9 <= 0.9";
    // TCut ebLowR9MC("0 < phoR9 && phoR9 <= 0.9");
    // TCut eeLowR9MC("0 < phoR9 && phoR9 <= 0.9");
    ebHighR9 = "0.9 < phoR9";
    eeHighR9 = "0.9 < phoR9";
    // These near muon veto cuts are for the "delta R to nearest track" electron veto
    ebSelection = "(minDEta > 0.04 | minDPhi > 0.1) & phoIsEB";
    eeSelection = "(minDEta > 0.04 | minDPhi > 0.2) & !phoIsEB";
    break;
  case Config::kCiCVeto:
    vetoCut = "phoDeltaRToTrack > 1";
    if (cfg.subdetector == Config::EcalBarrel &&
        cfg.r9Category == Config::LowR9) {
      vetoCut = "phoDeltaRToTrack > 0.062"; //eb low R9
    }
    ebLowR9 = ("phoR9 <= 0.94");
    eeLowR9 = ("phoR9 <= 0.94");
    ebHighR9 = ("phoR9 > 0.94");
    eeHighR9 = ("phoR9 > 0.94");
    // These near muon veto cuts are for the "delta R to nearest track" electron veto
    ebSelection = ("(minDEta > 0.04 | minDPhi > 0.1) & phoIsEB");
    eeSelection = ("(minDEta > 0.04 | minDPhi > 0.2) & !phoIsEB");
    break;   
  case Config::kPixelMatch:
    vetoCut = "!phoHasPixelMatch";
    ebLowR9 = ("phoR9 <= 0.94");
    eeLowR9 = ("phoR9 <= 0.95");
    ebHighR9 = ("phoR9 > 0.94");
    eeHighR9 = ("phoR9 > 0.95");
    // These cuts are for the pixel match veto
    ebSelection = ("(minDEta > 0.04 | minDPhi > 0.3) & phoIsEB");
    eeSelection = ("(minDEta > 0.08 | minDPhi > 0.3) & !phoIsEB");
    break;   
  case Config::kR9:
    vetoCut = "phoR9 > 0.94";
    ebLowR9 = ("phoR9 <= 0.94");
    eeLowR9 = ("phoR9 <= 0.95");
    ebHighR9 = ("phoR9 > 0.94");
    eeHighR9 = ("phoR9 > 0.95");
    // These cuts are for the pixel match veto
    ebSelection = ("phoIsEB");
    eeSelection = ("!phoIsEB");
    break;   
  case Config::kCorrR9:
    // HtoZg correction for barrel in 2011
    // See https://twiki.cern.ch/twiki/bin/view/CMS/HtoZgPhotonID
    vetoCutData = "phoR9 > 0.94";
    vetoCutEBMC   = "1.0048 * phoR9 > 0.94";
    vetoCutEEMC   = "1.00492 * phoR9 > 0.94";
    ebLowR9 = ("1.0048 * phoR9 <= 0.94");
    eeLowR9 = ("1.00492 * phoR9 <= 0.95");
    ebHighR9 = ("1.0048 * phoR9 > 0.94");
    eeHighR9 = ("1.00492 * phoR9 > 0.95");
    // These cuts are for the pixel match veto
    ebSelection = ("phoIsEB");
    eeSelection = ("!phoIsEB");
    break;   
  }

  TCut run2011A("id.run < 175860");
  TCut run2011B("id.run >= 175860");

  TCut selection("mmMass < 80 & phoPt > 10 & scEt > 10 & phoHoE < 0.5");
  selection = selection && mWindowCut;
  
  switch (cfg.subdetector) {
    case Config::EcalBarrel :
      label += "_EB";
      selection = selection && ebSelection;
      switch (cfg.r9Category) {
        case Config::LowR9 : selection = selection && ebLowR9 ; break;
        case Config::HighR9: selection = selection && ebHighR9; break;
      }
      break;
    case Config::EcalEndcaps: 
      label += "_EE"; 
      selection = selection && eeSelection;
      switch (cfg.r9Category) {
        case Config::LowR9 : selection = selection && eeLowR9 ; break;
        case Config::HighR9: selection = selection && eeHighR9; break;
      }
      break;
  }
  
  if (cfg.do4EtaCategories || cfg.do6EtaCategories) {
    switch (cfg.etaCategory) {
    case Config::Eta1of4 :
      selection = selection && etaBin1of4;
      label += "_eta1of4";
      break;
    case Config::Eta2of4 :
      selection = selection && etaBin2of4;
      label += "_eta2of4";
      break;
    case Config::Eta3of4 :
      selection = selection && etaBin3of4;
      label += "_eta3of4";
      break;
    case Config::Eta4of4 :
      selection = selection && etaBin4of4;
      label += "_eta4of4";
      break;
    case Config::Eta1of6 :
      selection = selection && etaBin1of6;
      label += "_eta1of6";
      break;
    case Config::Eta2of6 :
      selection = selection && etaBin2of6;
      label += "_eta2of6";
      break;
    case Config::Eta3of6 :
      selection = selection && etaBin3of6;
      label += "_eta3of6";
      break;
    case Config::Eta4of6 :
      selection = selection && etaBin4of6;
      label += "_eta4of6";
      break;
    case Config::Eta5of6 :
      selection = selection && etaBin5of6;
      label += "_eta5of6";
      break;
    case Config::Eta6of6 :
      selection = selection && etaBin6of6;
      label += "_eta6of6";
      break;
    } // switch over eta categories
  }

  switch (cfg.r9Category) {
    case Config::LowR9 : label += "_lowR9" ; break;
    case Config::HighR9: label += "_highR9"; break;
  }

  if (cfg.doPtBins) {
    switch (cfg.ptBin) {
    case Config::kPt10to12 : 
      selection = selection && pt10to12; 
      label += "_pt10to12" ; 
      break;
    case Config::kPt12to15 : 
      selection = selection && pt12to15; 
      label += "_pt12to15" ; 
      break;
    case Config::kPt15to20 : 
      selection = selection && pt15to20; 
      label += "_pt15to20" ; 
      break;
    case Config::kPt20up : 
      selection = selection && pt20up; 
      label += "_pt20up" ; 
      break;
    }
  }
  // TCut selection = ebSelection;
  // TCut selection = eeSelection;
  // TCut selection = ebSelection && highR9;
  // TCut selection = ebSelection && ebHighR9;
  // TCut selection = ebSelection && ebLowR9;
  // TCut selection = eeSelection && highR9;
  // TCut selection = eeSelection && eeHighR9;
  // TCut selection = eeSelection && eeLowR9;
  // TCut selection = ebSelection && nVtx1to2;
  // TCut selection = ebSelection && !nVtx1to2;
  // TCut selection = ebSelection && phoPt5to10;
  // TCut selection = ebSelection && phoPt10to20;
  // TCut selection = ebSelection && phoPt20up;

  // TCut run2011X = run2011A;
  // TCut selection = ebSelection && ebHighR9 && run2011X;
  // TCut selection = ebSelection && ebLowR9 && run2011X;
  // TCut selection = eeSelection && eeHighR9 && run2011X;
  // TCut selection = eeSelection && eeLowR9 && run2011X;

  TDirectory *outputDir = cfg.outputFile->mkdir(label.c_str());
  outputDir->cd();

  // gStyle->SetPadLeftMargin(1.3);
  string name = Form("m3_%s", label.c_str());
  TCanvas * c1 = new TCanvas(name.c_str(), name.c_str(), 20, 20, 800, 400);
  c1->Divide(2,1);
  c1->cd(1);

  // Automatically calculate the sum of squares of weights
  // since we deal with weighed histograms.
  TH1::SetDefaultSumw2();

  // Scale all MC such that z has event weight 1 to maintain it's statistical error

  // // Barrel MC, passing probes
  // double p_mc = tmc->Draw("mmgMass>>hp_mc(30,75,105)",
  //                         Form("pileup.weight * %f * (%s)",
  //                              weight[z],
  //                              (selection && vetoCut).GetTitle()
  //                             )
  //                         );
  // double pb_mc = tmc->Draw("mmgMass>>hpb_mc(30,75,105)",
  //                          Form("pileup.weight * %f * (%s)",
  //                               weight[z],
  //                               (selection && vetoCut && backgroundCut).GetTitle()
  //                              )
  //                         );
  // double pb_qcd = tqcd->Draw("mmgMass>>hpb_qcd(30,75,105)",
  //                            Form("pileup.weight * %f * (%s)",
  //                                  weight[qcd],
  //                                  (selection && vetoCut).GetTitle()
  //                                 )
  //                           );
  // double pb_w = tw->Draw("mmgMass>>hpb_w(30,75,105)",
  //                        Form("pileup.weight * %f * (%s)",
  //                              weight[w],
  //                              (selection && vetoCut).GetTitle()
  //                             )
  //                       );
  // double pb_tt = ttt->Draw("mmgMass>>hpb_tt(30,75,105)",
  //                          Form("pileup.weight * %f * (%s)",
  //                                weight[tt],
  //                                (selection && vetoCut).GetTitle()
  //                               )
  //                         );
  // double ps_mc = p_mc - pb_mc;
  // double eps_mc = sqrt(ps_mc);

  // // Barrel MC, failing probes
  // double f_mc = tmc->Draw("mmgMass>>hf_mc(6,75,105)",
  //                          Form("pileup.weight * %f * (%s)",
  //                               weight[z],
  //                               (selection && !vetoCut).GetTitle()
  //                              )
  //                         );
  // double fb_mc = tmc->Draw("mmgMass>>hfb_mc(6,75,105)",
  //                          Form("pileup.weight * %f * (%s)",
  //                                weight[z],
  //                                (selection && !vetoCut && backgroundCut).GetTitle()
  //                               )
  //                         );
  // double fb_qcd = tqcd->Draw("mmgMass>>hfb_qcd(6,75,105)",
  //                            Form("pileup.weight * %f * (%s)",
  //                                  weight[qcd],
  //                                  (selection && !vetoCut).GetTitle()
  //                                 )
  //                            );
  // double fb_w = tw->Draw("mmgMass>>hfb_w(6,75,105)",
  //                         Form("pileup.weight * %f * (%s)",
  //                               weight[w],
  //                               (selection && !vetoCut).GetTitle()
  //                              )
  //                        );
  // double fb_tt = ttt->Draw("mmgMass>>hfb_tt(6,75,105)",
  //                          Form("pileup.weight * %f * (%s)",
  //                                weight[tt],
  //                                (selection && !vetoCut).GetTitle()
  //                              )
  //                          );

  // double fs_mc = f_mc - fb_mc;
  // double efs_mc = sqrt(fs_mc);

  // // Barrel data
  // double p = tdata->Draw("mmgMass>>hp(30,75,105)", selection && vetoCut);
  // double f = tdata->Draw("mmgMass>>hf(6,75,105)", selection && !vetoCut);

  // double ps = ps_mc * p / (p_mc + pb_qcd + pb_w + pb_tt);
  // double fs = fs_mc * f / (f_mc + fb_qcd + fb_w + fb_tt);

  // double pb = p - ps;
  // double fb = f - fs;

  // double eps = Oplus(sqrt(p), pb + pb_qcd + pb_w + pb_tt); // 100 % error on bg
  // double efs = Oplus(sqrt(f), fb + pb_qcd + fb_w + fb_tt); // 100 % error on bg

  // Barrel MC, passing probes
  if (cfg.veto == Config::kCorrR9) {
    if (cfg.subdetector == Config::EcalBarrel) vetoCut = vetoCutEBMC;
    else                                       vetoCut = vetoCutEEMC;
  }
  double p_mc = tmc->Draw("mmgMass>>hp_mc(30,75,105)",
			  Form("pileup.weight * %f * (%s)",
			      weight[z],
			      (selection && vetoCut).GetTitle()
			      )
			  );
  double pb_mc = tmc->Draw("mmgMass>>hpb_mc(30,75,105)",
			  Form("pileup.weight * %f * (%s)",
				weight[z],
				(selection && vetoCut && backgroundCut).GetTitle()
			      )
			  );
  double pb_qcd = tqcd->Draw("mmgMass>>hpb_qcd(30,75,105)",
			    Form("pileup.weight * %f * (%s)",
				  weight[qcd],
				  (selection && vetoCut).GetTitle()
				  )
			    );
  double pb_w = tw->Draw("mmgMass>>hpb_w(30,75,105)",
			Form("pileup.weight * %f * (%s)",
			      weight[w],
			      (selection && vetoCut).GetTitle()
			      )
			);
  double pb_tt = ttt->Draw("mmgMass>>hpb_tt(30,75,105)",
			  Form("pileup.weight * %f * (%s)",
				weight[tt],
				(selection && vetoCut).GetTitle()
				)
			  );

  // Barrel MC, failing probes
  double f_mc = tmc->Draw("mmgMass>>hf_mc(15,75,105)",
			  Form("pileup.weight * %f * (%s)",
				weight[z],
				(selection && !vetoCut).GetTitle()
			      )
			  );
  double fb_mc = tmc->Draw("mmgMass>>hfb_mc(15,75,105)",
			  Form("pileup.weight * %f * (%s)",
				weight[z],
				(selection && !vetoCut && backgroundCut).GetTitle()
				)
			  );
  double fb_qcd = tqcd->Draw("mmgMass>>hfb_qcd(15,75,105)",
			    Form("pileup.weight * %f * (%s)",
				  weight[qcd],
				  (selection && !vetoCut).GetTitle()
				  )
			    );
  double fb_w = tw->Draw("mmgMass>>hfb_w(15,75,105)",
			  Form("pileup.weight * %f * (%s)",
				weight[w],
				(selection && !vetoCut).GetTitle()
			      )
			);
  double fb_tt = ttt->Draw("mmgMass>>hfb_tt(15,75,105)",
			  Form("pileup.weight * %f * (%s)",
				weight[tt],
				(selection && !vetoCut).GetTitle()
			      )
			  );

  // Mean weights
  double wp_mc = tmc->Draw(Form("pileup.weight * %f >> hwp_mc", weight[z]),
			    (selection && vetoCut).GetTitle());
  double wf_mc = tmc->Draw(Form("pileup.weight * %f >> hwf_mc", weight[z]),
			    (selection && !vetoCut).GetTitle());


  // Barrel data
  if (cfg.veto == Config::kCorrR9) {
    vetoCut = vetoCutData;
  }
  
  double p = tdata->Draw("mmgMass>>hp(30,75,105)", selection && vetoCut);
  double f = tdata->Draw("mmgMass>>hf(15,75,105)", selection && !vetoCut);

  // Get the histograms
  TH1F *hp = (TH1F*) gDirectory->Get("hp");
  TH1F *hp_mc = (TH1F*) gDirectory->Get("hp_mc");
  TH1F *hpb_mc = (TH1F*) gDirectory->Get("hpb_mc");
  TH1F *hpb_qcd = (TH1F*) gDirectory->Get("hpb_qcd");
  TH1F *hpb_w = (TH1F*) gDirectory->Get("hpb_w");
  TH1F *hpb_tt = (TH1F*) gDirectory->Get("hpb_tt");

  TH1F *hf = (TH1F*) gDirectory->Get("hf");
  TH1F *hf_mc = (TH1F*) gDirectory->Get("hf_mc");
  TH1F *hfb_mc = (TH1F*) gDirectory->Get("hfb_mc");
  TH1F *hfb_qcd = (TH1F*) gDirectory->Get("hfb_qcd");
  TH1F *hfb_w = (TH1F*) gDirectory->Get("hfb_w");
  TH1F *hfb_tt = (TH1F*) gDirectory->Get("hfb_tt");

  TH1F *hwp_mc = (TH1F*) gDirectory->Get("hwp_mc");
  TH1F *hwf_mc = (TH1F*) gDirectory->Get("hwf_mc");

  // Check for illegal pointers to histograms
  if (!hp_mc) {
    hp_mc = (TH1F*) hp->Clone("hp_mc");
    hp_mc->Sumw2();
    hp_mc->Scale(0);
  }

  if (!hpb_mc) {
    hpb_mc = (TH1F*) hp->Clone("hpb_mc");
    hpb_mc->Sumw2();
    hpb_mc->Scale(0);
  }

  if (!hpb_qcd) {
    hpb_qcd = (TH1F*) hp->Clone("hpb_qcd");
    hpb_qcd->Sumw2();
    hpb_qcd->Scale(0);
  }

  if (!hfb_qcd) {
    hfb_qcd = (TH1F*) hf->Clone("hfb_qcd");
    hfb_qcd->Sumw2();
    hfb_qcd->Scale(0);
  }

  if (!hfb_w) {
    hfb_w = (TH1F*) hf->Clone("hfb_w");
    hfb_w->Sumw2();
    hfb_w->Scale(0);
  }

  if (!hfb_tt) {
    hfb_tt = (TH1F*) hf->Clone("hfb_tt");
    hfb_tt->Sumw2();
    hfb_tt->Scale(0);
  }

  // Set the numbers of passing/failing events to the number of events. 
  // Use weighted events form MC, applying the pileup and cross-section weights.
  p = hp->Integral(1, 30);
  p_mc = hp_mc->Integral(1, 30);
  pb_mc = hpb_mc->Integral(1, 30);
  pb_qcd = hpb_qcd->Integral(1, 30);
  pb_w = hpb_w->Integral(1, 30);
  pb_tt = hpb_tt->Integral(1, 30);

  f = hf->Integral(1, 15);
  f_mc = hf_mc->Integral(1, 15);
  fb_mc = hfb_mc->Integral(1, 15);
  fb_qcd = hfb_qcd->Integral(1, 15);
  fb_w = hfb_w->Integral(1, 15);
  fb_tt = hfb_tt->Integral(1, 15);

  // Scale the MC by the average weight of the most significant sample. 
  // This is a poor man's estimate of the statistical significances of the sample.
  wp_mc = hwp_mc->GetMean();
  wf_mc = hwf_mc->GetMean();

  p_mc   /= wp_mc;
  pb_mc  /= wp_mc;
  pb_qcd /= wp_mc;
  pb_tt  /= wp_mc;
  pb_w   /= wp_mc;

  f_mc   /= wp_mc;
  fb_mc  /= wp_mc;
  fb_qcd /= wp_mc;
  fb_tt  /= wp_mc;
  fb_w   /= wp_mc;

  double ps_mc = p_mc - pb_mc;
  double eps_mc = sqrt(ps_mc);

  double fs_mc = f_mc - fb_mc;
  double efs_mc = sqrt(fs_mc);

  double ps = ps_mc * p / (p_mc + pb_qcd + pb_w + pb_tt);
  double fs = fs_mc * f / (f_mc + fb_qcd + fb_w + fb_tt);
  
  double pb = p - ps;
  double fb = f - fs;

  double eps = Oplus(sqrt(p), pb + pb_qcd + pb_w + pb_tt); // 100 % error on bg
  double efs = Oplus(sqrt(f), fb + pb_qcd + fb_w + fb_tt); // 100 % error on bg


  // Calculate efficiency
  double eff = ps / (ps + fs);
  double eff_mc = ps_mc / (ps_mc + fs_mc);

  // Efficiency error
  if (fs < 1.e-5) {
      fs = 1.;
  }
  double eeff = eff*(1-eff)*Oplus(eps/ps, efs/fs);
  double eeff_mc = eff_mc*(1-eff_mc)*Oplus(eps_mc/ps_mc, efs_mc/fs_mc);

  cout << "== Normal approx. errors == " << endl;
  cout << "veto efficiency in MC: " << eff_mc << " +/- " << eeff_mc << endl;
  cout << "veto efficiency in data: " << eff << " +/- " << eeff << endl;

  /// CL 1-sigma/68% Bayesian with Beta(1,1) prior with mode of posterior
  /// to define the interval

  TH1F h_pass("h_pass", "number of passing signal probes", 2, 0, 2);
  TH1F h_total("h_total", "number of all signal probes", 2, 0, 2);

  h_pass .GetXaxis()->SetBinLabel(1, "data");
  h_total.GetXaxis()->SetBinLabel(1, "data");
  h_pass .GetXaxis()->SetBinLabel(2, "MC");
  h_total.GetXaxis()->SetBinLabel(2, "MC");

  h_pass.Fill("data", ps);
  h_pass.Fill("MC"  , ps_mc);
  h_total.Fill("data", ps + fs);
  h_total.Fill("MC"  , ps_mc + fs_mc);

  TEfficiency *g_eff = new TEfficiency("eff", "data;sample;#epsilon_{PMV}",
                                       2, 0.5, 2.5);

  // Hack to fill the efficiency for data
  for ( int i = 0; i < (int) (ps + fs); ++i ) {
    if ( i < (int) fs ) {
      g_eff->Fill(/*fail*/ 0, /*data*/ 1);
    } else {
      g_eff->Fill(/*pass*/ 1, /*data*/ 1);
    }
  }

  // Hack to fill the efficiency for MC
  for ( int i = 0; i < (int) (ps_mc + fs_mc); ++i ) {
    if ( i < (int) fs_mc ) {
      g_eff->Fill(/*fail*/ 0, /*MC*/ 2);
    } else {
      g_eff->Fill(/*pass*/ 1, /*MC*/ 2);
    }
  }

  // // Hack to draw the efficiency
  // g_eff->GetXaxis()->SetBinLabel(1, "data");
  // g_eff->GetXaxis()->SetBinLabel(2, "MC");
  // g_eff->BayesDivide(&h_pass, &h_total);

  // Add systematic error on data in quadrature
  // Assume systematic errors = 100% background
  double eeff_syst = eff*(1-eff)*Oplus(pb/ps, fb/fs);

  cout << "Veto: " << vetoCut.GetTitle() << endl;
  cout << "== Clopper-Pearson errors == " << endl;
  cout << "Veto efficiencies: Data (%) | MC (%) | data/MC" << endl;
  cout << "Selection: " << selection.GetTitle() << endl;

  /// Data
  printf ( "%.2f + %.2f - %.2f (stat.) +/- %.2f (syst.) | ",
	  100 * g_eff->GetEfficiency(1),
	  100 * g_eff->GetEfficiencyErrorUp(1),
	  100 * g_eff->GetEfficiencyErrorLow(1),
	  100 * eeff_syst );

  /// MC
  printf ( "%.2f + %.2f - %.2f (stat.) | ",
	  100 * g_eff->GetEfficiency(2),
	  100 * g_eff->GetEfficiencyErrorUp(2),
	  100 * g_eff->GetEfficiencyErrorLow(2) );

  /// data / MC
  printf ( "%.4f + %.4f - %.4f\n",
	  g_eff->GetEfficiency(1) / g_eff->GetEfficiency(2),
	  Oplus( g_eff->GetEfficiencyErrorUp(1),
		  g_eff->GetEfficiencyErrorUp(2),
		  eeff_syst ),
	  Oplus( g_eff->GetEfficiencyErrorLow(1),
		  g_eff->GetEfficiencyErrorLow(2),
		  eeff_syst ) );
  
  /// Latex
  char latex[1000];
  /// Data
  sprintf (latex, "%.2f$^{+%.2f}_{-%.2f}$ & ",
           100 * g_eff->GetEfficiency(1),
	   Oplus(100 * g_eff->GetEfficiencyErrorUp(1), 100 * eeff_syst),
	   Oplus(100 * g_eff->GetEfficiencyErrorLow(1), 100 * eeff_syst) );
  /// MC
  sprintf (latex, "%s%.2f$^{+%.2f}_{-%.2f}$ & ",
           latex,
	   100 * g_eff->GetEfficiency(2),
	   100 * g_eff->GetEfficiencyErrorUp(2),
	   100 * g_eff->GetEfficiencyErrorLow(2) );
  /// data / MC
  sprintf (latex, "%s%.4f$^{+%.4f}_{-%.4f}$",
           latex,
	   g_eff->GetEfficiency(1) / g_eff->GetEfficiency(2),
	   Oplus( g_eff->GetEfficiencyErrorUp(1),
		  g_eff->GetEfficiencyErrorUp(2),
		  eeff_syst ),
	   Oplus( g_eff->GetEfficiencyErrorLow(1),
		  g_eff->GetEfficiencyErrorLow(2),
		  eeff_syst ) );

  cout << latex << endl;

  // Draw passing probes TODO: ADD W and ttbar
  TH1F *hp = (TH1F*) gDirectory->Get("hp");
  TH1F *hp_mc = (TH1F*) gDirectory->Get("hp_mc");
  TH1F *hpb_mc = (TH1F*) gDirectory->Get("hpb_mc");
  TH1F *hpb_qcd = (TH1F*) gDirectory->Get("hpb_qcd");

  // This is black magic
  hp_mc->Add(hpb_qcd);
  hpb_mc->Add(hpb_qcd);

  double scaleFactor = hp->Integral() / hp_mc->Integral();
  scaleFactor *= hp->GetBinWidth(1) / hp_mc->GetBinWidth(1);
  hp_mc->Scale(scaleFactor);
  hpb_mc->Scale(scaleFactor);
  hpb_qcd->Scale(scaleFactor);

  hp_mc->SetLineColor(kAzure - 9);
  hp_mc->SetFillColor(kAzure - 9);
  hpb_mc->SetLineColor(kSpring + 5);
  hpb_mc->SetFillColor(kSpring + 5);
  hpb_qcd->SetLineColor(kYellow - 7); // kOrange-2, kRed-3
  hpb_qcd->SetFillColor(kYellow - 7);

  hp_mc->SetTitle("Passing Probes");
  hp_mc->GetXaxis()->SetTitle("m(#mu#mu#gamma) (GeV)");
  hp_mc->GetYaxis()->SetTitle("Entries / 1 GeV");
  hp_mc->GetYaxis()->SetTitleOffset(1.7);


  hp_mc->SetStats(0);
  hpb_mc->SetStats(0);
  hpb_qcd->SetStats(0);

  hp->SetMarkerStyle(20);

  double ymax = TMath::Max(
      hp->GetMaximum() + TMath::Sqrt(hp->GetMaximum()),
      hp_mc->GetMaximum()
  );

  hp_mc->GetYaxis()->SetRangeUser(0, 1.1*ymax);


  TPad * pad1 = (TPad*) c1->cd(1);
  pad1->SetLeftMargin(0.15);
  hp_mc->Draw("hist");
  hpb_mc->Draw("hist same");
  hpb_qcd->Draw("hist same");
  hp->Draw("e0same");
  c1->cd(1)->RedrawAxis();


  // Draw failing probes
  TH1F *hf = (TH1F*) gDirectory->Get("hf");
  TH1F *hf_mc = (TH1F*) gDirectory->Get("hf_mc");
  TH1F *hfb_mc = (TH1F*) gDirectory->Get("hfb_mc");

  double scaleFactor = hf->Integral() / hf_mc->Integral();
  scaleFactor *= hf->GetBinWidth(1) / hf_mc->GetBinWidth(1);
  hf_mc->Scale(scaleFactor);
  hfb_mc->Scale(scaleFactor);

  hf_mc->SetLineColor(kAzure - 9);
  hf_mc->SetFillColor(kAzure - 9);
  hfb_mc->SetLineColor(kSpring + 5);
  hfb_mc->SetFillColor(kSpring + 5);

  hf_mc->SetTitle("Failing Probes");
  hf_mc->GetXaxis()->SetTitle("m(#mu#mu#gamma) (GeV)");
  hf_mc->GetYaxis()->SetTitle("Entries / 5 GeV");
  hf_mc->GetYaxis()->SetTitleOffset(1.2);


  hf_mc->SetStats(0);
  hfb_mc->SetStats(0);

  hf->SetMarkerStyle(20);

  double ymax = TMath::Max(
      hf->GetMaximum() + TMath::Sqrt(hf->GetMaximum()),
      hf_mc->GetMaximum()
  );

  hf_mc->GetYaxis()->SetRangeUser(0, 1.1*ymax);

  c1->cd(2);
  hf_mc->Draw("hist");
  hfb_mc->Draw("hist same");
  hf->Draw("e0same");
  c1->cd(2)->RedrawAxis();

  string name = Form("eff_%s", label.c_str());  
  TCanvas *c2 = new TCanvas(name.c_str(), name.c_str(), 40, 40 ,400, 400);
  c2->SetRightMargin(0.02);
  c2->SetLeftMargin(0.12);
  
  g_eff->Draw("p");
  c2->Modified();
  c2->Update();
  TH2F *frame;
  if (cfg.veto == Config::kR9 || cfg.veto == Config::kCorrR9) {
    frame = new TH2F("frame","",2,0.5,2.5,1,0.35,0.65);
  } else {
    frame = new TH2F("frame","",2,0.5,2.5,1,0.7,1);
  }
  frame->SetStats(0);
  frame->GetYaxis()->SetTitleOffset(1.5);
  frame->GetYaxis()->SetTitle("Efficiency");
  frame->GetXaxis()->SetLabelSize(0.08);
  frame->GetXaxis()->SetBinLabel(1,"data");
  frame->GetXaxis()->SetBinLabel(2,"MC");
  frame->Draw();
  TGraphAsymmErrors *gr1 = g_eff->GetPaintedGraph();
  gr1->GetXaxis()->SetBinLabel( gr1->GetXaxis()->FindBin(1), "data" );
  gr1->GetXaxis()->SetBinLabel( gr1->GetXaxis()->FindBin(2), "MC" );
  gr1->SetMarkerStyle(20);
  //g_eff->GetPaintedGraph()->Draw("p");
  gr1->Draw("p");
  
  outputDir->cd();
  g_eff->Write("Efficiency");
  gr1->Write("EfficiencyGraph");
  frame->Write("EfficiencyFrame");
 
  c1->Print(Form("m3_%s.eps" , label.c_str()));
  c1->Print(Form("m3_%s.png" , label.c_str()));
  c2->Print(Form("eff_%s.eps", label.c_str()));
  c2->Print(Form("eff_%s.png", label.c_str()));
  
  c1->Write("c1");
  c2->Write("c2");
  
  return string(latex);
} // calculateEfficiencies
