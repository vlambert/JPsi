import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.cmsstyle as cmsstyle
import FWLite.Tools.canvases as canvases
import FWLite.Tools.xychi2fitter as xychi2fitter

from FWLite.Tools.xychi2fitter import XYChi2Fitter as Fitter

#==============================================================================
## Define global data attributes
_filename  = '/home/veverka/data/resTrueVsPt_HggV2Ression_NoMuonBias_EGMPaperCategories.root'
#_filename  = '/Users/veverka/Work/Data/phosphor/resTrueVsPt_HggV2Ression_NoMuonBias_EGMPaperCategories.root'
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
    do_barrel_allr9_fits()
    do_barrel_highr9_fits()
    do_barrel_lowr9_fits()
    do_endcap_allr9_fits()
    do_endcap_highr9_fits()
    do_endcap_lowr9_fits()
    report_noise_terms()
## End of main().


#==============================================================================
def do_barrel_allr9_fits():
    '''
    B A R R E L   A L L   R 9
    '''
    systematics = 0.1
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EB_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel',
        title     = 'Barrel, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter


    #______________________________________________________________________________
    ## S from TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EB_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_SfromTB',
        title     = 'Barrel, MC Truth, S from TB',
        systematics = systematics,
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #______________________________________________________________________________
    ## N from TB 
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EB_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_NfromTB',
        title     = 'Barrel, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_barrel)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_barrel_allr9_fits()


#==============================================================================
def do_barrel_highr9_fits():
    '''
    B A R R E L   H I G H   R 9
    '''
    systematics = 0.05
    
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EB_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_highR9',
        title     = 'Barrel, R9 > 0.94, MC Truth',
        systematics = systematics,
        yrange    = (-1, 5),
        )

    fitter.S.setVal(4.258)
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_barrel)
    fitter.C.setVal(0.5098)

    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter


    #______________________________________________________________________________
    ## S from TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EB_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_highR9_SfromTB',
        title     = 'Barrel, R9 > 0.94, MC Truth, S from TB',
        systematics = systematics,
        yrange    = (-1, 5),
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #______________________________________________________________________________
    ## N from TB 
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EB_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_highR9_NfromTB',
        title     = 'Barrel, R9 > 0.94, MC Truth, N from TB',
        systematics = systematics,
        yrange    = (-1, 5),
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_barrel)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_barrel_highr9_fits()


#==============================================================================
def do_barrel_lowr9_fits():
    '''
    B A R R E L   L O W   R 9
    '''
    systematics = 0.1
    
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EB_lowR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_lowR9',
        title     = 'Barrel, R9 < 0.94, MC Truth',
        systematics = systematics,
        # yrange    = (-1, 5),
        )

    fitter.S.setVal(4.258)
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_barrel)
    fitter.C.setVal(0.5098)

    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter


    #______________________________________________________________________________
    ## S from TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EB_lowR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_lowR9_SfromTB',
        title     = 'Barrel, R9 < 0.94, MC Truth, S from TB',
        systematics = systematics,
        # yrange    = (-1, 5),
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_barrel)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #______________________________________________________________________________
    ## N from TB 
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EB_lowR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_lowR9_NfromTB',
        title     = 'Barrel, R9 < 0.94, MC Truth, N from TB',
        systematics = systematics,
        # yrange    = (-1, 5),
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_barrel)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_barrel_lowr9_fits()


#==============================================================================
def do_endcap_allr9_fits():
    '''
    E N D C A P S   A L L   R 9
    '''

    systematics = 0.1

    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EE_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps',
        title     = 'Endcaps, MC Truth',
        systematics = systematics,
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter


    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EE_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_SfromTB',
        title     = 'Endcaps, MC Truth, S from TB',
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
        graphname = 'regressions_restrue_EE_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_NfromTB',
        title     = 'Endcaps, MC Truth, N from TB',
        systematics = systematics,
        )
    fitter.S.setVal(eefitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_endcaps)
    fitter.C.setVal(eefitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_endcap_allr9_fits()


#==============================================================================
def do_endcap_highr9_fits():
    '''
    E N D C A P S   H I G H   R 9
    '''

    systematics = 0.1
    
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EE_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_highR9',
        title     = 'Endcaps, R9 > 0.95, MC Truth',
        systematics = systematics,
        # yrange    = (-1, 5),
        )

    fitter.S.setVal(4.258)
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_endcaps)
    fitter.C.setVal(0.5098)

    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter


    #______________________________________________________________________________
    ## S from TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EE_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_highR9_SfromTB',
        title     = 'Endcaps, R9 > 0.95, MC Truth, S from TB',
        systematics = systematics,
        # yrange    = (-1, 5),
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #______________________________________________________________________________
    ## N from TB 
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EE_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_highR9_NfromTB',
        title     = 'Endcaps, R9 > 0.95, MC Truth, N from TB',
        systematics = systematics,
        # yrange    = (-1, 5),
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_endcaps)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_endcaps_highr9_fits()


#==============================================================================
def do_endcap_lowr9_fits():
    '''
    E N D C A P S   L O W   R 9
    '''

    systematics = 0.1
    
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EE_lowR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_lowR9',
        title     = 'Endcaps, R9 < 0.95, MC Truth',
        systematics = systematics,
        # yrange    = (-1, 5),
        )

    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_endcaps)
    fitter.C.setVal(0.5098)

    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter


    #______________________________________________________________________________
    ## S from TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EE_lowR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_lowR9_SfromTB',
        title     = 'Endcaps, R9 < 0.95, MC Truth, S from TB',
        systematics = systematics,
        # yrange    = (-1, 5),
        )
    fitter.S.setVal(_stochastic_from_tb/_mean_sqrt_cosh_eta_endcaps)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #______________________________________________________________________________
    ## N from TB 
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EE_lowR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_lowR9_NfromTB',
        title     = 'Endcaps, R9 < 0.95, MC Truth, N from TB',
        systematics = systematics,
        # yrange    = (-1, 5),
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/_mean_cosh_eta_endcaps)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_endcaps_highr9_fits()


#==============================================================================
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
        if 'highR9' in f.name:
            text += '_highr9'
        elif 'lowR9' in f.name:
            text += '_lowr9'
        else:
            text += '_allr9'
        text += ' = %.4g # +/- %.4g' % (f.N.getVal(), f.N.getError())
        report.append(text)
    print '\n'.join(report)
## End of report_noise_terms()


#==============================================================================
if __name__ == '__main__':
    main()
    import user
