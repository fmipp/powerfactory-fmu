@ECHO OFF

REM Create the PowerFactory FMU for testing RMS simulations with the following command:

python.exe ..\..\powerfactory_fmu_create.py -v -m PFTestRMS -p TestRMS.pfd -i TestRMS-inputs.txt -o TestRMS-outputs.txt -r 1 ElmLod.Load.plini=0.6

PAUSE