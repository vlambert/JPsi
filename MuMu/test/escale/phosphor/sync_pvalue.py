'''
Calculate the p-value of the chi2 between two different
results.
'''
import ROOT

ndof = 3
chi2_over_ndof = [
    0.251, # L/B - EGM
    0.169, # EGM - P
    0.251, # L/B - P
    ]
    
    
for chi in chi2_over_ndof:
    print chi, ROOT.TMath.Prob(ndof * chi, ndof)
