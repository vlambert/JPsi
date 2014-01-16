'''
Fit plots of energy resolution vs pt for monte carlo truth from 2012 Vecbos
ntuples run with PHOSPHOR method.

28 August 2013 Valere Lambert
'''

import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.cmsstyle as cmsstyle
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.xychi2fitter as xychi2fitter
from JPsi.MuMu.common.xychi2fitter import XYChi2Fitter as Fitter

_filename  = 'testtruth.root'
# _filename  = '/Users/veverka/Work/Data/phosphor/resDataVsPt_HggV2Ression_NoMuonBias_EGMPaperCategories.root'

_stochastic_from_tb = 3.
_noise_from_tb      = 21.
_mean_cosh_eta_barrel  = 1.37
_mean_cosh_eta_endcaps = 3.70
_mean_sqrt_cosh_eta_barrel  = 1.16
_mean_sqrt_cosh_eta_endcaps = 1.91
fitters = []

ROOT.RooAbsReal.defaultIntegratorConfig().setEpsAbs(1e-08)
ROOT.RooAbsReal.defaultIntegratorConfig().setEpsRel(1e-08)



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

    report_noise_terms()
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
        graphname = 'regressions_restruth_EB_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_LowNV_HighR9',
        title     = 'Barrel NVtx < 19 R_{9}^{#gamma} > 0.94, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter


    #__________________________________________________________________________
    ## S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_LowNV_HighR9_SfromTB',
        title     = 'Barrel NVtx < 19 R_{9}^{#gamma} > 0.94, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #__________________________________________________________________________
    ## N from TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_LowNV_HighR9_NfromTB',
        title     = 'Barrel NVtx < 19 R_{9}^{#gamma} > 0.94, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_barrel)
    fitter.C.setVal(ebfitter.C.getVal())

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
        graphname = 'regressions_restruth_EB_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_HighNV_HighR9',
        title     = 'Barrel NVtx > 18 R_{9}^{#gamma} > 0.94, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter


    #__________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_HighNV_HighR9_SfromTB',
        title     = 'Barrel NVtx > 18 R_{9}^{#gamma} > 0.94, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #__________________________________________________________________________
    ## Fix N to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_HighNV_HighR9_NfromTB',
        title     = 'Barrel NVtx > 18 R_{9}^{#gamma} > 0.94, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_barrel)
    fitter.C.setVal(ebfitter.C.getVal())

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
        graphname = 'regressions_restruth_EB_sixie_LowNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_LowNV_LowR9',
        title     = 'Barrel NVtx < 19 R_{9}^{#gamma} < 0.94, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter


    #__________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_LowNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_LowNV_LowR9_SfromTB',
        title     = 'Barrel NVtx < 19 R_{9}^{#gamma} < 0.94, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #__________________________________________________________________________
    ## Fix N to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_LowNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_LowNV_LowR9_NfromTB',
        title     = 'Barrel NVtx < 19 R_{9}^{#gamma} < 0.94, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_barrel)
    fitter.C.setVal(ebfitter.C.getVal())

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
        graphname = 'regressions_restruth_EB_sixie_HighNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_HighNV_LowR9',
        title     = 'Barrel NVtx > 18 R_{9}^{#gamma} < 0.94, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter

    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_HighNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_HighNV_LowR9_SfromTB',
        title     = 'Barrel NVtx > 18 R_{9}^{#gamma} < 0.94, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix N to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_HighNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_HighNV_LowR9_NfromTB',
        title     = 'Barrel NVtx > 18 R_{9}^{#gamma} < 0.94, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_barrel)
    fitter.C.setVal(ebfitter.C.getVal())

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
        graphname = 'regressions_restruth_EE_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_LowNV_HighR9',
        title     = 'Endcaps NVtx < 19 R_{9}^{#gamma} > 0.94, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter

    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_LowNV_HighR9_SfromTB',
        title     = 'Endcaps NVtx < 19 R_{9}^{#gamma} > 0.94, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix N to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_LowNV_HighR9_NfromTB',
        title     = 'Endcaps NVtx < 19 R_{9}^{#gamma} > 0.94, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(eefitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_endcaps)
    fitter.C.setVal(eefitter.C.getVal())

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
        graphname = 'regressions_restruth_EE_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_HighNV_HighR9',
        title     = 'Endcaps NVtx > 18 R_{9}^{#gamma} > 0.94, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter

    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_HighNV_HighR9_SfromTB',
        title     = 'Endcaps NVtx > 18 R_{9}^{#gamma} > 0.94, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)

    #______________________________________________________________________________
    ## Fix N to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_HighNV_HighR9_NfromTB',
        title     = 'Endcaps NVtx > 18 R_{9}^{#gamma} > 0.94, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(eefitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_endcaps)
    fitter.C.setVal(eefitter.C.getVal())

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
        graphname = 'regressions_restruth_EE_sixie_LowNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_LowNV_LowR9',
        title     = 'Endcaps NVtx < 19 R_{9}^{#gamma} < 0.94, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter
    

    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_LowNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_LowNV_LowR9_SfromTB',
        title     = 'Endcaps NVtx < 19 R_{9}^{#gamma} < 0.94, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    

    #______________________________________________________________________________
    ## Fix N to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_LowNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_LowNV_LowR9_NfromTB',
        title     = 'Endcaps NVtx < 19 R_{9}^{#gamma} < 0.94, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(eefitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_endcaps)
    fitter.C.setVal(eefitter.C.getVal())
    
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
        graphname = 'regressions_restruth_EE_sixie_HighNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_HighNV_LowR9',
        title     = 'Endcaps NVtx > 18 R_{9}^{#gamma} < 0.94, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter
    
    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_HighNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_HighNV_LowR9_SfromTB',
        title     = 'Endcaps NVtx > 18 R_{9}^{#gamma} < 0.94, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix N to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_HighNV_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_HighNV_LowR9_NfromTB',
        title     = 'Endcaps NVtx > 18 R_{9}^{#gamma} < 0.94, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(eefitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_endcaps)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
       
