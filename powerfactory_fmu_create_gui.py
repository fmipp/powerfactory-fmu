# -----------------------------------------------------------------
# Copyright (c) 2017-2020, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file TRNSYS_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------

from gooey import Gooey, GooeyParser
import os, sys, argparse

import powerfactory_fmu_create

# Retrieve the absolute path to the root directory of the PowerFactory FMU Export Utility.
# This has to be done differently in case the GUI has already been packaged with the help of
# PyInstaller (via sys.executable) or in case this script is run using Python (via __file__).
pf_fmu_root_dir = os.path.dirname( sys.executable ) if getattr( sys, 'frozen', False ) else os.path.dirname( __file__ )
pf_fmu_root_dir = os.path.abspath( pf_fmu_root_dir )

# Retrieve the absolute path to the directory containing the icons.
# This has to be done differently in case the GUI has already been packaged with the help of
# PyInstaller (via sys._MEIPASS) or in case this script is run using Python (via __file__).
gui_image_dir = sys._MEIPASS if getattr( sys, 'frozen', False ) else os.path.join( os.path.dirname( __file__ ), 'sources', 'logo' )
gui_image_dir = os.path.abspath( gui_image_dir )


@Gooey(
   program_name = 'FMI++ PowerFactory FMU Export Utility',
   required_cols = 1, # Number of columns in the "Required" section.
   optional_cols = 2, # Number of columbs in the "Optional" section.
   default_size=( 1200, 960 ), # starting size of the GUI
   image_dir = gui_image_dir,
   # menu=[{
      # 'name': 'File',
      # 'items': [{
         # 'type': 'AboutDialog',
         # 'menuTitle': 'About',
         # 'name': 'FMI++ PowerFactory FMU Export Utility',
         # 'description': 'The FMI++ PowerFactory FMU Export Utility is a stand-alone tool for exporting FMUs for Co-Simulation from DIgSILENT PowerFactory models. It is open-source and freely available. It is based on code from the FMI++ library and the Boost C++ libraries.',
         # 'website': 'https://powerfactory-fmu.sourceforge.net',
         # 'developer': 'https://www.ait.ac.at/profile/detail/Widl-Edmund',
         # #'license': 'BSD'
         # }]
      # }]
   )
def parseCommandLineArgumentsGooey():
   # Create new parser.
   parser = GooeyParser( description = 'This program generates FMUs for Co-Simulation (tool coupling) from PowerFactory PFD files.', prog = 'powerfactory_fmu_create' )

   # Define mandatory arguments.
   required_args = parser.add_argument_group( 'Required arguments' )
   required_args.add_argument( '-m', '--model-id', required = True, help = 'Specify FMU model identifier', metavar = 'FMI model identifier' )
   required_args.add_argument( '-p', '--pfd-file', required = True, help = 'Path to PowerFactory PFD file', metavar = 'PowerFactory PFD file', widget = 'FileChooser' )

   time_args = parser.add_argument_group( 'Time Advance Mechanism', 'Specify exactly one time advance mechanism' )
   time_args.add_argument( '-t', '--trigger', action = 'append', default = [], help = 'Specify a trigger for advancing simulation time (name:scale)', metavar = 'Trigger' )
   time_args.add_argument( '-s', '--dpl-script', action = 'append', default = [], help = 'Specify a DPL-script for advancing simulation time (name:scale:offset)', metavar = 'DPL script' )
   time_args.add_argument( '-r', '--rms-sim', action = 'append', default = [], help = 'Specify the RMS simulation integrator step size (in seconds)', metavar = 'RMS simulation' )

   optional_args = parser.add_argument_group( 'Optional arguments' )
   optional_args.add_argument( '-v', '--verbose', action = 'store_true', default = True, help = 'Turn on log messages', metavar = 'Verbosity' )
   optional_args.add_argument( '-l', '--litter', action = 'store_true', help = 'Do not clean-up intermediate files', metavar = 'Litter' )
   optional_args.add_argument( '-i', '--input-var-file', default = None, help = 'Specify file containing list of input variable names', metavar = 'Input variable definition file', widget = 'FileChooser' )
   optional_args.add_argument( '-o', '--output-var-file', default = None, help = 'Specify file containing list of output variable names', metavar = 'Output variable definition file', widget = 'FileChooser' )
   optional_args.add_argument( '-f', '--fmi-version', choices = [ '1', '2' ], default = '2', help = 'Specify FMI version (default: 2)', metavar = 'FMI version' )
   optional_args.add_argument( '-d', '--pf-install-dir', default = None, help = 'Path to PowerFactory installation directory', metavar = 'PowerFactory installation directory', widget = 'DirChooser' )
   optional_args.add_argument( 'extra_arguments', nargs = '*', default = None, help = 'Start values and/or extra files (absolute paths or paths relative to current working directory)', metavar = 'Additional arguments' )

   return parser.parse_args()


if __name__ == '__main__':

   powerfactory_fmu_create.main( pf_fmu_root_dir, parseCommandLineArgumentsGooey )