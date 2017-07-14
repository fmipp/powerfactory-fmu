# -----------------------------------------------------------------------
# Copyright (c) 2015-2017, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file POWERFACTORY_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------------

########################################################################
#
# This script provides the list of files included into a release of 
# the FMI++ PowerFactory Export Utility.
#
########################################################################


# List of source files (including relative path) that are originally from FMI++.
files_from_fmipp = [
    'sources\\fmipp\\common\\FMIPPConfig.h',
    'sources\\fmipp\\common\\FMUType.h',
    'sources\\fmipp\\common\\fmi_v1.0\\fmi_cs.h',
    'sources\\fmipp\\common\\fmi_v1.0\\fmiModelTypes.h',
    'sources\\fmipp\\common\\fmi_v2.0\\fmi_2.h',
    'sources\\fmipp\\common\\fmi_v2.0\\fmi2ModelTypes.h',
    'sources\\fmipp\\export\\functions\\fmi_v1.0\\fmiFunctions.cpp',
    'sources\\fmipp\\export\\functions\\fmi_v1.0\\fmiFunctions.h',
    'sources\\fmipp\\export\\include\\FMIComponentFrontEndBase.h',
    'sources\\fmipp\\export\\include\\ScalarVariable.h',
	'sources\\fmipp\\export\\include\\HelperFunctions.h',
    'sources\\fmipp\\export\\src\\FMIComponentFrontEndBase.cpp',
    'sources\\fmipp\\export\\src\\HelperFunctions.cpp',
    'sources\\fmipp\\export\\src\\ScalarVariable.cpp',
	'sources\\fmipp\\import\\base\\include\\ModelDescription.h',
	'sources\\fmipp\\import\\base\\include\\PathFromUrl.h',
    'sources\\fmipp\\import\\base\\src\\ModelDescription.cpp',
    'sources\\fmipp\\import\\base\\src\\PathFromUrl.cpp',
	"sources\\fmipp\\import\\base\\include\\CallbackFunctions.h", # only for testing
	"sources\\fmipp\\import\\base\\include\\LogBuffer.h", # only for testing
	"sources\\fmipp\\import\\base\\src\\CallbackFunctions.cpp", # only for testing
	"sources\\fmipp\\import\\base\\src\\LogBuffer.cpp", # only for testing
]

# Source code for the PowerFactory FMU Export Utility.
source_code = [
	'sources\\api\\include\\PowerFactory.h',
	'sources\\api\\include\\PowerFactoryLoggerBase.h',
	'sources\\api\\include\\PowerFactoryRMS.h',
	'sources\\api\\include\\SmartValue.h',
	'sources\\api\\include\\Utils.h',
	'sources\\api\\src\\PowerFactory.cpp',
	'sources\\api\\src\\PowerFactoryRMS.cpp',
	'sources\\api\\src\\Utils.cpp',
	'sources\\fmiadapter\\include\\digusermodel.def',
	'sources\\fmiadapter\\include\\digusermodel.h',
	'sources\\fmiadapter\\include\\FMIAdapter.h',
	'sources\\fmiadapter\\include\\GetNextEventStatus.h',
	'sources\\fmiadapter\\include\\RmsSimEventQueue.h',
	'sources\\fmiadapter\\src\\accessRmsSimEventQueue.cpp',
	'sources\\fmiadapter\\src\\digusermodel.c',
	'sources\\fmiadapter\\src\\FMIAdapter.c',
	'sources\\fmiadapter\\src\\RmsSimEventQueue.cpp',
	'sources\\frontend\\include\\PowerFactoryExtraOutput.h',
	'sources\\frontend\\include\\PowerFactoryFrontEnd.h',
	'sources\\frontend\\include\\PowerFactoryRealScalar.h',
	'sources\\frontend\\include\\PowerFactoryTimeAdvance.h',
	'sources\\frontend\\src\\PowerFactoryExtraOutput.cpp',
	'sources\\frontend\\src\\PowerFactoryFrontEnd.cpp',
	'sources\\frontend\\src\\PowerFactoryRealScalar.cpp',
	'sources\\frontend\\src\\PowerFactoryTimeAdvance.cpp',
]

# Additional list of files (including relative path) from the repository that are part of the release.
additional_files = [
    'powerfactory_fmu_install.py', # installation script
    'powerfactory_fmu_create.py', # script for creating a PowerFactory FMU
    'build.bat', # batch script for FMU compilation
    'binaries\\README.md',
	'examples\\dplscript\\README.md',
	'examples\\dplscript\\TestDPLScript.pfd',
	'examples\\dplscript\\TestDPLScript-inputs.txt',
	'examples\\dplscript\\TestDPLScript-outputs.txt',
	'examples\\rms\\README.md',
	'examples\\rms\\TestRMS.pfd',
	'examples\\rms\\TestRMS-inputs.txt',
	'examples\\rms\\TestRMS-outputs.txt',
	'examples\\triggers\\README.md',
	'examples\\triggers\\TestTriggers.pfd',
	'examples\\triggers\\TestTriggers-characteristics.csv',
	'examples\\triggers\\TestTriggers-inputs.txt',
	'examples\\triggers\\TestTriggers-outputs.txt',
    'license\\BOOST_SOFTWARE_LICENSE.txt',
    'license\\FMIPP_LICENSE.txt',
    'license\\POWERFACTORY_FMU_LICENSE.txt',
	'sources\\README.md'
]

# List of files (without binaries and docs) that are part of the release.
files_for_release = files_from_fmipp + source_code + additional_files

# List of binaries that are not provided by the repository (see also README in 'binaries' subfolder).
required_binaries = [
    'binaries\\libboost_filesystem-vc120-mt-1_58.lib', # static BOOST Filesystem library
    'binaries\\libboost_system-vc120-mt-1_58.lib', # static BOOST System libarary
    'binaries\\libboost_thread-vc120-mt-1_58.lib', # static BOOST Thread libarary
    'binaries\\libfmipp_fmu_frontend.lib', # static library containing pre-compiled parts of the front end
    'binaries\\fmiadapter.dll', # to be copied to PowerFactory's bin directory (e.g., C:\DIgSILENT\pf2017)
]

# The compiled documentation in PDF format (not part of the repository).
doc_file = 'doc\\powerfactory-fmu-doc.pdf'

