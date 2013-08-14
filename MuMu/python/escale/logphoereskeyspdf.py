"""
logphoereskeyspdf - The log(photon Ereco/Egen) KEYS PDF.

This module defines the class LogPhoErecoOverEgenKeysPdf which implements a
RooAbsPdf resulting from a parametrization and transformation of the observable
of a RooKeysPdf.

The shape of the PDF is taken from the RooKeysPdf trained on the given
data of phoERes = 100 * (Ereco/Egen - 1).

The parametrization introduces dependence on the photon energy scale
and resolution phoERes -> s0 + (phoERes - s) * r0/r.
Here, the photon energy scale and resolution parameters are named
s and r, and the scale and resolution of the KEYS PDF shape trained
on the data is s0 and r0.
They are named `mode' and `width' and `shapemode' and `shapewidth'
in the code and they bear the meaning of the mode and effective sigma of
the shape of 100 * (Ereco/Egen - 1).
The effective sigma is defined at the shortes interval containing
68% of the total volume of the observable.  This corresponds to
2*sigma of the normal distribution.
The factor of 100 is to express s and r in %.
The phoERes is expressed in terms of log(Ereco/Egen) as
phoERes = 100 * (1 + exp(logErecoOverEgen))
or
x = 100 * (1+exp(t)).
Together with the dependence on s and r then
x -> s0 + (100 * (1 + exp(t)) - s) * r0 / r.

This class is closely related to the somewhat more generic
ParametrizedKeysPdf class.

Mapping of the names in the code:
x .. phoERes
t .. log(Ereco/Egen)

Jan Veverka, Caltech, 18 January 2011
"""

import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.tools as tools


##------------------------------------------------------------------------------
class LogPhoeresKeysPdf(ROOT.RooKeysPdf):
    'Introduce location and scale parameters.'

    def __init__(self, name, title, x, t, s, r, data,
                 mirror=ROOT.RooKeysPdf.NoMirror, rho=1., forcerange=True):
        # t.setMin(ROOT.TMath.Log(1 + 0.01 * x.getMin()))
        # t.setMax(ROOT.TMath.Log(1 + 0.01 * x.getMax()))
        
        self.w = ROOT.RooWorkspace('logErecoOverEgen')
        # self.w.Import(data)
        self.shape = ROOT.RooKeysPdf(name + '_shape', title + ' shape', x, data,
                                     mirror, rho)
        self.r0val = tools.pdf_effsigma(self.shape, x)
        if self.r0val <= 0.:
            raise RuntimeError, ('Illegal value of pdf width: %f.' %
                                 self.r0val)
        self.r0 = ROOT.RooRealVar(name + '_r0', name + '_r0', self.r0val)
        self.s0val = tools.pdf_mode(self.shape, x)
        self.s0 = ROOT.RooRealVar(name + '_s0', name + '_s0', self.s0val)

        ## Define the transformation of x that introduces the dependence on the
        ## t, s and r
        self.xtransform = ROOT.RooClassFactory.makeFunctionInstance(
            'Roo' + name.title() + 'Xtransform',
            name + '_xtransform',
            "{s0} + (100 * (exp(t) - 1) - {s}) * {r0} / {r}".format(
                t=t.GetName(),
                s=s.GetName(),
                r=r.GetName(),
                s0=self.s0.GetName(),
                r0=self.r0.GetName()
                ),
            ROOT.RooArgList(t, s, r, self.s0, self.r0)
            )

        if forcerange:
            ## Restrict the allowed tranformed values to the range where the
            ## PDF was trained.
            self.xtransform_fullrange = self.xtransform
            self.xtransform_fullrange.SetName(name + '_xtransform_fullrange')
            self.xtransform_fullrange.SetTitle(name + '_xtransform_fullrange')
            self.xtransform = ROOT.RooClassFactory.makeFunctionInstance(
                'Roo' + name.title() + 'RangeTransform',
                name + '_xtransform',
                ('{lo} * ({x} <= {lo}) + '
                 '{x} * ({lo} < {x} & {x} < {hi}) + '
                 '{hi} * ({hi} <= {x})').format(
                    x=self.xtransform_fullrange.GetName(),
                    lo=x.getMin(),
                    hi=x.getMax()
                    ),
                ROOT.RooArgList(self.xtransform_fullrange)
                )

        self.customizer = ROOT.RooCustomizer(self.shape, 'transform')
        self.customizer.replaceArg(x, self.xtransform)

        ROOT.RooKeysPdf.__init__(self, self.customizer.build())
        self.SetName(name)
        self.SetTitle(title)
    ## end of __init__
## end of LogPhoeresKeysPdf
