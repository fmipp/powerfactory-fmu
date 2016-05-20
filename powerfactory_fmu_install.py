# ------------------------------------------------------------------------
# Copyright (c) 2015, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file POWERFACTORY_FMU_LICENSE.txt for details.
# ------------------------------------------------------------------------

import sys, os, shutil, pickle


def savePowerFactoryInstallDir( pf_install_dir ):
        # Save name of install directory to file (used by script 'powerfactory_fmu_create.py').
        output = open( 'powerfactory_fmu_install.pkl', 'wb' )
        pickle.dump( pf_install_dir, output )
        output.close()


def installPFSim( pf_install_dir ):
        # Check if file binaries\digexdyn.dll exists.
        digexdyn_file_name = os.path.join( 'binaries', 'digexdyn.dll' )
        if ( False == os.path.isfile( digexdyn_file_name ) ):
                print '\nERROR: file', digexdyn_file_name, 'not found'
                sys.exit()

        # Check if file binaries\digexdyn.dll exists.
        digexfun1_file_name = os.path.join( 'binaries', 'digexfun1.dll' )
        if ( False == os.path.isfile( digexfun1_file_name ) ):
                print '\nERROR: file', digexfun1_file_name, 'not found'
                sys.exit()

        # Copy digexdyn.dll and digexfun1.dll to PowerFactory installation directory
        shutil.copy( os.path.join( 'binaries', 'digexdyn.dll' ), pf_install_dir )
        shutil.copy( os.path.join( 'binaries', 'digexfun1.dll' ), pf_install_dir )


if __name__ == "__main__":
        
        # Check for correct number of input parameters.
        if( 2 != len( sys.argv ) ):
                print '\nERROR: Wrong number of arguments!'
                print '\nUsage:\n\n\tpython powerfactory_fmu_install.py <powerfactory_install_directory>\n'
                sys.exit()

        # Set PowerFactory installation directory.
        pf_install_dir = sys.argv[1]
        
        # Check if directory exists.
        if( False == os.path.isdir( pf_install_dir ) ):
                print '\nERROR:', pf_install_dir, 'is not a valid directory'
	
        # Save name of install directory to file (used by script 'powerfactory_fmu_create.py').
        savePowerFactoryInstallDir( pf_install_dir )
        
        # Install PFSim.
        installPFSim( pf_install_dir )

        print '\nFMI++ PowerFactory FMU Export Utility successfully installed.'
        print '\nATTENTION: Please do not forget to add PowerFactory\'s installation directory to the Windows path!!!'
