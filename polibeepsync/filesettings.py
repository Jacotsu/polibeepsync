__copyright__ = """Copyright 2020 Davide Olianas (ubuntupk@gmail.com), Di
Campli Raffaele (dcdrj.pub@gmail.com)."""

__license__ = """This f is part of poliBeePsync.
poliBeePsync is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

poliBeePsync is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with poliBeePsync. If not, see <http://www.gnu.org/licenses/>.
"""

from configparser import RawConfigParser, MissingSectionHeaderError
import os
import re


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


__version__ = find_version("__init__.py")


def settingsFromFile(infile, defaults):
    """Given a path string :attr:`infile`, load settings and return them as
    dictionary.

    Args:
        infile (str): a path to a file
        defaults (dict): a dictionary containing fallback values
    """
    config = RawConfigParser()
    config.optionxform = lambda option: option
    try:
        with open(infile) as f:
            try:
                config.read_file(f)
            except MissingSectionHeaderError:
                config['General'] = defaults
    except OSError:
        config['General'] = defaults
    for key in defaults:
        if key not in config['General']:
            config['General'][key] = defaults[key]
    try:
        if int(config['General']['UpdateEvery']) <= 0:
            config['General']['UpdateEvery'] = defaults['UpdateEvery']
    except ValueError:
        # can't convert to integer
        config['General']['UpdateEvery'] = defaults['UpdateEvery']
    for value in ('SyncNewCourses', ):
        try:
            booleanvalue = config.getboolean('General', value)
            config['General'][value] = str(booleanvalue)
        except ValueError:
            # can't convert to boolean
            config['General'][value] = defaults[value]
    return dict(config['General'])


def settingsToFile(insettings, filepath):
    """Given a dict, save to file in the format specified by configparser"""
    config = RawConfigParser()
    config.optionxform = lambda option: option
    config['General'] = insettings
    try:
        dirpath = os.path.dirname(filepath)
        os.makedirs(dirpath, exist_ok=True)
        with open(filepath, 'w') as f:
            config.write(f)
    except OSError:
        if not os.path.isdir(dirpath):
            raise
