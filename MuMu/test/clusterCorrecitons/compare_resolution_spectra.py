import copy
import ROOT

import JPsi.MuMu.common.r9Chains as r9Chains
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.cmsstyle as cmsstyle

from JPsi.MuMu.common.plotter import Plotter

canvases.wwidth = 500

chains = r9Chains.getChains('v1')
plots = []

ROOT.gStyle.SetTitleOffset(1.25, "Y")
# ROOT.gStyle.SetPadRightMargin(0.02)
# ROOT.gStyle.SetPadLeftMargin(0.15)
# ROOT.gStyle.SetPadTopMargin(0.02)

### Configuration
plot = Plotter(
    cuts = [
        '!isEBEtaGap',
        '!isEBPhiGap',
        ## Module +4
        '1.16 < scEta & scEta < 1.44',
    ],
    expression = '100*(scRawE / genE - 1)',
    binning = '50,-10,10',
    name = 'mp4',
    title = '',
    xtitle = 'E_{raw}^{SC}/E_{gen}^{#gamma} - 1 (%)',
    ytitle = 'a.u.',
    labels = [
        'Barrel',
        'Module +4',
        '#eta/#phi-cracks Removed',
    ],
    trees = [chains[n] for n in 'g93p01 g94cms g94p02'.split()],
    colors = [ROOT.kRed, ROOT.kBlack, ROOT.kBlue,],
    ltitles = ['Spring11 MC', 'Summer11 MC', 'Winter11 MC'],
    drawopts = 'e0 e0hist e0'.split(),
    markerstyles = [20, 21, 22],
    normalize_to_unit_area = True,
    legendkwargs = dict(position = (0.675, 0.9, 0.95, 0.7)),
)

plots.append(plot)

#### Meat
c1 = canvases.next('raw_over_gen_module_p4')
plot.draw()
c1.SetGrid()
c1.RedrawAxis()
c1.Update()


## Plot Module -4
plots.append(
    plot.clone(
        name = 'mm4',
        cuts = [
            '!isEBEtaGap',
            '!isEBPhiGap',
            ## Module +4
            '-1.44 < scEta & scEta < -1.16',
        ],
        labels = [
            'Barrel',
            'Module -4',
            '#eta/#phi-cracks Removed',
        ],
    )
)

c1 = canvases.next('raw_over_gen_module_m4')
plots[-1].draw()
c1.SetGrid()
c1.RedrawAxis()
c1.Update()

## Plot Module +1
plots.append(
    plot.clone(
        name = 'mp1',
        cuts = [
            '!isEBEtaGap',
            '!isEBPhiGap',
            ## Module +1
            '0.02 < scEta & scEta < 0.42',
        ],
        labels = [
            'Barrel',
            'Module +1',
            '#eta/#phi-cracks Removed',
        ],
    )
)
c1 = canvases.next('raw_over_gen_module_p1')
plots[-1].draw()
c1.SetGrid()
c1.RedrawAxis()
c1.Update()

## Plot Module -1
plots.append(
    plot.clone(
        name = 'mm1',
        cuts = ['!isEBEtaGap', '!isEBPhiGap',
                ## Module 11
                '-0.02 > scEta & scEta > -0.42',],
        labels = [
            'Barrel',
            'Module -1',
            '#eta/#phi-cracks Removed',
        ],
    )
)
c1 = canvases.next('raw_over_gen_module_m1')
plots[-1].draw()
c1.SetGrid()
c1.RedrawAxis()
c1.Update()



###############################################################################
## RECO over GEN plots
reco_over_gen_plots = copy.deepcopy(plots)
for p in reco_over_gen_plots:
    p.expression = '100*(scE / genE - 1)'
    p.xtitle = 'E_{cor}^{SC}/E_{gen}^{#gamma} - 1 (%)'
    p.name = 'reco_over_gen_' + p.name
    c1 = canvases.next(p.name)
    p.draw()
    c1.SetGrid()
    c1.RedrawAxis()
    c1.Update()

if __name__ == '__main__':
    import user
