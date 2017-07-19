# -----------------------------------------------------------------------
# Copyright (c) 2015-2017, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file POWERFACTORY_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------------


cmake_minimum_required(VERSION 2.8)

#
# This project builds tests for the PowerFactory FMU Export Utility.
# It requires Microsoft Visual Studio 2013.
#

# Define project.
project( PF_FMU_Export_Utility_Test )

# Variables to be defined by the user.
set( User_PF_ROOT_DIR "C:/DIgSILENT/pf2017" CACHE PATH "directory containing the implementation of the PF API" )
set( User_PF_API_LIB_DIR "C:/DIgSILENT/pf2017/Api/lib/VS2013" CACHE PATH "directory containing the implementation of the PF API" )

# Other project-specific variables.
set( MODEL_IDENTIFIER "PF_FMU_Test" CACHE STRING "FMI model identfier" )
set( PF_FMU_BIN_DIR "${PROJECT_SOURCE_DIR}/../../binaries" )
set( PF_FMU_SRC_DIR "${PROJECT_SOURCE_DIR}/../../sources" )

# OS-specific settings.
if ( NOT DEFINED WIN32 )
   message( FATAL_ERROR "This project requires Windows." )
endif ()

if ( NOT DEFINED MSVC12 )
   message( FATAL_ERROR "This project requires Microsift Visual Studio 2013" )
else ()
   if (CMAKE_SIZEOF_VOID_P EQUAL 8)
      set(FMU_BIN_DIR "win64")
   else ()
      set(FMU_BIN_DIR "win32")
   endif ()
   set(FMU_BIN_EXT ".dll")
endif ()
add_definitions(-DFMU_BIN_DIR="${FMU_BIN_DIR}")
add_definitions(-DFMU_BIN_EXT="${FMU_BIN_EXT}")

# Compiler flags.
add_definitions( -DMODEL_IDENTIFIER=${MODEL_IDENTIFIER} )
add_definitions( -DFRONT_END_TYPE=PowerFactoryFrontEnd )
add_definitions( -DFRONT_END_TYPE_INCLUDE="frontend/include/PowerFactoryFrontEnd.h" )
add_definitions( -DBUILD_FMI_DLL )
add_definitions( -DBOOST_ALL_NO_LIB )
add_definitions( -D_CRT_SECURE_NO_WARNINGS )
add_definitions( -D_WINSOCK_DEPRECATED_NO_WARNINGS )
add_definitions( /W3 )

# Boost setup.
set( Boost_USE_MULTITHREADED ON )
set( Boost_USE_STATIC_RUNTIME OFF )
# Note: The flag below is set to OFF in order to make the tests (defined below) work.
# However, ususally this flag should be set to ON when building the API for PowerFactory.
set( Boost_USE_STATIC_LIBS OFF )
# Find packages needed for unit test framework.
find_package( Boost COMPONENTS system filesystem unit_test_framework REQUIRED )
if ( Boost_FOUND )
   include_directories( ${Boost_INCLUDE_DIRS} )
   link_directories( ${Boost_LIBRARY_DIRS} )
endif ()


# Include directories.
include_directories( ${PF_FMU_SRC_DIR} )
include_directories( ${PF_FMU_SRC_DIR}/fmipp )

# Source code.
add_library( ${MODEL_IDENTIFIER} SHARED
	${PF_FMU_SRC_DIR}/fmipp/export/functions/fmi_v1.0/fmiFunctions.cpp
)

# Link library.
target_link_libraries( ${MODEL_IDENTIFIER}
	Shlwapi
	${CMAKE_DL_LIBS}
	${User_PF_API_LIB_DIR}/digapivalue.lib
	${PF_FMU_BIN_DIR}/fmiadapter.lib
	${PF_FMU_BIN_DIR}/libfmipp_fmu_frontend.lib
	${PF_FMU_BIN_DIR}/libboost_filesystem-vc120-mt-1_58.lib
	${PF_FMU_BIN_DIR}/libboost_thread-vc120-mt-1_58.lib
	${PF_FMU_BIN_DIR}/libboost_system-vc120-mt-1_58.lib )



# Path to XML model description and additional files.
set( FMU_URI_BASE "file://${PROJECT_SOURCE_DIR}/../../examples" CACHE INTERNAL "" )
add_definitions( -DFMU_URI_BASE="${FMU_URI_BASE}" )

