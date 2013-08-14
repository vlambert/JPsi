import ROOT
import JPsi.MuMu.common.roofit as roofit
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.cmsstyle as cmsstyle
import JPsi.MuMu.common.energyScaleChains as esChains

## Define the model
w = ROOT.RooWorkspace('w', 'w')

## Dimuon mass in terms of m(mmg) and m(mg)'s
mmMassFunc = w.factory('''FormulaVar::mmMassFunc(
    "sqrt(mmgMass^2 - m1gOplusM2g^2)",
    {mmgMass[0,200], m1gOplusM2g[0,200]}
    )''')

## Breit-Wigner modelling Z-lineshape
zmmGenShape = w.factory('''BreitWigner::zmmGenShape(mmMass[20,200],
                                                    MZ[91.2], GZ[2.5])''')
## Dimuon mass resolution
mmMassRes = w.factory('''Gaussian::mmMassRes(mmMass,
                                             mmScale[0,-10,10],
                                             mmRes[1.5,0.1,10])''')

## Model for the reconstructed dimuon invariant mass
mmMass = w.var('mmMass')
mmMass.setBins(1000, 'fft')
# mmMassPdf = w.factory('FCONV::mmMassPdf(mmMass, zmmGenShape, mmMassRes)')
mmMassPdf = w.factory('''Voigtian::mmMassPdf(mmMass,
                                             FormulaVar::mmMean("MZ+mmScale",
                                                                {MZ,mmScale}),
                                             GZ, mmRes)''')
## Get data
chains = esChains.getChains('v11')
weight = w.factory('dummyWeight[1,0,55]')
weight.SetTitle('1')

mmgMass = w.var('mmgMass')
m1gOplusM2g = w.var('m1gOplusM2g')
m1gOplusM2g.SetTitle('sqrt(mmgMass^2-mmMass^2)')

isrData = dataset.get(tree=chains['z'], variable=mmMass, weight=weight,
                      cuts=['!isFSR', 'mmgMass < 200', 'mmMass < 200',
                            'phoPt > 15', 'Entry$ < 500000'])
mmgMassIsrData = dataset.get(variable=mmgMass)
m1gOplusM2gIsrData = dataset.get(variable=m1gOplusM2g)

isrData.merge(mmgMassIsrData, m1gOplusM2gIsrData)

## Fit the model to the data
mmMassPdf.fitTo(isrData, roofit.Range(60,120))

## Plot the data and the fit
mmPlot = mmMass.frame(roofit.Range(60,120))
isrData.plotOn(mmPlot)
mmMassPdf.plotOn(mmPlot)
canvases.next('mmMass')
mmPlot.Draw()

## Model for the reconstructed mmg mass of the ISR through transformation
# mmgMassIsrPdf = ROOT.RooFFTConvPdf('mmgMassIsrPdf', 'mmgMassIsrPdf', mmMassFunc,
#                                    mmMass, zmmGenShape, mmMassRes)
mmgMassPdf = w.factory('Voigtian::mmgMassPdf(mmMassFunc, mmMean, GZ, mmRes)')

## Plot the mmg mass data and model overlaid without fitting (!)
mmgPlot = mmgMass.frame(roofit.Range(60,200))
isrData.plotOn(mmgPlot)
isrData_m1gOplusM2g = isrData.reduce(ROOT.RooArgSet(m1gOplusM2g))
isrData_m1gOplusM2g_binned = isrData_m1gOplusM2g.binnedClone()
isrData_m1gOplusM2g.get().find('m1gOplusM2g').setBins(40)
isrData_m1gOplusM2g_binned2 = isrData_m1gOplusM2g.binnedClone()

# mmgMassPdf.plotOn(mmgPlot, roofit.ProjWData(isrData_m1gOplusM2g),
#                  roofit.LineColor(ROOT.kRed))
mmgMassPdf.plotOn(mmgPlot, roofit.ProjWData(isrData_m1gOplusM2g_binned),
                  roofit.LineColor(ROOT.kRed))
mmgMassPdf.plotOn(mmgPlot, roofit.ProjWData(isrData_m1gOplusM2g_binned2),
                  roofit.LineStyle(ROOT.kDashed))
canvases.next('mmgMass')
mmgPlot.Draw()

for c in canvases.canvases:
    c.Update()

canvases.make_plots()

if __name__ == '__main__':
    import user

