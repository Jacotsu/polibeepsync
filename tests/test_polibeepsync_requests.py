import pytest
from polibeepsync.common import User
import os


def get_file(name):
    here = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(here, name)


def test_logout():
    me = User(11111111, 'fakepassword')
    me.logout()
    assert me.logged is False
