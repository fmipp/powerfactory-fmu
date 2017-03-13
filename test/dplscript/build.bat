@ECHO OFF

REM Create the PowerFactory FMU for testing the simulation time advance mechanism based on triggers with the following command:

D:\Python34\python ..\..\powerfactory_fmu_create.py -v -m PFTestDPLScript -p TestDPLScript.pfd -i TestDPLScript-inputs.txt -o TestDPLScript-outputs.txt -s SetTime:1:0 ElmLod.Load.plini=0.6

PAUSE