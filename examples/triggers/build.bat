@ECHO OFF

REM Create the PowerFactory FMU for testing the simulation time advance mechanism based on triggers with the following command:

D:\Python34\python ..\..\powerfactory_fmu_create.py -v -m PFTestTriggers -p TestTriggers.pfd -i TestTriggers-inputs.txt -o TestTriggers-outputs.txt -t Trigger:60 TestTriggers-characteristics.csv ElmLod.Load.plini=0.6

PAUSE