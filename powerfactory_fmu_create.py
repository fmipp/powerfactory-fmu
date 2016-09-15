# -----------------------------------------------------------------------
# Copyright (c) 2015, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file POWERFACTORY_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------------

### Python 2
# import sys, os, shutil, time, getpass, uuid, urlparse, urllib, getopt, pickle, subprocess, glob
# def _print( *arg ): print ' '.join( map( str, arg ) )

### Python 3
import sys, os, shutil, time, getpass, uuid, urllib.parse, urllib, getopt, pickle, subprocess, glob
def _print( *arg ): print( ' '.join( map( str, arg ) ) )


# Helper function.
def is_float( str ):
	"""Check if string describes a float variable."""
	try: float( str )
	except ValueError: return False
	return True


def generatePowerFactoryFMU(
		fmi_model_identifier,
		pfd_file_name,
		pf_install_dir,
		triggers,
		dpl_script,
		fmi_input_vars,
		fmi_output_vars,
		start_values,
		optional_files,
		pf_fmu_root_dir ):
	"""Generate an FMU for PowerFactory.

    Keyword arguments:
	fmi_model_identifier -- FMI model identfier for FMU (string)
	pfd_file_name -- name of PFD file (string)
	pf_install_dir -- PowerFactory installation directory (string)
	triggers -- definition of triggers for simulation time advance(list of strings)
	dpl_script -- definition of DPL script for simulation time advance(list of strings)
	fmi_input_vars -- definition of input variable names (list of strings)
	fmi_output_vars -- definition of output variable names (list of strings)
	start_values -- definition of start values (map of strings to strings)
	optional_files -- definition of additional files (list of strings)
        pf_fmu_root_dir -- path to root dir of PF FMU Export Utility (string)
	"""
	
	# Template string for XML model description header.
	model_description_header = '<?xml version="1.0" encoding="UTF-8"?>\n<fmiModelDescription fmiVersion="1.0" modelName="__MODEL_NAME__" modelIdentifier="__MODEL_IDENTIFIER__" description="PowerFactory FMI CS export" generationTool="FMI++ PowerFactory Export Utility" generationDateAndTime="__DATE_AND_TIME__" variableNamingConvention="flat" numberOfContinuousStates="0" numberOfEventIndicators="0" author="__USER__" guid="{__GUID__}">\n\t<ModelVariables>\n'

	# Template string for XML model description of scalar variables.
	scalar_variable_node = '\t\t<ScalarVariable name="__VAR_NAME__" valueReference="__VAL_REF__" variability="continuous" causality="__CAUSALITY__">\n\t\t\t<Real__START_VALUE__/>\n\t\t</ScalarVariable>\n'

	# Template string for XML model description footer.
	model_description_footer = '\t</ModelVariables>\n\t<Implementation>\n\t\t<CoSimulation_Tool>\n\t\t\t<Capabilities canHandleVariableCommunicationStepSize="true" canHandleEvents="true" canRejectSteps="false" canInterpolateInputs="false" maxOutputDerivativeOrder="0" canRunAsynchronuously="false" canSignalEvents="false" canBeInstantiatedOnlyOncePerProcess="false" canNotUseMemoryManagementFunctions="true"/>\n\t\t\t<Model entryPoint="fmu://__PFD_FILE_NAME__" manualStart="false" type="application/x-powerfactory">__ADDITIONAL_FILES__</Model>\n\t\t</CoSimulation_Tool>\n\t</Implementation>\n\t<VendorAnnotations>\n\t\t<powerfactory>\n\t\t\t__TIME_ADVANCE_MECHANISM__\n\t\t</powerfactory>\n\t</VendorAnnotations>\n</fmiModelDescription>'

	# Create new XML model description file.
	model_description_name = 'modelDescription.xml'
	model_description = open( model_description_name, 'w' )

	#
	# Replace template arguments in header.
	#

	# FMI model identifier.
	model_description_header = model_description_header.replace( '__MODEL_IDENTIFIER__', fmi_model_identifier )

	# Model name.
	fmi_model_name = os.path.basename( pfd_file_name ).split( '.' )[0] # Deck file name with extension.
	model_description_header = model_description_header.replace( '__MODEL_NAME__', fmi_model_name )

	# Creation date and time.
	model_description_header = model_description_header.replace( '__DATE_AND_TIME__', time.strftime( "%Y-%m-%dT%H:%M:%S" ) )

	# Author name.
	model_description_header = model_description_header.replace( '__USER__', getpass.getuser() )

	# GUID.
	model_description_header = model_description_header.replace( '__GUID__', str( uuid.uuid1() ) )

	# Write header to file.
	model_description.write( model_description_header );

	#
	# Add scalar variable description.
	#
	input_val_ref = 1 # Value references for inputs start with 1.
	for var in fmi_input_vars:
		scalar_variable_description = scalar_variable_node
		scalar_variable_description = scalar_variable_description.replace( '__VAR_NAME__', var )
		scalar_variable_description = scalar_variable_description.replace( '__CAUSALITY__', "input" )
		scalar_variable_description = scalar_variable_description.replace( '__VAL_REF__', str( input_val_ref ) )
		if var in start_values:
			start_value_description = ' start=\"' + start_values[var] + '\"'
			scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', start_value_description )
			if ( True == verbose ): _print( '[DEBUG] Added start value to model description: ', var, '=', start_values[var] )
		else:
			scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', '' )
		input_val_ref += 1
		# Write scalar variable description to file.
		model_description.write( scalar_variable_description );

	# Value references for outputs start with 1001 (except there are already input value references with corresponding values).
	output_val_ref = 1001 if ( input_val_ref < 1001 ) else input_val_ref
	for var in fmi_output_vars:
		scalar_variable_description = scalar_variable_node
		scalar_variable_description = scalar_variable_description.replace( '__VAR_NAME__', var )
		scalar_variable_description = scalar_variable_description.replace( '__CAUSALITY__', "output" )
		scalar_variable_description = scalar_variable_description.replace( '__VAL_REF__', str( output_val_ref ) )
		if var in start_values:
			start_value_description = ' start=\"' + start_values[var] + '\"'
			scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', start_value_description )
			if ( True == verbose ): _print( '[DEBUG] Added start value to model description: ', var, '=', start_values[var] )
		else:
			scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', '' )
		output_val_ref += 1
		# Write scalar variable description to file.
		model_description.write( scalar_variable_description );

	#
	# Replace template arguments in footer.
	#

	# Input deck file.
	model_description_footer = model_description_footer.replace( '__PFD_FILE_NAME__', os.path.basename( pfd_file_name ) )

	# Additional input files.
	if ( 0 == len( optional_files ) ):
		model_description_footer = model_description_footer.replace( '__ADDITIONAL_FILES__', '' )
	else:
		additional_files_description = ''
		for file_name in optional_files:
			additional_files_description += '\n\t\t\t\t<File file=\"fmu://' + os.path.basename( file_name ) + '\"/>'
			if ( True == verbose ): _print( '[DEBUG] Added additional file to model description: ', os.path.basename( file_name ) )
		additional_files_description += '\n\t\t\t'
		model_description_footer = model_description_footer.replace( '__ADDITIONAL_FILES__', additional_files_description )

	# String for description of time advance mechanism.
	time_advance_description = ''

	# Time advance mechanism via triggers.
	if ( 0 != len( triggers ) ):
		for trigger in triggers:
			labels = trigger.split( ':' )
			min_label_size = min( map( len, labels ) )
			if ( ( 2 != len( labels ) ) or
			     ( 0 == min_label_size ) or
			     ( False == is_float( labels[1] ) ) ):
				_print( '\n[ERROR] A trigger for simulation time advance needs to be defined in the form \"<name>:<scale>\".' )
				raise Exception( 13 )
			time_advance_description += '<Trigger name="' + labels[0] + '" scale="' + labels[1] + '"/>'

	# Time advance mechanism via DPL script.
	if ( 0 != len( dpl_script ) ):
		# Defintion of more than one DPL script not supported (see above)!
		labels = dpl_script[0].split( ':' )
		min_label_size = min( map( len, labels ) )
		if ( ( 3 != len( labels ) ) or
			 ( 0 == min_label_size ) or
			 ( False == is_float( labels[1] ) ) or
			 ( False == is_float( labels[2] ) ) ):
			_print( '\n[ERROR] A DPL script for simulation time advance needs to be defined in the form \"<name>:<scale>:<offset>\".' )
			raise Exception( 14 )
		time_advance_description += '<DPLScript name="' + labels[0] + '" scale="' + labels[1] + '" offset="' + labels[2] + '"/>'

	# Add description of time advance mechanism.
	model_description_footer = model_description_footer.replace( '__TIME_ADVANCE_MECHANISM__', time_advance_description )

	# Write footer to file.
	model_description.write( model_description_footer );

	# Close file.
	model_description.close()

	# Check if model description is XML compliant.
	#import xml.etree.ElementTree as ET
	#tree = ET.parse( 'model_description.xml' )

	# FMU shared library name.
	fmu_shared_library_name = fmi_model_identifier + '.dll'

	# Check if batch file for build process exists.
	build_process_batch_file = pf_fmu_root_dir + '\\build.bat'
	if ( False == os.path.isfile( build_process_batch_file ) ):
		_print( '\n[ERROR] Could not find file', build_process_batch_file )
		raise Exception( 15 )

	# Compile FMU shared library.
	for file_name in glob.glob( fmi_model_identifier + '.*' ):
		if not ".pfd" in file_name: os.remove( file_name ) # Do not accidentaly remove the deck file!
	if ( True == os.path.isfile( 'fmiFunctions.obj' ) ): os.remove( 'fmiFunctions.obj' )
	build_process = subprocess.Popen( [build_process_batch_file, fmi_model_identifier, pf_install_dir ] )
	stdout, stderr = build_process.communicate()

	# Check if batch script has executed successfully.
	if ( False == os.path.isfile( fmu_shared_library_name ) ):
		_print( '\n[ERROR] Not able to create shared library:', fmu_shared_library_name )
		raise Exception( 16 )

	# Check if working directory for FMU creation already exists.
	if ( True == os.path.isdir( fmi_model_identifier ) ):
		shutil.rmtree( fmi_model_identifier, False )

	# Working directory path for the FMU DLL.
	binaries_dir = os.path.join( fmi_model_identifier, 'binaries', 'win32' )

	# Create working directory (incl. sub-directories) for FMU creation.
	os.makedirs( binaries_dir )

	# Copy all files to working directory.
	shutil.copy( model_description_name, fmi_model_identifier ) # XML model description.
	shutil.copy( pfd_file_name, fmi_model_identifier ) # PowerFactory deck file.
	for file_name in optional_files: # Additional files.
		shutil.copy( file_name, fmi_model_identifier )
	shutil.copy( fmu_shared_library_name, binaries_dir ) # FMU DLL.

	# Create ZIP archive.
	if ( True == os.path.isfile( fmi_model_identifier + '.zip' ) ):
		os.remove( fmi_model_identifier + '.zip' )
	shutil.make_archive( fmi_model_identifier, 'zip', fmi_model_identifier )

	# Finally, create the FMU!!!
	if ( True == os.path.isfile( fmi_model_identifier + '.fmu' ) ):
		os.remove( fmi_model_identifier + '.fmu' )
	os.rename( fmi_model_identifier + '.zip', fmi_model_identifier + '.fmu' )

	# Clean up.
	if ( False == litter ):
		os.remove( model_description_name )
		os.remove( 'build.log' )
		os.remove( 'fmiFunctions.obj' )
		shutil.rmtree( fmi_model_identifier, False )
		for file_name in glob.glob( fmi_model_identifier + '.*' ):
			if not ( ( ".fmu" in file_name ) or ( ".pfd" in file_name ) ): os.remove( file_name )


