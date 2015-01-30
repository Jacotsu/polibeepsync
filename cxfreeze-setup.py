from cx_Freeze import setup, Executable
import requests.certs
import os
import sys

build_exe_options = {"packages": ['requests', 'polibeepsync'],
                     "include_files":[(requests.certs.where(),'cacert.pem')],
                     }

base=None
if sys.platform == 'win32':
	base = 'Win32GUI'

executables = [
    Executable(os.path.join('polibeepsync', 'qtgui.py'), base=base)
]

setup(
    name="poliBeePsync",
    version="0.3.1a",
    options = {'build_exe': build_exe_options},
      executables=executables, requires=['requests', 'PySide']
      )
