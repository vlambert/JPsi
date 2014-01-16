'''
Fit plots of energy resolution vs pt for monte carlo from 2012 Vecbos
ntuples run with PHOSPHOR method.

28 August 2013 Valere Lambert
'''

import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.cmsstyle as cmsstyle
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.xychi2fitter import XYChi2Fitter as Fitter

_filename  = 'testmc.root'
# _filename  = '/Users/veverka/Work/Data/phosphor/resDataVsPt_HggV2Ression_NoMuonBias_EGMPaperCategories.root'
_stochastic_from_tb = 3.
_mean_sqrt_cosh_eta_barrel  = 1.16
_mean_sqrt_cosh_eta_endcaps = 1.91
#Enhanced Z+Jets
#_noise_from_mc_barrel_highr9_lownv = 23.87 # +/- 40.49
#_noise_from_mc_barrel_highr9_highnv = 26.54 # +/- 36.53
#_noise_from_mc_barrel_lowr9_lownv = 75.07 # +/- 34.27
#_noise_from_mc_barrel_lowr9_highnv = 79.69 # +/- 33.12
#_noise_from_mc_endcaps_highr9_lownv = 33.13 # +/- 43.96
#_noise_from_mc_endcaps_highr9_highnv = 34.2 # +/- 42.9
#_noise_from_mc_endcaps_lowr9_lownv = 89.12 # +/- 34.51
#_noise_from_mc_endcaps_lowr9_highnv = 99.94 # +/- 199.9
#_noise_from_mc_barrel_lowr9 = 76.32 # +/- 34.17
#_noise_from_mc_barrel_highr9 = 24.36 # +/- 39.73
#_noise_from_mc_endcaps_lowr9 = 92.11 # +/- 40.85
#_noise_from_mc_endcaps_highr9 = 33.46 # +/- 43.64
#_noise_from_mc_barrel_lownv = 23.87 # +/- 40.49
#_noise_from_mc_barrel_highnv = 26.54 # +/- 36.53
#_noise_from_mc_endcaps_lownv = 78.56 # +/- 32.27
#_noise_from_mc_endcaps_highnv = 94.48 # +/- 37.07

_noise_from_mc_barrel_highr9_lownv = 23.27 # +/- 40.83
_noise_from_mc_barrel_highr9_highnv = 26.5 # +/- 36.77
_noise_from_mc_barrel_lowr9_lownv = 74.61 # +/- 34.46
_noise_from_mc_barrel_lowr9_highnv = 78.93 # +/- 33.25
_noise_from_mc_endcaps_highr9_lownv = 33.37 # +/- 43.37
_noise_from_mc_endcaps_highr9_highnv = 34.43 # +/- 42.63
_noise_from_mc_endcaps_lowr9_lownv = 88.58 # +/- 34.74
_noise_from_mc_endcaps_lowr9_highnv = 99.56 # +/- 199.2
_noise_from_mc_barrel_lowr9 = 75.85 # +/- 34.18
_noise_from_mc_barrel_highr9 = 23.98 # +/- 39.49
_noise_from_mc_endcaps_lowr9 = 91.48 # +/- 37.9
_noise_from_mc_endcaps_highr9 = 33.83 # +/- 42.58
_noise_from_mc_barrel_lownv = 23.27 # +/- 40.83
_noise_from_mc_barrel_highnv = 26.5 # +/- 36.77
_noise_from_mc_endcaps_lownv = 78.04 # +/- 32.36
_noise_from_mc_endcaps_highnv = 93.37 # +/- 31.45

fitters = []

#==============================================================================
def main():
    '''
    Main entry point of execution
    '''

    do_barrel_highr9_lownv_fits()
    do_barrel_highr9_highnv_fits()
    do_barrel_lowr9_lownv_fits()
    do_barrel_lowr9_highnv_fits()
    do_endcap_highr9_lownv_fits()
    do_endcap_highr9_highnv_fits()
    do_endcap_lowr9_lownv_fits()
    do_endcap_lowr9_highnv_fits()

    do_barrel_lowr9_fits()
    do_barrel_highr9_fits()
    do_endcap_lowr9_fits()
    do_endcap_highr9_fits()
    
    do_barrel_lownv_fits()
    do_barrel_highnv_fits()
    do_endcap_lownv_fits()
    do_endcap_highnv_fits()
    
    canvases.make_plots("png eps root".split())
        
## End of main().


