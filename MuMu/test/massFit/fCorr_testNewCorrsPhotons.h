#ifndef INC_FCORR_TESTNEWCORRSPHOTONS
#define INC_FCORR_TESTNEWCORRSPHOTONS

namespace fcorr{
  inline double electron_br1(double brLinear, double e) {
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
    //

    // this is for 31X
    if ( brLinear < 1.1 ) brLinear = 1.1;
    if ( brLinear > 8 ) brLinear = 8.0;

    // pre 3_10_0
//    double p0 = -0.05185;
//    double p1 = 0.1354;
//    double p2 = 0.9165;
//    double p3 = -0.0005626;
//    double p4 = 1.385;

    // 4_1_3 af
    // first version
//    double p0 = -0.0625;
//    double p1 = 0.1331;
//    double p2 = 0.9329;
//    double p3 = -0.0007823;
//    double p4 = 1.1;
    // second version
    double p0 = -0.002362;
    double p1 = 0.004314;
    double p2 = 1.001;
    double p3 = 0.0003413;
    double p4 = 3.124;

    double threshold = p4;

    double y = p0*threshold*threshold + p1*threshold + p2;
    double yprime = 2*p0*threshold + p1;
    double a = p3;
    double b = yprime - 2*a*threshold;
    double c = y - a*threshold*threshold - b*threshold;

    double fCorr_testNewCorrsPhotons = 1;
    if ( brLinear < threshold )
      fCorr_testNewCorrsPhotons = p0*brLinear*brLinear + p1*brLinear + p2;
    else
      fCorr_testNewCorrsPhotons = a*brLinear*brLinear + b*brLinear + c;

    return e/fCorr_testNewCorrsPhotons;

  }

  inline double electron_br1_complete(double et, double eta) {
    double fCorr_testNewCorrsPhotons = 0;

    // hybrid SC
    // fBrem
    // 4_1_3 af
    // first version
//    double c0 = 0.997;
//    double c1 = -0.1427;
//    double c2 = 0;
    // second version
    double c0 = 0.9963;
    double c1 = -0.1158;
    double c2 = -4.189;

    // fEtEta
    // 4_1_3 af
    // first version
//    double c4 = 0.8589;
//    double c5 = 37.48;
//    double c6 = 1.491;
    // second version
    double c4 = 0.9009;
    double c5 = 39.67;
    double c6 = 1.253;

    // final fitting
    double c7 = 1.081;  // curve point in eta distribution
    double c8 = 7.6;     // sharpness of the curve
    double c3 = -0.00181;


    double p0 = c0 + c1/(et + c2);
    double p1 = c4/(et + c5) + c6/(et*et);

    fCorr_testNewCorrsPhotons = p0 + p1*atan(c8*(c7 - fabs(eta))) + c3*fabs(eta);

    return et/fCorr_testNewCorrsPhotons;
  }

}
#endif //INC_FCORR
