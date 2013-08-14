from basicRoot import *

##########################################################################
### MUONS
##########################################################################

# see Fig. 17 of AN2008_097_v3.pdf for the pt dependence of sigmpa(pt_mu)/pt_mu
muPtPt = "({pt}<=10) + ({pt}>10)*(-5+6*log10({pt}))"

# Eta dependence taken from CMS PAS TRK-10-004 eq. (5) and
b0, b1, b2, b3, b4 = 1.61, 5e-3, 1.9e-2, 1.4e-2, 1.5
cParameter = "{b2} + {b3} * ({b0} - {b4}) * ({b0} - {b4}) - {b1} * {b0} * {b0}".format(
  b0=b0, b1=b1, b2=b2, b3=b3, b4=b4
  )
cParameterValue = eval(cParameter)
muPtEtaTerm1 = "({c} + {b1}*({eta})^2) * (abs({eta}) <= {b0})".format(
  b0=b0, b1=b1, c=cParameterValue, eta="{eta}"
  )
muPtEtaTerm2 = "({b2} + {b3} * (abs({eta}) - {b4})^2) * (abs({eta}) > {b0})".format(
  b0=b0, b2=b2, b3=b3, b4=b4, eta="{eta}"
  )
muPtEta = muPtEtaTerm1 + " + " + muPtEtaTerm2

# combine eta and pt dependence
muPtPtEta = "({fpt})*({feta})".format(fpt=muPtPt, feta=muPtEta)

# plot pt dependence
# fMuPtPt = TF1("fMuPtPt", muPtPt.format(pt="x"), 1, 10e3)
# c1 = TCanvas()
# fMuPtPt.Draw()
# c1.SetLogx()

# plot eta dependence
# fMuPtEta = TF1("fMuPtEta", muPtEta.format(eta="x"), -2.4, 2.4)
# c2 = TCanvas("c2", "muPtEta", 30, 30, 700, 500)
# fMuPtEta.Draw()

# build daughter expressions
mu1PtPtEta = muPtPtEta.format(pt="muPt[dau1[mm]]", eta="muEta[dau1[mm]]")
mu2PtPtEta = muPtPtEta.format(pt="muPt[dau2[mm]]", eta="muEta[dau2[mm]]")

# add the daughters in quadrature
muPtErr = "sqrt( ({e1})^2 + ({e2})^2 )".format(e1=mu1PtPtEta, e2=mu2PtPtEta)

phoMuErr = "0.5 * ({Mz}^2+{Mmumu}^2) / ({Mz}^2-{Mmumu}^2) * {muPtErr}".format(
  Mz = 91.1876, Mmumu = "mass[mm]", muPtErr = muPtErr
)


##########################################################################
### ECAL
##########################################################################
# see CMS IN 2000/028 for EE, 2008 JINST 3 S08004 and CMS DN-2007/12 for EB

sTerm = "{s} / sqrt({e})"
nTerm = "{n} / {e}"
phoEResolution = "sqrt( ({sTerm})^2 + ({nTerm})^2 + ({c})^2 )".format(
  sTerm=sTerm, nTerm=nTerm, c="{c}"
  )
phoEBErr = phoEResolution.format(
  s = 0.035, n = 0.15, c = 0.02, e = "{e}"
  )
phoEEErr = phoEResolution.format(
  s = 0.05, n = 0.45, c = 0.06, e = "{e}"
  )
phoEcalErr = "(abs({eta}) < 1.5) * {eb} + (abs({eta}) > 1.5) * {ee}".format(
  eta = "phoEta[g]", eb = phoEBErr, ee = phoEEErr
)
