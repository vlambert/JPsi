/**
  * Jan Veverka, Caltech,  26 October 2011
  */

#include <algorithm>
#include <cmath>
#include <list>
#include <iostream>

#include "TError.h"
#include "TH1I.h"
#include "TMath.h"

#include "JPsi/MuMu/interface/DataDrivenBinning.h"

using namespace cit;

/// Make this a ROOT class
ClassImp(DataDrivenBinning)

///----------------------------------------------------------------------------
/// Default constructor
DataDrivenBinning::DataDrivenBinning()
{}


///----------------------------------------------------------------------------
DataDrivenBinning::DataDrivenBinning(const_iterator first, const_iterator last,
                                     size_t minBinContent,
				     size_t maxBinContent) :
  ModalInterval(first, last, 1.),
  updatedBoundaries_(false),
  updatedMedians_(false),
  minBinContent_(minBinContent),
  maxBinContent_(maxBinContent),
  boundaries_(0),
  medians_(0),
  niceNumbers_(0)
{
  initNiceNumbers();
}


///----------------------------------------------------------------------------
DataDrivenBinning::DataDrivenBinning(size_t n, double* first,
                                     size_t minBinContent,
				     size_t maxBinContent) :
  ModalInterval(n, first, 1.),
  updatedBoundaries_(false),
  updatedMedians_(false),
  minBinContent_(minBinContent),
  maxBinContent_(maxBinContent),
  boundaries_(0),
  medians_(0),
  niceNumbers_(0)
{
  initNiceNumbers();
}


///----------------------------------------------------------------------------
DataDrivenBinning::DataDrivenBinning(std::vector<double> const & data,
                                     size_t minBinContent,
				     size_t maxBinContent) :
  ModalInterval(data, 1.),
  updatedBoundaries_(false),
  updatedMedians_(false),
  minBinContent_(minBinContent),
  maxBinContent_(maxBinContent),
  boundaries_(0),
  medians_(0),
  niceNumbers_(0)
{
  initNiceNumbers();
}


///----------------------------------------------------------------------------
/*
DataDrivenBinning::DataDrivenBinning(RooAbsReal& x, 
				     RooDataSet const& data,
                                     size_t minBinContent,
				     size_t maxBinContent) :
  ModalInterval(x, data, 1.),
  updatedBoundaries_(false),
  updatedMedians_(false),
  minBinContent_(minBinContent),
  maxBinContent_(maxBinContent),
  boundaries_(0),
  medians_(0),
  niceNumbers_(0)
{
  initNiceNumbers();
}
*/

///----------------------------------------------------------------------------
DataDrivenBinning::~DataDrivenBinning()
{}


///----------------------------------------------------------------------------
void
DataDrivenBinning::initNiceNumbers()
{
  niceNumbers_.push_back(1);
  niceNumbers_.push_back(2);
  niceNumbers_.push_back(2.5);
  niceNumbers_.push_back(5);

  std::sort(niceNumbers_.begin(), niceNumbers_.end());
}


///----------------------------------------------------------------------------
double
DataDrivenBinning::getNiceBinWidth(double maxBinWidth) const
{
  /// Find a, n such that maxBinWidth = a * 10^n with a in [1, 10), n integer.
  double n = floor(log10(maxBinWidth));
  double a = maxBinWidth * pow(10, -n);

  /// Find greatest nice number smaller or equal to a.  Nice numbers are
  /// sorted in ascending order. Loop over them backwards, from the greatest
  /// to the least.
  std::vector<double>::const_reverse_iterator nice = niceNumbers_.rbegin();
  for (; nice != niceNumbers_.rend(); ++nice) {
    if (*nice <= a) {
      /// Found a good nice number.  Retrun the corresponding nice bin width.
      a = *nice;
      return a * pow(10, n);
    }
  } /// End of loop over nice numbers.

  /// This should never happen!
  Warning("getNiceBinWidth", "Failed.");
  return maxBinWidth;
}


