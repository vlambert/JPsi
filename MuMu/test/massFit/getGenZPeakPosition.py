from ROOT import *

## Find the peak position of Yong's BWxCB fit to gen level m(ee)
## http://www.hep.caltech.edu/~yongy/Zmumu_gen.gif
w = RooWorkspace("w", "w")

## Add pdf's to the workspace
w.factory("BreitWigner::bw(mass[40,150],bwMean[91.1876],bwWidth[2.4952])")
w.factory("CBShape::cb(mass,cbBias[0.30],cbSigma[0.3],cbCut[1.47],cbPower[1.08])")
w.factory("FFTConvPdf::BWxCB(mass,bw,cb)")
w.var("mass").setBins(1000000, "fft")
w.factory("Exponential::bg(mass,expRate[-0.0853])")

## RooAddPdf is a little tricky, the following line doesn't work
# w.factory("AddPdf::model({BWxCB, bg},{nsig[27960],nbkg[2476]})")

## Start a workaround for the S+B model
pdf_list = RooArgList(w.pdf("BWxCB"), w.pdf("bg"))
w.factory("{nsig[27960],nbkg[2476]}")
coeff_list = RooArgList(w.var("nsig"), w.var("nbkg"))
model = RooAddPdf("model", "s+b", pdf_list, coeff_list)

## Import the model to the workspace too
setattr(w, "Import", getattr(w, "import"))
w.Import(model)

## Export the mass and model to the interpreter
mass = w.var("mass")
model = w.pdf("model")

## Make a plot of the mass
plot = mass.frame()
model.plotOn(plot, RooFit.Range(90,92))
plot.Draw()
