__copyright__ = "Copyright 2014 Davide Olianas (ubuntupk@gmail.com)."

__license__ = """This file is part of poliBeePsync.
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

__version__ = 0.1

from configparser import RawConfigParser, MissingSectionHeaderError
import os


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
        with open(infile, 'rt') as f:
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
