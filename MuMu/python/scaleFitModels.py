"""Defines PDF's for the energy scale extraction from fit to s = E_reco/E_kin
using the Z->mumugamma FSR events.  Models are stored in a workspace together
with argument lists of observables (only s), parameters and snapshots of
their initial values. Supported models (instance names in brackets):
  * Crystal-Ball Line Shape (cbShape, model)
  * Cruijff (cruijff)
  * Bifurcated Gaussian (bifurGauss)
  * (Normal) Gaussian
  * Log-Normal

The parameter argument set and inital snapshots are stored as
`parameters_<model name>' and `initial_<model name>' where <model name>
is the name used above.

Plan to implement, Log-Normal, Bifurcated Log-Normal and Gamma
distributions.
"""

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *

## Load custom models
gSystem.Load('libJPsiMuMu')

## Define the workspace
ws1 = RooWorkspace( 'ws1', 'mmg energy scale' )

## Define the quantity to be fitted and the event weight
s = RooRealVar( 's', '100 * (1/kRatio - 1)', -100, 100, '%' )
mmgMass = RooRealVar( 'mmgMass', 'mmgMass', 60, 120, 'GeV' )
# w = RooRealVar( 'w', 'pileup.weight', 0, 99 )
w = RooRealVar( 'w', '1', 0, 99 )

smw = RooArgSet(s, mmgMass, w)
ws1.Import(smw)

## Variables for models of s and mass
ws1.factory('''{
    #Deltas[0, -50, 50],
    #Deltas2[0, -50, 50],
    #Deltas3[0, -50, 50],
    #mu[0, -50, 50],
    #sigma[20, 0.1, 100],
    #sigma2[30, 0.1, 100],
    #sigma3[40, 0.1, 100],
    #sigmaL[20, 0.2, 100],
    #sigmaR[20, 0.2, 100],
    #alpha[-1.5, -10, 0],
    #alphaL[10, 0.2, 100],
    #alphaR[10, 0.2, 100],
    n[1.5, 0.1, 10],
    ln#gamma[3,0.001,20],
    t[-1.5,-3.1415,10],
    tL[-1.5,-3.1415,10],
    tR[-1.5,-3.1415,10],
    Ns[100, 0.1, 9999999],
    Nb[100, 0.1, 9999999],
    N1[100, 0.1, 9999999],
    N2[100, 0.1, 9999999],
    N3[100, 0.1, 9999999],
    N[100, 0.1, 9999999]
}''')

## Functions for models of s
ws1.factory('''{
    FormulaVar::ik("1+s/100", {s}),
    FormulaVar::k("1+#sigma/100", {#sigma}),
    FormulaVar::m0("(1+#Deltas/100)*pow(k,log(k))", {#Deltas, k}),
    FormulaVar::#gamma("exp(ln#gamma)", {ln#gamma}),
    FormulaVar::#beta("#sigma/(100*sqrt(#gamma))", {#sigma, #gamma}),
    FormulaVar::#nu("1+#Deltas/100-#beta*(#gamma-1)", {#Deltas, #beta, #gamma}),
    FormulaVar::ik_gamma("max(#nu, 1+s/100)", {#nu, s})
}''')

sModels = [
    ## For backward compatibility
    ws1.factory('Gaussian::gauss(s, #Deltas, #sigma)'),
    ws1.factory('Gaussian::gauss2(s, #Deltas2, #sigma2)'),
    ws1.factory('Gaussian::gauss3(s, #Deltas3, #sigma3)'),
    ## Same notation as in the AN
    ws1.factory('Gaussian::gauss_an(s, #mu, #sigma)'),
    ws1.factory('Lognormal::lognormal(ik, m0, k)'),
    ws1.factory('BifurGauss::model(s, #Deltas, #sigmaL, #sigmaR)'),
    ws1.factory('CBShape::cbShape(s, #Deltas, #sigma, #alpha, n)'),
    ws1.factory('CBShape::cbShape_an(s, #mu, #sigma, #alpha, n)'),
    ## Didn't figure out how to compile new models in FWLite yet.
    ## Comment this out to be able to run on FWLite
    ws1.factory('''RooCruijff::cruijff(s, #Deltas, #sigmaL, #sigmaR, #alphaL,
                                       #alphaR)'''),
    ws1.factory('BifurGauss::bifurGauss(s, #Deltas, #sigmaL, #sigmaR)'),
    ws1.factory('BifurGauss::bifurGauss_an(s, #mu, #sigmaL, #sigmaR)'),
    ws1.factory('Gamma::gamma(ik_gamma, #gamma, #beta, #nu)'),
    ## Custom PDF's
    ws1.factory('RooBifurGshPdf::bifurGsh(s, #Deltas, #sigmaL, tL, #sigmaR, tR)'),
    ws1.factory('RooBifurSechPdf::bifurSech(s, #Deltas, #sigmaL, #sigmaR)'),
    ws1.factory('RooGshPdf::gsh(s, #Deltas, #sigma, t)'),
    ws1.factory('RooSechPdf::sech(s, #Deltas, #sigma)'),
    ws1.factory('BreitWigner::bw(s, #Deltas, #sigma)'),
    ## TODO: finish the extended bifur. GSH
    ws1.factory('ExtendPdf::eBifurGsh(bifurGsh, N)'),
    ## Sum models
    ws1.factory('SUM::sumGaussGauss(N1*gauss, N2*gauss2)'),
    ws1.factory('SUM::sumCruijffGauss(N1*cruijff, N2*gauss2)'),
    ws1.factory('SUM::sumBwGauss(N1*bw, N2*gauss2)'),
    ws1.factory('SUM::sumGauss3(N1*gauss, N2*gauss2, N3*gauss3)'),
] ## end of models definition

massModels = [
    ## PDF's for invariant mass fit
    ws1.factory('''
        FCONV::signal( mmgMass,
                       BreitWigner::zlinebw( mmgMass,
                                             mZ[91.1876],
                                             #GammaZ[2.4952] ),
                       CBShape::cb( mmgMass,
                                    #Deltam[0, -10, 10],
                                    #sigmaCB[1.5, 0.1, 10],
                                    #alphaCB[1.5, 0.1, 10],
                                    nCB[1.5, 0.1, 20] ) )
    '''),
    ws1.factory('''
        Exponential::background( mmgMass, #alphaB[-0.1, -10, 1] )
    '''),
    ws1.factory('''
        SUM::m3Model( Ns * signal,
                      Nb * background )
    '''),

]

ws1.pdf('signal').setBufferFraction(0.25)

## Define observables
sObservables = RooArgSet(s)
massObservables = RooArgSet(mmgMass)

## Define parameters for model
for x, models in [ (sObservables, sModels),
                   (massObservables, massModels) ]:
    for m in models:
        parameters = m.getParameters(x)
        ws1.defineSet(m.GetName() + '_params', parameters)
        ws1.saveSnapshot(m.GetName() + '_init', parameters, True)

if __name__ == '__main__':
    import user
