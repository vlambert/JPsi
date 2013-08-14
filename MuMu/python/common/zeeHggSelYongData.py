import os
import socket
import JPsi.MuMu.common.dataset as dataset

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.zeeHggSelYongChains import getChains


def getData(version='v1', nentries=-1):
    chains = getChains(version)
    data = {}
    for name, chain in chains.items():
        mass = RooRealVar('mass', 'mass', 60, 120)
        weight = RooRealVar('weight', 'weight', 0, 999)
        if nentries > 0:
            cuts = ['Entry$ < %d' % nentries]
        else:
            cuts = []
        data[name] = dataset.get(tree=chain, variable=mass, weight=weight,
                                 cuts=cuts)
    return data

if __name__ == "__main__":
    import user

