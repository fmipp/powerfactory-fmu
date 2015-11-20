Create the PowerFactory FMUs with the following command (from the PowerFactory-FMU root directory):

FMU for testing the simulation time advance mechanism based on triggers:
python powerfactory-fmu-create.py -v -m PFTestTriggers -p test\TestTriggers.pfd -i test\TestTriggers-inputs.txt -o test\TestTriggers-outputs.txt -t Trigger:60 ElmLod.Load.plini=0.1

FMU for testing the simulation time advance mechanism based on a DPL script:
python powerfactory-fmu-create.py -v -m PFTestDPLScript -p test\TestDPLScript.pfd -i test\TestDPLScript-inputs.txt -o test\TestDPLScript-outputs.txt -s SetTime:1:0
