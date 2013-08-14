#!/cms/sw/slc5_amd64_gcc434/external/python/2.6.4-cms14/bin/python

def print_debug(i):
	print "DEBUG+++++++++++++++DEBUG%d" % i

print_debug(0)
import getopt
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
print_debug(1)
#import ConfigParser, StringIO
from Phosphor_Config_Parser import parse_cfg_file
print_debug(10)
from Phosphor_Calculator import init, init_cfg_file, process_real_data, process_monte_carlo, outro
print_debug(2)
from Phosphor_Globals import Globals
#from Phosphor_Globals import debug, version, verbose, cfg_file, use_real_data
from Phosphor_Globals import *
sw = ROOT.TStopwatch()
sw2 = ROOT.TStopwatch()

print_debug(3)

#exit(1)


#=== MAIN =====================================================================

def main():
    print "DEBUG+++++++++++++++DEBUG1"
    sw.Start()
    sw2.Start()
    global  version, verbose, debug, cfg_file, use_real_data
    
    print 'ARGV      :', sys.argv[1:]
    try:
        options, remainder = getopt.gnu_getopt(sys.argv[1:], 'o:c:vdih', ['cfg_file=','output=','verbose','debug','DataType=','DetectorType=','treeversion=','R9Low=','R9High=','PtLow=','PtHigh=','help',])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        #usage()
        sys.exit(2)

    Globals.CmdFlag = False
    
    for opt, arg in options:
        #   print 'OPT: ', opt, 'ARG: ', arg
        
        if opt in ('-c', '--cfg_file'):
            cfg_file = arg
	    continue
        elif opt in ('-o', '--output'):
            Globals.outputfile = arg
	    continue
        elif opt == '-i':
	    Globals.CmdFlag = True
	    continue
        elif opt in ('-v', '--verbose'):
            verbose = True
	    continue
        elif opt in ('-d', '--debug'):
            debug = True
	    continue
        elif opt == '--treeversion':
            Globals.model_tree_version = Globals.data_tree_version = arg
	    continue
	elif opt == '--DataType':
	    Globals.DataType = arg
	    continue
	elif opt == '--DetectorType':
	    Globals.DetectorType = arg
            if Globals.DetectorType=='EE':
                Globals.cuts.append('!phoIsEB')
 	        continue
            elif Globals.DetectorType=='EB':
                Globals.cuts.append('phoIsEB')
                continue
            else:
                raise RuntimeError, 'Wrong Detector Type, Please Try EE or EB'
	
	elif opt == '--PtLow':
	    Globals.cuts.append('phoPt >= %s' % arg)
            ptlow = '_PtLow_%s' % arg
            ptlow1 = arg
            if debug:
                print '===CUTS===', Globals.cuts
            continue
        elif opt == '--PtHigh':
            Globals.cuts.append('phoPt < %s' % arg)
            pthigh = '_PtHigh_%s' % arg
            pthigh1 = arg
            if debug:
                print '===CUTS===', Globals.cuts
	    continue
        elif opt == '--R9Low':
            Globals.cuts.append('phoR9 >= %s' % arg)
            r9low = '_R9Low_%s' % arg
            if debug:
                print '===CUTS===', Globals.cuts
            continue
        elif opt == '--R9High':
	    Globals.cuts.append('phoR9 < %s' % arg)
            r9high = '_R9high_%s' % arg
            if debug:
                print '===CUTS===', Globals.cuts
            continue
	elif opt in ('-h','--help'):
            print '========================HERE THE HELP WILL BE PUT!!! HAHA========================================'
            sys.exit(2)

    if debug:
        print 'VERSION   :', version
        print 'VERBOSE   :', verbose
        print 'OUTPUT    :', Globals.outputfile
        print 'REMAINING :', remainder

    	
    if Globals.CmdFlag == True:

        print "********CUTS: ", Globals.cuts
	Globals.name = Globals.DataType + "_" + Globals.DetectorType + "_" + Globals.model_tree_version + r9low + r9high + ptlow + pthigh #+ dilepcut
	Globals.latex_title = Globals.DataType + ', ' + Globals.DetectorType + ', E_{T}^{#gamma} [%s,%s]'%(ptlow1 ,pthigh1)

	Globals.cuts.append('mmMass + mmgMass < 180')
        Globals.cuts.append('minDeltaR < 1.5')
	Globals.cuts.append('mmgMass > 52')
	Globals.cuts.append('mu1Pt > 15')
	Globals.cuts.append('mu2Pt > 10')
        
        if debug:
            print 'COMMAND Line CONFIGURATION ------>:'
            
        #parse_cfg_file(cfg_file)
        print "======COMMNAD LINE CONFIGURATION=========", 
        init_cfg_file()
        
        if Globals.DataType == 'data':
	   print "============= DATA ==========="
           process_real_data()
        elif Globals.DataType == 'mc':
            print "============= MC ==========="
            process_monte_carlo()
        else:
            raise RuntimeError, 'Wrong Data Type, Please Try DataType = data or DataType = mc'

    elif cfg_file == 'empty':

        print "USING NAME AS CONFIGURATION FILE"
        
        if debug:
            print "USING NAME AS CONFIGURATION FILE"
        init()
        
        if use_real_data:
	    print "=====DATA is being proccess====="
            process_real_data()
        else:
	    print "=====DATA is being proccess====="
            process_monte_carlo()

    else:

        Globals.cuts.append('mmMass + mmgMass < 180')
        Globals.cuts.append('minDeltaR < 1.5')
	Globals.cuts.append('mmgMass > 52')
	Globals.cuts.append('mu1Pt > 15')
	Globals.cuts.append('mu2Pt > 10')
        
        if debug:
            print 'Calling Parse Configuration File Function------>:'
            
        parse_cfg_file(cfg_file)
        print "======CONFIG FILE PARSED=========", 
        init_cfg_file()
        
        if Globals.DataType == 'data':
	   print "=============CONFIG FILE DATA==========="
           process_real_data()
        elif Globals.DataType == 'mc':
            print "=============CONFIG FILE DATA==========="
            process_monte_carlo()
        else:
            raise RuntimeError, 'Wrong Data Type, Please Try DataType = data or DataType = mc'

    outro()

if __name__ == '__main__':
    main()
