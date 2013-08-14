from ROOT import *

def bwPlusExpModel(ws):
    bw = ws.factory("BreitWigner::bw(m[20,200],M[91.19],Gamma[2.49])")
    exp = ws.factory("Exponential::exp(m, lambda[-0.1, -10, 1])")
    return ws.factory("AddPdf::model(bw, exp, fbw[0.95, 0, 1])")

def rbwPlusExpModel(ws):
    ## do the relativistic breit-wigner here
    frbw0 = TF1("frbw0", "1/(pow(x*x - [0]*[0], 2) + [0]*[0]*[1]*[1])", 20, 200)
#     frbw2 = TF1("frbw2", "1/(pow(x*x - [0]*[0], 2) + x*x*[1]*[1])", 60, 120)
#     frbw4 = TF1("frbw4", "1/(pow(x*x - [0]*[0], 2) + x*x*x*x*[1]*[1]/([0]*[0]))", 60, 120)
    frbw0.SetParName(0, "M")
    frbw0.SetParName(1, "Gamma")
    rbw0 = RooFit.bindPdf(frbw0, m)


ws = RooWorkspace("ws")
model = bwPlusExpModel(ws)
m = ws.var("m")
data = RooDataSet.read("dimuonGenMass_Zmumu-powheg-Summer10.txt", RooArgList(m))

m.setRange(60,120)

model.fitTo(data)

plot = m.frame()
data.plotOn(plot)
model.plotOn(plot)
plot.Draw()
