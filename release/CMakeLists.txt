# -----------------------------------------------------------------------
# Copyright (c) 2015-2018, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file POWERFACTORY_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------------

cmake_minimum_required(VERSION 3.12.0)

#
# This project builds the PowerFactory FMI front end 
# component, which can be used to build a shared library 
# that is compliant with the FMI specification.
#
# ATTENTION: When using Visual Studio, be sure to compile
# in "Release" mode.
#


# Variables to be defined by the user.
set( User_PF_API_INCLUDE_DIR "C:/DIgSILENT/pf2018/Api/include" CACHE PATH "directory containing the implementation of the PF API" )
set( User_PF_USER_MODEL_LIB_DIR "C:/DIgSILENT/pf2018/digusermodel/Release/VS2013" CACHE PATH "directory containing the implementation of library 'ControllerLibrary.lib'" )


# Define project.
project( FMIPP_POWERFACTORY_FMU_EXPORT )


# OS- and compiler-specific settings.
if ( NOT DEFINED WIN32 )
   message( FATAL_ERROR "This project requires Windows." )
else ()
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

      # Additional compiler flags.
      add_definitions( -DBUILD_FMI_DLL )
      add_definitions( -DBOOST_ALL_NO_LIB )
      add_definitions( -D_CRT_SECURE_NO_WARNINGS )
      add_definitions( -D_WINSOCK_DEPRECATED_NO_WARNINGS )

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


# Boost setup.
set( Boost_USE_STATIC_LIBS ON ) # OFF when using shared Boost libs.
set( Boost_USE_MULTITHREADED ON )
set( Boost_USE_STATIC_RUNTIME OFF )
find_package( Boost COMPONENTS thread system filesystem REQUIRED )
if ( Boost_FOUND )
   include_directories( ${Boost_INCLUDE_DIRS} )
   link_directories( ${Boost_LIBRARY_DIRS} )
endif ()


# Include directories.
include_directories( ${PROJECT_SOURCE_DIR}/../sources )
include_directories( ${PROJECT_SOURCE_DIR}/../sources/fmipp )
include_directories( ${User_PF_API_INCLUDE_DIR} )


# PowerFactory front end component library (pre-compiled basis for FMU DLL).
add_library( libfmipp_fmu_frontend STATIC
	${PROJECT_SOURCE_DIR}/../sources/frontend/src/PowerFactoryFrontEnd.cpp
	${PROJECT_SOURCE_DIR}/../sources/frontend/src/PowerFactoryTimeAdvance.cpp
	${PROJECT_SOURCE_DIR}/../sources/frontend/src/PowerFactoryExtraOutput.cpp
	${PROJECT_SOURCE_DIR}/../sources/frontend/src/PowerFactoryRealScalar.cpp
	${PROJECT_SOURCE_DIR}/../sources/api/src/PowerFactory.cpp
	${PROJECT_SOURCE_DIR}/../sources/api/src/PowerFactoryRMS.cpp
	${PROJECT_SOURCE_DIR}/../sources/api/src/Utils.cpp
	${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/FMIComponentFrontEndBase.cpp
	${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/HelperFunctions.cpp
	${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/ScalarVariable.cpp
	${PROJECT_SOURCE_DIR}/../sources/fmipp/import/base/src/ModelDescription.cpp
	${PROJECT_SOURCE_DIR}/../sources/fmipp/import/base/src/PathFromUrl.cpp
)


# DLL for user-defined PowerFactory DSL model (FMIAdapter).
add_library( fmiadapter SHARED
	${PROJECT_SOURCE_DIR}/../sources/fmiadapter/include/digusermodel.def
	${PROJECT_SOURCE_DIR}/../sources/fmiadapter/src/digusermodel.c
	${PROJECT_SOURCE_DIR}/../sources/fmiadapter/src/FMIAdapter.c
	${PROJECT_SOURCE_DIR}/../sources/fmiadapter/src/RmsSimEventQueue.cpp
	${PROJECT_SOURCE_DIR}/../sources/fmiadapter/src/accessRmsSimEventQueue.cpp
)


target_link_libraries( fmiadapter
	Shlwapi
	${CMAKE_DL_LIBS}
	${Boost_LIBRARIES}
	${User_PF_USER_MODEL_LIB_DIR}/ControllerLibrary.lib
)
