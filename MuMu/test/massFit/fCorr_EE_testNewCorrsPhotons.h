#ifndef INC_FCORR_EE_TESTNEWCORRSPHOTONS
#define INC_FCORR_EE_TESTNEWCORRSPHOTONS

namespace fcorr_ee{
  inline double electron_br1(double brLinear, double e) {
    // These corrections are tuned on CMSSW 18x dynamicHybridSuperClusters!
    // YM: 02/05/2008
    //
    // first parabola (for brLinear < threshold)
    // p0*x^2 + p1*x + p2
    // second parabola (for brLinear >= threshold)
    // ax^2 + bx + c, make y and y' the same in threshold
    // y = p0*threshold^2 + p1*threshold + p2
    // yprime = p1 + 2*p0*threshold
    // a = p3
    // b = yprime - 2*a*threshold
    // c = y - a*threshold^2 - b*threshold
    // final result is multiplied by cos(p5/br + p6*br + p7)

    // make NO correction if brLinear is invalid!
    if ( brLinear == 0 ) return e;
    // make a flat correction if brLinear is too big (>9)

    // FM with preshower
    if ( brLinear > 6.5 ) brLinear = 6.5;
    if ( brLinear < 0.9 ) brLinear = 0.9;

    // ============= Fixed Matrix With Preshower SC
    // 3_10_0 implemented in CMSSW_4_2_X
//    double p0 = -0.07945;
//    double p1 = 0.1298;
//    double p2 = 0.9147;
//    double p3 = -0.001565;
//    double p4 = 0.9;

    // test corrections from 413 diphotons
    // first version
//    double p0 = -0.0728;
//    double p1 = 0.1323;
//    double p2 = 0.9201;
//    double p3 = 0.002501;
//    double p4 = 1.118;
    // second version
    double p0 = -0.07667;
    double p1 = 0.1407;
    double p2 = 0.9157;
    double p3 = 0.00251;
    double p4 = 1.117;

    double threshold = p4;

    double y = p0*threshold*threshold + p1*threshold + p2;
    double yprime = 2*p0*threshold + p1;
    double a = p3;
    double b = yprime - 2*a*threshold;
    double c = y - a*threshold*threshold - b*threshold;

    double fCorr = 1;
    if ( brLinear < threshold )
      fCorr = p0*brLinear*brLinear + p1*brLinear + p2;
    else
      fCorr = a*brLinear*brLinear + b*brLinear + c;

    return e/fCorr;

  }

  inline double electron_br1_complete(double et, double eta) {
    double fCorr = 0.;

    /*
    // 3_10_0 implemented in CMSSW_4_2_X
    double c0 = -3.516;
    double c1 = -2.362;

    double c2 = 2.151;
    double c3 = 1.572;

    double c4 = -0.336;
    double c5 = -0.2807;

    double c6 = 3.2;
    double c7 = 0.0;
    */

    // test corrections from 413 diphotons
    double c0 = -1.513;
    double c1 = -0.4142;

    double c2 = 1.239;
    double c3 = 0.2625;

    double c4 = -0.2016;
    double c5 = -0.02905;

    double c6 = 1.7;
    double c7 = 0.0;

    double p0 = c0 + c1/sqrt(et);
    double p1 = c2 + c3/sqrt(et);
    double p2 = c4 + c5/sqrt(et);
    double p3 = c6 + c7/sqrt(et);

    // make correction constant
    if ( fabs(eta) < 1.6 ) eta = 1.6;
    if ( fabs(eta) > 2.6 ) eta = 2.6;
    fCorr = p0 + p1*fabs(eta) + p2*eta*eta + p3/fabs(eta);

    if ( 1./fCorr > 1.2 ) return et/1.2;
    if ( 1./fCorr < 0.5 ) return et/0.5;
    return et/fCorr;
  }

}
#endif //INC_FCORR_EE


