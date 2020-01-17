# -----------------------------------------------------------------------
# Copyright (c) 2017-2020, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file PowerFactory_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------------

from gooey import Gooey, GooeyParser
import os, sys, argparse

import powerfactory_fmu_install

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
    program_name = 'FMI++ PowerFactory FMU Export Utility Installer',
    required_cols = 1, # Number of columns in the "Required" section.
    optional_cols = 1, # Number of columbs in the "Optional" section.
    default_size=( 610, 350 ), # starting size of the GUI
    image_dir = gui_image_dir
    )
def parseCommandLineArgumentsGooey():
    # Create new parser.
    parser = GooeyParser( description = 'This program installs the FMI++ PowerFactory FMU Export Utility', prog = 'powerfactory_fmu_install' )

    # Define optional arguments.
    parser.add_argument( 'PowerFactory_install_dir', metavar = 'PowerFactory installation directory', widget = 'DirChooser' )

    cmd_line_args = parser.parse_args()
    return cmd_line_args.PowerFactory_install_dir


if __name__ == '__main__':

    powerfactory_fmu_install.main( pf_fmu_root_dir, parseCommandLineArgumentsGooey() )