///----------------------------------------------------------------------------
/// The MEAT.
void
DataDrivenBinning::updateBoundaries()
{
  // std::cout << "Entering DataDrivenBinning::updateBoundaries()...\n";
  updateBinningRange();

  /// Check if the result is already cahed
  if (updatedBoundaries_) {
    /// We are done.
    return;
  }

  /// Get a range to cover all data and store it.
  double xstart, xstop;
  setFraction(1.);
  getBounds(xstart, xstop);

  /// Get the maximum bin width given by maxBinContent
  setNumberOfEntriesToCover(maxBinContent_);
  double maxBinWidth = length();
  // std::cout << "maxBinWidth: " << maxBinWidth << std::endl;

  /// Find the greatest "nice looking" bin width smaller than the max.
  binWidth_ = getNiceBinWidth(maxBinWidth);
  // std::cout << "binWidth_: " << binWidth_ << std::endl;

  /// Increase the range so that bounds are multiples of (nice) binWidth_
  xstart = TMath::Floor(xstart / binWidth_) * binWidth_;
  xstop  = TMath::Ceil(xstop / binWidth_) * binWidth_;
  size_t nbins = (size_t) ((xstop - xstart) / binWidth_);
  // std::cout << "range: " << xstart << ", " << xstop << std::endl;
  // std::cout << "n bins: " << nbins << std::endl;

  /// TODO: Use the fact that we already have sorted data and
  /// simplify the code bellow so that it doesn't need the TH1F.

  /// Get the bin frequencies for uniform bins.
  TH1I * hist = new TH1I("hist", "hist", nbins, xstart, xstop);
  for (const_iterator ix = x_.begin(); ix != x_.end(); ++ix) {
    hist->Fill(*ix);
  }

  /// Store the bincontents.
  std::vector<double> contents;

  /// Merge bins with low frequencies.  Store bin boundaries.  Loop over
  /// the uniform bins forward.
  size_t binContent = 0;
  boundaries_.push_back(xstart);
  for (size_t bin = 1; bin <= nbins; ++bin) {
    binContent += hist->GetBinContent(bin);
    // std::cout << "bin " << bin << ", content: " << binContent << std::endl;
    if (binContent >= minBinContent_) {
      double newBoundary = hist->GetBinLowEdge(bin) + binWidth_;
      /// Check if the new boundary is already in the vector.
      std::vector<double>::const_iterator it;
      it = std::find(boundaries_.begin(), boundaries_.end(), newBoundary);
      if (it == boundaries_.end()) {
	/// Didn't find the new boundary in the vector. Let's include it.
        // std::cout << "New boundary: " << newBoundary << std::endl;
	boundaries_.push_back(newBoundary);
	contents.push_back(binContent);
	binContent = 0;
      } // End of check whether new boundary is in the vector.
    } // End of check of the bin contents.
  } // End of forward loop over bins

  /// The last bin stays "open".

  /// The last bin may have too few entries.  Walk over the boundaries
  /// backward and remove them as needed
  std::vector<double>::const_reverse_iterator content  = contents.rbegin();
  for (; content != contents.rend(); ++content) {
    if (binContent >= minBinContent_) {
      /// We are done!
      break;
    }
    /// Remove the boundary
    // std::cout << "last bin content: " << binContent << std::endl;
    // std::cout << "removing boundary: " << boundaries_.back() << std::endl;
    boundaries_.pop_back();
    binContent += *content;
  } // End of backward loop over the bin contents.

  /// Add the last upper boundary of the binning.
  boundaries_.push_back(xstop);

  /// Set the flag that the bin boundaries are up to date.
  updatedBoundaries_ = true;
  updatedMedians_ = false;

  /// Cleanup allocated memory
  delete hist;
}


