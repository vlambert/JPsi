#include "datasetUtilities.h"

//-----------------------------------------------------------------------------
// Helper function for the r9 categorization
int isHighR9(int isEB, float r9) {
  switch (isEB) {
    case 0:
      // Endcaps
      return r9 > 0.95 ? 1 : 0;
    case 1:
      // Barrel
      return r9 > 0.94 ? 1 : 0;
    default:
      // This should never happen
      throw 1;
  } // switch
} // isHighR9
