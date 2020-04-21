# -*- mode: python ; coding: utf-8 -*-
import sys
import glob
import shutil
import re

exclude_files = [
    '**/docs**',
    '**/tests**',
    '**/Qt5Designer**',
    '**/Qt5Location**',
    '**/opengl32sw**',
    '**/QtBluetooth**',
    '**/QtDBus**',
    '**/QtDesigner**',
    '**/QtHelp**',
    '**/QtLocation**',
    '**/QtMultimedia**',
    '**/QtMultimediaWidgets**',
    '**/QtNetwork**',
    '**/QtNetworkAuth**',
    '**/QtNfc**',
    '**/QtOpenGL**',
    '**/QtPositioning**',
    '**/QtPrintSupport**',
    '**/QtQuick**',
    '**/QtQuickWidgets**',
    '**/QtRemoteObjects**',
    '**/QtSensors**',
    '**/QtSerialPort**',
    '**/QtSql**',
    '**/QtTest**',
    '**/QtWebChannel**',
    '**/QtWebSockets**',
    '**/Qt3D**',
    '**/examples**',
    '**/audio**',
    '**/canbus**',
    '**/gamepads**',
    '**/geoservices**',
    '**/printsupport**',
    '**/scenegraph**',
    '**/sceneparsers**',
    '**/sensorgestures**',
    '**/sensors**',
    '**/texttospeech**',
    '**/QtBluetooth**',
    '**/QtGamepad**',
    '**/QtGraphicalEffects**',
    '**/QtLocation**',
    '**/QtNfc**',
    '**/QtQuick3D**',
    '**/QtRemoteObjects**',
    '**/QtTest**',
    '**/QtWebEngine**',
    '**/resources/qtwebengine***',
    '**/translations/qtwebengine_**',
    '**/shiboken2/docs**'
]

hidden_imports = ['PySide2.QtXml']
if sys.platform in ['win32', 'win64', 'linux']:
    hidden_imports += ['pywin32', 'win32timezone']

def read(*names, **kwargs):
    with open(
        os.path.join('.', *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

block_cipher = None


a = Analysis(['polibeepsync/qtgui.py'],
             pathex=['/home/jacotsu/polibeepsync'],
             binaries=[],
             datas=[('polibeepsync/*', 'polibeepsync')],
             hiddenimports=hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=exclude_files,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)


pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

# First, generate an executable file
# Notice that the icon is a .icns file - Apple's icon format
# Also note that console=True
if sys.platform == 'darwin':
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              name='PoliBeePsync',
              debug=False,
              strip=True,
              upx=True,
              runtime_tmpdir=None,
              console=False,
              icon='imgs/icons/polibeepsync.icns')
    app = BUNDLE(exe,
                 name='PoliBeePsync.app',
                 info_plist={
                     'NSHighResolutionCapable': 'True',
                     'CFBundleName': 'poliBeePSync',
                     'CFBundleDisplayName': 'poliBeePSync',
                     'CFBundleShortVersionString':
                        find_version("polibeepsync/__init__.py"),
                     'CFBundleVersion':
                        find_version("polibeepsync/__init__.py"),
                     'CFBundleIdentifier': 'com.github.jacotsu.polibeepsync',
                     'NSHumanReadableCopyright': 'Copyright © Davide Olianas, '
                     'Raffaele Di Campli 2020'
                 },
                 icon='imgs/icons/polibeepsync.icns')
elif sys.platform in ['win32', 'win64', 'linux']:
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              name='PoliBeePsync',
              debug=False,
              strip=False,
              upx=True,
              runtime_tmpdir=None,
              console=False,
              icon='imgs/icons/polibeepsync.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='PoliBeePsync')
