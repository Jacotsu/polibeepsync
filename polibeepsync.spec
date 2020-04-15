# -*- mode: python ; coding: utf-8 -*-
import sys
import glob
import shutil
import re

deletable_files = [
    'dist/PoliBeePsync/**.pyc',
    'dist/PoliBeePsync/**/docs**',
    'dist/PoliBeePsync/**/tests**',
    'dist/PoliBeePsync/**/Qt5Designer**',
    'dist/PoliBeePsync/**/Qt5Location**',
    'dist/PoliBeePsync/**/opengl32sw**',
    'dist/PoliBeePsync/**/QtBluetooth**',
    'dist/PoliBeePsync/**/QtDBus**',
    'dist/PoliBeePsync/**/QtDesigner**',
    'dist/PoliBeePsync/**/QtHelp**',
    'dist/PoliBeePsync/**/QtLocation**',
    'dist/PoliBeePsync/**/QtMultimedia**',
    'dist/PoliBeePsync/**/QtMultimediaWidgets**',
    'dist/PoliBeePsync/**/QtNetwork**',
    'dist/PoliBeePsync/**/QtNetworkAuth**',
    'dist/PoliBeePsync/**/QtNfc**',
    'dist/PoliBeePsync/**/QtOpenGL**',
    'dist/PoliBeePsync/**/QtPositioning**',
    'dist/PoliBeePsync/**/QtPrintSupport**',
    'dist/PoliBeePsync/**/QtQuick**',
    'dist/PoliBeePsync/**/QtQuickWidgets**',
    'dist/PoliBeePsync/**/QtRemoteObjects**',
    'dist/PoliBeePsync/**/QtSensors**',
    'dist/PoliBeePsync/**/QtSerialPort**',
    'dist/PoliBeePsync/**/QtSql**',
    'dist/PoliBeePsync/**/QtTest**',
    'dist/PoliBeePsync/**/QtWebChannel**',
    'dist/PoliBeePsync/**/QtWebSockets**',
    'dist/PoliBeePsync/**/Qt3D**',
    'dist/PoliBeePsync/**/examples**',
    'dist/PoliBeePsync/**/audio**',
    'dist/PoliBeePsync/**/canbus**',
    'dist/PoliBeePsync/**/gamepads**',
    'dist/PoliBeePsync/**/geoservices**',
    'dist/PoliBeePsync/**/printsupport**',
    'dist/PoliBeePsync/**/scenegraph**',
    'dist/PoliBeePsync/**/sceneparsers**',
    'dist/PoliBeePsync/**/sensorgestures**',
    'dist/PoliBeePsync/**/sensors**',
    'dist/PoliBeePsync/**/texttospeech**',
    'dist/PoliBeePsync/**/QtBluetooth**',
    'dist/PoliBeePsync/**/QtGamepad**',
    'dist/PoliBeePsync/**/QtGraphicalEffects**',
    'dist/PoliBeePsync/**/QtLocation**',
    'dist/PoliBeePsync/**/QtNfc**',
    'dist/PoliBeePsync/**/QtQuick3D**',
    'dist/PoliBeePsync/**/QtRemoteObjects**',
    'dist/PoliBeePsync/**/QtTest**',
    'dist/PoliBeePsync/**/QtWebEngine**',
    'dist/PoliBeePsync/**/resources/qtwebengine***',
    'dist/PoliBeePsync/**/translations/qtwebengine_**',
    'dist/PoliBeePsync/shiboken2/docs**'
]

hidden_imports=['PySide2.QtXml']
if sys.platform == 'win32' or sys.platform == 'win64':
    hidden_imports += ['pywin32', 'wind32timezones']

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

def delete_globbed_files(glob_list):
    for _glob in glob_list:
        matching_paths = glob.glob(_glob, recursive=True)
        for path in matching_paths:
            shutil.rmtree(path, ignore_errors=True)

block_cipher = None


a = Analysis(['polibeepsync/qtgui.py'],
             pathex=['/home/jacotsu/polibeepsync'],
             binaries=[],
             datas=[('polibeepsync/*', 'polibeepsync')],
             hiddenimports=['PySide2.QtXml'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)


pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = None
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
    delete_globbed_files(deletable_files)
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
elif sys.platform == 'win32' or sys.platform == 'win64' \
        or sys.platform == 'linux':
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
    delete_globbed_files(deletable_files)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='PoliBeePsync')

