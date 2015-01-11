import pytest
import requests_mock
from polibeepsync.common import User


def test_logout():
    me = User(11111111, 'fakepassword')
    me.logout()
    assert me.logged is False

