import math
import ROOT

## Load FWLite
ROOT.TMath.Prob(1,1)

## Values from table on slide 21 of
## https://indico.cern.ch/getFile.py/access?contribId=0&resId=0&materialId=slides&confId=219068
names = 'EB_highR9 EB_allR9 EE_allR9'.split()
## S_true
true = [0.388, 0.523, 0.758]
## S_true Error
etrue = [0.016, 0.017, 0.042]
## S_MC
mc = [0.276, 0.911, 0.02]
## S_MC Error
emc = [0.087, 0.069, 0.14]

oplus = lambda x,y: math.sqrt(x*x + y*y)

## Print pulls
print '== Fit - True Pull =='
chi2 = 0
for name, x, y, ex, ey in zip(names, true, mc, etrue, emc):
    pull = (x - y) / oplus(ex, ey)
    print name, pull
    chi2 += pull * pull

print 'global chi2 p-value:', ROOT.TMath.Prob(chi2, 3)
