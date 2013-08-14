'''
phosphormodel4 - The Photone Energy Scale and Resolution Model v4.
This module defines the class PhosphorModel4 that implements a
RooMomentMorph PDF for the mmg mass depending on the photon energy scale
and resolution.  The dependence on the scale is introduced through
the scaling transformation of the mmg mass observable as desribed in
test/escale/phosphormodel3.py.  The dependence on the resolution is
is introduced through the moment morphing.

Jan Veverka, Caltech, 27 January 2012
'''

import array
import ROOT
import JPsi.MuMu.common.roofit as roo

from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf

##------------------------------------------------------------------------------
class PhosphorModel4(ROOT.RooMomentMorph):
    def __init__(self, name, title, mass, phos, phor, data, workspace, 
                 phostarget, phortargets, rho=1.5,
                 mirror=ROOT.RooKeysPdf.NoMirror,
                 mrangetrain=(40,140), mrangenorm=(50,130), mrangefit=(60,120)):
        '''PhosphorModel4(str name, str title, RooRealVar mass, RooRealVar phos,
            RooRealVar phor, RooDataSet data, float phostarget,
            [float] phortargets, float rho=1.5,
            int mirror=ROOT.RooKeysPdf.NoMirror)
        name - PDF name
        title - PDF title
        mass - mumugamma invariant mass (GeV), observable
        phos - photon energy scale (%), parameter
        phor - photon energy resolution (%), paramter
        data - (mmMass, mmgMass, phoERes = 100*(phoEreco/phoEgen - 1), dataset
            on which the shapes of reference PDFs are trained.
        phostarget - target reference value of the photon energy scale at which
            the model is being trained
        phortargetss - a list of target photon energy resolution values for the
            moment morphing
        rho - passed to trained RooKeysPdfs
        mirror - passed to trained RooKeysPdfs        
        '''
        ## Attach args.
        self._name = name
        self._title = title
        self._mass = mass
        self._phos = phos
        self._phor = phor
        self._data = data
        self._phostarget = phostarget
        self._phortargets = phortargets[:]
        self._rho = rho
        self._mirror = mirror
        ## Attach other attributes.
        self._massrange = (mass.getMin(), mass.getMax())
        self._sdata_list = []
        self._phostrue_list = []
        self._phortrue_list = []
        self._dlogm_dphos_list = []
        self._msubs_list = []
        self._keys_pdfs = []
        self._keys_modes = []
        self._keys_effsigmas = []
        self._keys_fitresults = []
        self._pdfs = []
        self._custs = []
        self._pdfrefs = []
        self._mrefs = []
        self._workspace = workspace
        ## self._workspace = ROOT.RooWorkspace(name + '_workspace',
        ##                                     title + ' workspace')
        w = self._workspace
        self.w = w
        ## Import important args in workspace.
        # w.Import(ROOT.RooArgSet(mass, phos, phor))
        w.Import(mass)
        w.Import(phos)
        w.Import(phor)
        w.Import(self._data)
        w.factory(
            'ConstVar::{name}_phostarget({value})'.format(
                name=name, value=self._phostarget
                )
            )
        ## Define the morphing parameter. This an identity with the
        ## photon resolution for now.
        mpar = self._mpar = w.factory(            
            'expr::{name}_mpar("{phor}", {{{phor}}})'.format(
            ## 'expr::{name}_mpar("sqrt(3^2 + {phor}^2)", {{{phor}}})'.format(
            ## 'expr::{name}_mpar("2.325+sqrt(0.4571 + (0.1608*{phor})^2)", {{{phor}}})'.format(
                name=name, phor=phor.GetName()
                )
            )
        ## Define the formula for dlog(m)/dphos.
        self._dlogm_dphos_func = w.factory('''
            expr::dlogm_dphos_func("0.5 * (1 - mmMass^2 / mmgMass^2) * mmgMass",
                                   {mmMass, mmgMass})
            ''')
        ## Get the calibrator.
        self._calibrator = MonteCarloCalibrator(self._data)
        ## Loop over target reference photon energy resolutions in phortargets.
        for index, phortarget in enumerate(self._phortargets):
            ## Store the target photon resolution value.
            w.factory(
                'ConstVar::{name}_phortarget_{index}({value})'.format(
                    name=name, index=index, value=phortarget
                    )
                )

            ## Get the corresponding smeared RooDataSet sdata named
            ##     {name}_sdata_{index} and attach it to self._sdata
            sdata = self._calibrator.get_smeared_data(
                self._phostarget, phortarget, name + '_sdata_%d' % index,
                title + ' sdata %d' % index,
                ## Get the true scale and resolution with errors. (This can be
                ##     added to the calibrator and snapshots of
                ##     self._calibrator.s and self._calibrator.r stored as
                ##     {name}_sdata_{index}_sr in self._calibrator.w)
                dofit=True
                )
            self._sdata_list.append(sdata)
            w.Import(sdata)
            phostrue = ROOT.RooRealVar(self._calibrator.s,
                                       name + '_phostrue_%d' % index)
            phortrue = ROOT.RooRealVar(self._calibrator.r,
                                       name + '_phortrue_%d' % index)
            phostrue.setConstant(True)
            phortrue.setConstant(True)
            self._phostrue_list.append(phostrue)
            self._phortrue_list.append(phortrue)
            w.Import(phostrue)
            w.Import(phortrue)            

            ## Calculate the dlogm/dphos {name}_dlogm_dphos_{index}
            ##     for the smeared dataset.
            sdata.addColumn(self._dlogm_dphos_func)
            dlogm_dphos = w.factory(
                '''
                {name}_dlogm_dphos_{index}[{mean}, 0, 1]
                '''.format(name=name, index=index,
                           mean=sdata.mean(sdata.get()['dlogm_dphos_func']))
                )
            dlogm_dphos.setConstant(True)
            self._dlogm_dphos_list.append(dlogm_dphos)

            ## Define the mass scaling {name}_msubs{i} introducing
            ##     the dependence on phos. This needs self._calibrator.s and
            ##     dlogm_dphos.
            ## msubs = w.factory(
            ##     '''
            ##     cexpr::{msubs}(
            ##         "{mass}*(1 - 0.01 * {dlogm_dphos} * ({phos} - {phostrue}))",
            ##         {{ {mass}, {dlogm_dphos}, {phos}, {phostrue} }}
            ##         )
            ##     '''.format(msubs = name + '_msubs_%d' % index,
            ##                mass = self._mass.GetName(),
            ##                dlogm_dphos = dlogm_dphos.GetName(),
            ##                phos = self._phos.GetName(),
            ##                phostrue = phostrue.GetName())
            ## )
            ## msubs = w.factory(
            ##     '''
            ##     LinearVar::{msubs}(
            ##         {mass},
            ##         expr::{slope}(
            ##             "(1 - 0.01 * {dlogm_dphos} * ({phos} - {phostrue}))",
            ##             {{ {dlogm_dphos}, {phos}, {phostrue} }}
            ##             ),
            ##         0
            ##         )
            ##     '''.format(msubs = name + '_msubs_%d' % index,
            ##                slope = name + '_msubs_slope_%d' % index,
            ##                mass = self._mass.GetName(),
            ##                dlogm_dphos = dlogm_dphos.GetName(),
            ##                phos = self._phos.GetName(),
            ##                phostrue = phostrue.GetName())
            ## )
            msubs = w.factory(
                '''
                LinearVar::{msubs}(
                    {mass}, 1,
                    expr::{offset}(
                        "- 0.01 * {dlogm_dphos} * ({phos} - {phostrue})",
                        {{ {dlogm_dphos}, {phos}, {phostrue} }}
                        )
                    )
                '''.format(msubs = name + '_msubs_%d' % index,
                           offset = name + '_msubs_offset_%d' % index,
                           mass = self._mass.GetName(),
                           dlogm_dphos = dlogm_dphos.GetName(),
                           phos = self._phos.GetName(),
                           phostrue = phostrue.GetName())
            )
            self._msubs_list.append(msubs)
            
            ## Build the corresponding parametrized KEYS PDF {name}_kyes_{index}
            ##     with {name}_keys_mode_{index} and
            ##     {name}_keys_effsigma_{index}.
            keys_mode = w.factory(
                '{name}_keys_mode_{index}[91.2, 60, 120]'.format(
                    name=name, index=index
                    )
                )
            keys_effsigma = w.factory(
                '{name}_keys_effsigma_{index}[3, 0.1, 60]'.format(
                    name=name, index=index
                    )
                )
            mass.setRange(*mrangetrain)
            keys_pdf = ParametrizedKeysPdf(name + '_keys_pdf_%d' % index,
                                           name + '_keys_pdf_%d' % index,
                                           mass, keys_mode, keys_effsigma,
                                           sdata)
            self._keys_modes.append(keys_mode)
            self._keys_effsigmas.append(keys_effsigma)
            self._keys_pdfs.append(keys_pdf)
                                       
            ## Fit the KEYS PDF to the training data and save the result
            ##     {name}_keys_fitresult_{index} and parameter snapshots
            ##     {name}_keys_mctrue_{index}.
            mass.setRange(*mrangenorm)
            keys_fitresult = keys_pdf.fitTo(sdata, roo.Range(*mrangefit),
                                            roo.Strategy(2), roo.NumCPU(8),
                                            roo.Save(True))
            self._keys_fitresults.append(keys_fitresult)
            w.Import(keys_fitresult, name + '_keys_fitresult_%d' % index)
            w.saveSnapshot(name + '_mctrue_%d' % index,
                           ','.join([phostrue.GetName(),
                                     phortrue.GetName(),
                                     keys_mode.GetName(),
                                     keys_effsigma.GetName()]))
            
            ## Sample the fitted KEYS PDF to a histogram {name}_hist_{index}.
            mass.setRange(*mrangetrain)
            hist = keys_pdf.createHistogram(name + '_hist_%d' % index,
                                            mass, roo.Binning(1000))

            ## Build a RooDataHist {name}_dhist{index} of the sampled histogram.
            dhist = ROOT.RooDataHist(name + '_dhist_%d' % index,
                                     name + '_dhist_%d' % index,
                                     ROOT.RooArgList(mass), hist)
            w.Import(dhist)
            
            ## Build a RooHistPdf {name}_pdf_{index} using the dhist and msubs.
            ## pdf = w.factory(
            ##     'HistPdf::{name}({{{msubs}}}, {{{mass}}}, {dhist}, 1)'.format(
            ##         name = name + '_pdf_%d' % index, msubs = msubs.GetName(),
            ##         mass = mass.GetName(), dhist = dhist.GetName()
            ##         )
            ##     )
            pdf = w.factory(
                'HistPdf::{name}({{{mass}}}, {dhist}, 1)'.format(
                    name = name + '_pdf_%d' % index, msubs = msubs.GetName(),
                    mass = mass.GetName(), dhist = dhist.GetName()
                    )
                )
            self._pdfs.append(pdf)
            mass.setRange(*self._massrange)

            ## Supstitute for mass using customizer.
            cust = ROOT.RooCustomizer(pdf, 'msubs_%d' % index)
            self._custs.append(cust)
            cust.replaceArg(mass, msubs)
            pdfref = cust.build()
            pdfref.addOwnedComponents(ROOT.RooArgSet(msubs))
            pdfref.SetName(name + '_pdfref_%d' % index)
            pdfref.SetTitle(name + '_pdfref_%d' % index)
            w.Import(pdfref)
            self._pdfrefs.append(pdfref)
            
            ## Calculate morphing parameter reference values float mref[index].
            phorval = phor.getVal()
            phor.setVal(phortrue.getVal())
            self._mrefs.append(mpar.getVal())
            phor.setVal(phorval)
        ## End of loop over target phortargets

        ## Define the RooMomentMorph model.
        model = w.factory(
            '''
            MomentMorph::{name}({mpar}, {{{mass}}}, {{{pdfs}}}, {{{mrefs}}})
            '''.format(name=name, mpar=mpar.GetName(), mass=mass.GetName(),
                       pdfs=','.join([f.GetName() for f in self._pdfs]),
                       # pdfs=','.join([f.GetName() for f in self._pdfrefs]),
                       mrefs=','.join([str(m) for m in self._mrefs]))
            )
        
        ## Quick hack to make things work.
        cust = ROOT.RooCustomizer(model, 'msub')
        cust.replaceArg(mass, self._msubs_list[0])
        model2 = cust.build()
        
        ROOT.RooMomentMorph.__init__(self, model2)
        self.SetName(name)
        self.SetTitle(title)
    ## End of __init__()

    def make_mctrue_graph(self, xname='phor', yname='keys_effsigma'):
        vardict = {'phos': self._phostrue_list,
                   'phor': self._phortrue_list,
                   'keys_mode': self._keys_modes,
                   'keys_effsigma': self._keys_effsigmas}            
        x = array.array('d', [v.getVal() for v in vardict[xname]])
        y = array.array('d', [v.getVal() for v in vardict[yname]])
        ex = array.array('d', [v.getError() for v in vardict[xname]])
        ey = array.array('d', [v.getError() for v in vardict[yname]])
        print len(vardict[xname]), x, y, ex, ey
        graph = ROOT.TGraphErrors(len(vardict[xname]), x, y, ex, ey)
        return graph
        ## for xvar in
    ## End of make_mctrue_graph()
## End of PhosphorModel4
