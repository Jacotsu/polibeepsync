from setuptools import setup
import setup as og_setup

APP = ['poliBeePSync.py']
DATA_FILES = []
OPTIONS = {
 'O1': True,
 'app': 'poliBeePSync.py',
 'arch': 'x86_64',
 'dist_dir': 'packaging/mac_os/',
 'packages': 'requests,appdirs,PySide2,beautifulsoup4,lxml,pyparsing,'
             'keyring,signalslot,PyQt5',
 'plist': {
     'CFBundleName': 'poliBeePSync',
     'CFBundleShortVersionString': og_setup.find_version("polibeepsync"
                                                         "/__init__.py"),
     'CFBundleVersion': og_setup.find_version("polibeepsync/__init__.py"),
     'CFBundleIdentifier': 'com.github.jacotsu.polibeepsync',
     'NSHumanReadableCopyright': '@ Davide Olianas, Raffaele Di Campli 2020'
 }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    name='poliBeePsync',
    version=og_setup.find_version("polibeepsync/__init__.py"),
    url="https://github.com/Jacotsu/polibeepsync",
    author="Davide Olianas, Raffaele Di Campli",
    author_email="ubuntupk@gmail.com, dcdrj.pub@gmail.com",
    license='GPLv3+',
    python_requires='>=3.7',
    packages=['polibeepsync'],
    package_data={'': ['new_gui.ui']},
    include_package_data=True,
    description="Sync files from https://beep.metid.polimi.it "
    "(for students of Politecnico di Milano)",
    long_description=og_setup.long_description,
    classifiers=og_setup.classifiers,
    entry_points={
        'console_scripts': [
            'polibeepsync=polibeepsync.qtgui:main',
        ],
        'gui_scripts': [
            'polibeepsync-gui=polibeepsync.qtgui:main'
        ]
    }
)