# Helper function.
def usage():
	"""Print the usage of this script when used as main program."""
	_print( '\nABOUT:' )
	_print( 'This script generates FMUs for Co-Simulation (tool coupling) from PowerFactory' )
	_print( '\nUSAGE:' )
	_print( 'python powerfactory_fmu_create.py [-h] [-v] [-d pf_install_dir] -m model_id -p pfd_file [-i input_var_file] [-o output_var_file] [-t name:scale] [-s name:scale:offset] [additional_file_1 ... additional_file_N] [var1=start_val1 ... varN=start_valN]' )
	_print( '\nREQUIRED ARGUMENTS:' )
	_print( '-m, --model-id=\t\tspecify FMU model identifier' )
	_print( '-p, --pfd-file=\tpath to PowerFactory PFD file' )
	_print( '\nOPTIONAL ARGUMENTS:' )
	_print( '-i, --input-var-file=\tspecify file containing list of input variable names' )
	_print( '-o, --output-var-file=\tspecify file containing list of output variable names' )
	_print( '-t, --trigger=\t\tspecify a trigger for advancing simulation time' )
	_print( '-s, --dpl-script=\tspecify a DPL-script for advancing simulation time' )
	_print( '-h, --help\t\tdisplay this information' )
	_print( '-v, --verbose\t\tturn on log messages' )
	_print( '-l, --litter\t\tdo not clean-up intermediate files' )
	_print( '-d, --pf-install-dir=\tpath to PowerFactory installation directory' )
	_print( '\nFiles containing lists of input and output variable name are expected to be in clear text, listing exactly one valid variable name per line. Variable names are supposed to be of the  form "<class-name>.<object-name>.<parameter-name>".' )
	_print( '\nTriggers for simulation time advance need to be defined in the form \"<name>:<scale>\". The name has to be given according to the trigger\'s object name in the PFD file. Times given to the FMU are interpreted as seconds, therefore the scale can be adjusted to match the trigger\'s internal unit of time (e.g., 60 for minutes or 3600 for hours). Multiple triggers may be defined. Alternatively, a single DPL script may be specified to advance simulation time in the form \"<name>:<scale>:<offset>\".' )
	_print( '\nAdditional files may be specified (e.g., CSV load profiles or extra output definition files) that will be automatically copied to the FMU.' )
	_print( '\nStart values for variables may be defined. For instance, to set variable with name \"var1\" to value 12.34, specifiy \"var1=12.34\" in the command line as optional argument.' )


