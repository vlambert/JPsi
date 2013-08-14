import math

oplus = lambda x,y: math.sqrt(x*x + y*y)

def getScale(dmVal, dmErr):
    """Returns scale and it's error in per-cent."""
    p0Val, p0Err = 0.06246, 0.005282
    p1Val, p1Err = 15.05, 0.1351
    sVal = (dmVal - p0Val)/p1Val
    sErr = math.fabs(sVal * oplus(p1Err/p1Val, oplus(dmErr, p1Err)/(dmVal-p0Val)))
    return (100*sVal, 100*sErr)

print "Endcaps Dec22ReReco + Winter10 MC: (%.4f +/- %.4f)%%" % getScale(-0.871 - 0.132, oplus(0.41, 0.067) )
print "Endcaps Nov4ReReco + Fall10 MC:    (%.4f +/- %.4f)%%" % getScale(-1.307 - 0.11 , oplus(0.53, 0.13) )
print "Barrel  Dec22ReReco + Winter10 MC: (%.4f +/- %.4f)%%" % getScale( 0.24  - 0.362, oplus(0.35, 0.062) )
print "Barrel  Nov4ReReco + Fall10 MC:    (%.4f +/- %.4f)%%" % getScale( 0.08  - 0.317, oplus(0.22, 0.057) )