## End do_endcap_lowr9_highnv_fits()
#==============================================================================

def do_barrel_lowr9_fits():
    '''
    Barrel Low R9 
    '''
    
    systematics = 0.2
    #__________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_LowR9',
        title     = 'Barrel R_{9}^{#gamma} < 0.94, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter
    
    
    #__________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_LowR9_SfromTB',
        title     = 'Barrel R_{9}^{#gamma} < 0.94, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    
    #__________________________________________________________________________
    ## Fix N to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_LowR9_NfromTB',
        title     = 'Barrel R_{9}^{#gamma} < 0.94, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_barrel)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    ## End of do_barrel_lowr9_fits()
    
    #==============================================================================
    
    
def do_barrel_highr9_fits():
    '''
    Barrel High R9
    '''
    
    systematics = 0.2
    #__________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_HighR9',
        title     = 'Barrel R_{9}^{#gamma} > 0.94, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter
    
    
    #__________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_HighR9_SfromTB',
        title     = 'Barrel R_{9}^{#gamma} > 0.94, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    
    #__________________________________________________________________________
    ## Fix N to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_HighR9_NfromTB',
        title     = 'Barrel R_{9}^{#gamma} > 0.94, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_barrel)
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    ## End of do_barrel_highr9_fits()
    #==============================================================================                                                                                        

