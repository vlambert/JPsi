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

mt.rtargets = [0.05, 0.2] + [0.5 + 0.5 * i for i in range(20)]
mt.stargets = ['nominal'] * len(mt.rtargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:]:
    mt.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    mt.outputfilename = 'masstransform_resscan_EB_highR9_phoPt%d-%d.root' % (lo, hi)
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

mt.rtargets = [0.05, 0.2] + [0.5 + 0.5 * i for i in range(20)]
mt.stargets = ['nominal'] * len(mt.rtargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:]:
    mt.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    mt.outputfilename = 'masstransform_resscan_EB_lowR9_phoPt%d-%d.root' % (lo, hi)
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

mt.rtargets = [0.05, 0.2] + [0.5 + 0.5 * i for i in range(20)]
mt.stargets = ['nominal'] * len(mt.rtargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:]:
    mt.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    mt.outputfilename = 'masstransform_resscan_EE_highR9_phoPt%d-%d.root' % (lo, hi)
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

mt.rtargets = [0.05, 0.2] + [0.5 + 0.5 * i for i in range(20)]
mt.stargets = ['nominal'] * len(mt.rtargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:]:
    mt.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    mt.outputfilename = 'masstransform_resscan_EE_lowR9_phoPt%d-%d.root' % (lo, hi)
    mt.main()
