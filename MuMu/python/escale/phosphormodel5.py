'''
phosphormodel5 - The Photone Energy Scale and Resolution Model v5.
This module defines the class PhosphorModel5 that implements a
RooMomentMorph PDF for the mmg mass depending on the photon energy scale
and resolution.  The dependence on the scale is introduced through
the scaling transformation of the mmg mass observable as desribed in
test/escale/phosphormodel3.py.  The dependence on the resolution is
is introduced through the moment morphing.  The difference w.r.t.
PhoSPhoR model 4 is in the technical implementation.  The final PDF is
based on a 2D HistPdf in mass and resolution.  The moment morhphing
in resolution is done pair-wise only, then sampled with higher granularity
into histograms in mass and resolution in resolution range corresponding
to the reference resolution boundaries.  These histograms are then
"stitched together" in resolution to cover the full range and used
to define the model HistPdf.  Then, the dependence on the
scale is introduced.  The binnings in resolution and mass are taken from the
binnnings named "cache" if they exists or from thir default binnings
otherwise.

Jan Veverka, Caltech, 30 January 2012
'''

import array
import ROOT
import JPsi.MuMu.common.roofit as roo

from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf

ROOT.gSystem.Load('libJPsiMuMu')

##------------------------------------------------------------------------------
#class PhosphorModel5(ROOT.RooHistPdf):
class PhosphorModel5(ROOT.RooPhosphorPdf):
    ##--------------------------------------------------------------------------
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
        self._dm_dphos_list = []
        self._msubs_list = []
        self._keys_pdfs = []
        self._keys_modes = []
        self._keys_effsigmas = []
        self._keys_fitresults = []
        self._pdfs = []
        self._custs = []
        # self._pdfrefs = []
        self._mrefs = []
        self._phormorphs = []
        self._phorhists = []
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
            ## 'expr::{name}_mpar("2 + sqrt(0.5^2 + 0.05 * {phor}^2)", {{{phor}}})'.format(
            ## 'expr::{name}_mpar("2.325+sqrt(0.4571 + (0.1608*{phor})^2)", {{{phor}}})'.format(
                name=name, phor=phor.GetName()
                )
            )
        ## Define the formula for dlog(m)/dphos.
        self._dm_dphos_func = w.factory('''
            expr::dm_dphos_func("0.5 * (1 - mmMass^2 / mmgMass^2) * mmgMass",
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

            ## Calculate the dlogm/dphos {name}_dm_dphos_{index}
            ##     for the smeared dataset.
            sdata.addColumn(self._dm_dphos_func)
            dm_dphos = w.factory(
                '''
                {name}_dm_dphos_{index}[{mean}, 0, 1]
                '''.format(name=name, index=index,
                           mean=sdata.mean(sdata.get()['dm_dphos_func']))
                )
            dm_dphos.setConstant(True)
            self._dm_dphos_list.append(dm_dphos)

            ## Define the mass scaling {name}_msubs{i} introducing
            ##     the dependence on phos. This needs self._calibrator.s and
            ##     dm_dphos.
            ## msubs = w.factory(
            ##     '''
            ##     LinearVar::{msubs}(
            ##         {mass}, 1,
            ##         expr::{offset}(
            ##             "- 0.01 * {dm_dphos} * ({phos} - {phostrue})",
            ##             {{ {dm_dphos}, {phos}, {phostrue} }}
            ##             )
            ##         )
            ##     '''.format(msubs = name + '_msubs_%d' % index,
            ##                offset = name + '_msubs_offset_%d' % index,
            ##                mass = self._mass.GetName(),
            ##                dm_dphos = dm_dphos.GetName(),
            ##                phos = self._phos.GetName(),
            ##                phostrue = phostrue.GetName())
            ## )
            ## LinearVar cannot be persisted.
            msubs = w.factory(
                '''
                expr::{msubs}(
                     "{mass} - 0.01 * {dm_dphos} * ({phos} - {phostrue})",
                     {{ {mass}, {dm_dphos}, {phos}, {phostrue} }}
                     )
                '''.format(msubs = name + '_msubs_%d' % index,
                           mass = self._mass.GetName(),
                           dm_dphos = dm_dphos.GetName(),
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
                                           sdata, rho=self._rho)
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
                                            mass, roo.Binning('cache'))

            ## Build a RooDataHist {name}_dhist{index} of the sampled histogram.
            dhist = ROOT.RooDataHist(name + '_dhist_%d' % index,
                                     name + '_dhist_%d' % index,
                                     ROOT.RooArgList(mass), hist)
            w.Import(dhist)
            
            ## Build a RooHistPdf {name}_pdf_{index} using the dhist and msubs.
            ## pdf = w.factory(
            pdf = w.factory(
                'HistPdf::{name}({{{mass}}}, {dhist}, 1)'.format(
                    name = name + '_pdf_%d' % index, msubs = msubs.GetName(),
                    mass = mass.GetName(), dhist = dhist.GetName()
                    )
                )
            self._pdfs.append(pdf)
            mass.setRange(*self._massrange)

            ## Calculate morphing parameter reference values float mref[index].
            phorval = phor.getVal()
            phor.setVal(phortrue.getVal())
            self._mrefs.append(mpar.getVal())
            phor.setVal(phorval)
        ## End of loop over target phortargets

        ## Make the reference and cache binnings in phor
        self._check_phor_ranges()
        partitions = self._partition_binning(self._phor, 'cache', 'reference')

        ## Loop over phor reference bins and define pairwise RooMomentMorphs.
        for ilo in range(len(self._mrefs) - 1):
            ihi = ilo + 1
            mlo = self._mrefs[ilo]
            mhi = self._mrefs[ihi]
            pdflo = self._pdfs[ilo]
            pdfhi = self._pdfs[ihi]
            phormorph = w.factory(
                '''
                MomentMorph::{name}_phormorph_{ilo}to{ihi}(
                    {mpar}, {{{mass}}}, {{{pdfs}}}, {{{mrefs}}}
                    )
                '''.format(name=name, ilo=ilo, ihi=ihi,
                           mpar=mpar.GetName(), mass=mass.GetName(),
                           pdfs = '%s, %s' % (pdflo.GetName(), pdfhi.GetName()),
                           mrefs = '%f, %f' % (mlo, mhi))
                )
            self._phormorphs.append(phormorph)
            ## Sample the morph in a 2D histogram in mass and phor.
            phorhist = phormorph.createHistogram(
                name + '_phorhist_%dto%d' % (ilo, ihi),
                mass, roo.Binning('cache'),
                roo.YVar(phor, roo.Binning(partitions[ilo]))
                )
            self._phorhists.append(phorhist)            
        ## End of loop over phor reference bins.
        self._stitch_phorhists()
        self._phor_dhist = phor_dhist = ROOT.RooDataHist(
            name + '_phor_dhist', name + '_phor_dhist',
            ROOT.RooArgList(mass, phor), self._phorhist
            )

        average_index = (len(self._msubs_list) + 1) / 2
        msubs = self._msubs_list[average_index]
        
        ## self._model = model = ROOT.RooHistPdf(
        ##     name + '_phor_histpdf', name + '_phor_histpdf',
        ##     ROOT.RooArgList(msubs, phor), ROOT.RooArgList(mass, phor), phor_dhist, 2
        ##     )
        ## self._model = model = ROOT.RooPhosphorPdf(
        ##     name + '_phor_histpdf', name + '_phor_histpdf', mass, msubs, phor, phor_dhist, 2
        ##     )
        
        ## ## Quick hack to make things work.
        ## self._customizer = customizer = ROOT.RooCustomizer(model, 'msub')
        ## customizer.replaceArg(mass, msubs)
        ## model = customizer.build()
        
        # ROOT.RooHistPdf.__init__(self, model)
        ROOT.RooPhosphorPdf.__init__(self, name, title, mass, msubs, phos, phor,
                                     phor_dhist, 2)
        self.SetName(name)
        self.SetTitle(title)
    ## End of __init__()

    ##--------------------------------------------------------------------------
    def make_mctrue_graph(self, xname='phor', yname='keys_effsigma'):
        vardict = {'phos': self._phostrue_list,
                   'phor': self._phortrue_list,
                   'keys_mode': self._keys_modes,
                   'keys_effsigma': self._keys_effsigmas}            
        x = array.array('d', [v.getVal() for v in vardict[xname]])
        y = array.array('d', [v.getVal() for v in vardict[yname]])
        ex = array.array('d', [v.getError() for v in vardict[xname]])
        ey = array.array('d', [v.getError() for v in vardict[yname]])
        graph = ROOT.TGraphErrors(len(vardict[xname]), x, y, ex, ey)
        return graph
        ## for xvar in
    ## End of make_mctrue_graph()

    ##--------------------------------------------------------------------------
    def _partition_binning(self, x, fine, coarse):
        '''partition_binning(RooAbsArg x, str fine, str coarse)
        fine .. name of the binning of x to be partitioned
        coarse .. name of the binning of x to define the partitioning
        '''
        fbins = x.getBinning(fine)
        cbins = x.getBinning(coarse)
        ## Create empty lists of bins, one for each group.
        boundaries = []
        for cbin in range(cbins.numBins()):
            boundaries.append([])
        ## Loop over the fine bins
        for fbin in range(fbins.numBins()):
            groupindex = cbins.binNumber(fbins.binCenter(fbin))
            ## Add the low boundary to the right group.
            boundaries[groupindex].append(fbins.binLow(fbin))
            ## Check if the high boundary has to be added.
            if fbin == fbins.numBins() - 1:
                ## This is the last bin.  Have to add the high boundary to the
                ## current group.
                boundaries[groupindex].append(fbins.binHigh(fbin))
                continue
            if fbin == 0:
                ## This is the first bin.  There is no previous bin,
                ## so that's it. The low edge of this bin will not
                ## be addede anywhere else.
                continue
            if len(boundaries[groupindex]) == 1:
                ## This is the first bin in this group.  Add the boundary also
                ## to the previous group.
                boundaries[groupindex-1].append(fbins.binLow(fbin))
        ## End of loop over boundaries.
        names = []
        for i, iboundaries in enumerate(boundaries):
            barray = array.array('d', iboundaries)
            nbins = len(barray) - 1
            name = '%s_%dto%d' % (fine, i, i+1)
            names.append(name)
            binning = ROOT.RooBinning(nbins, barray, name)
            x.setBinning(binning, name)
        return names
    ## End of partition_binning().

    ##--------------------------------------------------------------------------
    def _check_phor_ranges(self):
        'Make sure that phor ranges reference and cache are well defined.'
        if not self._phor.hasBinning('cache'):
            self._phor.setBins(100, 'cache')
        boundaries = array.array('d', [x.getVal() for x in self._phortrue_list])
        nbins = len(boundaries) - 1
        refbins = ROOT.RooBinning(nbins, boundaries, 'reference')
        self._phor.setBinning(refbins, 'reference')
    ## End of _check_phor_ranges()

    ##--------------------------------------------------------------------------
    def _stitch_phorhists(self):
        'Assemble the phorhists in one histogram with larger phor range.'
        self._phorhist = ROOT.TH2F(self._name + '_phorhist',
                                   self._name + '_phorhist',
                                   self._mass.getBinning('cache').numBins(),
                                   self._mass.getBinning('cache').array(),
                                   self._phor.getBinning('cache').numBins(),
                                   self._phor.getBinning('cache').array())
        ## Loop over the source histograms.
        for h in self._phorhists:
            ## Loop over the x-axis bins.
            for binx in range(1, h.GetNbinsX() + 1):
                xcenter = h.GetXaxis().GetBinCenter(binx)
                ## Loop over the y-axis bins.
                for biny in range(1, h.GetNbinsY() + 1):
                    ## Set the content of the target histogram for this bin.
                    ycenter = h.GetYaxis().GetBinCenter(biny)
                    targetbin = self._phorhist.FindBin(xcenter, ycenter)
                    self._phorhist.SetBinContent(targetbin,
                                                  h.GetBinContent(binx, biny))
                    ## End of loop over the y-axis bins.
                ## End of loop over the x-axis bins.
            ## End of loop over the source histograms.
        ## End of _stitch_phorhists().

    ##--------------------------------------------------------------------------
    ## def selfNormalized(self):
    ##     'Override the RooHistPdfs need for normalization'
    ##     return True
    ## End of selfNormalized.

## End of PhosphorModel5
