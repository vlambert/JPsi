from makeFsrHistos import *
gROOT.LoadMacro("resolutionErrors.C")
# selAll  = lyonSel["all"] + "& 87 < mmgMass & mmgMass < 95"
# selFake = lyonSel["fake"] + "& 87 < mmgMass & mmgMass < 95"
selAll  = newSel["all"] + "& 87 < mmgMass & mmgMass < 95"
selFake = newSel["fake"] + "& 87 < mmgMass & mmgMass < 95"
ch.Draw("(zMassPdg()^2-mass[mm]^2)/(mmgMass^2-mass[mm]^2)>>hdata(40,0,2)",
  selAll
  )
chainMC.Draw("(zMassPdg()^2-mass[mm]^2)/(mmgMass^2-mass[mm]^2)>>hmc(40,0,2)",
  selAll
  )
chainMC.Draw("(zMassPdg()^2-mass[mm]^2)/(mmgMass^2-mass[mm]^2)>>hmcfake(40,0,2)",
  selFake
  )
hdata = gDirectory.Get("hdata")
hmc = gDirectory.Get("hmc")
hmcfake = gDirectory.Get("hmcfake")
hdata.SetStats(1)
hmc.SetStats(1)
hmc.Scale(2.798e-3)
hmcfake.Scale(2.798e-3)
hmc.Fit("gaus")
hdata.Fit("gaus")
# sdata = hdata.GetListOfFunctions().FindObject("stats")
# sdata.SetOptFit(1111)
# hdata.GetListOfFunctions().Remove(sdata)
# hdata.SetStats(0)
# smc = hmc.GetListOfFunctions().FindObject("stats")
# smc.SetOptFit(1111)
# hmc.GetListOfFunctions().Remove(smc)
# hmc.SetStats(0)
# hmc.Draw()
# hmcfake.SetStats(0)
hmcfake.Draw("same")
hdata.Draw("same")
sdata.Draw()
smc.Draw()
