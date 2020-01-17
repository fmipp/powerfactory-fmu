# Example: Time advance mechanism based on triggers

Create the PowerFactory FMUs for testing the simulation time advance mechanism based on triggers with the following commands.

## FMI 1.0

```
python.exe ..\..\powerfactory_fmu_create.py -v -f 1 -m PFTestTriggersV1 -p TestTriggers.pfd -i TestTriggers-inputs.txt -o TestTriggers-outputs.txt -t Trigger:60 TestTriggers-characteristics.csv ElmLod.Load.plini=0.6
```

## FMI 2.0

```
python.exe ..\..\powerfactory_fmu_create.py -v -m PFTestTriggersV2 -p TestTriggers.pfd -i TestTriggers-inputs.txt -o TestTriggers-outputs.txt -t Trigger:60 TestTriggers-characteristics.csv ElmLod.Load.plini=0.6
```
