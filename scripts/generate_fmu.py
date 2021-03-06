# -----------------------------------------------------------------------
# Copyright (c) 2020, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file POWERFACTORY_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------------

#
# Collection of helper functions for creating FMU CS according to FMI 2.0 for DIgSILENT PowerFactory.
#

### Import helper functions for specific FMI versions.
from .fmi1 import *
from .fmi2 import *


def generatePowerFactoryFMU(
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
   modules ):
   """Generate an FMU for PowerFactory.

   Keyword arguments:
   fmi_version -- FMI version (string)
   fmi_model_identifier -- FMI model identfier for FMU (string)
   pfd_file_name -- name of PFD file (string)
   pf_install_dir -- PowerFactory installation directory (string)
   triggers -- definition of triggers for simulation time advance (list of strings)
   dpl_script -- definition of DPL script for simulation time advance (list of strings)
   rms_sim -- RMS simulation setup (list of strings)
   fmi_input_vars -- definition of input variable names (list of strings)
   fmi_output_vars -- definition of output variable names (list of strings)
   start_values -- definition of start values (map of strings to strings)
   optional_files -- definition of additional files (list of strings)
   pf_fmu_root_dir -- path to root dir of PF FMU Export Utility (string)
   litter -- do not clean-up intermediate files (bool)
   verbose -- turn verbosity on/off (bool)
   modules -- named tuple containing all imported modules
   """

   # Create FMU model description.
   model_description_name = createModelDescription( fmi_version, fmi_model_identifier, pfd_file_name,
      pf_install_dir, triggers, dpl_script, rms_sim,fmi_input_vars, fmi_output_vars, start_values, optional_files, verbose, modules )

   # Create FMU shared library.
   fmu_shared_library_name = createSharedLibrary( fmi_model_identifier, pf_fmu_root_dir, pf_install_dir, fmi_version, verbose, modules )

   # Check if working directory for FMU creation already exists.
   if ( True == modules.os.path.isdir( fmi_model_identifier ) ):
      modules.shutil.rmtree( fmi_model_identifier, False )

   # Working directory path for the FMU DLL.
   binaries_dir = modules.os.path.join( fmi_model_identifier, 'binaries', 'win64' )

   # Create working directory (incl. sub-directories) for FMU creation.
   modules.os.makedirs( binaries_dir )

   # Resources directory path.
   resources_dir = modules.os.path.join( fmi_model_identifier, 'resources' )

   # Create resources directory for FMU creation.
   modules.os.makedirs( resources_dir )

   # Copy all files to working directory.
   modules.shutil.copy( model_description_name, fmi_model_identifier ) # XML model description.
   modules.shutil.copy( pfd_file_name, resources_dir ) # PowerFactory PFD file.
   for file_name in optional_files: # Additional files.
      modules.shutil.copy( file_name, resources_dir )
   modules.shutil.copy( fmu_shared_library_name, binaries_dir ) # FMU DLL.

   # Create ZIP archive.
   if ( True == modules.os.path.isfile( fmi_model_identifier + '.zip' ) ):
      modules.os.remove( fmi_model_identifier + '.zip' )
   modules.shutil.make_archive( fmi_model_identifier, 'zip', fmi_model_identifier )

   # Finally, create the FMU!!!
   fmu_file_name = fmi_model_identifier + '.fmu'
   if ( True == modules.os.path.isfile( fmu_file_name ) ):
      modules.os.remove( fmu_file_name )
   modules.os.rename( fmi_model_identifier + '.zip', fmu_file_name )

   # Clean up.
   if ( False == litter ):
      for fn in [ model_description_name, 'build.log', 'fmiFunctions.obj' ]:
         modules.os.remove( fn ) if modules.os.path.isfile( fn ) else None
      modules.shutil.rmtree( fmi_model_identifier, False )
      for file_name in modules.glob.glob( fmi_model_identifier + '.*' ):
         if not ( ( ".fmu" in file_name ) or ( ".dck" in file_name ) or ( ".tpf" in file_name ) ): modules.os.remove( file_name )

   # Return name of created FMU.
   return fmu_file_name