# Add and link executable.
add_executable( testPowerFactoryBasics WIN32
	${PROJECT_SOURCE_DIR}/testPowerFactoryBasics.cpp
	${PF_FMU_SRC_DIR}/fmipp/import/base/src/CallbackFunctions.cpp
	${PF_FMU_SRC_DIR}/fmipp/import/base/src/LogBuffer.cpp )
target_link_libraries( testPowerFactoryBasics
	${MODEL_IDENTIFIER}
	${Boost_FILESYSTEM_LIBRARY}
	${Boost_SYSTEM_LIBRARY}
	${Boost_UNIT_TEST_FRAMEWORK_LIBRARY} )

# Add and link executable.
add_executable( testPowerFactoryTriggers WIN32
	${PROJECT_SOURCE_DIR}/testPowerFactoryTriggers.cpp
	${PF_FMU_SRC_DIR}/fmipp/import/base/src/CallbackFunctions.cpp
	${PF_FMU_SRC_DIR}/fmipp/import/base/src/LogBuffer.cpp )
target_link_libraries( testPowerFactoryTriggers
	${MODEL_IDENTIFIER}
	${Boost_FILESYSTEM_LIBRARY}
	${Boost_SYSTEM_LIBRARY}
	${Boost_UNIT_TEST_FRAMEWORK_LIBRARY} )

# Add and link executable.
add_executable( testPowerFactoryDPLScript WIN32
	${PROJECT_SOURCE_DIR}/testPowerFactoryDPLScript.cpp
	${PF_FMU_SRC_DIR}/fmipp/import/base/src/CallbackFunctions.cpp
	${PF_FMU_SRC_DIR}/fmipp/import/base/src/LogBuffer.cpp )
target_link_libraries( testPowerFactoryDPLScript
	${MODEL_IDENTIFIER}
	${Boost_FILESYSTEM_LIBRARY}
	${Boost_SYSTEM_LIBRARY}
	${Boost_UNIT_TEST_FRAMEWORK_LIBRARY} )

# Add and link executable.
add_executable( testPowerFactoryRMS WIN32
	${PROJECT_SOURCE_DIR}/testPowerFactoryRMS.cpp
	${PF_FMU_SRC_DIR}/fmipp/import/base/src/CallbackFunctions.cpp
	${PF_FMU_SRC_DIR}/fmipp/import/base/src/LogBuffer.cpp )
target_link_libraries( testPowerFactoryRMS
	${MODEL_IDENTIFIER}
	${Boost_FILESYSTEM_LIBRARY}
	${Boost_SYSTEM_LIBRARY}
	${Boost_UNIT_TEST_FRAMEWORK_LIBRARY} )

# Post build action: copy executable to (new) subdirectory test.
add_custom_command( TARGET ${MODEL_IDENTIFIER} POST_BUILD
	COMMAND ${CMAKE_COMMAND} -E copy ${PF_FMU_BIN_DIR}/fmiadapter.lib ${User_PF_ROOT_DIR} )

# Post build action: copy executable to (new) subdirectory test.
add_custom_command( TARGET ${MODEL_IDENTIFIER} POST_BUILD
	COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/test )
	
# Post build action: copy executable to (new) subdirectory test.
add_custom_command( TARGET testPowerFactoryBasics POST_BUILD
	COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:testPowerFactoryBasics> ${CMAKE_BINARY_DIR}/test )

# Post build action: copy executable to (new) subdirectory test.
add_custom_command( TARGET testPowerFactoryTriggers POST_BUILD
	COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:testPowerFactoryTriggers> ${CMAKE_BINARY_DIR}/test )

# Post build action: copy executable to (new) subdirectory test.
add_custom_command( TARGET testPowerFactoryDPLScript POST_BUILD
	COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:testPowerFactoryDPLScript> ${CMAKE_BINARY_DIR}/test )

# Post build action: copy executable to (new) subdirectory test.
add_custom_command( TARGET testPowerFactoryRMS POST_BUILD
	COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:testPowerFactoryRMS> ${CMAKE_BINARY_DIR}/test )

# Add test.
enable_testing()
include( ${PROJECT_SOURCE_DIR}/CMakeAddTests.txt )
add_test_fmipp( testPowerFactoryBasics )
add_test_fmipp( testPowerFactoryTriggers )
add_test_fmipp( testPowerFactoryDPLScript )
add_test_fmipp( testPowerFactoryRMS )
