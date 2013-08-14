/**
  \class  PileupReweighter
  \brief  Calculate event weight to reweigh MC for pileup.
  \author Jan Veverka, Caltech
  \date   May 26, 2011

*/

#include <vector>
#include "TH1.h"

namespace cit {
  //---------------------------------------------------------------------------
  class PileupReweighter {
  public:
    /// constructor
    PileupReweighter( const TH1 & numPileupSimulation,
                      const TH1 & numPileupTarget )
    /// destructor
    ~PileupReweighter;
    /// calculate the event weight
    double operator()( const unsigned & numPileup );
  private:
    /// stores weigts indexed by the numPileup
    std::vector<double> weights;
  }; // end of class PileupReweighter

} // end of namespace cit