'''
Facilitates the plotting of variables versus the the fit range iteration.
    Usage: python -i plotScaleVsFitRangeIter.py
'''
from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *

gSystem.Load('libJPsiMuMu')
from ROOT import RooCruijff

## Defaults for customizeable data
filename = '/home/veverka/cmssw/CMSSW_4_2_3/src/JPsi/MuMu/test/escale/test.root'
wsname = 'ws1'
snapshot = 'EB_lowR9_mc_pt10-12_cbShape'
variable = '#Deltas'
xtitle = 'Fit Range Iteration'
ytitle = '#Deltas (%)'
labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'E_{T}^{#gamma} #in [10,12] GeV', 'Powheg S4', 'CB' ]
graphs = []

## Other defaults
_maxIter = 999
_file = False
_workspace = False
_yvar = False

#------------------------------------------------------------------------------
def init():
    '''Initialize private data members.'''
    global _file, _workspace, _yvar
    if not _file or _file.GetName() != filename:
        _file = ROOT.TFile(filename)
    if not _workspace or _workspace.GetName() != wsname:
        _workspace = _file.Get(wsname)
    if not _yvar or _yvar.GetName() != variable:
        _yvar = _workspace.var(variable)
## end of init()

#------------------------------------------------------------------------------
def makeGraph():
    '''Makes a graph using the current workspace and variable.'''
    global _workspace, _yvar, graph
    x, ex = array('d', []), array('d', [])
    y, ey = array('d', []), array('d', [])
    for i in range(_maxIter):
        if not _workspace.loadSnapshot(snapshot + '_iter%d' % i):
            break
        x.append(i)
        y.append( _yvar.getVal() )
        ex.append(0)
        ey.append( _yvar.getError() )

    graph = TGraphErrors(len(x), x, y, ex, ey)
## end of makeGraph()

#------------------------------------------------------------------------------
def plot():
    '''Plots the current graph with appropriate ranges and labels.'''
    n = graph.GetN()
    ymin = min( [ graph.GetY()[i] - graph.GetEY()[i] for i in range(n) ] )
    ymax = max( [ graph.GetY()[i] + graph.GetEY()[i] for i in range(n) ] )
    dy = ymax - ymin

    graph.SetTitle( ';%s;%s' % (xtitle, ytitle) )
    graph.GetXaxis().SetLimits( -0.5, n + 0.5 )
    graph.GetHistogram().SetMinimum(ymin - 0.1 * dy)
    graph.GetHistogram().SetMaximum(ymax + 0.1 * dy)
    graph.Draw("ap")
    graphs.append(graph)
## end of plot()

#------------------------------------------------------------------------------
def main():
    '''Initializes private members and makes and plots the graph.
    Takes configuration from the current values of the customizeable data
    members.'''
    init()
    makeGraph()
    plot()
## end of main()


if __name__ == '__main__':
    import user
    main()
