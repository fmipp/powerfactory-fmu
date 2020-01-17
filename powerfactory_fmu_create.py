# -----------------------------------------------------------------------
# Copyright (c) 2020, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file POWERFACTORY_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------------

#
# This file is used to create FMUs for CoSimulation for DiGSILENT PowerFactory.
#
# By default, it should be used with Python 3. By uncommenting lines 14 & 15
# and commenting lines 18 & 20, it can also be used with Python 2.
#

### Python 2
# import sys, os, shutil, time, getpass, uuid, getopt, pickle, subprocess, glob, argparse, urlparse, urllib, collections
# def log( *arg ): print ' '.join( map( str, arg ) )

### Python 3
import sys, os, shutil, time, getpass, uuid, getopt, pickle, subprocess, glob, argparse, urllib.parse as urlparse, urllib.request as urllib, collections
def log( *arg ): print( ' '.join( map( str, arg ) ), flush = True )

from scripts.utils import *
from scripts.generate_fmu import *

def main( pf_fmu_root_dir = os.path.dirname( __file__ ), parser = None ):

   Modules = collections.namedtuple( 'Modules', [ 'sys', 'os', 'shutil', 'time', 'getpass', 'uuid', 'urlparse', 'urllib', 'getopt', 'pickle', 'subprocess', 'glob', 'argparse', 'log' ] )
   modules = Modules( sys, os, shutil, time, getpass, uuid, urlparse, urllib, getopt, pickle, subprocess, glob, argparse, log )

   # Retrieve parsed command line arguments.
   cmd_line_args = parseCommandLineArguments( modules ) if ( parser == None ) else parser()

   # FMI model identifier.
   fmi_model_identifier = cmd_line_args.model_id

   # PowerFactory PFD file.
   pfd_file_name = cmd_line_args.pfd_file

   # File containing FMI input variable names.
   input_var_file_name = cmd_line_args.input_var_file

   # File containing FMI output variable names.
   output_var_file_name = cmd_line_args.output_var_file

   # List of triggers (for simulation time advance).
   triggers = cmd_line_args.trigger

   # DPL script (for simulation time advance).
   dpl_script = cmd_line_args.dpl_script

   # RMS simulation setup.
   rms_sim = cmd_line_args.rms_sim

   # Set PowerFactory install dir.
   pf_install_dir = cmd_line_args.pf_install_dir

   # Verbose flag.
   verbose = cmd_line_args.verbose

   # Litter flag.
   litter = cmd_line_args.litter

   # FMI version
   fmi_version = cmd_line_args.fmi_version
   if ( True == verbose ): modules.log( '[DEBUG] Using FMI version', fmi_version )

   # Check if specified PFD file exists.
   if ( False == isFileCaseSensitive( pfd_file_name, modules ) ):
      modules.log( '\n[ERROR] Invalid PowerFactory PFD file: ', pfd_file_name )
      sys.exit(4)

   # Retrieve start values and additional files from command line arguments.
   ( optional_files, start_values ) = parseAdditionalInputs( cmd_line_args.extra_arguments, verbose, modules  )

   # No install directory provided -> read from file (created by script 'powerfactory_fmu_install.py').
   if ( None == pf_install_dir ):
      pkl_file_name = modules.os.path.join( pf_fmu_root_dir, 'powerfactory_fmu_install.pkl' )
      if ( True == isFileCaseSensitive( pkl_file_name, modules ) ):
         pkl_file = open( pkl_file_name, 'rb' )
         pf_install_dir = modules.pickle.load( pkl_file )
         pkl_file.close()
      else:
         modules.log( '\n[ERROR] Please run \'powerfactory_fmu_install.exe\' or provide the PowerFactory installation directory as optional argument!' )
         modules.sys.exit(5)

   # Check if specified PowerFactory install directory exists.
   if ( False == modules.os.path.isdir( pf_install_dir ) ):
       modules.log( '\n[WARNING] PowerFactory install directory does not exist: ', pf_install_dir )

   if ( True == verbose ):
      modules.log( '[DEBUG] FMI model identifier: ', fmi_model_identifier )
      modules.log( '[DEBUG] PowerFactory PFD file: ', pfd_file_name )
      modules.log( '[DEBUG] PowerFactory install directory: ', pf_install_dir )
      modules.log( '[DEBUG] Aditional files: ' )
      for file_name in optional_files:
         modules.log( '\t', file_name )

   # Issue a warning in case no files contining input/outout variable name list have been specified.
   if ( ( None == input_var_file_name ) and ( None == output_var_file_name ) ):
      modules.log( '[WARNING] Neither input nor output variable names specified!' )

   # Lists containing the FMI input and output variable names.
   fmi_input_vars = []
   fmi_output_vars = []

   # Parse file to retrieve FMI input variable names.
   if ( None != input_var_file_name ):
      retrieveLabelsFromFile( input_var_file_name, fmi_input_vars, modules );

      if ( True == verbose ):
         modules.log( '[DEBUG] FMI input parameters:' )
         for var in fmi_input_vars:
            modules.log( '\t', var )

   # Parse file to retrieve FMI output variable names.
   if ( None != output_var_file_name ):
      retrieveLabelsFromFile( output_var_file_name, fmi_output_vars, modules );

      if ( True == verbose ):
         modules.log( '[DEBUG] FMI output parameters:' )
         for var in fmi_output_vars:
            modules.log( '\t', var )

   # Check options for time advance mechanism.
   if ( ( 0 == len( dpl_script ) ) and ( 0 == len( triggers ) ) and ( 0 == len( rms_sim ) ) ):
      modules.log( '\n[ERROR] no mechanism for time advance specified' )
      sys.exit(10)
   elif ( ( 0 != len( dpl_script ) ) and ( 0 != len( triggers ) ) ):
      modules.log( '\n[ERROR] Mixing of mechanisms for time advance (triggers and DPL scripts) is not supported!' )
      sys.exit(11)
   elif ( 1 < len( dpl_script ) ):
      modules.log( '\n[ERROR] Defintion of more than one DPL script for simulation time advance is not supported!' )
      sys.exit(12)
   elif ( 1 < len( rms_sim ) ):
      modules.log( '\n[ERROR] Defintion of more than one RMS simulation setup is not supported!' )
      sys.exit(13)

   try:
      fmu_name = generatePowerFactoryFMU(
         fmi_version,
			fmi_model_identifier,
			pfd_file_name,
			pf_install_dir,
			triggers,
			dpl_script,
			rms_sim,
			fmi_input_vars,
			fmi_output_vars,
			start_values,
			optional_files,
			pf_fmu_root_dir,
			litter,
         verbose,
         modules )

      if ( True == verbose ): modules.log( "[DEBUG] FMU created successfully:", fmu_name )

   except Exception as e:
      modules.log( e )
      modules.sys.exit( e.args[0] )


# Main function
if __name__ == "__main__":
    main()
