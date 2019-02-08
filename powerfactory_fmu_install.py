# ------------------------------------------------------------------------
# Copyright (c) 2015-2017, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file POWERFACTORY_FMU_LICENSE.txt for details.
# ------------------------------------------------------------------------

import sys, os, shutil, pickle, subprocess

# def _print( *arg ): print ' '.join( map( str, arg ) )
def _print( *arg ): print( ' '.join( map( str, arg ) ) )


def savePowerFactoryInstallDir( pf_install_dir ):
        # Save name of install directory to file (used by script 'powerfactory_fmu_create.py').
        output = open( 'powerfactory_fmu_install.pkl', 'wb' )
        pickle.dump( pf_install_dir, output )
        output.close()


def installPFSim( pf_install_dir ):
        # Check if file binaries\fmiadapter.dll exists.
        fmiadapter_file_name = os.path.join( 'binaries', 'fmiadapter.dll' )
        if ( False == os.path.isfile( fmiadapter_file_name ) ):
                _print( '\nERROR: file', fmiadapter_file_name, 'not found' )
                sys.exit()

        # Copy fmiadapter.dll to PowerFactory installation directory
        shutil.copy( fmiadapter_file_name, pf_install_dir )


def checkForPFAPI( pf_install_dir ):
        # Check if PowerFactory API is available.
        pf_api_dir_name = os.path.join( pf_install_dir, 'Api' )
        if ( False == os.path.isdir( pf_api_dir_name ) ):
                _print( '\nERROR: PowerFactory API not found in directory', pf_api_dir_name )
                sys.exit()


def checkForPFExecutable():
        try:
                devnull = open(os.devnull, 'w')
                status = subprocess.call( [ 'WHERE', 'PowerFactory.exe' ], stdout=devnull, stderr=devnull )
                if ( 0 != status ): _print( '\nATTENTION: \'PowerFactory.exe\' not found. Please add PowerFactory\'s installation directory to the system path!' )

        except:
                _print( 'Unexpected error:', sys.exc_info()[0] )


if __name__ == "__main__":

        # Check for correct number of input parameters.
        if ( 2 != len( sys.argv ) ):
                _print( '\nERROR: Wrong number of arguments!' )
                _print( '\nUsage:\n\n\tpython powerfactory_fmu_install.py <powerfactory_install_directory>\n' )
                sys.exit()

        # Set PowerFactory installation directory.
        pf_install_dir = sys.argv[1]

        # Check if directory exists.
        if ( False == os.path.isdir( pf_install_dir ) ):
                _print( '\nWARNING:', pf_install_dir, 'is not a valid directory' )

        # Save name of install directory to file (used by script 'powerfactory_fmu_create.py').
        savePowerFactoryInstallDir( pf_install_dir )

        # Install PFSim.
        installPFSim( pf_install_dir )

        # Check if PF main executable (PowerFactory.exe) is included in the system path.
        checkForPFExecutable()

        # Check if PF API is available.
        checkForPFAPI( pf_install_dir )

        _print( '\nFMI++ PowerFactory FMU Export Utility successfully installed.' )
