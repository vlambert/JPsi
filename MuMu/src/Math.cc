/// C++ math functions
#include <math.h>
#include <cfloat>

/// ROOT's math functions
#include "TMath.h"

#include "JPsi/MuMu/interface/Math.h"

/*******************************************************************************
 * GENERALIZED SECANT HYPERBOLIC density in standard form (zero mean and
 * unit variance).
 * THE GENERALIZED SECANT HYPERBOLIC DISTRIBUTION AND ITS PROPERTIES,
 * D. C. Vaughan,
 * Communications in Statistics - Theory and Methods, Volume 31, Issue 2, 2002
 * http://www.tandfonline.com/doi/abs/10.1081/STA-120002647
 *
 * This calculates the auxiliary functions a(t), c1(t) and c2(t) as defined
 * by equation (4) of in 
 * Skew Generalized Secant Hyperbolic Distributions:
 * Unconditional and Conditional Fit to Asset Returns,
 * Matthias Fischer,
 * AUSTRIAN JOURNAL OF STATISTICS,
 * Volume 33 (2004), Number 3, 293–304
 * http://www.stat.tugraz.at/AJS/ausg043/043Fischer.pdf
 *
 */
void cit::math::gsh_a_c1_c2(double t, double &a, double &c1, double &c2) {
  static const double pi = TMath::Pi();
  static const double pi2 = pi*pi;
  /// Avoid dividing by x if |x| is smaller than epsilon.
  static const double epsilon = 100. * FLT_EPSILON;

  if (t <= -pi)
    return;

  double t2 = t*t;
  if (t <= 0.) {
    /// t in (-pi, 0]
    a  = cos(t);
    c2 = sqrt((pi2 - t2)/3.);
    if (t < -epsilon) {
      /// t in (-pi, -epsilon)
      c1 = c2 * sin(t) / t;
    } else {
      /// t in [-epsilon, 0]
      /// avoid division by a very small t by expanding sin(t) / t;
      c1 = c2 * (1. - t2/6. + t2*t2/120.);
    }
  } else {
    /// t in (0, +infinity)
    a  = cosh(t);
    c2 = sqrt((pi2 + t*t)/3.);
    if (t < epsilon) {
      /// t in (0, epsilon)
      /// avoid division by a very small t by expanding sinh(t) / t;
      c1 = c2 * (1. + t2/6. + t2*t2/120.);
    } else {
      /// t in [epsilon, +infinity)
      c1 = c2 * sinh(t) / t;
    }
  }
}


/*******************************************************************************
 * The actual generalized hyperbolic secant density, see gsh_a_c1_c2 above for 
 * details.
 */
double cit::math::gsh(double x, double t) {
  double a, c1, c2;
  cit::math::gsh_a_c1_c2(t, a, c1, c2);
  /// voila!
  return c1 / (exp(c2*x) + 2.*a + exp(-c2*x));
}


/*******************************************************************************
 * The CDF of the generalized hyperbolic secant density.
 */
double cit::math::gshCdf(double x, double t) {
  static const double pi = TMath::Pi();
  static const double pi2 = pi*pi;
  static const double piOverSqrt3 = TMath::Pi() / TMath::Sqrt(3.);
  static const double oneThird = 1./3.;

  /// Avoid dividing by t, sin(t) and sinh(t) if |t| < epsilon.
  static const double epsilon = 100. * FLT_EPSILON;

  if (t <= -pi)
    return 0.;

  if (t <= 0.) {
    /// t in (-pi, 0]
    if (t < -epsilon) {
      /// t in (-pi, -epsilon), it's safe to divide by sin(t)
      double c2 = sqrt(oneThird*(pi2 - t*t)); 
      double arg = - (TMath::Exp(c2*x) + TMath::Cos(t)) / TMath::Sin(t);
      double arccot = TMath::PiOver2() - TMath::ATan(arg);
      return 1. + arccot / t;
    } else {
      /// t in [-epsilon, 0]
      /// avoid division by a very small numbers by expanding in t;
      double f = 1./(1. + TMath::Exp(x));
      return 1. - f + (f/6. - 0.5*f*f + f*f*f/3.)*t*t;
    }
  } else {
    /// t in (0, +infinity)
    if (t < epsilon) {
      /// t in (0, epsilon)
      /// avoid division by a very small t by expanding sinh(t) / t;
      double f = 1./(1. + TMath::Exp(x));
      return 1. - f - (f/6. - 0.5*f*f + f*f*f/3.)*t*t;
    } else {
      /// t in [epsilon, +infinity)
      double c2 = sqrt(oneThird*(pi2 + t*t)); 
      double inverse_arg = TMath::SinH(t) / (TMath::Exp(c2*x) + TMath::CosH(t));
      double arccoth = TMath::ATanH(inverse_arg);
      return 1. - arccoth / t;
    }
  }
  // This should never happen.
  return 1.;
}
