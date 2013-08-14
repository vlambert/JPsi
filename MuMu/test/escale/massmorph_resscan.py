#!/usr/bin/env python
import massmorph as mm
from JPsi.MuMu.common.binedges import BinEdges

#-------------------------------------------------------------------------------
## EB, R9 > 0.94
## baselinecuts = [
##     'phoIsEB',
##     'phoR9 > 0.94',
##     'mmMass + mmgMass < 190',
##     'isFSR',
##     'phoGenE > 0',
##     ]

## mm.rtargets = [0.05, 0.2] + [0.5 + 0.5 * i for i in range(20)]
## mm.stargets = [0] * len(mm.rtargets)

## for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:]:
##     mm.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
##     mm.outputfilename = 'massmorph_resscan_EB_highR9_phoPt%d-%d.root' % (lo, hi)
##     mm.main()

#-------------------------------------------------------------------------------
## EB, R9 < 0.94
baselinecuts = [
    'phoIsEB',
    'phoR9 < 0.94',
    'mmMass + mmgMass < 190',
    'isFSR',
    'phoGenE > 0',
    ]

mm.rtargets = [0.05, 0.2] + [0.5 + 0.5 * i for i in range(20)]
mm.stargets = [0] * len(mm.rtargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:]:
    mm.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    mm.outputfilename = 'massmorph_resscan_EB_lowR9_phoPt%d-%d.root' % (lo, hi)
    mm.main()

#-------------------------------------------------------------------------------
## EE, R9 > 0.95
baselinecuts = [
    '!phoIsEB',
    'phoR9 > 0.95',
    'mmMass + mmgMass < 190',
    'isFSR',
    'phoGenE > 0',
    ]

mm.rtargets = [0.05, 0.2] + [0.5 + 0.5 * i for i in range(20)]
mm.stargets = [0] * len(mm.rtargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:]:
    mm.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    mm.outputfilename = 'massmorph_resscan_EE_highR9_phoPt%d-%d.root' % (lo, hi)
    mm.main()

#-------------------------------------------------------------------------------
## EE, R9 < 0.95
baselinecuts = [
    '!phoIsEB',
    'phoR9 < 0.95',
    'mmMass + mmgMass < 190',
    'isFSR',
    'phoGenE > 0',
    ]

mm.rtargets = [0.05, 0.2] + [0.5 + 0.5 * i for i in range(20)]
mm.stargets = [0] * len(mm.rtargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:]:
    mm.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    mm.outputfilename = 'massmorph_resscan_EE_lowR9_phoPt%d-%d.root' % (lo, hi)
    mm.main()
