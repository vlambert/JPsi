// A namespace of useful mathematical functions
#ifndef JPSI_MUMU_MATH_H
#define JPSI_MUMU_MATH_H

#include "TMath.h"

namespace cit {
  namespace math {
    inline double sech(double x) {return 1./TMath::CosH(x);}
    // Generalized Secant Hyperbolic density with zero mean and unit variance
    void   gsh_a_c1_c2(double t, double &a, double &c1, double &c2);
    double gsh(double x, double t);
    // CDF of GSH PDF
    double gshCdf(double x, double t);
  } // end of namespace math
} // end of namespace cit

#endif
