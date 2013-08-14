#include "TMath.h"
#include <cmath>
#ifdef __CINT__
static const double M_PI = TMath::Pi();
#endif

inline double deltaPhi(double phi1, double phi2) {
    double result = phi1 - phi2;
    while (result > M_PI) result -= 2*M_PI;
    while (result <= -M_PI) result += 2*M_PI;
    return result;
}

inline double deltaTheta(double eta1, double eta2) {
    double theta1 = 2. * TMath::ATan(TMath::Exp(-eta1));
    double theta2 = 2. * TMath::ATan(TMath::Exp(-eta2));
    double result = theta2 - theta1;
    while (result > M_PI) result -= 2*M_PI;
    while (result <= -M_PI) result += 2*M_PI;
    return result;
}

