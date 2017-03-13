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
set( User_PF_API_INCLUDE_DIR "D:/DIgSILENT/pf2016/Api/include" CACHE PATH "directory containing the implementation of the PF API" )
set( User_PF_USER_MODEL_LIB_DIR "D:/DIgSILENT/pf2016/digusermodel/Release" CACHE PATH "directory containing the implementation of library 'ControllerLibrary.lib'" )

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
include_directories( ${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory )
include_directories( ${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/api/include )
include_directories( ${User_FMIPP_SOURCE_DIR} )
include_directories( ${User_PF_API_INCLUDE_DIR} )


# PowerFactory front end component library (for FMU DLL).
add_library( libfmipp_fmu_frontend STATIC
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/PowerFactoryFrontEnd.cpp
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/PowerFactoryTimeAdvance.cpp
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/PowerFactoryExtraOutput.cpp
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/PowerFactoryRealScalar.cpp
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/api/src/PowerFactory.cpp
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/api/src/PowerFactoryRMS.cpp
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/api/src/SimpleLogger.cpp
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/api/src/Utils.cpp
	${User_FMIPP_SOURCE_DIR}/export/src/FMIComponentFrontEndBase.cpp
	${User_FMIPP_SOURCE_DIR}/export/src/HelperFunctions.cpp
	${User_FMIPP_SOURCE_DIR}/export/src/ScalarVariable.cpp
	${User_FMIPP_SOURCE_DIR}/import/base/src/ModelDescription.cpp
	${User_FMIPP_SOURCE_DIR}/import/base/src/PathFromUrl.cpp
)

add_library( digexdyn SHARED
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/digexdyn/digexdyn.def
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/digexdyn/digexdyn.cpp
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/digexdyn/userdyn.cpp
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/api/src/RmsSimEventQueue.cpp )

target_link_libraries( digexdyn
	Shlwapi
	${CMAKE_DL_LIBS}
	${Boost_LIBRARIES}
	)

add_library( FMIEventTrigger SHARED
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/FMIEventTrigger/digusermodel.def
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/FMIEventTrigger/digusermodel.c
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/FMIEventTrigger/FMIEventTrigger.c
	${User_FMIPP_SOURCE_DIR}/export/tools/powerfactory/FMIEventTrigger/accessRmsSimEventQueue.cpp )

target_link_libraries( FMIEventTrigger
	Shlwapi
	${CMAKE_DL_LIBS}
	${Boost_LIBRARIES}
	${User_PF_USER_MODEL_LIB_DIR}/ControllerLibrary.lib
	digexdyn
	)
