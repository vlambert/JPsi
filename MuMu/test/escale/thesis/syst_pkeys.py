import ROOT


for variable in 'mode sigma'.split():
    for ndata, seed in zip('200 500 1k 2k'.split(),
                           '18  16  19 17'.split()):
        sourcename = 'response_fits_ntoys1k_ndata%s_rho1.5_seed%s.root' % (ndata, seed)
        sourcefile = ROOT.TFile.Open(sourcename)
        rms = sourcefile.Get('keys_%s_val' % variable).GetRMS()
        err = sourcefile.Get('keys_%s_err' % variable).GetMean()
        #rms = sourcefile.Get('gauss_%s_val' % variable).GetRMS()
        #err = sourcefile.Get('gauss_%s_err' % variable).GetMean()
        print '%(variable)6s  %(ndata)3s %(rms)5.3f %(err)5.3f' % locals(),
        print '%5.3f' % (rms/err)
        sourcefile.Close()
