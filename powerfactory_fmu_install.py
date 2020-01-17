# -----------------------------------------------------------------------
# Copyright (c) 2015-2020, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file POWERFACTORY_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------------

import sys, os, shutil, pickle, subprocess

### Python 2
# def log( *arg ): print ' '.join( map( str, arg ) )

### Python 3
def log( *arg ): print( ' '.join( map( str, arg ) ) )


def savePowerFactoryInstallDir( pf_fmu_root_dir, pf_install_dir ):
   # Save name of install directory to file (used by script 'powerfactory_fmu_create.py').
   output = open( os.path.join( pf_fmu_root_dir, 'powerfactory_fmu_install.pkl' ), 'wb' )
   pickle.dump( pf_install_dir, output )
   output.close()


def installPFSim( pf_fmu_root_dir, pf_install_dir ):
   # Check if file binaries\fmiadapter.dll exists.
   fmiadapter_file_name = os.path.join( pf_fmu_root_dir, 'binaries', 'fmiadapter.dll' )
   if ( False == os.path.isfile( fmiadapter_file_name ) ):
      err = 'ERROR: file {} not found'.format( fmiadapter_file_name )
      raise( RuntimeError( err ) )
   
   # Copy fmiadapter.dll to PowerFactory installation directory
   shutil.copy( fmiadapter_file_name, pf_install_dir )


def checkForPFAPI( pf_install_dir ):
   # Check if PowerFactory API is available.
   pf_api_dir_name = os.path.join( pf_install_dir, 'Api' )
   if ( False == os.path.isdir( pf_api_dir_name ) ):
      err = 'ERROR: PowerFactory API not found in directory {}'.format( pf_api_dir_name )
      raise( Exception( err ) )


def checkForPFExecutable():
   devnull = open(os.devnull, 'w')
   status = subprocess.call( [ 'WHERE', 'PowerFactory.exe' ], stdout=devnull, stderr=devnull )
   if ( 0 != status ): 
      err = '\nERROR: \'PowerFactory.exe\' not found. Please add PowerFactory\'s installation directory to the system path!'
      raise( Exception( err ) )


def main( pf_fmu_root_dir, pf_install_dir ):
   try:
      # Check if directory exists.
      if ( False == os.path.isdir( pf_install_dir ) ):
         err = '\nWARNING: {} is not a valid directory'.format( pf_install_dir )
         raise( Exception( err ) )
   
      # Save name of install directory to file (used by script 'powerfactory_fmu_create.py').
      savePowerFactoryInstallDir( pf_fmu_root_dir, pf_install_dir )
   
      # Install PFSim.
      installPFSim( pf_fmu_root_dir, pf_install_dir )
   
      # Check if PF main executable (PowerFactory.exe) is included in the system path.
      checkForPFExecutable()
   
      # Check if PF API is available.
      checkForPFAPI( pf_install_dir )
   
      log( '\nFMI++ PowerFactory FMU Export Utility successfully installed.' )
   except Exception as e:
      log( e )


if __name__ == "__main__":

   # Check for correct number of input parameters.
   if ( 2 != len( sys.argv ) ):
      log( '\nERROR: Wrong number of arguments!' )
      log( '\nUsage:\n\n\tpython powerfactory_fmu_install.py <powerfactory_install_directory>\n' )
      sys.exit()

   # Set PowerFactory installation directory.
   pf_install_dir_ = sys.argv[1]

   # Relative or absolute path to PowerFactory FMU Export Utility.
   pf_fmu_root_dir_ = os.path.dirname( __file__ )

   main( pf_fmu_root_dir_, pf_install_dir_ )
