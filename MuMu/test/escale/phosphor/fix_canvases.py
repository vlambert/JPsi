import os
import glob
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.cmsstyle as cmsstyle

# target_dir_glob_pattern = '/Users/veverka/Desktop/PHOSPHOR/v2/*/*'
# target_dir_glob_pattern = '/home/veverka/jobs/outputs/htozg_v1/*_yyv5'
target_dir_glob_pattern = '/home/veverka/jobs/outputs/lyon_test/*/*'

for path in glob.glob(target_dir_glob_pattern):
    
    for fname in glob.glob(os.path.join(path, '*_landscape.root')):
        print fname
        rootfile = ROOT.TFile.Open(fname)
        cname = os.path.splitext(os.path.basename(fname))[0]
        canvas = rootfile.Get(cname)
        canvas.Draw()
        canvas.SetWindowSize(1200, 600)
        canvases.canvases.append(canvas)

    for mask in 'data combo logy fit phor phorhist'.split():
        for fname in glob.glob(os.path.join(path, '*_%s.root' % mask)):
            print fname
            rootfile = ROOT.TFile.Open(fname)
            cname = os.path.splitext(os.path.basename(fname))[0]
            canvas = rootfile.Get(cname)
            canvas.Draw()
            canvas.SetWindowSize(600, 400)
            canvases.canvases.append(canvas)

    canvases.update()
    canvases.make_plots('png pdf'.split(), path=path)
    del canvases.canvases[:]