# Helper function.
def variableNameIsValid( var_name ):
	"""Check if FMI variable name is of form "<class-name>.<object-name>.<parameter-name>".
	Also check if the parameter name (which may contains several ':') is valid.
	"""
	# Split the variable name using the '.' as seperator.
	labels = var_name.split( '.' )
	# Check if the variable consists of three labels.
	if ( 3 != len( labels ) ): return False
	# Check if there is no empty label.
	if ( 0 == min( map( len, labels ) ) ): return False
	# The parameter name may contain ':' as separators.
	sublabels = labels[2].split( ':' )
	# Check if the sublabels of the parameter name are valid.
	if ( 0 == min( map( len, sublabels ) ) ): return False
	# All checks successful, return True.
	return True


# Helper function. Retrieve labels from file. The file is expected to
# have one entry per line, comment lines start with a semicolon (;).
def retrieveLabelsFromFile( file_name, labels ):
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
				_print( '\n[ERROR]', line, 'is not a valid variable name' )
				sys.exit(8)


# Main function.
if __name__ == "__main__":

	# FMI model identifier.
	fmi_model_identifier = None

	# PowerFactory PFD file.
	pfd_file_name = None

	# Set PowerFactory install dir.
	pf_install_dir = None

	# File containing FMI input variable names.
	input_var_file_name = None

	# File containing FMI output variable names.
	output_var_file_name = None

	# Relative or absolute path to PF FMU Export Utility.
	pf_fmu_root_dir = os.path.dirname( sys.argv[0] ) if len( os.path.dirname( sys.argv[0] ) ) else '.'

	# List of optional files (e.g., weather file)
	optional_files = []

	# Dictionary of start values.
	start_values = {}

	# Verbose flag.
	verbose = False

	# Litter flag.
	litter = False

	# List of triggers (for simulation time advance).
	triggers = []

	# DPL script (for simulation time advance).
	dpl_script = []

	# Parse command line arguments.
	try:
		options_definition_short = "vhlm:p:i:o:d:t:s:"
		options_definition_long = [ "verbose", "help", "litter", "model-id=", 'pfd-file=', 'input-var-file=', 'output-var-file=', 'pf-install-dir=', 'trigger=', 'dpl-script' ]
		options, extra = getopt.getopt( sys.argv[1:], options_definition_short, options_definition_long )
	except getopt.GetoptError as err:
		_print( str( err ) )
		usage()
		sys.exit(1)

	# Parse options.
	for opt, arg in options:
		if opt in ( '-h', '--help' ):
			usage()
			sys.exit()
		elif opt in ( '-m', '--model-id' ):
			fmi_model_identifier = arg
		elif opt in ( '-p', '--pfd-file' ):
			pfd_file_name = arg
		elif opt in ( '-i', '--input-var-file' ):
			input_var_file_name = arg
		elif opt in ( '-o', '--output-var-file' ):
			output_var_file_name = arg
		elif opt in ( '-d', '--pf-install-dir' ):
			pf_install_dir = arg
		elif opt in ( '-v', '--verbose' ):
			verbose = True
		elif opt in ( '-l', '--litter' ):
			litter = True
		elif opt in ( '-t', '--trigger' ):
			triggers.append( arg )
		elif opt in ( '-s', '--scripts' ):
			dpl_script.append( arg )

	# Check if FMI model identifier has been specified.
	if ( None == fmi_model_identifier ):
		_print( '\n[ERROR] No FMU model identifier specified!' )
		usage()
		sys.exit(2)

	# Check if PowerFactory deck file has been specified.
	if ( None == pfd_file_name ):
		_print( '\n[ERROR] No PowerFactory PFD file specified!' )
		usage()
		sys.exit(3)
	elif ( False == os.path.isfile( pfd_file_name ) ): # Check if specified PFD file is valid.
		_print( '\n[ERROR] Invalid PowerFactory PFD file:', pfd_file_name )
		usage()
		sys.exit(4)
        
	# No PowerFactory install directory provided -> read from file (created by script 'powerfactory_fmu_install.py').
	if ( None == pf_install_dir ):
		pkl_file_name = pf_fmu_root_dir + '\\powerfactory_fmu_install.pkl'
		if ( True == os.path.isfile( pkl_file_name ) ):
			pkl_file = open( pkl_file_name, 'rb' )
			pf_install_dir = pickle.load( pkl_file )
			pkl_file.close()
		else:
			_print( '\n[ERROR] Please re-run script \'powerfactory_fmu_install.py\' or provide PowerFactory install directory via command line option -d (--pf-install-dir)!' )
			usage()
			sys.exit(5)

	# Check if specified PowerFactory install directory exists.
	if ( False == os.path.isdir( pf_install_dir ) ):
		_print( '\n[WARNING] Invalid PowerFactory install directory:', pf_install_dir )
		# usage()
		# sys.exit(6)

	# Retrieve additional files from command line arguments.
	for item in extra:
		if "=" in item:
			start_value_pair = item.split( '=' )
			varname = start_value_pair[0].strip(' "\n\t')
			value = start_value_pair[1].strip(' "\n\t')
			if ( True == verbose ): _print( '[DEBUG] Found start value:', varname, '=', value )
			start_values[varname] = value;
		elif ( True == os.path.isfile( item ) ): # Check if this is an additional input file.
			optional_files.append( item )
			if ( True == verbose ): _print( '[DEBUG] Found additional file:', item )
		else:
			_print( '\n[ERROR] Invalid input argument:', item )
			usage()
			sys.exit(7)

	if ( True == verbose ):
		_print( '[DEBUG] FMI model identifier:', fmi_model_identifier )
		_print( '[DEBUG] PowerFactory PFD file:', pfd_file_name )
		_print( '[DEBUG] PowerFactory install directory:', pf_install_dir )
		_print( '[DEBUG] Aditional files:' )
		for file_name in optional_files:
			_print( '\t', file_name )

	# Issue a warning in case no files contining input/outout variable name list have been specified.
	if ( ( None == input_var_file_name ) and ( None == output_var_file_name ) ):
		_print( '[WARNING] Neither input nor output variable names specified!' )

	# Lists containing the FMI input and output variable names.
	fmi_input_vars = []
	fmi_output_vars = []

	# Parse file to retrieve FMI input variable names.
	if ( None != input_var_file_name ):
		retrieveLabelsFromFile( input_var_file_name, fmi_input_vars );

		if ( True == verbose ):
			_print( '[DEBUG] FMI input parameters:' )
			for var in fmi_input_vars:
				_print( '\t', var )

	# Parse file to retrieve FMI output variable names.
	if ( None != output_var_file_name ):
		retrieveLabelsFromFile( output_var_file_name, fmi_output_vars );

		if ( True == verbose ):
			_print( '[DEBUG] FMI output parameters:' )
			for var in fmi_output_vars:
				_print( '\t', var )

	# Check options for time advance mechanism.
	if ( ( 0 == len( dpl_script ) ) and ( 0 == len( triggers ) ) ):
		_print( '\n[ERROR] no mechanism for time advance specified' )
		sys.exit(10)
	elif ( ( 0 != len( dpl_script ) ) and ( 0 != len( triggers ) ) ):
		_print( '\n[ERROR] Mixing of mechanisms for time advance (triggers and DPL scripts) is not supported!' )
		sys.exit(11)
	elif ( 1 < len( dpl_script ) ):
		_print( '\n[ERROR] Defintion of more than one DPL script for simulation time advance is not supported!' )
		sys.exit(12)
	
	# Generate FMU.
	try:
		generatePowerFactoryFMU(
			fmi_model_identifier,
			pfd_file_name,
			pf_install_dir,
			triggers,
			dpl_script,
			fmi_input_vars,
			fmi_output_vars,
			start_values,
			optional_files,
			pf_fmu_root_dir )
	except Exception as e:
		sys.exit( e.args[0] )
	
	if ( True == verbose ): _print( "[DEBUG] FMU created successfully!" )
