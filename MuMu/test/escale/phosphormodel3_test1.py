'''
Test the RooNDKeysPdf and its performance in plotting and fitting
together with several different constructors and substitutions
using RooFormulaVar and RooLinearVar.

Jan Veverka, Caltech, 25 January 2012.

Note:
- NDKeysPdf + LinearVar is O(10^3) and NDKeysPdf + expr is O(10^4)
  slower than KeysPdf and HistPdf variants!

- KeysPdf + LinearVar does not work - ther normalization breaks down!
'''
   
##- Boilerplate imports --------------------------------------------------------
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases

##------------------------------------------------------------------------------
def check_timer(label = ''):
    sw.Stop()
    ct, rt = sw.CpuTime(), sw.RealTime()
    print '+++', label, 'CPU time:', ct, 's, real time: %.2f' % rt, 's'
    sw.Reset()
    sw.Start()
    times.append((label, ct, rt))
    return ct, rt
## End of check_timer

##------------------------------------------------------------------------------
def fit_and_plot(pdf):
    canvases.next(pdf.GetName())
    plot = x.frame()
    data.plotOn(plot)
    print '+++ Fitting', pdf.GetName()
    w.var('m').setVal(m0)
    w.var('s').setVal(s0)
    pdf.fitTo(data, roo.Timer())
    pdf.plotOn(plot)
    pdf.paramOn(plot)
    plot.Draw()
    check_timer('fit_' + pdf.GetName())
## End of fit_and_plot().

##------------------------------------------------------------------------------
def substitute(name, xold, xnew, pdf):
    cust = ROOT.RooCustomizer(pdf, name)
    cust.replaceArg(xold, xnew)
    newpdf = cust.build()
    newpdf.SetName(name)
    newpdf.customizer = cust
    return newpdf
## End of substitute().    

##- Hack away ------------------------------------------------------------------
sw = ROOT.TStopwatch()
sw.Start()
times = []
m0 = -0.5
s0 = 1.5
w = ROOT.RooWorkspace('w', 'w')
g0 = w.factory('Gaussian::g0(x[-10,10],0,1)')
g1 = w.factory('Gaussian::g1(x,m[0,-5,5],s[1,0.1,5])')
g2 = w.factory('Gaussian::g2(expr::xexpr("(x-m)/s", {x,m,s}), 0, 1)')
g3 = w.factory(
    'Gaussian::g3(LinearVar::xlinv(x,expr::xslope("1/s",{s}),m), 0, 1)'
    )
g4 = w.factory('Gaussian::g4(cexpr::xcexpr("(x-m)/s", {x,m,s}), 0, 1)')

x = w.var('x')
xexpr = w.function('xexpr')
xlinv = w.function('xlinv')
xcexpr = w.function('xcexpr')

g5 = substitute('g5', x, xexpr, g0)
g6 = substitute('g6', x, xlinv, g0)
g7 = substitute('g7', x, xcexpr, g0)

check_timer('g1-6')

data = g1.generate(ROOT.RooArgSet(x), 10000)
w.Import(data)
check_timer('data')

k1 = w.factory('KeysPdf::k1(x, g1Data, NoMirror, 1.5)')
k2 = substitute('k2', x, xexpr, k1)
k3 = substitute('k3', x, xlinv, k1)
k4 = substitute('k4', x, xcexpr, k1)

check_timer('k1-4')

## ndk1 = ROOT.RooNDKeysPdf('ndk1', 'ndk1', ROOT.RooArgList(x), data, 'a', 1.5)
## check_timer('ndk1')

## cndk2 = ROOT.RooCustomizer(ndk1, 'cndk2')
## cndk2.replaceArg(x, w.function('xexpr'))
## ndk2 = cndk2.build()
## check_timer('ndk2')

## cndk3 = ROOT.RooCustomizer(ndk1, 'cndk3')
## cndk3.replaceArg(x, w.function('xlinv'))
## ndk3 = cndk3.build()
## check_timer('ndk3')

hk1 = k1.createHistogram('hk1', x)
hk1.Scale(1000)
dhk1 = ROOT.RooDataHist('dhk1', 'dhk1', ROOT.RooArgList(x), hk1)
hfk1 = ROOT.RooHistPdf('hfk1', 'hfk1', ROOT.RooArgSet(x), dhk1, 2)

hfk2 = ROOT.RooHistPdf('hfk2', 'hfk2', ROOT.RooArgList(w.function('xexpr')),
                       ROOT.RooArgList(x), dhk1, 2)

hfk3 = ROOT.RooHistPdf('hfk3', 'hfk3', ROOT.RooArgList(w.function('xlinv')),
                       ROOT.RooArgList(x), dhk1, 2)

hfk4 = ROOT.RooHistPdf('hfk4', 'hfk4', ROOT.RooArgList(w.function('xcexpr')),
                       ROOT.RooArgList(x), dhk1, 2)

hfk5 = substitute('hfk5', x, xexpr, hfk1)
hfk6 = substitute('hfk6', x, xlinv, hfk1)
hfk7 = substitute('hfk7', x, xcexpr, hfk1)

## chfk5 = ROOT.RooCustomizer(hfk1, 'chfk5')
## chfk5.replaceArg(x, w.function('xexpr'))
## hfk5 = chfk5.build()
## hfk5.SetName('hfk5')

## chfk6 = ROOT.RooCustomizer(hfk1, 'chfk6')
## chfk6.replaceArg(x, w.function('xlinv'))
## hfk6 = chfk6.build()
## hfk6.SetName('hfk6')

## chfk7 = ROOT.RooCustomizer(hfk1, 'chfk7')
## chfk7.replaceArg(x, w.function('xcexpr'))
## hfk7 = chfk7.build()
## hfk7.SetName('hfk7')
## check_timer('hfk1-7')

x.setRange(-5, 5)

for f in [g1, g2, g3, g4, g5, g6, g7, k1, k2, k3, k4,
          hfk1, hfk2, hfk3, hfk4, hfk5, hfk6, hfk7]:
    fit_and_plot(f)

canvases.update()

print 'label        CPU (s)    Real (s)'
for l, ct, rt in times:
    print "%10s   %7.2f   %7.2f" % (l, ct, rt)

if __name__ == '__main__':
    # main()
    import user
