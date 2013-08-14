#!/usr/bin/env python
import massmorph as mm
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

mm.stargets = [-25 + 2.5*i for i in range(21)][10:11]
mm.rtargets = [2.] * len(mm.stargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:1]:
    mm.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    filenamemask = 'massmorph_scalescan_EB_highR9_phoPt%d-%d.root'
    mm.outputfilename = filenamemask % (lo, hi)
    mm.main()

#-------------------------------------------------------------------------------
## EB, R9 < 0.94
baselinecuts = [
    'phoIsEB',
    'phoR9 < 0.94',
    'mmMass + mmgMass < 190',
    'isFSR',
    'phoGenE > 0',
    ]

mm.stargets = [-25 + 2.5*i for i in range(21)]
mm.rtargets = [2.] * len(mm.stargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:0]:
    mm.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    filenamemask = 'massmorph_scalescan_EB_lowR9_phoPt%d-%d.root'
    mm.outputfilename = filenamemask % (lo, hi)
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

mm.stargets = [-25 + 2.5*i for i in range(21)]
mm.rtargets = [2.] * len(mm.stargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:0]:
    mm.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    filenamemask = 'massmorph_scalescan_EE_highR9_phoPt%d-%d.root'
    mm.outputfilename = filenamemask % (lo, hi)
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

mm.stargets = [-25 + 2.5*i for i in range(21)]
mm.rtargets = [2.] * len(mm.stargets)

for lo, hi in list(BinEdges([10, 12, 15, 20, 25, 30, 100]))[:0]:
    mm.cuts = baselinecuts + ['%d <= phoPt & phoPt < %d' % (lo, hi)]
    filenamemask = 'massmorph_scalescan_EE_lowR9_phoPt%d-%d.root'
    mm.outputfilename = filenamemask % (lo, hi)
    mm.main()


