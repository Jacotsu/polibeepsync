from cx_Freeze import setup, Executable
import requests.certs
import os

build_exe_options = {"packages": ['requests', 'polibeepsync'],
                     "include_files":[(requests.certs.where(),'cacert.pem')],
                     }

executables = [
    Executable(os.path.join('polibeepsync', 'qtgui.py'))
]

setup(
    name="prova",
    version="0.1.1",
    options = {'build_exe': build_exe_options},
      executables=executables, requires=['requests', 'PySide']
      )