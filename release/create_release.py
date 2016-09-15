# ---------------------------------------------------------------------------------
# Copyright (c) 2015, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file POWERFACTORY_FMU_LICENSE.txt for details.
# ---------------------------------------------------------------------------------

###################################################################################
#
# This script creates a new release of the FMI++ PowerFactory FMU Export Utility.
#
# Before running this scrip, do the following:
#   - compile the documentation (doc\powerfactory-fmu-doc.tex)
#   - compile the FMI++ related binaries (release\CMakeLists.txt)
#   - copy the external BOOST libraries (see binaries\README.txt)
#
###################################################################################


import sys, os, zipfile, zlib

# def _print( *arg ): print ' '.join( map( str, arg ) )
def _print( *arg ): print( ' '.join( map( str, arg ) ) )

# Import module with lists of files for release.
from release_file_list import *


def checkFilesExist( doc_file, required_binaries, cwd ):
    # Check if files from repository are available.
    for file in files_for_release:
        full_file_name = cwd + '\\..\\' + file
        if ( False == os.path.isfile( full_file_name ) ):
            _print( file, 'not found' )
            return False
    
    # Check if additional binaries are available.
    for file in required_binaries:
        full_file_name = cwd + '\\..\\' + file
        if ( False == os.path.isfile( full_file_name ) ):
            _print( file, 'not found' )
            return False

    # Check if documentation is available.
    if ( False == os.path.isfile( cwd + '\\..\\' + doc_file ) ):
        _print( doc_file, 'not found' )
        return False
    
    return True


def createRelease( release_file, release_name, cwd ):
    base_name = '\\' + release_name + '\\'
    for file in files_for_release:
        release_file.write( cwd + '\\..\\' + file, base_name + file )
    
    for file in required_binaries:
        release_file.write( cwd + '\\..\\' + file, base_name + file )
    
    release_file.write( cwd + '\\..\\' + doc_file, base_name + 'documentation\\powerfactory-fmu-doc.pdf' )


if __name__ == "__main__":

    if len( sys.argv ) != 2:
        _print( 'Usage:\n\tpython create-release.py <release-name>\n' )
        _print( 'Attention: Be sure to execute this script from subfolder \'release\'\n' )
        sys.exit()
    
    # Get current working directory (should be subfolder 'release').
    cwd = os.getcwd()
    if ( 'release' != os.path.basename( cwd ) ):
        _print( 'Attention: Be sure to execute this script from subfolder \'release\'\n' )
        sys.exit()
    
    # Check if files exist.
    if ( False == checkFilesExist( doc_file, required_binaries, cwd ) ):
        sys.exit()
    
    # Define release name.
    release_name = 'powerfactory-fmu-' + sys.argv[1]

    # Define release file name.
    release_file_name = release_name + '.zip'
    
    # Create release archive.
    release_file = zipfile.ZipFile( release_file_name, 'w', compression = zipfile.ZIP_DEFLATED )
    
    # Copy files to release archive.
    createRelease( release_file, release_name, cwd )
    
    # Close release archive.
    release_file.close()
