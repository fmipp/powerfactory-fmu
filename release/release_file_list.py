# ----------------------------------------------------------------------
# Copyright (c) 2015, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file TRNSYS_FMU_LICENSE.txt for details.
# ----------------------------------------------------------------------

########################################################################
#
# This script provides the list of files included into a release of 
# the FMI++ PowerFactory Export Utility.
#
########################################################################


# List of source files (including relative path) that are originally from FMI++.
files_from_fmipp = [
    'sources\\common\\FMIPPConfig.h',
    'sources\\common\\FMIType.h',
    'sources\\common\\fmi_v1.0\\fmi_cs.h',
    'sources\\common\\fmi_v1.0\\fmiModelTypes.h',
    'sources\\export\\functions\\fmiFunctions.cpp',
    'sources\\export\\functions\\fmiFunctions.h',
    'sources\\export\\include\\FMIComponentFrontEndBase.h',
    'sources\\export\\examples\\powerfactory\\PowerFactoryFrontEnd.h'
]

# Additional list of files (including relative path) from the repository that are part of the release.
additional_files = [
    'powerfactory_fmu_install.py', # installation script
    'powerfactory_fmu_create.py', # script for creating a PowerFactory FMU
    'build.bat', # batch script for FMU compilation
    'binaries\\README.txt',
    'license\\BOOST_SOFTWARE_LICENSE.txt',
    'license\\FMIPP_LICENSE.txt',
    'license\\POWERFACTORY_FMU_LICENSE.txt',
    'test\\dplscript\\README.txt',
    'test\\dplscript\\TestDPLScript.pfd',
    'test\\dplscript\\TestDPLScript-inputs.txt',
    'test\\dplscript\\TestDPLScript-outputs.txt',
    'test\\triggers\\README.txt',
    'test\\triggers\\TestTriggers.pfd',
    'test\\triggers\\TestTriggers-inputs.txt',
    'test\\triggers\\TestTriggers-outputs.txt',
    'test\\triggers\\TestTriggers-characteristics.csv'
]

# List of files (without binaries and docs) that are part of the release.
files_for_release = files_from_fmipp + additional_files

# List of binaries that are not provided by the repository (see also README in 'binaries' subfolder).
required_binaries = [
    'binaries\\libboost_chrono-vc100-mt-1_58.lib', # static BOOST Chrono libarary
    'binaries\\libboost_date_time-vc100-mt-1_58.lib', # static BOOST date-time library
    'binaries\\libboost_filesystem-vc100-mt-1_58.lib', # static BOOST Filesystem library
    'binaries\\libboost_regex-vc100-mt-1_58.lib', # static BOOST Regex libarary
    'binaries\\libboost_system-vc100-mt-1_58.lib', # static BOOST System libarary
    'binaries\\libboost_thread-vc100-mt-1_58.lib', # static BOOST Thread libarary
    'binaries\\libfmipp_fmu_frontend.lib', # static library containing pre-compiled parts of the front end
    'binaries\\PFSim.lib', # static PFSim wrapper library
    'binaries\\digexdyn.lib', # include library for 'digexdyn.dll'
    'binaries\\digexdyn.dll', # to be copied to PowerFactory's bin directory (e.g., C:\DIgSILENT\pf152)
    'binaries\\digexfun1.lib', # include library for 'digexfun1.dll'
    'binaries\\digexfun1.dll', # to be copied to PowerFactory's bin directory (e.g., C:\DIgSILENT\pf152)
]

# The compiled documentation in PDF format (not part of the repository).
doc_file = 'doc\\powerfactory-fmu-doc.pdf'

