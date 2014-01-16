import os
import re
import sys
import ROOT

_titlePattern = re.compile("^[A-Z]")

### Black Magic to Make RooFit work on MacOS X --------------------------------
if sys.platform == 'darwin':
    try:
        import libRooFit
    except ImportError:
        pass

### Rename the RooWorkspace::import method to avoid conflict with Python--------
setattr(ROOT.RooWorkspace, 'Import', getattr(ROOT.RooWorkspace, 'import'))

### To be able to embed auto-compiled expressions and PDFs in the workspace ----
for path in 'ROOTSYS ROOFITSYS'.split():
    try:
        for subdir in 'include roofit/core'.split():
            fullpath = os.path.join(os.environ[path], subdir)
            if os.path.exists(fullpath):
                ROOT.RooWorkspace.addClassDeclImportDir(fullpath)
    except KeyError:
        ## Environmental variable ROOTSYS or ROOFITSYS is not defined
        pass

### Define all the callable attributes of ROOT.RooFit -------------------------
for method in dir(ROOT.RooFit):
    if callable(getattr(ROOT.RooFit, method)) and re.search(_titlePattern, method):
        if method in vars():
            print "% not imported since it already exists!" % method
        else:
            setattr(sys.modules[__name__], method, getattr(ROOT.RooFit, method))

### Enlarge the size of the pad top margin -------------------------------------
ROOT.gStyle.SetPadTopMargin(0.1)

if __name__ == '__main__':
    import user
