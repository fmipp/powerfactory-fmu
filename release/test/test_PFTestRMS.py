import pytest
import os
import fmipp


def sim_PFTestRMS( 
   zip_command, 
   evtParam_Controller_Pext1_input, 
   evtParam_Controller_Pext2_input, 
   expected_results,
   fmi_version ):
   if 1 == fmi_version:
      fmu_wrapper_class = fmipp.FMUCoSimulationV1
      model_name = 'PFTestRMSV1'
   elif 2 == fmi_version:
      fmu_wrapper_class = fmipp.FMUCoSimulationV2
      model_name = 'PFTestRMSV2'
   else:
      raise RuntimeError( 'unknown FMI version: {}'.format( fmi_version ) )

   work_dir = os.path.join( os.path.dirname( __file__ ), '..', '..', 'examples', 'rms' ) # define working directory
   path_to_fmu = os.path.join( work_dir, model_name + '.fmu' ) # path to FMU
   uri_to_extracted_fmu = fmipp.extractFMU(
      path_to_fmu, work_dir, command = zip_command
      )

   logging_on = False
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
   stop_time = 270.
   stop_time_defined = True
   status = fmu.initialize( start_time, stop_time_defined, stop_time )
   assert status == fmipp.fmiOK

   time = 0.
   step_size = 30.
   new_step = True
   while ( time <= stop_time ):
      if ( time % 60 ) == 0:
         fmu.setRealValue( 'EvtParam.Controller.Pext1', evtParam_Controller_Pext1_input[time] )
         fmu.setRealValue( 'EvtParam.Controller.Pext2', evtParam_Controller_Pext2_input[time] )
      
      status = fmu.doStep( time, step_size, new_step )
      time = time + step_size

      if( time % 60 ) == 30:
         x1 = fmu.getRealValue( 'ElmTr2.Transformer.m:P:buslv' ) # retrieve output variable 'ElmTr2.Transformer.m:P:buslv'
         assert round( x1, 5 ) == expected_results[ time ][ 'ElmTr2.Transformer.m:P:buslv' ]
         
         x2 = fmu.getRealValue( 'ElmLod.Generation.m:I1:bus1' ) # retrieve output variable 'ElmLod.Generation.m:I1:bus1'
         assert round( x2, 5 ) == expected_results[ time ][ 'ElmLod.Generation.m:I1:bus1' ]


@pytest.fixture
def fix_zip_command():
   return '"C:\\Program Files\\7-Zip\\7z.exe" -y -o{dir} x {fmu} > nul'


@pytest.fixture
def fix_EvtParam_Controller_Pext1_input():
   input = {
      0.: -1.0,
      60.: -0.5,
      120.: -1.0,
      180.: -1.5,
      240.: -2.0
   }
   
   return input


@pytest.fixture
def fix_EvtParam_Controller_Pext2_input():
   input = {
      0.: 2.0,
      60.: 0.5,
      120.: 1.0,
      180.: 1.5,
      240.: 2.0
   }
   
   return input

   
@pytest.fixture
def fix_PFTestRMS_expected_results():
   expected_results = {
      30.: { 'ElmTr2.Transformer.m:P:buslv': -0.89504, 'ElmLod.Generation.m:I1:bus1': 1.48945 },
      90.: { 'ElmTr2.Transformer.m:P:buslv': 0.01403, 'ElmLod.Generation.m:I1:bus1': 0.73285 },
      150.: { 'ElmTr2.Transformer.m:P:buslv': 0.05495, 'ElmLod.Generation.m:I1:bus1': 1.50371 },
      210.: { 'ElmTr2.Transformer.m:P:buslv': 0.11969, 'ElmLod.Generation.m:I1:bus1': 2.30737 },
      270.: { 'ElmTr2.Transformer.m:P:buslv': 0.20321, 'ElmLod.Generation.m:I1:bus1': 3.13618 }
   }
   
   return expected_results


@pytest.mark.fmi1
def test_fmi1_PFTestRMS( fix_zip_command, fix_EvtParam_Controller_Pext1_input, fix_EvtParam_Controller_Pext2_input, fix_PFTestRMS_expected_results ):
   sim_PFTestRMS( fix_zip_command, fix_EvtParam_Controller_Pext1_input, fix_EvtParam_Controller_Pext2_input, fix_PFTestRMS_expected_results, 1 )


@pytest.mark.fmi2
def test_fmi2_PFTestRMS( fix_zip_command, fix_EvtParam_Controller_Pext1_input, fix_EvtParam_Controller_Pext2_input, fix_PFTestRMS_expected_results ):
   sim_PFTestRMS( fix_zip_command, fix_EvtParam_Controller_Pext1_input, fix_EvtParam_Controller_Pext2_input, fix_PFTestRMS_expected_results, 2 )
