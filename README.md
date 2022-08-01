# The FMI++ PowerFactory FMU Export Utility

The FMI++ PowerFactory FMU Export Utility is a stand-alone tool for exporting FMUs for Co-Simulation (FMI Version 1.0 & 2.0) from [DIgSILENT PowerFactory](https://www.digsilent.de/en/powerfactory.html) models. 
It is open-source (BSD-like license) and freely available. 
It is based on code from the [FMI++ library](https://github.com/fmipp/fmipp) and the [Boost C++ libraries](https://boost.org).

Instructions on installation and usage are given in the documentation, which is provided as part of the [binary release version](https://github.com/fmipp/powerfactory-fmu/releases/download/v1.0/powerfactory-fmu-v1.0-PF2019-SP4-x64.zip).

The FMI++ PowerFactory FMU Export Utility provides a graphical user interface (new in version v1.0) and - alternatively - Python scripts that generate FMUs from certain PowerFactory models.
Additional files (e.g., time series files) and start values for exported variables can be specified.


Currently, two types of simulations are supported:

+ In **quasi-static steady-state simulations** a power system’s evolution with respect to time is captured by a series of load flow snapshots.
+ **RMS simulations** allow to calculate the time-dependent dynamics of electromechanical models, including control devices (new in version v0.6).

## Features

+ compliant to FMU for Co-Simulation (version 1.0 and 2.0)
+ creates FMUs from certain DiGSILENT PowerFactory models
+ supports quasi-static steady-state simulations
+ supports RMS simulations
+ graphical user interface