# Create model description.
def createModelDescription(
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
   verbose,
   modules ):

   # Retrieve templates for different parts of XML model description according to FMI version.
   ( model_description_header, scalar_variable_node, model_description_footer ) = getModelDescriptionTemplates( fmi_version, verbose, modules )

   # FMI model identifier.
   model_description_header = model_description_header.replace( '__MODEL_IDENTIFIER__', fmi_model_identifier )

   # Model name.
   fmi_model_name = modules.os.path.basename( pfd_file_name ).split( '.' )[0] # Deck file name with extension.
   model_description_header = model_description_header.replace( '__MODEL_NAME__', fmi_model_name )

   # Creation date and time.
   model_description_header = model_description_header.replace( '__DATE_AND_TIME__', modules.time.strftime( "%Y-%m-%dT%H:%M:%S" ) )

   # Author name.
   model_description_header = model_description_header.replace( '__USER__', modules.getpass.getuser() )

   # GUID.
   model_description_header = model_description_header.replace( '__GUID__', str( modules.uuid.uuid1() ) )

   # Define a string to collect all scalar variable definitions.
   model_description_scalars = ''

   # Add scalar input variables description. Value references for inputs start with 1.
   input_val_ref = 1
   for var in fmi_input_vars:
      scalar_variable_description = scalar_variable_node
      scalar_variable_description = scalar_variable_description.replace( '__VAR_NAME__', var )
      scalar_variable_description = scalar_variable_description.replace( '__CAUSALITY__', "input" )
      scalar_variable_description = scalar_variable_description.replace( '__VAL_REF__', str( input_val_ref ) )
      scalar_variable_description = scalar_variable_description.replace( '__INITIAL__', '' )
      if var in start_values:
         start_value_description = ' start=\"' + start_values[var] + '\"'
         scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', start_value_description )
         if ( True == verbose ): modules.log( '[DEBUG] Added start value to model description: ', var, '=', start_values[var] )
      else:
         scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', '' )
      input_val_ref += 1
      # Write scalar variable description to file.
      model_description_scalars += scalar_variable_description;

   # Add scalar input variables description. Value references for outputs start with 1001 (except there are already input value references with corresponding values).
   output_val_ref = 1001 if ( input_val_ref < 1001 ) else input_val_ref
   for var in fmi_output_vars:
      scalar_variable_description = scalar_variable_node
      scalar_variable_description = scalar_variable_description.replace( '__VAR_NAME__', var )
      scalar_variable_description = scalar_variable_description.replace( '__CAUSALITY__', "output" )
      scalar_variable_description = scalar_variable_description.replace( '__VAL_REF__', str( output_val_ref ) )
      if var in start_values:
         start_value_description = ' start=\"' + start_values[var] + '\"'
         scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', start_value_description )
         scalar_variable_description = scalar_variable_description.replace( '__INITIAL__', 'initial="exact"' )
         if ( True == verbose ): modules.log( '[DEBUG] Added start value to model description: ', var, '=', start_values[var] )
      else:
         scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', '' )
         scalar_variable_description = scalar_variable_description.replace( '__INITIAL__', '' )
      output_val_ref += 1
      # Write scalar variable description to file.
      model_description_scalars += scalar_variable_description;

   # Time advance mechanism.
   ( model_description_header, model_description_footer ) = \
      addTimeAdvanceMechanismToModelDescription( triggers, dpl_script, rms_sim, model_description_header, model_description_footer, fmi_version, verbose, modules )

   # Input PFD file.
   ( model_description_header, model_description_footer ) = \
      addPFDFileToModelDescription( pfd_file_name, model_description_header, model_description_footer, fmi_version, verbose, modules )

   # Optional files.
   ( model_description_header, model_description_footer ) = \
      addOptionalFilesToModelDescription( model_description_header, model_description_footer, optional_files, fmi_version, verbose, modules)

   # Create new XML model description file.
   model_description_name = 'modelDescription.xml'
   model_description = open( model_description_name, 'w' )
   model_description.write( model_description_header );
   model_description.write( model_description_scalars );
   model_description.write( model_description_footer );
   model_description.close()

   return model_description_name


# Get templates for the XML model description depending on the FMI version.
def getModelDescriptionTemplates( fmi_version, verbose, modules ):
   if ( '1' == fmi_version ): # FMI 1.0
      return fmi1GetModelDescriptionTemplates( verbose, modules )
   elif ( '2' == fmi_version ): # FMI 2.0
      return fmi2GetModelDescriptionTemplates( verbose, modules )


# Add PFD file as entry point to XML model description.
def addPFDFileToModelDescription( pfd_file_name, header, footer, fmi_version, verbose, modules ):
   if ( '1' == fmi_version ): # FMI 1.0
      return fmi1AddPFDFileToModelDescription( pfd_file_name, header, footer, verbose, modules )
   elif ( '2' == fmi_version ): # FMI 2.0
      return fmi2AddPFDFileToModelDescription( pfd_file_name, header, footer, verbose, modules )


# Add PFD file as entry point to XML model description.
def addTimeAdvanceMechanismToModelDescription( triggers, dpl_script, rms_sim, header, footer, fmi_version, verbose, modules ):
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
            raise Exception( 14 )
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
         raise Exception( 15 )
      time_advance_description += '<DPLScript name="' + labels[0] + '" scale="' + labels[1] + '" offset="' + labels[2] + '"/>'

   # RMS simulation setup.
   if ( 0 != len( rms_sim ) ):
      # Defintion of more than one RMS simulation setup not supported (see above)!
      stepsize = rms_sim[0]
      if ( False == is_float( stepsize ) ):
         _print( '\n[ERROR] A RMS simulation setup needs to define the integrator step size (in seconds).' )
         raise Exception( 16 )
      time_advance_description += '<RMSSimulation stepsize="' + stepsize + '"/>'

   if ( '1' == fmi_version ): # FMI 1.0
      return fmi1AddTimeAdvanceMechanismToModelDescription( time_advance_description, header, footer, fmi_version, verbose, modules )
   elif ( '2' == fmi_version ): # FMI 2.0
      return fmi2AddTimeAdvanceMechanismToModelDescription( time_advance_description, header, footer, fmi_version, verbose, modules )


# Add optional files to XML model description.
def addOptionalFilesToModelDescription( header, footer, optional_files, fmi_version, verbose, modules ):
   if ( '1' == fmi_version ):
      return fmi1AddOptionalFilesToModelDescription( optional_files, header, footer, verbose, modules )
   if ( '2' == fmi_version ):
      return fmi2AddOptionalFilesToModelDescription( optional_files, header, footer, verbose, modules )


# Create DLL for FMU.
def createSharedLibrary( fmi_model_identifier, pf_fmu_root_dir, pf_install_dir, fmi_version, verbose, modules ):
   if ( '1' == fmi_version ):
      return fmi1CreateSharedLibrary( fmi_model_identifier, pf_fmu_root_dir, pf_install_dir, verbose, modules )
   if ( '2' == fmi_version ):
      return fmi2CreateSharedLibrary( fmi_model_identifier, pf_fmu_root_dir, pf_install_dir, verbose, modules )
