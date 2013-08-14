import JPsi.MuMu.common.energyScaleChains as esChains
import ROOT

ROOT.gROOT.LoadMacro('tools.C+')
ROOT.gROOT.LoadMacro('CMSStyle.C')
ROOT.CMSstyle()

chains = esChains.getChains('v11')
t = chains['z']
mu1 = 'mu1GenPt,mu1GenEta,mu1GenPhi,0.1056'
mu2 = 'mu2GenPt,mu2GenEta,mu2GenPhi,0.1056'
pho = 'phoGenEt,phoGenEta,phoGenPhi,0'
mmMassGen = 'twoBodyMass({mu1}, {mu2})'.format(mu1=mu1, mu2=mu2)
mmgMassGen = 'threeBodyMass({mu1}, {mu2}, {pho})'.format(mu1=mu1,
                                                         mu2=mu2,
                                                         pho=pho)
kRatioGen = 'kRatio({mmgMass}, {mmMass})'.format(mmgMass=mmgMassGen,
                                                 mmMass=mmMassGen)
t.Draw(kRatioGen, 'mmgMass- & mu1GenPt>0 & mu2GenPt>0 & phoGenEt>0')
if __name__ == '__main__':
    import user