"""
rangesafekeyspdf - The Range-Safe KEYS PDF.

This module defines the class RangeSafeKeysPdf which implements a
RooAbsPdf resulting from restricting the range of the observable
based on the training range.

The observable may be extended for the training to guarantee vanishing
tails.  This is controlled by the rangebuf parameter.  It is the fraction
of the full range that is added to both sides.  The default value is 0.
This feature is not implemented yet.

Jan Veverka, Caltech, 13 January 2012
"""

import ROOT
import JPsi.MuMu.common.roofit as roo


##------------------------------------------------------------------------------
class RangeSafeKeysPdf(ROOT.RooKeysPdf):
    '''Restrict the range of the observable for the KEYS PDF evaluation
    to a range based on the range used for the training.'''

    def __init__(self, name, title, x, data,
                 mirror=ROOT.RooKeysPdf.NoMirror, rho=1., rangebuf=0.0):

        self.shape = ROOT.RooKeysPdf(name + '_shape', title + ' shape', x, data,
                                     mirror, rho)

        ## Restrict the allowed x values to the range where the
        ## PDF was trained.
        ## TODO: Use a custom compiled class for this instead of the
        ## interpreted RooFormulaVar.
        self.rangerestriction = ROOT.RooFormulaVar(
            '_'.join([name, x.GetName(), 'rangerestriction']),
            ''.join(['Range Restriction of ', x.GetTitle(),
                     ' in ', title]),
            ''.join(['{lo} * ({x} <= {lo}) + ',
                     '{x} * ({lo} < {x} & {x} < {hi}) + ',
                     '{hi} * ({hi} <= {x})']).format(x=x.GetName(),
                                                     lo=x.getMin(),
                                                     hi=x.getMax()),
            ROOT.RooArgList(x)
            )

        self.customizer = ROOT.RooCustomizer(self.shape, 'range')
        self.customizer.replaceArg(x, self.rangerestriction)

        ROOT.RooKeysPdf.__init__(self, self.customizer.build())
        self.SetName(name)
        self.SetTitle(title)
    ## end of __init__
## end of RangeSafeKeysPdf
