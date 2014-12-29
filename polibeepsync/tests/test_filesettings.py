import pytest
import os
from polibeepsync.filesettings import settingsFromFile, settingsToFile
from configparser import RawConfigParser


@pytest.fixture
def default_settings_dict():
    conf = {
        'UpdateEvery': '60',
        'RootFolder': 'root',
        'SyncNewCourses': 'False'
    }
    return conf


@pytest.fixture
def default_settings_file(tmpdir):
    conf = RawConfigParser()
    conf.optionxform = lambda option: option
    conf['General'] = {
        'UpdateEvery': '60',
        'RootFolder': 'root',
        'SyncNewCourses': 'False'
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


def test_notallvaluesarepresent(tmpdir):
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
    sets = settingsFromFile(str(f), default_settings_dict())
    merge = {
        'UpdateEvery': '50',
        'RootFolder': 'custom',
        'SyncNewCourses': 'False'
    }
    assert sets == merge


def test_allpresent_someinvalid(tmpdir):
    """File accessible, all values present, some not valid"""
    conf = RawConfigParser()
    conf.optionxform = lambda option: option
    conf['General'] = {
        'UpdateEvery': '-10',
        'SyncNewCourses': 'randomtext'
    }
    f = tmpdir.mkdir('fold').join('sets.ini')
    with open(str(f), 'w') as setsfile:
        conf.write(setsfile)
    sets = settingsFromFile(str(f), default_settings_dict())
    nice = {
        'UpdateEvery': '60',
        'RootFolder': 'root',
        'SyncNewCourses': 'False'
    }
    assert sets == nice


def test_somepresent_allinvalid(tmpdir):
    """Not all values present, all are invalid, file accessible"""
    conf = RawConfigParser()
    conf.optionxform = lambda option: option
    conf['General'] = {
        'UpdateEvery': 'noatanumer',
        'SyncNewCourses': 'False'
    }
    f = tmpdir.mkdir('fold').join('sets.ini')
    with open(str(f), 'w') as setsfile:
        conf.write(setsfile)
    sets = settingsFromFile(str(f), default_settings_dict())
    nice = {
        'UpdateEvery': '60',
        'RootFolder': 'root',
        'SyncNewCourses': 'False'
    }
    assert sets == nice


def test_missingsection(tmpdir):
    f = tmpdir.mkdir('fold').join('sets.ini')
    text = """UpdateEvery = 60\nRootFOlder = root\n
\nSyncNewCourses = True"""
    with open(str(f), 'w') as setsfile:
        setsfile.write(text)
    sets = settingsFromFile(str(f), default_settings_dict())
    assert sets == default_settings_dict()


def test_missingfolder():
    sets = settingsFromFile('/i/dont/exist/sets.ini', default_settings_dict())
    assert sets == default_settings_dict()


def test_missingfile(tmpdir):
    f = tmpdir.mkdir('fold')
    sets = settingsFromFile(str(f)+"nofile.ini", default_settings_dict())
    assert sets == default_settings_dict()


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
        'SyncNewCourses': 'True'
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
