from distutils.core import setup
from esky.bdist_esky import Executable
import requests.certs
import os
import sys

#build_exe_options = {"packages": ['requests', 'polibeepsync'],
#                     "include_files":[(requests.certs.where(),'cacert.pem')],
#                     }

base=None
if sys.platform == 'win32':
	base = 'Win32GUI'

executables = [
    Executable(os.path.join('polibeepsync', 'qtgui.py'))
]
#prog = Executable('polibeepsync/qtgui.py', base=base)

data_files = ['.venv34/lib/python3.4/site-packages/requests/cacert.pem']

setup(
    name="poliBeePsync",
    version="0.3.1",
    options = {#'build_exe': build_exe_options,
               "bdist_esky": {
        "freezer_module": "cx_freeze"}},
      scripts=executables,
      data_files = data_files
      )
