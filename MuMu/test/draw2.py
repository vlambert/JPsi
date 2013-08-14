import ROOT
def draw2(chain, name1 = "data36x",
    name2 = "data38x",
    varexp = "phoPt",
    selection = "isVbtfBaselineCand & orderByVProb==0 & abs(mass-90)<30 & run < 144114 & phoPt>10 & phoHadronicOverEm<0.5",
    option = "",
    nentries = 999999999L,
    firstentry = 0L
    ):

    if ROOT.gDirectory.Get(name1): ROOT.gDirectory.Get(name1).Delete()
    if ROOT.gDirectory.Get(name2): ROOT.gDirectory.Get(name2).Delete()
    chain[name1].Draw(varexp + ">>" + name1, selection, option, nentries, firstentry)
    chain[name2].Draw(varexp + ">>" + name2, selection, option + "same", nentries, firstentry)
    h1 = ROOT.gDirectory.Get(name1)
    h2 = ROOT.gDirectory.Get(name2)
    h1.SetLineColor(7)
    h1.SetFillColor(7)
    ymax = max(h1.GetMaximum(), h2.GetMaximum() )
    ymin = min(h1.GetMinimum(), h2.GetMinimum() )
    h1.GetYaxis().SetRangeUser(ymin, ymax*1.1)
    h2.GetYaxis().SetRangeUser(ymin, ymax*1.1)
    list(ROOT.gROOT.GetListOfCanvases())[-1].RedrawAxis()
    nbins = h1.GetNbinsX()
    print "Underflow:", h1.GetBinContent(0),  h2.GetBinContent(0)
    print "Overflow: ", h1.GetBinContent(nbins+1),  h2.GetBinContent(nbins+1)
    print "Entries:  ", h1.GetEntries(), h2.GetEntries()
    return h1, h2
