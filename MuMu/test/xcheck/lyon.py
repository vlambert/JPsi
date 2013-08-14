import exceptions
import ROOT

class Event:
    """Container for the Lyon's mmg event data"""
    varNames = tuple("""run         
                        lumi        
                        eid         
                        mmgMass     
                        phoPt       
                        nearMuPt    
                        farMuPt     
                        drNear      
                        drFar       
                        mmMass      
                        nearMuEta   
                        farMuEta    
                        phoEta      
                        k           
                        """.split())
    
    @staticmethod
    def initLeafs(struct):
        for xname in Event.varNames:
            setattr(struct, xname, 0)
    
    def __init__(self, line):
        varNames = Event.varNames
        values = line.split()
        self.rootType = {}
        self.ttreeType = {}
        if len(values) != len(varNames):
            "Error parsing `%s':" % line
            raise RuntimeError, "Expected %d values, received %d." % \
                                ( len(varNames), len(values) )
        for xname, xval in zip(varNames, values):
            try:
                setattr( self, xname, int(xval) )
                self.rootType[xname] = "Int_t"
                self.ttreeType[xname] = "I"
            except exceptions.ValueError:
                setattr( self, xname, float(xval) )
                self.rootType[xname] = "Float_t"
                self.ttreeType[xname] = "F"
    
    def cppStruct(self, name):
        """Generate c++ source defining a struct holding the event data."""
        code = "struct %s {" % name
        for xname, xtype in self.rootType.items():
            code += " %s %s;" % (xtype, xname)
        return code + "};"
    
    def makeBranches(self, tree, struct, prefix):
        """For the given tree, create branches corresponding to data members"""
        for xname, xtype in self.ttreeType.items():
            tree.Branch(prefix + xname,
                        ROOT.AddressOf(struct, xname),
                        xname + "/" + xtype)

    def setLeafs(self, struct):
        for xname in Event.varNames:
            setattr(struct, xname, getattr(self, xname) )