# --------------------------------------------------------------
# Copyright (c) 2015, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file TRNSYS_FMU_LICENSE for details.
# --------------------------------------------------------------

cmake_minimum_required(VERSION 2.8)

#
# This project builds the PowerFactory FMI front end 
# component, which can be used to build a shared library 
# that is compliant with the FMI specification.
#
# ATTENTION: When using Visual Studio, be sure to compile
# in "Release" mode.
#


# Variables to be defined by the user.
set( User_FMIPP_SOURCE_DIR "D:/Development/fmipp" CACHE PATH "FMI++ source directory" )
set( User_PFSIM_SOURCE_DIR "D:/Tools/PFupdates/src/PFSim/src" CACHE PATH "PFSim source directory" )

# Define project.
project( FMIPP_POWERFACTORY_FMU_EXPORT )


# OS- and compiler-specific settings.
if ( NOT DEFINED WIN32 )
   message( FATAL_ERROR "This project requires Windows." )
else ()
   if ( CMAKE_SIZEOF_VOID_P EQUAL 8 )
      set( FMU_BIN_DIR "win64" )
   else ()
      set( FMU_BIN_DIR "win32" )
   endif ()
   set( FMU_BIN_EXT ".dll" )

   set( PATH_SEPARATOR ";" )
   set( CMAKE_SHARED_LIBRARY_PREFIX "" )
   set( CMAKE_SHARED_MODULE_PREFIX "" )
   add_definitions( -DWIN32 )

   if ( MINGW )
      message( FATAL_ERROR "This project requires Visual Studio." )
   endif ()

   if ( MSVC )
      # disable auto-linking and use cmake's dependency handling
      add_definitions( -DBOOST_ALL_NO_LIB /W3 )
	  
      # Define target output directory.
      foreach( OUTPUTCONFIG ${CMAKE_CONFIGURATION_TYPES} )
	     string( TOUPPER ${OUTPUTCONFIG} OUTPUTCONFIG )
         set( CMAKE_RUNTIME_OUTPUT_DIRECTORY_${OUTPUTCONFIG} ${PROJECT_SOURCE_DIR}/../binaries )
         set( CMAKE_LIBRARY_OUTPUT_DIRECTORY_${OUTPUTCONFIG} ${PROJECT_SOURCE_DIR}/../binaries )
         set( CMAKE_ARCHIVE_OUTPUT_DIRECTORY_${OUTPUTCONFIG} ${PROJECT_SOURCE_DIR}/../binaries )
      endforeach( OUTPUTCONFIG CMAKE_CONFIGURATION_TYPES )

      # Add reminder to compile in "Release" mode when using Visual Studio.
      message( "ATTENTION: The PowerFactory wrapper has to be compiled in RELEASE mode!!!" )

   endif ()

endif ()


# Compiler flags.
add_definitions( -DBUILD_FMI_DLL )
add_definitions( -DBOOST_ALL_NO_LIB )


# Boost dependencies here
if ( MSVC )
   set( Boost_USE_STATIC_LIBS ON ) # OFF when using shared Boost libs.
   set( Boost_USE_MULTITHREADED ON )
   set( Boost_USE_STATIC_RUNTIME OFF )
endif ()

find_package( Boost )

if ( Boost_FOUND )
   include_directories( ${Boost_INCLUDE_DIRS} )
endif ()

# PowerFactory front end component library (for FMU DLL).
add_library( libfmipp_fmu_frontend STATIC
	     ${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/PowerFactoryFrontEnd.cpp
	     ${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/PowerFactoryTimeAdvance.cpp
	     ${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/PowerFactoryExtraOutput.cpp
	     ${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/PowerFactoryRealScalar.cpp
	     ${User_FMIPP_SOURCE_DIR}/export/src/FMIComponentFrontEndBase.cpp
	     ${User_FMIPP_SOURCE_DIR}/export/src/HelperFunctions.cpp
	     ${User_FMIPP_SOURCE_DIR}/export/src/ScalarVariable.cpp
	     ${User_FMIPP_SOURCE_DIR}/import/base/src/ModelDescription.cpp
	     ${User_FMIPP_SOURCE_DIR}/import/base/src/PathFromUrl.cpp
		 )

# Include directories.
include_directories( ${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory )
include_directories( ${User_FMIPP_SOURCE_DIR} )
include_directories( ${User_PFSIM_SOURCE_DIR} )
