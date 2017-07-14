// ------------------------------------------------------------------------
// Copyright (c) 2015-2017, AIT Austrian Institute of Technology GmbH.
// All rights reserved. See file POWERFACTORY_FMU_LICENSE.txt for details.
// ------------------------------------------------------------------------

/// \file testPowerFactoryRMS.cpp

#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE testPowerFactoryRMS

// #ifndef _CRT_SECURE_NO_WARNINGS
// #define _CRT_SECURE_NO_WARNINGS
// #endif

#include <boost/test/unit_test.hpp>
#include <boost/filesystem.hpp>
#include <cmath>
#include <cstdio>

#include "import/base/include/CallbackFunctions.h"
#include "export/functions/fmi_v1.0/fmiFunctions.h"

#ifdef _MSC_VER
#pragma comment( linker, "/SUBSYSTEM:CONSOLE" )
#pragma comment( linker, "/ENTRY:mainCRTStartup" )
#endif


namespace
{
	// Define callback functions.
	static  fmiCallbackFunctions functions =
	{ callback::verboseLogger, callback::allocateMemory, callback::freeMemory, callback::stepFinished };

	// Check values with a precision of 5e-3 percent.
	const double testPrecision = 5e-3;
}



BOOST_AUTO_TEST_CASE( test_power_factory_fmu_rms )
{
	fmiStatus status = fmiFatal;

	std::string fmuLocation = std::string( FMU_URI_BASE ) + std::string( "/rms" );

	fmiComponent pfSlave = fmiInstantiateSlave( "PFTestRMS",
						    "{PFACTORY-2016-SP40-RMS0-simulation00}",
						    fmuLocation.c_str(),
						    "application/x-powerfactory", 0, fmiTrue,
						    fmiFalse, functions, fmiTrue );
	BOOST_REQUIRE_MESSAGE( 0 != pfSlave, "fmiInstantiateSlave(...) failed." );

	fmiReal tStart = 0.;

	status = fmiInitializeSlave( pfSlave, tStart, fmiFalse, 0. );
	BOOST_REQUIRE_MESSAGE( fmiOK == status, "fmiInitializeSlave(...) failed." );

	fmiValueReference ctrl_pext1_ref = 1;

	fmiValueReference ctrl_pext2_ref = 2;

	fmiReal trafo_power;
	fmiValueReference trafo_power_ref = 1001;

	fmiReal generator_current;
	fmiValueReference generator_current_ref = 1002;

	//
	// Run a simulation.
	//
	fmiReal time = tStart;
	fmiReal delta = 30.;

	fmiReal ctrl_pext1_in[5] = { -1.0, -0.5, -1.0, -1.5, -2.0 };
	fmiReal ctrl_pext2_in[5] = { 2.0, 0.5, 1.0, 1.5, 2.0 };

	fmiReal trafo_power_compare[5] = { -0.8945882342025551, 0.014028633571793542, 0.054946367031286567, 0.11968154638124694, 0.20319977527771305 };
	fmiReal generator_current_compare[5] = { 1.4890783654280786, 0.7327992828973128, 1.503625321464907, 2.3072655990748006, 3.1360915700379866 };

	unsigned int count = 0;
	while ( time < tStart + 10*delta )
	{
		if ( count % 2 == 0 ) {
			// Set input variable EvtParam.Controller.Pext1
			status = fmiSetReal( pfSlave, &ctrl_pext1_ref, 1, ctrl_pext1_in + count/2 );
			BOOST_REQUIRE_MESSAGE( fmiOK == status, "fmiGetReal(...) failed." );

			// Set input variable EvtParam.Controller.Pext2
			status = fmiSetReal( pfSlave, &ctrl_pext2_ref, 1, ctrl_pext2_in + count/2 );
			BOOST_REQUIRE_MESSAGE( fmiOK == status, "fmiGetReal(...) failed." );
		}
			
		// Make co-simulation step.
		status = fmiDoStep( pfSlave, time, delta, true );
		BOOST_REQUIRE_MESSAGE( fmiOK == status, "fmiDoStep(...) failed." );
    
		if ( count % 2 == 1 ) {
			status = fmiGetReal( pfSlave, &trafo_power_ref, 1, &trafo_power );
			BOOST_REQUIRE_MESSAGE( fmiOK == status, "fmiGetReal(...) failed." );
			BOOST_CHECK_CLOSE( trafo_power, trafo_power_compare[count/2], testPrecision );

			status = fmiGetReal( pfSlave, &generator_current_ref, 1, &generator_current );
			BOOST_REQUIRE_MESSAGE( fmiOK == status, "fmiGetReal(...) failed." );
			BOOST_CHECK_CLOSE( generator_current, generator_current_compare[count/2], testPrecision );
		}

		// Advance time and counter.
		time += delta;
		++count;
	}


	//
	// Terminate simulation.
	//

	status = fmiTerminateSlave( pfSlave );
	BOOST_REQUIRE_MESSAGE( fmiOK == status, "fmiTerminateSlave(...) failed." );

	fmiFreeSlaveInstance( pfSlave );

}