#==============================================================================
def do_barrel_highr9_lownv_fits():
    '''
    Barrel High R9 Low NV
    '''
    systematics = 0.2
    #__________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowNV_HighR9',
        title     = 'Barrel NVtx < 19 R_{9}^{#gamma} > 0.94, MC Fit',
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
        graphname = 'regressions_resmc_EB_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowNV_HighR9_SfromTB',
        title     = 'Barrel NVtx < 19 R_{9}^{#gamma} > 0.94, MC Fit, S from TB',
        systematics = systematics,
        yrange    = (-1 ,6),
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #__________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowNV_HighR9_NfromMC',
        title     = 'Barrel NVtx < 19 R_{9}^{#gamma} > 0.94, MC Fit, N from MC',
        systematics = systematics,
        yrange    = (-1 , 6),
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_highr9_lownv)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)

    #__________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowNV_HighR9_SfromTB_NfromMC',
        title     = 'Barrel NVtx < 19 R_{9}^{#gamma} > 0.94, MC Fit, S from TB, N from MC',
        systematics = systematics,
        yrange    = (-1 , 6),
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_highr9_lownv)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_barrel_highr9_lownv_fits()


#==============================================================================
def do_barrel_highr9_highnv_fits():
    '''
    Barrel High R9 High NV
    '''

    systematics = 0.2
    #__________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighNV_HighR9',
        title     = 'Barrel NVtx > 18 R_{9}^{#gamma} > 0.94, MC Fit',
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
        graphname = 'regressions_resmc_EB_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighNV_HighR9_SfromTB',
        title     = 'Barrel NVtx > 18 R_{9}^{#gamma} > 0.94, MC Fit, S from TB',
        systematics = systematics,
        yrange    = (-1, 6),
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #__________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighNV_HighR9_NfromMC',
        title     = 'Barrel NVtx > 18 R_{9}^{#gamma} > 0.94, MC Fit, N from MC',
        systematics = systematics,
        yrange    = (-1, 6),
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_highr9_highnv)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)

    #__________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighNV_HighR9_SfromTB_NfromMC',
        title     = 'Barrel NVtx > 18 R_{9}^{#gamma} > 0.94, MC Fit, S from TB, N from MC',
        systematics = systematics,
        yrange    = (-1, 6),
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_highr9_highnv)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_barrel_highr9_fits()


#==============================================================================
def do_barrel_lowr9_lownv_fits():
    '''
    Barrel Low R9 Low NV
    '''

    systematics = 0.2
    #__________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_LowNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowNV_LowR9',
        title     = 'Barrel NVtx < 19 R_{9}^{#gamma} < 0.94, MC Fit',
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
        graphname = 'regressions_resmc_EB_sixie_LowNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowNV_LowR9_SfromTB',
        title     = 'Barrel NVtx < 19 R_{9}^{#gamma} < 0.94, MC Fit, S from TB',
        systematics = systematics,
         yrange    = (-1, 20),
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #__________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_LowNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowNV_LowR9_NfromMC',
        title     = 'Barrel NVtx < 19 R_{9}^{#gamma} < 0.94, MC Fit, N from MC',
        systematics = systematics,
        yrange    = (-1, 20),
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_lowr9_lownv)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)

    #__________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_LowNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowNV_LowR9_SfromTB_NfromMC',
        title     = 'Barrel NVtx < 19 R_{9}^{#gamma} < 0.94, MC Fit, S from TB, N from MC',
        systematics = systematics,
        yrange    = (-1, 20),
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_lowr9_lownv)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_barrel_lowr9_fits()


