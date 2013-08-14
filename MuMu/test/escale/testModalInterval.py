import ROOT
from JPsi.MuMu.common.modalinterval import ModalInterval
from JPsi.MuMu.vector import vector

## Configuration
nSigmaCoverage = 1.
mean = 0.
sigma = 1.
n = 100000

## Get some toy data
print ("Sampling Gaussian PDF with mean=%g and sigma=%g "
       "%d times..." % (mean, sigma, n))
data = vector('double')()
data.reserve(n)
for i in range(n):
  data.push_back(ROOT.gRandom.Gaus(0,1))

## Create the ModalInterval object
mi = ModalInterval(data)

## Pring the full range of toy data
mi.setFraction(1.)
print "\nShortest interval covering all data:"
print "[%f, %f]" % tuple(mi.bounds())

## Print the range corresponding to n effective sigma
print "\nRange corresponding to +/-%g effective sigma:" % nSigmaCoverage
mi.setSigmaLevel(nSigmaCoverage)
print "[%f, %f]" % tuple(mi.bounds())
