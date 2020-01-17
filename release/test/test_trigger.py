#import pytest
import os
import fmipp


def sim_PFTestTriggers( zip_command, expected_results, fmi_version ):
   if 1 == fmi_version:
      fmu_wrapper_class = fmipp.FMUCoSimulationV1
      model_name = 'PFTestTriggersV1'
   elif 2 == fmi_version:
      fmu_wrapper_class = fmipp.FMUCoSimulationV2
      model_name = 'PFTestTriggersV2'
   else:
      raise RuntimeError( 'unknown FMI version: {}'.format( fmi_version ) )

   work_dir = os.path.join( os.path.dirname( os.path.abspath( __file__ ) ), '..', '..', 'examples', 'triggers' ) # define working directory
   path_to_fmu = os.path.join( work_dir, model_name + '.fmu' ) # path to FMU
   uri_to_extracted_fmu = fmipp.extractFMU(
      path_to_fmu, work_dir, command = zip_command
      )

   logging_on = True
   time_diff_resolution = 1e-9
   fmu = fmu_wrapper_class(
      uri_to_extracted_fmu, model_name,
      logging_on, time_diff_resolution
      )

   instance_name = "test1"
   visible = False
   interactive = False
   status = fmu.instantiate( instance_name, 0., visible, interactive )
   assert status == fmipp.fmiOK

   start_time = 0.
   stop_time = 300.
   stop_time_defined = True
   status = fmu.initialize( start_time, stop_time_defined, stop_time )
   assert status == fmipp.fmiOK

   time = 0.
   step_size = 60.
   new_step = True
   while ( time <= stop_time ):
      x = fmu.getRealValue( 'ElmTerm.Node.m:u' ) # retrieve output variable 'ElmTerm.Node.m:u '
      assert round( x, 5 ) == expected_results[ time ]

      status = fmu.doStep( time, step_size, new_step )
      time = time + step_size

   print('BEFORE TERMINATE')
   #fmu.terminate()
   print('AFTER TERMINATE')
   #del fmu
   print('AFTER DEL')


fix_zip_command = '"C:\\Program Files\\7-Zip\\7z.exe" -y -o{dir} x {fmu}'


fix_PFTestTriggers_expected_results = {
      0.: 1.03205,
      60.: 1.02631,
      120.: 1.02036,
      180.: 1.01422,
      240.: 1.00785,
      300.: 1.00125,
      }

# print( '#################### FMI1 ####################' )
# sim_PFTestTriggers( fix_zip_command, fix_PFTestTriggers_expected_results, 1 )

print( '#################### FMI2 ####################' )
sim_PFTestTriggers( fix_zip_command, fix_PFTestTriggers_expected_results, 2 )
