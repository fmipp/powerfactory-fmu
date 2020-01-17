@ECHO OFF

REM Store current working directory.
SET CWD=%CD%

REM Root directory of FMI++ PowerFactory FMU Export Utility.
SET PF_FMU_ROOT_DIR=%~dp0\..\..

REM Build FMU for testing triggers (PFTestTriggersV1.fmu and PFTestTriggersV2.fmu).
CD %PF_FMU_ROOT_DIR%\examples\triggers
RMDIR /Q /S PFTestTriggersV1 PFTestTriggersV2
DEL /Q PFTestTriggersV1.fmu PFTestTriggersV2.fmu
CALL build.bat

REM Build FMU for testing DPL scripts (PFTestDPLScriptV1.fmu and PFTestDPLScriptV2.fmu).
CD %PF_FMU_ROOT_DIR%\examples\dplscript
RMDIR /Q /S PFTestDPLScriptV1 PFTestDPLScriptV2
DEL /Q PFTestDPLScriptV1.fmu PFTestDPLScriptV2.fmu
CALL build.bat

REM Build FMU for testing RMS simulations (PFTestRMSV1.fmu and PFTestRMSV2.fmu).
CD %PF_FMU_ROOT_DIR%\examples\rms
RMDIR /Q /S PFTestRMSV1 PFTestRMSV2
DEL /Q PFTestRMSV1.fmu PFTestRMSV2.fmu
CALL build.bat

REM Change back to directory for testing.
CD %PF_FMU_ROOT_DIR%\release\test

REM Run test for triggers.
pytest -rpP -m fmi1 test_PFTestTriggers.py
SET TEST_TRIGGER_V1_RES=%ERRORLEVEL%
pytest -rpP -m fmi2 test_PFTestTriggers.py
SET TEST_TRIGGER_V2_RES=%ERRORLEVEL%
SET /A "TEST_TRIGGER_RES=%TEST_TRIGGER_V1_RES%|%TEST_TRIGGER_V2_RES%"

REM Run test for DPL scripts.
pytest -rpP -m fmi1 test_PFTestDPLScript.py
SET TEST_DPL_SCRIPT_V1_RES=%ERRORLEVEL%
pytest -rpP -m fmi2 test_PFTestDPLScript.py
SET TEST_DPL_SCRIPT_V2_RES=%ERRORLEVEL%
SET /A "TEST_DPL_SCRIPT_RES=%TEST_DPL_SCRIPT_V1_RES%|%TEST_DPL_SCRIPT_V2_RES%"

REM Run test for RMS simulations.
pytest -rpP -m fmi1 test_PFTestRMS.py
SET TEST_RMS_SIM_V1_RES=%ERRORLEVEL%
pytest -rpP -m fmi2 test_PFTestRMS.py
SET TEST_RMS_SIM_V2_RES=%ERRORLEVEL%
SET /A "TEST_RMS_SIM_RES=%TEST_RMS_SIM_V1_RES%|%TEST_RMS_SIM_V2_RES%"

REM Final test result.
SET /A "TEST_RES=%TEST_TRIGGER_RES%|%TEST_DPL_SCRIPT_RES%|%TEST_RMS_SIM_RES%"

REM Change back to previous working directory.
CD %CWD%

REM Return final result.
EXIT /B %TEST_RES%