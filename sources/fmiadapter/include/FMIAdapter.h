/* -----------------------------------------------------------------------
 * Copyright (c) 2015-2017, AIT Austrian Institute of Technology GmbH.
 * All rights reserved. See file POWERFACTORY_FMU_LICENSE.txt for details.
 * -----------------------------------------------------------------------*/

#ifndef _POWER_FACTORY_FMIADAPTER_H
#define _POWER_FACTORY_FMIADAPTER_H

// Project includes.
#include "fmiadapter/include/digusermodel.h"
#include "fmiadapter/include/GetNextEventStatus.h"

// DLL info for DSL model definition
#define DESCRIPTION "FMIAdapter"
#define VERSION "0.1 (2017 SP3)"
#define CREATED "11.07.2017"
#define AUTHOR "Edmund Widl"
#define COMPANY "AIT Austrian Institute of Technology GmbH"
#define COPYRIGHT "AIT Austrian Institute of Technology GmbH"
#define CHECKSUM "7D6F-F3C2-B3F1-49C8"

// Define size of character arrays used for retrieving events from the queue.
#define LENNAME 30
#define LENTYPE 10
#define LENTARGET 30
#define LENEVT 100

// Helper macros for handling the output signal.
#define ___trigger 0
#define trigger *(pInstance->m_outputSigs[0].m_value)
#define trigger___init(val) *(pInstance->m_outputSigs[0].m_value)=val

#endif // _POWER_FACTORY_FMIADAPTER_H