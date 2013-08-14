#include <algorithm>

#include "TMath.h"
#include "TTree.h"
#include "RooArgSet.h"
#include "RooAbsArg.h"

#include "JPsi/MuMu/interface/ModalInterval.h"

using namespace cit;

ClassImp(ModalInterval)

///----------------------------------------------------------------------------
/// Default constructor.
ModalInterval::ModalInterval() :
  fraction_(1.),
  updatedIntervalBounds_(false),
  x_(0)
{
  lower_ = x_.begin();
  upper_ = x_.end() - 1;
}


///----------------------------------------------------------------------------
ModalInterval::ModalInterval(const_iterator first, const_iterator last,
                             double fraction) :
  fraction_(fraction),
  updatedIntervalBounds_(false),
  x_(0)
{
  readData(first, last);
}


///----------------------------------------------------------------------------
ModalInterval::ModalInterval(size_t n, double* first, double fraction) :
  fraction_(fraction),
  updatedIntervalBounds_(false),
  x_(0)
{
  readData(n, first);
}


///----------------------------------------------------------------------------
ModalInterval::ModalInterval(std::vector<double> const& data, double fraction) :
  fraction_(fraction),
  updatedIntervalBounds_(false),
  x_(0)
{
  readData(data);
}


///----------------------------------------------------------------------------
/*
ModalInterval::ModalInterval(RooAbsReal& x, RooDataSet const& data, 
			     double fraction) :
  fraction_(fraction),
  updatedIntervalBounds_(false),
  x_(0)
{
  readData(x, data);
}
*/

///----------------------------------------------------------------------------
ModalInterval::~ModalInterval(){}


///----------------------------------------------------------------------------
void
ModalInterval::getBounds(double& lower, double& upper)
{
  updateIntervalBounds();
  lower = *lower_;
  upper = *upper_;
  return;
}


///----------------------------------------------------------------------------
void
ModalInterval::updateIntervalBounds()
{
  /// Check if we need to update the calculation
  if (updatedIntervalBounds_ == true) {
    /// Cached values are up to date. No need to carry on.
    return;
  }

  /// Check if the fraction is less than unity
  if (fraction_ >= 1.) {
    /// The fraction is greater or equal to one.  We return an interval
    /// containing all the data.
    lower_ = x_.begin();
    upper_  = x_.end() - 1;
    updatedIntervalBounds_ = true;
    return;
  }

  /// Here comes the meat.

  /// Set the default bounds include the left-most interval.
  initBounds();

  /// Calculate the size of the default interval.
  double dx = *upper_ - *lower_;

  /// Find the smallest interval containing at least fraction of the
  /// total entries. Loop over all intervals.
  for (std::vector<double>::const_iterator first = lower_, last  = upper_;
       last < x_.end(); ++first, ++last)
  {
    /// Compare the size of the defoult interval with the current one.
    if (*last - *first < dx) {
      /// Found new shortest interval.  Store its bounds and size.
      lower_ = first;
      upper_  = last;
      dx = *upper_ - *lower_;
    }
  } /// End of loop over all intervals.

  updatedIntervalBounds_ = true;
  return;
}


///----------------------------------------------------------------------------
double
ModalInterval::lowerBound() {
  updateIntervalBounds();
  return *lower_;
}


///----------------------------------------------------------------------------
double
ModalInterval::upperBound() {
  updateIntervalBounds();
  return *upper_;
}


///----------------------------------------------------------------------------
double
ModalInterval::length() {
  updateIntervalBounds();
  return *upper_ - *lower_;
}


///----------------------------------------------------------------------------
std::vector<double>
ModalInterval::bounds() {
  updateIntervalBounds();
  std::vector<double> bounds(2);
  bounds[0] = *lower_;
  bounds[1] = *upper_;
  return bounds;
}


///----------------------------------------------------------------------------
/// Update the default interval boundaries to the left most interval.
void
ModalInterval::initBounds() {
  /// Calculate the number of data entries in the interval
  size_t interval_entries = TMath::Ceil(fraction_ * x_.size());

  /// Update the bounds.
  lower_ = x_.begin();
  upper_  = x_.begin() + interval_entries - 1;

  updatedIntervalBounds_  = false;
}


///----------------------------------------------------------------------------
void
ModalInterval::readData(size_t n, double* first) {
  readData(first, first + n);
}


///----------------------------------------------------------------------------
void
ModalInterval::readData(std::vector<double> const& data) {
  readData(data.begin(), data.end());
}


///----------------------------------------------------------------------------
/*
void
ModalInterval::readData(RooAbsReal& x, RooDataSet const& data) {
  updatedIntervalBounds_ = false;

  /// Make sure this is a univariate dataset.
  assert(data.get()->getSize() == 1);

  const Long64_t nentries = data.tree()->GetEntries();
  x_.clear();
  x_.reserve(nentries);

  /// Loop over all the entries and fill the values in the internal cache
  for (Int_t i=0; i < nentries; ++i) {
    // RooAbsReal *xx = (RooAbsReal*)data.get(i)->first();
    data.get(i);
    x_.push_back(x.getVal());
  }
  
  /// Sort the data
  std::sort(x_.begin(), x_.end());
}
*/

///----------------------------------------------------------------------------
void
ModalInterval::setFraction(double fraction) {
  fraction_ = fraction;
  if (fraction_ > 1.)
    fraction_ = 1.;
  if (fraction_ < 0.)
    fraction_ = 0.;
  initBounds();
  updatedIntervalBounds_  = false;
}


///----------------------------------------------------------------------------
/// Set the fraction of the events in terms of nsigma such that it is same as
/// for a Gaussian distribution in mean +/- nsigma * sigma
void
ModalInterval::setSigmaLevel(double nsigma) {
  fraction_ = 1 - TMath::Prob(nsigma*nsigma, 1);
  initBounds();
  updatedIntervalBounds_  = false;
}


///----------------------------------------------------------------------------
/// Set the number of the data entries that the interval must cover
void
ModalInterval::setNumberOfEntriesToCover(size_t entries) {
  /// The '-0.5' compensates for rounding upward when calculating the
  /// number of entries in the interval
  fraction_ = (entries - 0.5) / x_.size();
  if (fraction_ > 1.)
    fraction_ = 1.;
  if (fraction_ < 0.)
    fraction_ = 0.;
  initBounds();
  updatedIntervalBounds_  = false;
}

