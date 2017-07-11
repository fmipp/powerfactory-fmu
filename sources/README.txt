This directory contains the complete source code for:
 - the FMI-compliant frontend component
 - an extended API for interacting with PowerFactory
 - the DLL implementing the FMIAdapter DSL model

In addiotion, it contains the minimum set of source code required 
from the FMI++ library that is needed to compile an FMU (using 
the pre-compiled "libfmipp_fmu_frontend.lib"). For compiling the
library "libfmipp_fmu_frontend.lib", a complete version of the
FMI++ library is required, see http://fmipp.sourceforge.net