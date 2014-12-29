# run this with python buildwin.py bdist_msi
import sys
from cx_Freeze import setup, Executable

base=None
if sys.platform == 'win32':
	base = 'Win32GUI'

executables = [
	Executable('polibeepsync\qtgui.py', base=base)]

setup(name='poliBeePsync',
	version='0.1.1',
	executables=executables)