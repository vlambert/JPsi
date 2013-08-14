# Test formula for the invariant mass of 2 massless bodies
# as a function of there pt, eta and phi
# m_{12} = \sqrt{p_1^{\perp}p_2^{\perp}\left[\cosh(\eta_1+\eta_2) - cos(\phi_1-\phi_2)\right]}

from basicRoot import *
from ROOT import gRandom, AddressOf, TTree, TLorentzVector
from math import sqrt, sin, cos, sinh, cosh, pi

## Define the new formula
def formula(a, b):
  """Returns invariant mass of a+b from pt, eta, phi
  Assumes massless particles"""
  cosh12 = cosh(a.eta - b.eta)
  cos12 = cos(a.phi - b.phi)
  return sqrt( 2 * a.pt * b.pt * (cosh12 - cos12) )

## Define root structs to set branch addresses
gROOT.ProcessLine("""
  struct FourVector {
    float pt;
    float eta;
    float phi;
    float m;
  };
  """.replace("\n", "")
  )

gROOT.ProcessLine("struct RootFloat {float value;};")

from ROOT import FourVector, RootFloat

## Define the fourvectors and the invariant masses
p1, p2 = FourVector(), FourVector()
P1, P2 = TLorentzVector(), TLorentzVector()
m12, m12formula = RootFloat(), RootFloat()

## Make the tree and it's branches
t = TTree("t", "test m12 formula")
t.Branch("p1", AddressOf(p1, "pt"), "pt/F:eta/F:phi/F:m/F")
t.Branch("p2", AddressOf(p2, "pt"), "pt/F:eta/F:phi/F:m/F")
t.Branch("m12", AddressOf(m12, "value"), "m12/F")
t.Branch("m12formula", AddressOf(m12formula, "value"), "m12formula/F")

## Generate random values and fill the tree with them
for i in range(1000):
  p1.pt, p1.eta, p1.phi = gRandom.Exp(10), gRandom.Gaus(0, 1.5), gRandom.Uniform(-pi, pi)
  p2.pt, p2.eta, p2.phi = gRandom.Exp(10), gRandom.Gaus(0, 1.5), gRandom.Uniform(-pi, pi)

  P1.SetPtEtaPhiM(p1.pt, p1.eta, p1.phi, 0)
  P2.SetPtEtaPhiM(p2.pt, p2.eta, p2.phi, 0)

  m12.value = (P1+P2).M()
  m12formula.value = formula(p1,p2)

  t.Fill()

# Done!
print "Done!"
