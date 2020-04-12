from setuptools import setup
import os
import re


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def read(*names, **kwargs):
    with open(
        os.path.join(os.path.dirname(__file__), *names),
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


classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: X11 Applications :: Qt",
    "Intended Audience :: Education",
    "License :: OSI Approved :: GNU General Public License v3 or later "
    "(GPLv3+)",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.7"
]


setup(
    name='poliBeePsync',
    version=find_version("polibeepsync/__init__.py"),
    url="https://github.com/Jacotsu/polibeepsync",
    author="Davide Olianas, Raffaele Di Campli",
    author_email="ubuntupk@gmail.com, dcdrj.pub@gmail.com",
    license='GPLv3+',
    install_requires=[
        "appdirs",
        "beautifulsoup4",
        "keyring",
        "lxml",
        "pyparsing",
        "PyQt5",
        "PySide2",
        "requests",
        "signalslot"
    ],
    python_requires='>=3.7',
    packages=['polibeepsync'],
    package_data={'': ['new_gui.ui', 'beep.pem']},
    include_package_data=True,
    description="Sync files from https://beep.metid.polimi.it "
    "(for students of Politecnico di Milano)",
    long_description=long_description,
    classifiers=classifiers,
    entry_points={
        'console_scripts': [
            'polibeepsync=polibeepsync.qtgui:main',
        ],
        'gui_scripts': [
            'polibeepsync-gui=polibeepsync.qtgui:main'
        ]
    }
)
