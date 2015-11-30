Create the PowerFactory FMUs with the following command (from the test directory):

FMU for testing the simulation time advance mechanism based on triggers:
python ..\powerfactory-fmu-create.py -v -m PFTestTriggers -p TestTriggers.pfd -i TestTriggers-inputs.txt -o TestTriggers-outputs.txt -t Trigger:60 ElmLod.Load.plini=0.1

FMU for testing the simulation time advance mechanism based on a DPL script:
python ..\powerfactory-fmu-create.py -v -m PFTestDPLScript -p TestDPLScript.pfd -i TestDPLScript-inputs.txt -o TestDPLScript-outputs.txt -s SetTime:1:0
