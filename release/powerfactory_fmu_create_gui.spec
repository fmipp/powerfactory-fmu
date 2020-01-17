## Create the GUI with the following commands (with the project's root directory as working directory):
##
## > pip install gooey pyinstaller
## > pyinstaller -w -F release\powerfactory_fmu_create_gui.spec
##
## Before running these commands, edit the following two lines to fir your installation:
pf_fmu_root_dir = 'C:\\Development\\powerfactory-fmu'
python_scripts_dir = 'C:\\Python37-x64\\Scripts'

import gooey
gooey_root = os.path.dirname(gooey.__file__)
gooey_languages = Tree(os.path.join(gooey_root, 'languages'), prefix = 'gooey/languages')
gooey_images = Tree(os.path.join(gooey_root, 'images'), prefix = 'gooey/images')

a = Analysis( [ os.path.join( pf_fmu_root_dir, 'powerfactory_fmu_create_gui.py' ) ],
              pathex = [ python_scripts_dir ],
              hiddenimports = [],
              hookspath = None,
              runtime_hooks = None,
			  datas = [ ( os.path.join( pf_fmu_root_dir, 'sources', 'logo', 'config_icon.png' ), '.' ) ]
              )

pyz = PYZ( a.pure )

options = [ ( 'u', None, 'OPTION' ) ]

exe = EXE( pyz,
           a.scripts,
           a.binaries,
           a.zipfiles,
           a.datas,
           options,
           gooey_languages,
           gooey_images,
           name = 'powerfactory_fmu_create.exe',
           debug = False,
           strip = None,
           upx = True,
           console = False,
           icon = os.path.join( pf_fmu_root_dir, 'sources', 'logo', 'program_icon.ico' )
		   )