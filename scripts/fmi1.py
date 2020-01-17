# -----------------------------------------------------------------------
# Copyright (c) 2020, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file POWERFACTORY_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------------


#
# Collection of helper functions for creating FMU CS according to FMI 1.0
#

from .utils import *


# Get templates for the XML model description depending on the FMI version.
def fmi1GetModelDescriptionTemplates( verbose, modules ):
   # Template string for XML model description header.
   header = '<?xml version="1.0" encoding="UTF-8"?>\n<fmiModelDescription fmiVersion="1.0" modelName="__MODEL_NAME__" modelIdentifier="__MODEL_IDENTIFIER__" description="PowerFactory FMI CS export" generationTool="FMI++ PowerFactory Export Utility" generationDateAndTime="__DATE_AND_TIME__" variableNamingConvention="flat" numberOfContinuousStates="0" numberOfEventIndicators="0" author="__USER__" guid="{__GUID__}">\n\t<VendorAnnotations>\n\t\t<Tool name="powerfactory">\n\t\t\t__TIME_ADVANCE_MECHANISM__\n\t\t</Tool>\n\t</VendorAnnotations>\n\t<ModelVariables>\n'

   # Template string for XML model description of scalar variables.
   scalar_variable_node = '\t\t<ScalarVariable name="__VAR_NAME__" valueReference="__VAL_REF__" variability="continuous" causality="__CAUSALITY__">\n\t\t\t<Real__START_VALUE__/>\n\t\t</ScalarVariable>\n'

   # Template string for XML model description footer.
   footer = '\t</ModelVariables>\n\t<Implementation>\n\t\t<CoSimulation_Tool>\n\t\t\t<Capabilities canHandleVariableCommunicationStepSize="true" canHandleEvents="true" canRejectSteps="false" canInterpolateInputs="false" maxOutputDerivativeOrder="0" canRunAsynchronuously="false" canSignalEvents="false" canBeInstantiatedOnlyOncePerProcess="false" canNotUseMemoryManagementFunctions="true"/>\n\t\t\t<Model entryPoint="fmu://resources/__PFD_FILE_NAME__" manualStart="false" type="application/x-powerfactory">__ADDITIONAL_FILES__</Model>\n\t\t</CoSimulation_Tool>\n\t</Implementation>\n</fmiModelDescription>'

   return ( header, scalar_variable_node, footer )


# Add PFD file as entry point to XML model description.
def fmi1AddPFDFileToModelDescription( pfd_file_name, header, footer, vebose, modules ):
   footer = footer.replace( '__PFD_FILE_NAME__', modules.os.path.basename( pfd_file_name ) )
   return ( header, footer )


# Add optional files to XML model description.
def fmi1AddOptionalFilesToModelDescription( optional_files, header, footer, verbose, modules ):
   if ( 0 == len( optional_files ) ):
      footer = footer.replace( '__ADDITIONAL_FILES__', '' )
   else:
      additional_files_description = ''
      indent = '\n\t\t\t'

      for file_name in optional_files:
         additional_files_description += indent + '\t<File file=\"fmu://resources/' + modules.os.path.basename( file_name ) + '\"/>'
         if ( True == verbose ): modules.log( '[DEBUG] Added additional file to model description: ', modules.os.path.basename( file_name ) )
      additional_files_description += indent

      footer = footer.replace( '__ADDITIONAL_FILES__', additional_files_description )

   return ( header, footer )


# Create DLL for FMU.
def fmi1CreateSharedLibrary( fmi_model_identifier, pf_fmu_root_dir, pf_install_dir, verbose, modules ):
   # Define name of shared library.
   fmu_shared_library_name = fmi_model_identifier + '.dll'

   # Check if batch file for build process exists.
   build_process_batch_file = modules.os.path.join( pf_fmu_root_dir, 'scripts', 'fmi1_build.bat' )
   if ( False == modules.os.path.isfile( build_process_batch_file ) ):
      modules.log( '\n[ERROR] Could not find file: ', build_process_batch_file )
      raise Exception( 8 )
   # Remove possible leftovers from previous builds.
   for file_name in modules.glob.glob( fmi_model_identifier + '.*' ):
      if not ( ".pfd" in file_name ): modules.os.remove( file_name ) # Do not accidentaly remove the deck file!
   if ( True == modules.os.path.isfile( 'fmiFunctions.obj' ) ): modules.os.remove( 'fmiFunctions.obj' )
   # Compile FMU shared library.
   build_process = modules.subprocess.Popen( [build_process_batch_file, fmi_model_identifier, pf_install_dir ] )
   stdout, stderr = build_process.communicate()

   if ( False == modules.os.path.isfile( fmu_shared_library_name ) ):
      modules.log( '\n[ERROR] Not able to create shared library: ', fmu_shared_library_name )
      raise Exception( 17 )

   return fmu_shared_library_name


def fmi1AddTimeAdvanceMechanismToModelDescription( time_advance_description, header, footer, fmi_version, verbose, modules ):

   # Add description of time advance mechanism.
   header = header.replace( '__TIME_ADVANCE_MECHANISM__', time_advance_description )
   
   return ( header, footer )
