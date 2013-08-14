'''
Test the norm value caching
'''

import array
import ROOT
import JPsi.MuMu.common.roofit as roo

w = ROOT.RooWorkspace('w')
model = w.factory("""EXPR::model(
    '1/((x-a)*(x-a) + 0.01) + 1/((y-a)*(y-a) + 0.01) + 1/((z-a)*(z-a) + 0.01)',
    x[-1,1], y[-1,1], z[-1,1], a[-5,5])""")
model.setNormValueCaching(3)
## This line causes a seg fault!
model.getVal(ROOT.RooArgSet(*[w.var(n) for n in 'x y z'.split()]))
if __name__ == '__main__':
    import user
