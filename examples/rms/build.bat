@ECHO OFF

REM Create the PowerFactory FMUs for testing RMS simulations with the following commands:

REM FMI 1.0
python.exe ..\..\powerfactory_fmu_create.py -v -f 1 -m PFTestRMSV1 -p TestRMS.pfd -i TestRMS-inputs.txt -o TestRMS-outputs.txt -r 1 ElmLod.Load.plini=0.6

ECHO.

REM FMI 2.0
python.exe ..\..\powerfactory_fmu_create.py -v -m PFTestRMSV2 -p TestRMS.pfd -i TestRMS-inputs.txt -o TestRMS-outputs.txt -r 1 ElmLod.Load.plini=0.6

ECHO.