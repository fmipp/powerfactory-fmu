Create the PowerFactory FMU with the following command (from the PowerFactory-FMU root directory):

python powerfactory-fmu-create.py -v -m PFTest -p test\TestTriggers.pfd -i test\test-inputs.txt -o test\test-outputs.txt -t Trigger:60 ElmLod.Load.plini=0.1
