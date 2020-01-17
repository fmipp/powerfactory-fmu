# Example: Time advance mechanism based on DPL scripts

Create the PowerFactory FMUs for testing the simulation time advance mechanism based on DPL scripts with the following commands.

## FMI 1.0

```
python.exe ..\..\powerfactory_fmu_create.py -v -f 1 -m PFTestDPLScriptV1 -p TestDPLScript.pfd -i TestDPLScript-inputs.txt -o TestDPLScript-outputs.txt -s SetTime:1:0 ElmLod.Load.plini=0.6
```

## FMI 2.0

```
python.exe ..\..\powerfactory_fmu_create.py -v -m PFTestDPLScriptV2 -p TestDPLScript.pfd -i TestDPLScript-inputs.txt -o TestDPLScript-outputs.txt -s SetTime:1:0 ElmLod.Load.plini=0.6
```