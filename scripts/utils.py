# -----------------------------------------------------------------------
# Copyright (c) 2020, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file POWERFACTORY_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------------


#
# Collection of helper functions for creating FMU CS according to FMI 2.0 for DIgSILENT PowerFactory.
#

# Parse command line arguments.
def parseCommandLineArguments( modules ):
   # Create new parser.
   parser = modules.argparse.ArgumentParser( description = 'This script generates FMUs for Co-Simulation (tool coupling) for DIgSILENT PowerFactory.', prog = 'pf_fmu_create' )

   # Define optional arguments.
   parser.add_argument( '-f', '--fmi-version', choices = [ '1', '2' ], default = '2', help = 'Specify FMI version (default: 2)' )
   parser.add_argument( '-i', '--input-var-file', default = None, help = 'Specify file containing list of input variable names. Files containing lists of input variable names are expected to be in clear text, listing exactly one valid variable name per line. Variable names are supposed to be of the  form "<class-name>.<object-name>.<parameter-name>". For RMS simulations, input events have to be specified in the form \"<event-type>.<target-slot>.<parameter-name>\" (currently only events of type "EvtParam" are supported).', metavar = 'INPUT-VAR-FILE' )
   parser.add_argument( '-o', '--output-var-file', default = None, help = 'Specify file containing list of output variable names. Files containing lists of output variable names are expected to be in clear text, listing exactly one valid variable name per line. Variable names are supposed to be of the  form "<class-name>.<object-name>.<parameter-name>".', metavar = 'OUTPUT-VAR-FILE' )
   parser.add_argument( '-t', '--trigger', action = 'append', default = [], help = 'Specify a trigger for advancing simulation time. Triggers for simulation time advance need to be defined in the form \"<name>:<scale>\". The name has to be given according to the trigger\'s object name in the PFD file. Times given to the FMU are interpreted as seconds, therefore the scale can be adjusted to match the trigger\'s internal unit of time (e.g., 60 for minutes or 3600 for hours). Multiple triggers may be defined.', metavar = 'TRIGGER' )
   parser.add_argument( '-s', '--dpl-script', action = 'append', default = [], help = 'Specify a DPL-script for advancing simulation time. A single DPL script may be specified to advance simulation time in the form \"<name>:<scale>:<offset>\". Times given to the FMU are interpreted as seconds, therefore the scale and offset can be adjusted to match the script\'s internal unit of time (e.g., 60 for minutes or 3600 for hours).', metavar = 'DPL-SCRIPT' )
   parser.add_argument( '-r', '--rms-sim', action = 'append', default = [], help = 'Specify an RMS simulation setup. For RMS simulations, the integrator step size (in seconds) has to be specified.', metavar = 'RMS-SIM' )
   parser.add_argument( '-d', '--pf-install-dir', default = None, help = 'Path to PowerFactory installation directory (e.g., C:\\DIgSILENT\\pf2019)', metavar = 'PF-INSTALL-DIR' )
   parser.add_argument( '-v', '--verbose', action = 'store_true', help = 'Turn on log messages' )
   parser.add_argument( '-l', '--litter', action = 'store_true', help = 'Do not clean-up intermediate files' )

   # Define mandatory arguments.
   required_args = parser.add_argument_group( 'required arguments' )
   required_args.add_argument( '-m', '--model-id', required = True, help = 'Specify FMU model identifier', metavar = 'MODEL-ID' )
   required_args.add_argument( '-p', '--pfd-file', required = True, help = 'Path to PowerFactory PFD file', metavar = 'PFD-FILE' )

   # Parse remaining optional arguments (start values, additional files).
   #parser.add_argument( 'extra_arguments', nargs = modules.argparse.REMAINDER, help = 'extra files and/or start values', metavar = 'additional arguments' )
   parser.add_argument( 'extra_arguments', nargs = '*', default = None, help = 'Extra files and/or start values', metavar = 'additional arguments' )

   # Add help for additional files.
   parser.add_argument_group( 'additional files', 'Additional files (e.g., CSV load profiles or extra output definition files) can be specified as additional arguments. These files will be automatically copied to the resources directory of the FMU.' )

   # Add help for start values.
   parser.add_argument_group( 'start values', 'Start values for variables may be defined. For instance, to set variable with name \"x.y.z\" to value 12.34, specifiy \"x.y.z=12.34\" as additional argument.' )

   return parser.parse_args()


# Parse additional command line inputs (start values, additional files).
def parseAdditionalInputs( extra_arguments, verbose, modules ):
   # List of optional files (e.g., weather file)
   optional_files = []

   # Dictionary of start values.
   start_values = {}

   # Retrieve additional files from command line arguments.
   if extra_arguments != None:
      for item in extra_arguments:
         if '=' in item:
            start_value_pair = item.split( '=' )
            varname = start_value_pair[0].strip(' "\n\t')
            value = start_value_pair[1].strip(' "\n\t')
            if ( True == verbose ): modules.log( '[DEBUG] Found start value: ', varname, '=', value )
            start_values[varname] = value;
         elif ( True == modules.os.path.isfile( item ) ): # Check if this is an additional input file.
            optional_files.append( item )
            if ( True == verbose ): modules.log( '[DEBUG] Found additional file: ', item )
         else:
            modules.log( '\n[ERROR] Invalid input argument: ', item )
            modules.sys.exit(7)

   return ( optional_files, start_values )


# Case-sensitive check for file names.
def isFileCaseSensitive( path, modules ):
   if not modules.os.path.isfile( path ): return False # exit early
   directory, filename = modules.os.path.split( path )
   if not directory:
      return filename in modules.os.listdir()
   return filename in modules.os.listdir( directory )


# Retrieve labels from file. The file is expected to have
# one entry per line, comment lines start with a semicolon (;).
def retrieveLabelsFromFile( file_name, labels, modules ):
   input_file = open( file_name, 'r' ) # Open the file.
   while True:
      line = input_file.readline() # Read next line.
      if not line: break # End of file.

      line = line.strip(' "\'\n\t') # Strip all leading and trailing whitespaces etc.

      semicolon_position = line.find( ';' ) # Check for comments.
      if ( 0 == semicolon_position ):
         continue # Comment line.
      elif ( -1 != semicolon_position ):
         line = line[0:semicolon_position].strip(' "\'\n\t') # Remove comment from line

      if 0 != len( line ):
         if ( variableNameIsValid( line ) ):
            labels.append( line ) # Append line to list of labels.
         else:
            modules.log( '\n[ERROR]', line, 'is not a valid variable name' )
            modules.sys.exit(8)


# Check if FMI variable name is of form "<class-name>.<object-name>.<parameter-name>".
# Also check if the parameter name (which may contains several ':') is valid.
def variableNameIsValid( var_name ):
   # Split the variable name using the '.' as seperator.
   labels = var_name.split( '.' )
   # Check if the variable consists of two (RMS input events) or three labels.
   if ( 3 != len( labels ) ): return False
   # Check if there is no empty label.
   if ( 0 == min( map( len, labels ) ) ): return False
   # The last label (parameter name) may contain ':' as separators.
   sublabels = labels[len(labels)-1].split( ':' )
   # Check if the sublabels of the parameter name are valid.
   if ( 0 == min( map( len, sublabels ) ) ): return False
   # All checks successful, return True.
   return True


# Check if string represents a floating point number.
def is_float( str ):
	"""Check if string describes a float variable."""
	try: float( str )
	except ValueError: return False
	return True