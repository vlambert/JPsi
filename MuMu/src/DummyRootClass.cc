#include "JPsi/MuMu/interface/DummyRootClass.h"
/**
  * This is just a boiler plate for adding new classes to ROOT and
  * using scram/gcc for compilation.
  * Jan Veverka, Caltech, 26 October 2011
  */

#include <iostream>

using namespace cit;

/// Make this a ROOT class
ClassImp(DummyRootClass)

///----------------------------------------------------------------------------
/// Constructor
DummyRootClass::DummyRootClass()
{}


///----------------------------------------------------------------------------
/// Destructor
DummyRootClass::~DummyRootClass()
{}


///----------------------------------------------------------------------------
/// Example method. Prints some information about adding new classes to ROOT
/// in the standard output.
void
DummyRootClass::about()
{
  std::cout <<
    "This is a dummy class demonstrating how to add a new class to ROOT\n"
    "and use it with PyROOT.\n"
    "It lives in UserCode/JanVeverka/JPsi/MuMu corresponding to the package\n"
    "JPsi/MuMu.  Modify accordingly for the package at hand."
    "Relative to `$CMSSW_BASE/src/JPsi/MuMu', the files that are\n"
    "involved in the process are:\n"
    "  1. interface/DummyRootClass.h\n"
    "  2. src/DummyRootClass.cc\n"
    "  3. src/LinkDef.h\n"
    "  4. src/classes.h\n"
    "  5. src/classes_def.xml\n"
    "  6. BuildFile.xml\n"
    "  7. python/dummyrootclass.py\n"
    "\n"
    "To print this message in PyROOT, you can do:\n"
    "  from JPsi.MuM.dummyrootclass import DummyRootClass\n"
    "  DummyRootClass().about()\n";
} /// end of about()
