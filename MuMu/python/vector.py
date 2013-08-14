"""Provides the function `vector' that surves as std::vector in PyROOT."""

def vector(ctype):
    """Given a string `ctype' returns the PyROOT's std::vector<ctype> type.
    Usage:
        VDouble = vector('double')
        x = VDouble(2)
        x.push_back(0.5)
        x.push_back(0.6)
    """
    ## Init ROOT
    import ROOT
    #ROOT.gROOT.ProcessLine('#include <vector>')

    ## Name of the C++ type
    name = 'cpp_std_vector_' + ctype

    ## Does ROOT have this typedef already?
    if not hasattr(ROOT, name):
        ## Define the typedef.
        line = 'typedef std::vector<%s> %s;' % (ctype, name)
        ROOT.gROOT.ProcessLine(line)

    ## Return the vector<ctype> type
    return getattr(ROOT, name)
