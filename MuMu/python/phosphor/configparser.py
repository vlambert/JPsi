#=== IMPORTS ==================================================================
import sys
import ConfigParser, StringIO
from JPsi.MuMu.phosphor.globals import Globals

#=== CONSTANTS ================================================================

# section name for options without section:
NOSECTION = 'NOSECTION'


#=== CLASSES ==================================================================

class SimpleConfigParser(ConfigParser.RawConfigParser):
    """
    Simple configuration file parser: based on ConfigParser from the standard
    library, slightly modified to parse configuration files without sections.

    Inspired from an idea posted by Fredrik Lundh:
    http://mail.python.org/pipermail/python-dev/2002-November/029987.html
    """

    def read(self, filename):
        text = open(filename).read()
        #print 'text: ', text
        print "[%s]\n" % NOSECTION + text
        f = StringIO.StringIO("[%s]\n" % NOSECTION + text)
        self.readfp(f, filename)

    def getoption(self, option):
        'get the value of an option'
        return self.get(NOSECTION, option)


    def getoptionslist(self):
        'get a list of available options'
        return self.options(NOSECTION)


    def hasoption(self, option):
        """
        return True if an option is available, False otherwise.
        (NOTE: do not confuse with the original has_option)
        """
        return self.has_option(NOSECTION, option)



def parse_cfg_file(cfg_file):
    """
    Uses SimpleConfigParser(ConfigParser.RawConfigParser) to parse a configuration
    file, then it converts the value assigned in the cofiguration file to the 'cuts'
    that phosphorcalculator need to perform calculations, it needs the file that it
    is going to be parsed ad an imput (cfg_file).
    """
    #global debug
    print '====== DEBUG =====', Globals.debug
    """
    Creating labels for final plots
    The format will be 'phosphor_DATA_EB_tree_version_yyv3_R9_from_0.6_to_0.9'
    """
    
    #Globals.latex_title = "phosphor___tree_version__R9_from__to_"
    print '===== finding phosphor_',Globals.latex_title.find('version') 
    """
    Starting to parse
    """
    cp = SimpleConfigParser()

    if Globals.debug:
        print 'Parsing %s...' % cfg_file

    cp.read(cfg_file)

    if Globals.debug:
        print 'Sections:', cp.sections()
  
        
    if Globals.debug:
        print 'getoptionslist():', cp.getoptionslist()
        
    for option in cp.getoptionslist():

        if Globals.debug:
            print "getoption('%s') = '%s'" % (option, cp.getoption(option))

        if option=='datatype':
            Globals.DataType = cp.getoption(option)
            if Globals.DataType in ('mc', 'data'):
                latex_title1 = 'phosphor_%s_'%Globals.DataType
                if Globals.debug:
                    print '======DATA TYPE======', Globals.DataType
                continue
            else:
                raise RuntimeError, 'Wrong Data Type, Please Try mc or data'
            
        elif option=='detectortype':
            Globals.DetectorType = cp.getoption(option)
            latex_title2 = '%s_'%Globals.DetectorType
            if Globals.DetectorType=='EE':
                Globals.cuts.append('!phoIsEB')
                continue
            elif Globals.DetectorType=='EB':
                Globals.cuts.append('phoIsEB')
                continue
            else:
                raise RuntimeError, 'Wrong Detector Type, Please Try EE or EB'
                
        elif option=='treeversion':
            Globals.model_tree_version = Globals.data_tree_version = cp.getoption(option)
            latex_title3 = 'tree_version_%s_'%Globals.model_tree_version
            continue
        
        elif option=='ptlow':
            Globals.cuts.append('phoPt >= %s' % cp.getoption(option))
            if Globals.debug:
                print '======CUTS======', Globals.cuts
            continue
        elif option=='pthigh':
            Globals.cuts.append('phoPt < %s' % cp.getoption(option))
            if Globals.debug:
                print '======CUTS======', Globals.cuts
            continue
        
        elif option=='r9low':
            Globals.cuts.append('phoR9 >= %s' % cp.getoption(option))
            latex_title4 = 'R9_from_%s_'%cp.getoption(option)
            if Globals.debug:
                print '======CUTS======', Globals.cuts
            continue
        
        elif option=='r9high':
            Globals.cuts.append('phoR9 < %s' % cp.getoption(option))
            latex_title5 = 'to_%s'%cp.getoption(option)
            if Globals.debug:
                print '======CUTS======', Globals.cuts
            continue


    Globals.latex_title = latex_title1 + latex_title2 + latex_title3 + latex_title4 + latex_title5
    Globals.outputfile = Globals.latex_title + '.root'
    if Globals.debug:
        print '====== Latex Label=====', Globals.latex_title
