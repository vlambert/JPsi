import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.cmsstyle as cmsstyle
import FWLite.Tools.canvases as canvases

from FWLite.Tools.xychi2fitter import XYChi2Fitter as Fitter

_filename  = '/home/veverka/data/resMC1of4VsPt_HggV2Ression_NoMuonBias_EGMPaperCategories.root'
#_filename  = '/Users/veverka/Work/Data/phosphor/resMC1of4VsPt_HggV2Ression_NoMuonBias_EGMPaperCategories.root'
_stochastic_from_tb = 3.

_noise_from_mc_barrel_allr9   = 44.13 # +/- 1.117
_noise_from_mc_barrel_highr9  = 18.27 # +/- 0.7555
_noise_from_mc_barrel_lowr9   = 76.07 # +/- 1.294
_noise_from_mc_endcaps_allr9  = 77.14 # +/- 1.525
_noise_from_mc_endcaps_highr9 = 27.55 # +/- 1.694
_noise_from_mc_endcaps_lowr9  = 94.09 # +/- 1.907

fitters = []

#==============================================================================
def main():
    '''
    Main entry point of execution
    '''
    do_barrel_allr9_fits()
    do_barrel_highr9_fits()
    do_barrel_lowr9_fits()
    do_endcap_allr9_fits()
    # do_endcap_highr9_fits() # crashes since some fits don't converge
    do_endcap_lowr9_fits()
## End of main().


#==============================================================================
def do_barrel_allr9_fits():
    '''
    B A R R E L   A L L   R 9
    '''
    systematics = 0.5
    #__________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_allR9',
        title     = 'Barrel, MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter


    #__________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_allR9_SfromTB',
        title     = 'Barrel, MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/1.16)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #__________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_allR9_NfromMC',
        title     = 'Barrel, MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/1.16)
    fitter.N.setVal(_noise_from_mc_barrel_allr9)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)

    #__________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_allR9_SfromTB_NfromMC',
        title     = 'Barrel, MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/1.16)
    fitter.N.setVal(_noise_from_mc_barrel_allr9)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_barrel_allr9_fits()


#==============================================================================
def do_barrel_highr9_fits():
    '''
    B A R R E L   H I G H   R 9
    '''

    systematics = 0.2
    #__________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_highR9',
        title     = 'Barrel, R9 > 0.94, MC Fit',
        systematics = systematics,
        yrange    = (-1, 6),
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter


    #__________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_highR9_SfromTB',
        title     = 'Barrel, R9 > 0.94, MC Fit, S from TB',
        systematics = systematics,
        yrange    = (-1, 6),
        )
    fitter.S.setVal(_stochastic_from_tb/1.16)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #__________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_highR9_NfromMC',
        title     = 'Barrel, R9 > 0.94, MC Fit, N from MC',
        systematics = systematics,
        yrange    = (-1, 6),
        )
    fitter.S.setVal(_stochastic_from_tb/1.16)
    fitter.N.setVal(_noise_from_mc_barrel_highr9)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)

    #__________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_highR9_SfromTB_NfromMC',
        title     = 'Barrel, R9 > 0.94, MC Fit, S from TB, N from MC',
        systematics = systematics,
        yrange    = (-1, 6),
        )
    fitter.S.setVal(_stochastic_from_tb/1.16)
    fitter.N.setVal(_noise_from_mc_barrel_highr9)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_barrel_highr9_fits()


#==============================================================================
def do_barrel_lowr9_fits():
    '''
    B A R R E L   L O W   R 9
    '''

    systematics = 0.5
    #__________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_lowR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_lowR9',
        title     = 'Barrel, R9 < 0.94, MC Fit',
        systematics = systematics,
        yrange    = (-1, 20),
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter


    #__________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_lowR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_lowR9_SfromTB',
        title     = 'Barrel, R9 < 0.94, MC Fit, S from TB',
        systematics = systematics,
        # yrange    = (-1, 6),
        )
    fitter.S.setVal(_stochastic_from_tb/1.16)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #__________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_lowR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_lowR9_NfromMC',
        title     = 'Barrel, R9 < 0.94, MC Fit, N from MC',
        systematics = systematics,
        # yrange    = (-1, 6),
        )
    fitter.S.setVal(_stochastic_from_tb/1.16)
    fitter.N.setVal(_noise_from_mc_barrel_lowr9)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)

    #__________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_lowR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_lowR9_SfromTB_NfromMC',
        title     = 'Barrel, R9 < 0.94, MC Fit, S from TB, N from MC',
        systematics = systematics,
        # yrange    = (-1, 6),
        )
    fitter.S.setVal(_stochastic_from_tb/1.16)
    fitter.N.setVal(_noise_from_mc_barrel_lowr9)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_barrel_lowr9_fits()


#==============================================================================
def do_endcap_allr9_fits():
    '''
    E N D C A P S   A L L   R 9
    '''
    systematics = 1.0
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_allR9',
        title     = 'Endcaps, MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter

    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_allR9_SfromTB',
        title     = 'Endcaps, MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/1.91)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_allR9_NfromMC',
        title     = 'Endcaps, MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/1.91)
    fitter.N.setVal(_noise_from_mc_endcaps_allr9)
    fitter.C.setVal(eefitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_allR9_SfromTB_NfromMC',
        title     = 'Endcaps, MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/1.91)
    fitter.N.setVal(_noise_from_mc_endcaps_allr9)
    fitter.C.setVal(eefitter.C.getVal())

    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_endcap_allr9_fits()


#==============================================================================
def do_endcap_highr9_fits():
    '''
    E N D C A P S   H I G H   R 9
    '''
    systematics = 1.0
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_highR9',
        title     = 'Endcaps, R9 > 0.95, MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter

    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_highR9_SfromTB',
        title     = 'Endcaps, R9 > 0.95, MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/1.91)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_highR9_NfromMC',
        title     = 'Endcaps, R9 > 0.95, MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/1.91)
    fitter.N.setVal(_noise_from_mc_endcaps_highr9)
    fitter.C.setVal(eefitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_highR9_SfromTB_NfromMC',
        title     = 'Endcaps, R9 > 0.95, MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/1.91)
    fitter.N.setVal(_noise_from_mc_endcaps_highr9)
    fitter.C.setVal(eefitter.C.getVal())

    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_endcap_highr9_fits()


#==============================================================================
def do_endcap_lowr9_fits():
    '''
    E N D C A P S   L O W   R 9
    '''
    systematics = 1.0
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_lowR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_lowR9',
        title     = 'Endcaps, R9 < 0.95, MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter

    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_lowR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_lowR9_SfromTB',
        title     = 'Endcaps, R9 < 0.95, MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/1.91)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_lowR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_lowR9_NfromMC',
        title     = 'Endcaps, R9 < 0.95, MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/1.91)
    fitter.N.setVal(_noise_from_mc_endcaps_lowr9)
    fitter.C.setVal(eefitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_lowR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_lowR9_SfromTB_NfromMC',
        title     = 'Endcaps, R9 < 0.95, MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/1.91)
    fitter.N.setVal(_noise_from_mc_endcaps_lowr9)
    fitter.C.setVal(eefitter.C.getVal())

    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_endcap_lowr9_fits()


#==============================================================================
if __name__ == '__main__':
    main()
    import user
