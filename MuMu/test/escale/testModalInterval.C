{
  /// Configuration
  double nSigmaCoverage = 1;
  double mean = 0;
  double sigma = 1;
  size_t n = 10000;

  /// Load the needed library and header file.
  gSystem->Load("libJPsiMuMu");
  #include "JPsi/MuMu/interface/ModalInterval.h"

  /// Generate data
  cout << "Sampling Gaussian PDF with mean=" << mean
       << " and sigma=" << sigma
       << " " << n << " times." << endl;
  vector<double> data;
  data.reserve(n);
  for (int i=0; i<n; ++i) {
    data.push_back(gRandom->Gaus(0,1));
  }

  /// Construct the modal interval object
  cit::ModalInterval mi(data.begin(), data.end());

  /// Get the interval to cover all data
  mi.setFraction(1.);
  cout << "Shortest interval covering all data: " << endl
       << "[" << mi.lowerBound() << ", " << mi.upperBound() << "]" << endl;

  /// Get the interval to cover mean +/- nsigma * sigma
  mi.setSigmaLevel(nSigmaCoverage);
  cout << "Shortest interval covering same fraction of data as mean +/- "
       << nSigmaCoverage << " sigma for a Gaussian: " << endl
       << "[" << mi.lowerBound() << ", " << mi.upperBound() << "]" << endl;
}
