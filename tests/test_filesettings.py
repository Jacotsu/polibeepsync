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

import pytest
import os
from polibeepsync.filesettings import settingsFromFile, settingsToFile
from configparser import RawConfigParser


@pytest.fixture
def default_settings_dict():
    conf = {
        'UpdateEvery': '60',
        'RootFolder': 'root',
        'SyncNewCourses': 'False',
        'DefaultTimeout': '10'
    }
    return conf


@pytest.fixture
def default_settings_file(tmpdir):
    conf = RawConfigParser()
    conf.optionxform = lambda option: option
    conf['General'] = {
        'UpdateEvery': '60',
        'RootFolder': 'root',
        'SyncNewCourses': 'False',
        'DefaultTimeout': '10'
    }
    f = tmpdir.mkdir('fold').join('sets.ini')
    with open(str(f), 'w') as setsfile:
        conf.write(setsfile)
    return str(f)


def test_allvaluesvalidpresent(default_settings_file, default_settings_dict):
    """All values are present in the config file
    All values are valid
    File is accessible"""
    sets = settingsFromFile(default_settings_file, default_settings_dict)
    assert sets == default_settings_dict


def test_notallvaluesarepresent(tmpdir, default_settings_dict):
    """Not all values are present; all are valid, file is accessible"""
    conf = RawConfigParser()
    conf.optionxform = lambda option: option
    conf['General'] = {
        'UpdateEvery': '50',
        'RootFolder': 'custom',
    }
    f = tmpdir.mkdir('fold').join('sets.ini')
    with open(str(f), 'w') as setsfile:
        conf.write(setsfile)
    sets = settingsFromFile(str(f), default_settings_dict)
    merge = {
        'UpdateEvery': '50',
        'RootFolder': 'custom',
        'SyncNewCourses': 'False',
        'DefaultTimeout': '10'
    }
    assert sets == merge


def test_allpresent_someinvalid(tmpdir, default_settings_dict):
    """File accessible, all values present, some not valid"""
    conf = RawConfigParser()
    conf.optionxform = lambda option: option
    conf['General'] = {
        'UpdateEvery': '-10',
        'SyncNewCourses': 'randomtext',
        'DefaultTimeout': 'kk'
    }
    f = tmpdir.mkdir('fold').join('sets.ini')
    with open(str(f), 'w') as setsfile:
        conf.write(setsfile)
    sets = settingsFromFile(str(f), default_settings_dict)
    nice = {
        'UpdateEvery': '60',
        'RootFolder': 'root',
        'SyncNewCourses': 'False',
        'DefaultTimeout': '10'
    }
    assert sets == nice


def test_somepresent_allinvalid(tmpdir, default_settings_dict):
    """Not all values present, all are invalid, file accessible"""
    conf = RawConfigParser()
    conf.optionxform = lambda option: option
    conf['General'] = {
        'UpdateEvery': 'noatanumer',
        'SyncNewCourses': 'lek',
        'DefaultTimeout': '-10'
    }
    f = tmpdir.mkdir('fold').join('sets.ini')
    with open(str(f), 'w') as setsfile:
        conf.write(setsfile)
    sets = settingsFromFile(str(f), default_settings_dict)
    nice = {
        'UpdateEvery': '60',
        'RootFolder': 'root',
        'SyncNewCourses': 'False',
        'DefaultTimeout': '10'
    }
    assert sets == nice


def test_missingsection(tmpdir, default_settings_dict):
    f = tmpdir.mkdir('fold').join('sets.ini')
    text = """UpdateEvery = 60\nRootFOlder = root\n
\nSyncNewCourses = True"""
    with open(str(f), 'w') as setsfile:
        setsfile.write(text)
    sets = settingsFromFile(str(f), default_settings_dict)
    assert sets == default_settings_dict


def test_missingfolder(default_settings_dict):
    sets = settingsFromFile('/i/dont/exist/sets.ini', default_settings_dict)
    assert sets == default_settings_dict


def test_missingfile(tmpdir, default_settings_dict):
    f = tmpdir.mkdir('fold')
    sets = settingsFromFile(str(f)+"nofile.ini", default_settings_dict)
    assert sets == default_settings_dict


def test_savefileexists(tmpdir, default_settings_dict):
    f = tmpdir.mkdir('fold').join('sets.ini')
    conf = RawConfigParser()
    conf.optionxform = lambda option: option
    conf['General'] = {
        'UpdateEvery': '30',
        'RootFolder': 'anotherroot',
        'SyncNewCourses': 'False'
    }
    with open(str(f), 'w') as setsfile:
        conf.write(setsfile)
    newsettings = {
        'UpdateEvery': '20',
        'RootFolder': 'finalroot',
        'SyncNewCourses': 'True',
        'DefaultTimeout': '10'
    }
    settingsToFile(newsettings, str(f))
    assert settingsFromFile(str(f), default_settings_dict) == newsettings


def test_saveioerror(tmpdir):
    """a generic IOError, for example we don't have write permission"""
    f = tmpdir.mkdir('fold').join('sets.ini')
    f.write('doesntmatter')
    os.chmod(str(f), 0o444)
    try:
        newsettings = {
            'UpdateEvery': '20',
            'RootFolder': 'finalroot',
            'SyncNewCourses': 'True'
        }
        settingsToFile(newsettings, str(f))
    except IOError:
        pass
