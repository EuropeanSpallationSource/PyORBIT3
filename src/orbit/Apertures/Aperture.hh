//The base class for Apertures. It defines the interface for Aperture
#ifndef APERTURE_H
#define APERTURE_H

//pyORBIT utils
#include "CppPyWrapper.hh"
#include "Bunch.hh"

using namespace std;

/** 
  The aperture class is used to define how a bunch propogates through an aperture
*/
    
class Aperture: public OrbitUtils::CppPyWrapper
{
public:
	
	/** Aperture */
  Aperture(double shape, double a, double b, double c, double d); //(double shape, double size...)

	/** Routine for transfering particles through a aperture */
	void checkBunch(Bunch* bunch, Bunch* lostbunch);

protected:

	//Counters	
	int nLost;

	//Aperture parameters
  double shape_, a_, b_, c_, d_;
	//int ma_, shape_;

};

//end of APERTURE_H ifdef
#endif
