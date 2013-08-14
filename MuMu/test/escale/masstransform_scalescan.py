#!/usr/bin/env python
import masstransform as mt
from JPsi.MuMu.common.binedges import BinEdges

#-------------------------------------------------------------------------------
## EB, R9 > 0.94
baselinecuts = [
    'phoIsEB',
    'phoR9 > 0.94',
    'mmMass + mmgMass < 190',
    'isFSR',
    'phoGenE > 0',
    ]

mt.stargets = [-25 + 2.5*i for i in range(21)]
mt.rtargets = ['nominal'] * len(mt.stargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:]:
    mt.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    filenamemask = 'masstransform_scalescan_EB_highR9_phoPt%d-%d.root'
    mt.outputfilename = filenamemask % (lo, hi)
    mt.main()

#-------------------------------------------------------------------------------
## EB, R9 < 0.94
baselinecuts = [
    'phoIsEB',
    'phoR9 < 0.94',
    'mmMass + mmgMass < 190',
    'isFSR',
    'phoGenE > 0',
    ]

mt.stargets = [-25 + 2.5*i for i in range(21)]
mt.rtargets = ['nominal'] * len(mt.stargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:]:
    mt.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    filenamemask = 'masstransform_scalescan_EB_lowR9_phoPt%d-%d.root'
    mt.outputfilename = filenamemask % (lo, hi)
    mt.main()

#-------------------------------------------------------------------------------
## EE, R9 > 0.95
baselinecuts = [
    '!phoIsEB',
    'phoR9 > 0.95',
    'mmMass + mmgMass < 190',
    'isFSR',
    'phoGenE > 0',
    ]

mt.stargets = [-25 + 2.5*i for i in range(21)]
mt.rtargets = ['nominal'] * len(mt.stargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:]:
    mt.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    filenamemask = 'masstransform_scalescan_EE_highR9_phoPt%d-%d.root'
    mt.outputfilename = filenamemask % (lo, hi)
    mt.main()

#-------------------------------------------------------------------------------
## EE, R9 < 0.95
baselinecuts = [
    '!phoIsEB',
    'phoR9 < 0.95',
    'mmMass + mmgMass < 190',
    'isFSR',
    'phoGenE > 0',
    ]

mt.stargets = [-25 + 2.5*i for i in range(21)]
mt.rtargets = ['nominal'] * len(mt.stargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:]:
    mt.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    filenamemask = 'masstransform_scalescan_EE_lowR9_phoPt%d-%d.root'
    mt.outputfilename = filenamemask % (lo, hi)
    mt.main()