#==============================================================================
def do_barrel_lowr9_highnv_fits():
    '''
    Barrel Low R9 High NV
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_HighNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighNV_LowR9',
        title     = 'Barrel NVtx > 18 R_{9}^{#gamma} < 0.94, MC Fit',
        systematics = systematics,
        yrange    = (-1, 20),
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter

    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_HighNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighNV_LowR9_SfromTB',
        title     = 'Barrel NVtx > 18 R_{9}^{#gamma} < 0.94, MC Fit, S from TB',
        systematics = systematics,
        yrange    = (-1 , 20),
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_HighNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighNV_LowR9_NfromMC',
        title     = 'Barrel NVtx > 18 R_{9}^{#gamma} < 0.94, MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_lowr9_highnv)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_HighNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighNV_LowR9_SfromTB_NfromMC',
        title     = 'Barrel NVtx > 18 R_{9}^{#gamma} < 0.94, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_lowr9_highnv)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_endcap_allr9_fits()


#==============================================================================
def do_endcap_highr9_lownv_fits():
    '''
    End Cap High R9 Low NV
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowNV_HighR9',
        title     = 'Endcaps NVtx < 19 R_{9}^{#gamma} > 0.94, MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter

    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowNV_HighR9_SfromTB',
        title     = 'Endcaps NVtx < 19 R_{9}^{#gamma} > 0.94, MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowNV_HighR9_NfromMC',
        title     = 'Endcaps NVtx < 19 R_{9}^{#gamma} > 0.94, MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_highr9_lownv)
    fitter.C.setVal(eefitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowNV_HighR9_SfromTB_NfromMC',
        title     = 'Endcaps NVtx < 19 R_{9}^{#gamma} > 0.94, MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_highr9_lownv)
    fitter.C.setVal(eefitter.C.getVal())

    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_endcap_highr9_fits()


#==============================================================================
def do_endcap_highr9_highnv_fits():
    '''
    End Cap High R9 High NV
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighNV_HighR9',
        title     = 'Endcaps NVtx > 18 R_{9}^{#gamma} > 0.94, MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter

    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighNV_HighR9_SfromTB',
        title     = 'Endcaps NVtx > 18 R_{9}^{#gamma} > 0.94, MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighNV_HighR9_NfromMC',
        title     = 'Endcaps NVtx > 18 R_{9}^{#gamma} > 0.94, MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_highr9_highnv)
    fitter.C.setVal(eefitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighNV_HighR9_SfromTB_NfromMC',
        title     = 'Endcaps NVtx > 18 R_{9}^{#gamma} > 0.94, MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_highr9_highnv)
    fitter.C.setVal(eefitter.C.getVal())

    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_endcap_lowr9_fits()


#==============================================================================

def do_endcap_lowr9_lownv_fits():
    '''
    End Cap Low R9 Low NV
    '''
    systematics = 0.2


    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_LowNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowNV_LowR9',
        title     = 'Endcaps NVtx < 19 R_{9}^{#gamma} < 0.94, MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter
    

    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_LowNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowNV_LowR9_SfromTB',
        title     = 'Endcaps NVtx < 19 R_{9}^{#gamma} < 0.94, MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    

    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_LowNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowNV_LowR9_NfromMC',
        title     = 'Endcaps NVtx < 19 R_{9}^{#gamma} < 0.94, MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_lowr9_lownv)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
                                
    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_LowNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowNV_LowR9_SfromTB_NfromMC',
        title     = 'Endcaps NVtx < 19 R_{9}^{#gamma} < 0.94, MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_lowr9_lownv)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    #______________________________________________________________________________
    
## End do_endcap_lowr9_lownv_fits()


def do_endcap_lowr9_highnv_fits():
    '''
    End Cap Low R9 High NV
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_HighNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighNV_LowR9',
        title     = 'Endcaps NVtx > 18 R_{9}^{#gamma} < 0.94, MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter
    
    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_HighNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighNV_LowR9_SfromTB',
        title     = 'Endcaps NVtx > 18 R_{9}^{#gamma} < 0.94, MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_HighNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighNV_LowR9_NfromMC',
        title     = 'Endcaps NVtx > 18 R_{9}^{#gamma} < 0.94, MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_lowr9_highnv)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_HighNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighNV_LowR9_SfromTB_NfromMC',
        title     = 'Endcaps NVtx > 18 R_{9}^{#gamma} < 0.94, MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_lowr9_highnv)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
## End do_endcap_lowr9_highnv_fits()


def do_barrel_lowr9_fits():
    '''
    Barrel Low R9
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowR9',
        title     = 'Barrel R_{9}^{#gamma} < 0.94, MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter
    

    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowR9_SfromTB',
        title     = 'Barrel R_{9}^{#gamma} < 0.94, MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowR9_NfromMC',
        title     = 'Barrel R_{9}^{#gamma} < 0.94, MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_lowr9)
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowR9_SfromTB_NfromMC',
        title     = 'Barrel R_{9}^{#gamma} < 0.94, MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_lowr9)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    ## End do_barrel_lowr9_fits()
    #================================================================================
                                                                                                        
def do_barrel_highr9_fits():
    
    '''
    Barrel High R9
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighR9',
        title     = 'Barrel R_{9}^{#gamma} > 0.94, MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter
    
    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighR9_SfromTB',
        title     = 'Barrel R_{9}^{#gamma} > 0.94, MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighR9_NfromMC',
        title     = 'Barrel R_{9}^{#gamma} > 0.94, MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_highr9)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighR9_SfromTB_NfromMC',
        title     = 'Barrel R_{9}^{#gamma} > 0.94, MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_highr9)
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)

    ## End do_barrel_highr9_fits()
    #================================================================================
    
    