def do_endcap_lowr9_fits():
    '''
    End Cap Low R9
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_LowR9',
        title     = 'Endcaps R_{9}^{#gamma} < 0.94, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter
    
    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_LowR9_SfromTB',
        title     = 'Endcaps R_{9}^{#gamma} < 0.94, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
                                                                    ## Fix N to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_R9Low_0_R9High_0.94_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_LowR9_NfromTB',
        title     = 'Endcaps R_{9}^{#gamma} < 0.94, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(eefitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_endcaps)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    
    ## End do_endcap_lowr9_fits()
    #==============================================================================
def do_endcap_highr9_fits():
    '''
    End Cap High R9
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_HighR9',
        title     = 'Endcaps R_{9}^{#gamma} > 0.94, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter
    
    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_HighR9_SfromTB',
        title     = 'Endcaps R_{9}^{#gamma} > 0.94, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix N to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_HighR9_NfromTB',
        title     = 'Endcaps  R_{9}^{#gamma} > 0.94, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(eefitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_endcaps)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    
    ## End do_endcap_highr9_fits()
    #==============================================================================
    
def do_barrel_lownv_fits():
    '''
    Barrel Low NV
    '''
    systematics = 0.2
    #__________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_LowNV',
        title     = 'Barrel NVtx < 19, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter
    
    
    #__________________________________________________________________________
    ## S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_LowNV_SfromTB',
        title     = 'Barrel NVtx < 19, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    
    #__________________________________________________________________________
    ## N from TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_LowNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_LowNV_NfromTB',
        title     = 'Barrel NVtx < 19, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_barrel)
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    ## End of do_barrel_highr9_lownv_fits()
    
    
    #==============================================================================
    

    
def do_barrel_highnv_fits():
    '''
    Barrel High NV
    '''
    systematics = 0.2
    #__________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_HighNV',
        title     = 'Barrel NVtx > 19, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter
    
    
    #__________________________________________________________________________
    ## S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_HighNV_R9Low_0.94_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_HighNV_SfromTB',
        title     = 'Barrel NVtx > 19, MC Truth, S from TB',
        systematics = systematics,
                                                        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)

    
    #__________________________________________________________________________
    ## N from TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EB_sixie_HighNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_HighNV_NfromTB',
        title     = 'Barrel NVtx > 19, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_barrel)
    fitter.C.setVal(ebfitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    ## End of do_barrel_highnv_fits()
    
    
    #==============================================================================
    

def do_endcap_lownv_fits():
    '''
    End Cap Low NV
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_LowNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_LowNV',
        title     = 'Endcaps NVtx < 18, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter
    
    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_LowNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_LowNV_SfromTB',
        title     = 'Endcaps NVtx < 18, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix N to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_LowNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_LowNV_NfromTB',
        title     = 'Endcaps NVtx < 18, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(eefitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_endcaps)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    
    ## End do_endcap_lownv_fits()
    #==============================================================================
    
def do_endcap_highnv_fits():
    '''
    End Cap High NV
    '''
    systematics = 0.2
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_HighNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_HighNV',
        title     = 'Endcaps NVtx > 18, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter
    
    #______________________________________________________________________________
    

    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_HighNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_HighNV_SfromTB',
        title     = 'Endcaps NVtx > 18, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    #______________________________________________________________________________
    ## Fix N to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restruth_EE_sixie_HighNV_R9Low_0_R9High_999_sixie',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_HighNV_NfromTB',
        title     = 'Endcaps NVtx > 18, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(eefitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_endcaps)
    fitter.C.setVal(eefitter.C.getVal())
    
    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
    
    
    ## End do_endcap__highnv_fits()
    #================================================================================

def report_noise_terms():
    report = []
    for f in fitters:
        if 'SfromTB' not in f.name:
            continue
        print f.title, ': ',
        f.N.Print()
        text = '_noise_from_mc'
        if 'Barrel' in f.name:
            text += '_barrel'
        else:
            text += '_endcaps'
        if 'HighR9' in f.name:
            text += '_highr9'
        elif 'LowR9' in f.name:
            text += '_lowr9'
        if 'HighNV' in f.name:
            text += '_highnv'    
        elif 'LowNV' in f.name:
            text += '_lownv'
        text += ' = %.4g # +/- %.4g' % (f.N.getVal(), f.N.getError())
        report.append(text)
        print '\n'.join(report)
## End of report_noise_terms()
#================================================================================                
if __name__ == '__main__':
    main()
    import user
