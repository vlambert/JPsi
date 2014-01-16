#include <iostream>
#include "PhosphorCorrectorFunctor.hh"

int main(){
  
  //Creates Functor object (true, means we are using the r9 categories)
  //zgamma::PhosphorCorrectionFunctor* obj = new zgamma::PhosphorCorrectionFunctor("PHOSPHOR_NUMBERS_EXPFIT_ERRORS.txt", true);

  zgamma::PhosphorCorrectionFunctor* obj = new zgamma::PhosphorCorrectionFunctor("short_test.txt", true);
  //zgamma::PhosphorCorrectionFunctor* obj = new zgamma::PhosphorCorrectionFunctor("2013_test.txt");


  std::cout << "\n============== ENERGY CORRECTION EXAMPLES ====================\n" << std::endl;
  ///////////////////////////////////////////////////////////////////////////
  /////////////MC HighR9 2012 Correction && Smearing Example/////////////////
  //////////////////////////////////////////////////////////////////////////

  // GetCorrEnergyMC(float R9, int year, double pt, double eta, double Egen)
  // So this method is only for MC since you are specifying the gen level Energy in the last entry
  std::cout << "MC 2012 EXAMPLE CORRECTION Low R9, Corrected energy:" << obj->GetCorrEnergyMC(0.93, 2012, 22., -1.23, 22.6) << std::endl;

  std::cout << "\n============== CATEGORIES EXAMPLES ====================\n" << std::endl;
  
  std::cout << "GATEGORY example 8: " << obj->GetCategory(0.93, 2012, 22., -1.23) << std::endl;

  std::cout << "Energy Error due to Scale: " << obj->ScaleEnError(0.93, 2012, 22., -1.23, 22.6) << "  Cat: " << obj->GetCategory(0.93, 2012, 22., -1.23) << std::endl;
  std::cout << "Energy Error due to Res: " << obj->ResEnError(0.93, 2012, 22., -1.23, 22.6) << "  Cat: " << obj->GetCategory(0.93, 2012, 22., -1.23) << std::endl;

}
