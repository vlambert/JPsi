import copy
import os
import re
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *
from JPsi.MuMu.common.plotData import PlotData
from JPsi.MuMu.scaleFitter import ScaleFitter
from JPsi.MuMu.scaleFitModels import ws1

#------------------------------------------------------------------------------
class BinEdges():
    'Takes a list of bin boundaries and iterates over bin low and high edges.'

    def __init__(self, binning):
        self.binning = binning
        self.bin = 0

    def __iter__(self):
        return self

    def next(self):
        self.bin += 1
        try:
            return (self.binning[self.bin-1],
                    self.binning[self.bin])
        except IndexError:
            raise StopIteration
## end of BinEdges


#------------------------------------------------------------------------------
class SubdetFitters():
    '''Takes a ScaleFitter instance and iterates it over the subdetectors
    while reflecting that in the members name, title, labels and cuts.'''
    def __init__(self, default_fitter):
        self.default_fitter = default_fitter
        self.subdet_iter = iter(['EB', 'EE'])
        fields = 'title cut'.split()
        self.data = {
            'EB': dict(title='Barrel', cut='phoIsEB'),
            'EE': dict(title='Endcaps', cut='!phoIsEB')
        }

    def __iter__(self):
        return self

    def next(self):
        subdet = self.subdet_iter.next()
        title = self.data[subdet]['title']
        cut = self.data[subdet]['cut']
        fitter = copy.deepcopy(self.default_fitter)
        fitter.name += '_%s' % subdet
        fitter.title += ', %s' % title
        fitter.labels += [title]
        fitter.cuts += [cut]
        return fitter
## end of SubdetFitters


#------------------------------------------------------------------------------
class SubdetR9Fitters():
    '''Takes a ScaleFitter instance and iterates it over the subdetectors
    and R9 categories while reflecting that in the members name, title,
    labels and cuts. This produces total of 4 categories with the R9 split
    at 0.94 and 0.95 in the Barrel and Endcaps:
        1. Barrel,  low  R9 (< 0.94),
        2. Barrel,  high R9 (> 0.94),
        3. Endcaps, low  R9 (< 0.95),
        4. Endcaps, high R9 (> 0.95).'''

    def __init__(self, mother):
        ## All members are inherited from the mother fitter
        self.mother = mother
        ## Iterator over categories
        self.categories = iter('EB_lowR9 EB_highR9 '
                               'EE_lowR9 EE_highR9'.split())
        ## For logging and ASCII reports
        titles = ('Barrel, R9 < 0.94',
                  'Barrel, R9 > 0.94',
                  'Endcaps, R9 < 0.95',
                  'Endcaps, R9 > 0.95')
        ## For latex labels on plots
        labels = (('Barrel', 'R_{9}^{#gamma} < 0.94'),
                  ('Barrel', 'R_{9}^{#gamma} > 0.94'),
                  ('Endcaps', 'R_{9}^{#gamma} < 0.95'),
                  ('Endcaps', 'R_{9}^{#gamma} > 0.95'),)
        ## For TTree selection expressions
        cuts = (('phoIsEB' , 'phoR9 < 0.94'),
                ('phoIsEB' , 'phoR9 > 0.94'),
                ('!phoIsEB' , 'phoR9 < 0.94'),
                ('!phoIsEB' , 'phoR9 < 0.94'),)
        fields = 'title labels cuts'.split()
        data = iter(zip(titles, labels, cuts))
        self.data = {
            'EB_lowR9' : dict(zip(fields, data.next())),
            'EB_highR9': dict(zip(fields, data.next())),
            'EE_lowR9' : dict(zip(fields, data.next())),
            'EE_highR9': dict(zip(fields, data.next())),
        }

    def __iter__(self):
        return self

    def next(self):
        name = self.categories.next()
        data = self.data[name]
        daughter = copy.deepcopy(self.mother)
        daughter.name += '_%s' % name
        daughter.title += ', %s' % data['title']
        daughter.labels += data['labels']
        daughter.cuts += data['cuts']
        return daughter
## end of SubdetFitters


if __name__ == '__main__':
    _chains = esChains.getChains('v10')

    test_fitter = ScaleFitter(
        name = 's',
        title = 's-Fit',
        source = '_chains["z"]',
        expression = '100 * (1/kRatio - 1)',
        cuts = ['mmMass < 80'], # 'phoR9 < 0.94', '30 < phoPt', 'phoPt < 9999'],
        labels = [#'R_{9}^{#gamma} < 0.94',
                  #'E_{T}^{#gamma} #in [X,Y] GeV',
                  'Powheg S4', 'Test Model'],
        xRange = (-20, 40),
        nBins = 120,
        fitRange = (-100, 100),
        pdf = 'lognormal',
#         graphicsExtensions = ['png', 'eps'],
        graphicsExtensions = [],
        massWindowScale = 1.5,
        fitScale = 2.0
    )

    print test_fitter.pydump(), ','

    for fit in SubdetR9Fitters(test_fitter):
        print fit.pydump()

    import user