///----------------------------------------------------------------------------
void
DataDrivenBinning::updateMedians()
{
  // std::cout << "Entering DataDrivenBinning::updateMedians\n";
  updateBoundaries();

  /// Check if the result is already cahed
  if (updatedMedians_) {
    /// We are done.
    return;
  }

  std::vector<const_iterator> binsFirstEntries;
  binsFirstEntries.reserve(boundaries_.size() + 1);

  /// The index of the first entry in the first bin is 0.
  binsFirstEntries.push_back(x_.begin());
  /// Loop over the bin boundaries.
  for (const_iterator ib = boundaries_.begin() + 1;
       ib != boundaries_.end(); ++ib) {
    /// Loop over the data. Find the first entry with x > boundary.
    for (const_iterator ix = binsFirstEntries.back() + 1;
	 ix < x_.end(); ++ix) {
      if (*ix < *ib) continue;
      /// ix points to the first entry in bin with low edge *ib.
      binsFirstEntries.push_back(ix);
      break;
    } /// End of loop over data.
  } /// End of loop over boundaries.

/*  for (size_t i=0; i < binsFirstEntries.size(); ++i) {
    std::cout << "bin " << i << " first entry: "
              << *binsFirstEntries[i] << std::endl;
  }*/
  /// Add the end of the data
  binsFirstEntries.push_back(x_.end());

  /// Loop over the first entries per bin calculate the medians
  /// iix is an iterator over iterators!
  medians_.reserve(boundaries_.size());
  std::vector<const_iterator>::const_iterator iix =  binsFirstEntries.begin();
  for (; iix + 1 < binsFirstEntries.end(); ++iix) {
    const_iterator ifirst = *iix;
    const_iterator ilast  = *(iix + 1);
    double median = TMath::Median( ilast - ifirst, &(*ifirst) );
    medians_.push_back(median);
  } /// End of loop over the first entries per bin.

  /// Set the flag that the bin medians are up to date.
  updatedMedians_ = true;

} /// End of updateMedians(...)



///----------------------------------------------------------------------------
void
DataDrivenBinning::updateBinningRange()
{
  /// Check if the range of the binning given by the modal interval is
  /// up to date.
  if (!updatedIntervalBounds_) {
    /// The binning range may have to be updated and so will the bin
    /// boundaries and medians.
    updatedMedians_ = updatedBoundaries_ = false;
  }

  /// Use the base class method to update the binning range.
  setFraction(1);
  updateIntervalBounds();
}


///----------------------------------------------------------------------------
std::vector<double> const &
DataDrivenBinning::binBoundaries()
{
  updateBoundaries();
  return boundaries_;
}


///----------------------------------------------------------------------------
std::vector<double> const &
DataDrivenBinning::binMedians()
{
  updateMedians();
  return medians_;
}


///----------------------------------------------------------------------------
RooBinning &
DataDrivenBinning::binning(RooBinning & bins)
{
  updateBoundaries();

  /// Reset the given binning.
  bins = RooBinning(boundaries_.front(), boundaries_.back(), bins.GetName());

  /// Insert all the boundaries except for the first and the last one.
  for (const_iterator b = boundaries_.begin() + 1;
       b < boundaries_.end() - 1; ++b) {
    bins.addBoundary(*b);
  }

  return bins;
}


///----------------------------------------------------------------------------
RooUniformBinning &
DataDrivenBinning::uniformBinning(RooUniformBinning & bins)
{
  updateBoundaries();

  /// Reset the given binning.
  double xlo = boundaries_.front();
  double xhi = boundaries_.back();
  size_t nbins = (xhi - xlo) / binWidth_;

  bins = RooUniformBinning(xlo, xhi, nbins, bins.GetName());
  return bins;
}


///----------------------------------------------------------------------------
RooHist &
DataDrivenBinning::applyTo(RooHist& hist)
{
  updateMedians();

  for (size_t i=0; i < boundaries_.size() - 1 &&
                   i < medians_.size() &&
                   i < (size_t) hist.GetN(); ++i) {
    double x = medians_[i];
    double y = hist.GetY()[i];
    double xlow = boundaries_[i];
    double xhigh = boundaries_[i+1];
    hist.SetPoint(i, x, y);
    hist.SetPointEXlow (i, x - xlow);
    hist.SetPointEXhigh(i, xhigh - x);

  }
  return hist;
}

