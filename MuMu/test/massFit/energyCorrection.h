#ifndef energyCorrection_h
#define energyCorrection_h

//-----------------------------------------------------------------------------
/**
    Returns energy corrected to the given level
      1: C(eta) correction for lateral leakage
      2: brem corrected
      3: f(eta) fully corrected (default)

    source:
    http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/ggAnalysis/ggNtuplizer/plugins/ggNtuplizer.cc?revision=1.40&view=markup
  */
float
corrE( float /*supercluster*/ rawEnergyWithPS,
       float /*supercluster*/ eta,
       float /*supercluster*/ brem,
       int /*correction*/ level = 3 );
float

/**
    Same as corrE but new as of Jun 2011 and tuned for photons
    source:
    https://twiki.cern.ch/twiki/bin/viewauth/CMS/PhotonEnergyCorrections
  */
newCorrE( float /*supercluster*/ rawEnergyWithPS,
          float /*supercluster*/ eta,
          float /*supercluster*/ brem,
          int /*correction*/ level = 3 );

#endif