def do_endcap_lowr9_fits():
    '''
    Endcaps Low R9
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowR9',
        title     = 'Endcaps R_{9}^{#gamma} < 0.94, MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter
    
    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowR9_SfromTB',
        title     = 'Endcaps R_{9}^{#gamma} < 0.94, MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowR9_NfromMC',
        title     = 'Endcaps R_{9}^{#gamma} < 0.94, MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_lowr9)
    fitter.C.setVal(eefitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    
    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowR9_SfromTB_NfromMC',
        title     = 'Endcaps R_{9}^{#gamma} < 0.94, MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_lowr9)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    ## End do_endcaps_lowr9_fits()
    #================================================================================
    
    
def do_endcap_highr9_fits():
    '''
    Endcaps High R9
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighR9',
        title     = 'Endcaps R_{9}^{#gamma} > 0.94, MC Fit',
        systematics = systematics,
                                                                                )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter
    
    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighR9_SfromTB',
        title     = 'Endcaps R_{9}^{#gamma} > 0.94, MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighR9_NfromMC',
        title     = 'Endcaps R_{9}^{#gamma} > 0.94, MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_highr9)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighR9_SfromTB_NfromMC',
        title     = 'Endcaps R_{9}^{#gamma} > 0.94, MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_highr9)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    ## End do_encap_highr9_fits()
    #================================================================================
    
    
def do_barrel_lownv_fits():
    
    '''
    Barrel  Low NV
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_LowNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowNV',
        title     = 'Barrel NVtx < 18 , MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter
    
    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_LowNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowNV_SfromTB',
        title     = 'Barrel NVtx < 18 , MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    
    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_LowNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowNV_NfromMC',
        title     = 'Barrel NVtx < 18 , MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_lownv)
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_LowNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_LowNV_SfromTB_NfromMC',
        title     = 'Barrel NVtx < 18 , MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_lownv)
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    ## End do_barrel_lownv_fits()
    
    
    
    #================================================================================
    
    
    
def do_barrel_highnv_fits():
    '''
    Barrel  High NV
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_HighNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighNV',
        title     = 'Barrel NVtx > 18 , MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter
    
    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_HighNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighNV_SfromTB',
        title     = 'Barrel NVtx > 18 , MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    
    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_HighNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighNV_NfromMC',
        title     = 'Barrel NVtx > 18 , MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_highnv)
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EB_sixie_HighNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Barrel_HighNV_SfromTB_NfromMC',
        title     = 'Barrel NVtx > 18 , MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(_noise_from_mc_barrel_highnv)
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    ## End do_barrel_highnv_fits()
    
    

    #================================================================================
    
    
def do_endcap_lownv_fits():
        
    '''
    End Cap Low NV
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_LowNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowNV',
        title     = 'Endcaps NVtx < 18 , MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter
    
    
    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_LowNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowNV_SfromTB',
        title     = 'Endcaps NVtx < 18 , MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_LowNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowNV_NfromMC',
        title     = 'Endcaps NVtx < 18 , MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_lownv)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_LowNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_LowNV_SfromTB_NfromMC',
        title     = 'Endcaps NVtx < 18 , MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_lownv)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    ## End do_endcap_lownv_fits()
    
    
    #================================================================================
    
    
def do_endcap_highnv_fits():
    
    '''
    End Cap High NV
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_HighNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighNV',
        title     = 'Endcaps NVtx > 18 , MC Fit',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter
    
    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_HighNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighNV_SfromTB',
        title     = 'Endcaps NVtx > 18 , MC Fit, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_HighNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighNV_NfromMC',
        title     = 'Endcaps NVtx > 18 , MC Fit, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_highnv)
    fitter.C.setVal(eefitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix S to TB and N to MC
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_resmc_EE_sixie_HighNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCFit_Endcaps_HighNV_SfromTB_NfromMC',
        title     = 'Endcaps NVtx > 18 , MC Fit, S from TB, N from MC',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_mc_endcaps_highnv)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    ## End do_endcap_highnv_fits()
                                                                    
#================================================================================

if __name__ == '__main__':
    main()
    import user
