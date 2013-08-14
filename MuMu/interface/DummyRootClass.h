#ifndef JPSI_MUMU_DUMMYROOTCLASS_H
#define JPSI_MUMU_DUMMYROOTCLASS_H

#include "TObject.h"

/**
  * This is just a boiler plate for adding new classes to ROOT and
  * using scram/gcc for compilation.
  * Jan Veverka, Caltech,  26 October 2011
  */

namespace cit {
  class DummyRootClass : public TObject {
    public:
      DummyRootClass();
      virtual ~DummyRootClass();

      /// Print info about this class.
      void about();

      /// Make this a ROOT class.
      /// Use 1 as the 2nd arg to store class in a ROOT file.
      ClassDef(DummyRootClass,0)

  };  /// end of declaration of class DummyRootClass
} /// end of namespace cit

#endif
