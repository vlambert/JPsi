#include <iostream>
#include "PhosphorCorrectorFunctor.hh"

int main(){
  
  //Creates Functor object (true, means we are using the r9 categories)
  //zgamma::PhosphorCorrectionFunctor* obj = new zgamma::PhosphorCorrectionFunctor("PHOSPHOR_NUMBERS_EXPFIT_ERRORS.txt", true);

  zgamma::PhosphorCorrectionFunctor* obj = new zgamma::PhosphorCorrectionFunctor("2013_Test_errors.txt", true);
  //zgamma::PhosphorCorrectionFunctor* obj = new zgamma::PhosphorCorrectionFunctor("2013_test.txt");


  std::cout << "\n============== ENERGY CORRECTION EXAMPLES ====================\n" << std::endl;
  ///////////////////////////////////////////////////////////////////////////
  /////////////MC HighR9 2012 Correction && Smearing Example/////////////////
  //////////////////////////////////////////////////////////////////////////

  // GetCorrEnergyMC(float R9, int year, double pt, double eta, double Egen)
  // So this method is only for MC since you are specifying the gen level Energy in the last entry
  std::cout << "MC 2012 EXAMPLE CORRECTION High R9, Corrected energy:" << obj->GetCorrEnergyMC(0.97, 2012, 14., -1.23, 25.6) << std::endl;

  //Same for 2011
  
  //std::cout << "MC 2011 EXAMPLE CORRECTION High R9, Corrected energy:" << obj->GetCorrEnergyMC(0.97, 2011, 14., -1.23, 25.6) << std::endl;
  

  ///////////////////////////////////////////////////////////////////////////
  /////////////MC LowR9 2012 Correction && Smearing Example/////////////////
  //////////////////////////////////////////////////////////////////////////

  std::cout << "MC 2012 EXAMPLE CORRECTION Low R9, Corrected energy:" << obj->GetCorrEnergyMC(0.8, 2012, 14., -1.23, 25.6) << std::endl;

  //Same for 2011
  
  //std::cout << "MC 2011 EXAMPLE CORRECTION Low R9, Corrected energy:" << obj->GetCorrEnergyMC(0.8, 2011, 14., -1.23, 25.6) << std::endl;



  ///////////////////////////////////////////////////////////////////////////
  /////////////Data EB HighR9 Correction && Smearing Example////////////////
  /////////////////////////////////////////////////////////////////////////
  
  //GetCorrEnergyData(float R9, int year, double pt, double eta)
  // Correction only for Data note no gen level info
  std::cout << "DATA 2012 EXAMPLE CORRECTION High R9, Corrected energy:" << obj->GetCorrEnergyData(0.97, 2012, 14., -1.23) << std::endl;
  
  //Same for 2011
  //std::cout << "DATA 2011 EXAMPLE CORRECTION High R9, Corrected energy:" << obj->GetCorrEnergyData(0.97, 2011, 14., -1.23) << std::endl;
  
  ///////////////////////////////////////////////////////////////////////////
  /////////////Data EB HighR9 Correction && Smearing Example////////////////
  /////////////////////////////////////////////////////////////////////////
  //GetCorrEnergyData(float R9, int year, double pt, double eta)
  // Correction only for Data note no gen level info
  
  std::cout << "DATA 2012 EXAMPLE CORRECTION Low R9, Corrected energy:" << obj->GetCorrEnergyData(0.8, 2012, 14., -1.23) << std::endl;
  //Same for 2011
  //std::cout << "DATA 2011 EXAMPLE CORRECTION Low R9, Corrected energy:" << obj->GetCorrEnergyData(0.8, 2011, 14., -1.23) << std::endl;
  

  std::cout << "STUPID EXAMPLE: " << obj->GetCorrEnergyMC(0.352681, 2012, 12.1111, -1.96477, 154.532) << " " << obj->GetCorrEtMC(0.352681, 2012, 12.1111, -1.96477, 154.532) << std::endl;


  /////////////////////////////////////////////////////////////////////////////////
  ////////////////////// Returns Category Number (0,23)///////////////////////////
  ////////////////////////////////////////////////////////////////////////////////
  
  std::cout << "\n============== CATEGORIES EXAMPLES ====================\n" << std::endl;
  
  /*std::cout << "==============2011 High R9 EB====================" << std::endl;
  
  std::cout << "GATEGORY example 0: " << obj->GetCategory(0.97, 2011, 11., -1.23) << std::endl;
  std::cout << "GATEGORY example 1: " << obj->GetCategory(0.97, 2011, 13.5, -1.23) << std::endl;
  std::cout << "GATEGORY example 2: " << obj->GetCategory(0.97, 2011, 17.5, -1.23) << std::endl;
  std::cout << "GATEGORY example 3: " << obj->GetCategory(0.97, 2011, 50., -1.23) << std::endl;
  
  std::cout << "==============2011 Low R9 EB====================" << std::endl;
  
  std::cout << "GATEGORY example 4: " << obj->GetCategory(0.8, 2011, 11., -1.23) << std::endl;
  std::cout << "GATEGORY example 5: " << obj->GetCategory(0.8, 2011, 13.5, -1.23) << std::endl;
  std::cout << "GATEGORY example 6: " << obj->GetCategory(0.8, 2011, 17.5, -1.23) << std::endl;
  std::cout << "GATEGORY example 7: " << obj->GetCategory(0.8, 2011, 50., -1.23) << std::endl;
  
  std::cout << "==============2011 High R9 EE====================" << std::endl;
  
  std::cout << "GATEGORY example 8: " << obj->GetCategory(0.97, 2011, 11., -1.73) << std::endl;
  std::cout << "GATEGORY example 9: " << obj->GetCategory(0.97, 2011, 13.5, -1.73) << std::endl;
  std::cout << "GATEGORY example 10: " << obj->GetCategory(0.97, 2011, 17.5, -1.73) << std::endl;
  std::cout << "GATEGORY example 11: " << obj->GetCategory(0.97, 2011, 50., -1.73) << std::endl;

  std::cout << "==============2011 Low R9 EE====================" << std::endl;

  std::cout << "GATEGORY example 12: " << obj->GetCategory(0.8, 2011, 11., -1.73) << std::endl;
  std::cout << "GATEGORY example 13: " << obj->GetCategory(0.8, 2011, 13.5, -1.73) << std::endl;
  std::cout << "GATEGORY example 14: " << obj->GetCategory(0.8, 2011, 17.5, -1.73) << std::endl;
  std::cout << "GATEGORY example 15: " << obj->GetCategory(0.8, 2011, 50., -1.73) << std::endl;
  */
  std::cout << "==============2012 High R9 EB====================" << std::endl;

  std::cout << "GATEGORY example 16: " << obj->GetCategory(0.97, 2012, 11., -1.23) << std::endl;
  std::cout << "GATEGORY example 17: " << obj->GetCategory(0.97, 2012, 13.5, -1.23) << std::endl;
  std::cout << "GATEGORY example 18: " << obj->GetCategory(0.97, 2012, 17.5, -1.23) << std::endl;
  std::cout << "GATEGORY example 19: " << obj->GetCategory(0.97, 2012, 50., -1.23) << std::endl;

  std::cout << "==============2012 Low R9 EB====================" << std::endl;

  std::cout << "GATEGORY example 20: " << obj->GetCategory(0.8, 2012, 11., -1.23) << std::endl;
  std::cout << "GATEGORY example 21: " << obj->GetCategory(0.8, 2012, 13.5, -1.23) << std::endl;
  std::cout << "GATEGORY example 22: " << obj->GetCategory(0.8, 2012, 17.5, -1.23) << std::endl;
  std::cout << "GATEGORY example 23: " << obj->GetCategory(0.8, 2012, 50., -1.23) << std::endl;

  std::cout << "==============2012 High R9 EE====================" << std::endl;

  std::cout << "GATEGORY example 24: " << obj->GetCategory(0.97, 2012, 11., -1.73) << std::endl;
  std::cout << "GATEGORY example 25: " << obj->GetCategory(0.97, 2012, 13.5, -1.73) << std::endl;
  std::cout << "GATEGORY example 26: " << obj->GetCategory(0.97, 2012, 17.5, -1.73) << std::endl;
  std::cout << "GATEGORY example 27: " << obj->GetCategory(0.97, 2012, 50., -1.73) << std::endl;

  std::cout << "==============2012 Low R9 EE====================" << std::endl;

  std::cout << "GATEGORY example 28: " << obj->GetCategory(0.8, 2012, 11., -1.73) << std::endl;
  std::cout << "GATEGORY example 29: " << obj->GetCategory(0.8, 2012, 13.5, -1.73) << std::endl;
  std::cout << "GATEGORY example 30: " << obj->GetCategory(0.8, 2012, 17.5, -1.73) << std::endl;
  std::cout << "GATEGORY example 31: " << obj->GetCategory(0.8, 2012, 50., -1.73) << std::endl;
  

  /////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////// ENERGY ERROR Due to different categories/////////////////////////////
  ////////Note that there are two different methods for Scale ans Res/////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////

  std::cout << "\n============== ENERGY ERROR EXAMPLES ====================\n" << std::endl;
  
  //std::cout << "Energy Error due to Scale: " << obj->ScaleEnError(0.8, 2011, 14., -1.23, 25.6) << "  Cat: " << obj->GetCategory(0.8, 2011, 14., -1.23) << std::endl;
  //std::cout << "Energy Error due to Res: " << obj->ResEnError(0.8, 2011, 14., -1.23, 25.6) << "  Cat: " << obj->GetCategory(0.8, 2011, 14., -1.23) << std::endl;
  
  //std::cout << "Energy Error due to Scale: " << obj->ScaleEnError(0.97, 2011, 14., -1.23, 25.6) << "  Cat: " << obj->GetCategory(0.97, 2011, 14., -1.23) << std::endl;
  //std::cout << "Energy Error due to Res: " << obj->ResEnError(0.97, 2011, 14., -1.23, 25.6) << "  Cat: " << obj->GetCategory(0.97, 2011, 14., -1.23) << std::endl;


  std::cout << "Energy Error due to Scale: " << obj->ScaleEnError(0.8, 2012, 14., -1.23, 25.6) << "  Cat: " << obj->GetCategory(0.8, 2012, 14., -1.23) << std::endl;
  std::cout << "Energy Error due to Res: " << obj->ResEnError(0.8, 2012, 14., -1.23, 25.6) << "  Cat: " << obj->GetCategory(0.8, 2012, 14., -1.23) << std::endl;

  std::cout << "Energy Error due to Scale: " << obj->ScaleEnError(0.97, 2012, 14., -1.23, 25.6) << "  Cat: " << obj->GetCategory(0.97, 2012, 14., -1.23) << std::endl;
  std::cout << "Energy Error due to Res: " << obj->ResEnError(0.97, 2012, 14., -1.23, 25.6) << "  Cat: " << obj->GetCategory(0.97, 2012, 14., -1.23) << std::endl;
}
