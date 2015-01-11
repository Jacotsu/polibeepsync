import pytest
import requests_mock
from polibeepsync.common import User
import os

def get_file(name):
    here = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(here, name)

def test_logout():
    me = User(11111111, 'fakepassword')
    me.logout()
    assert me.logged is False

# skip until I understand how to properly make assertions with requests
@pytest.mark.skipif(True, reason="Study requests_mock")
def test_validloginfirststep_italian():
    body = get_file('login-step1.htm')
    bodyf = open(body, 'rb')
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://beep.metid.polimi.it/polimi/login',
                       body=bodyf)
        m.register_uri('GET', 'https://aunicalogin.polimi.it/aunicalogin/aunicalogin/controller/IdentificazioneUnica.do?evn_jaf_cambio_lingua=event&lang=EN&screenName=/IdentificazioneUnica&freezecount=true&jaf_currentWFID=main&polij_step=0&__pj0=0&__pj1=cd97d32efad73eef04f28052f96dfa27')
        m.register_uri('POST', 'https://aunicalogin.polimi.it:443/aunicalogin/\
aunicalogin/controller/IdentificazioneUnica.do?&jaf_currentWFID=main')
        me = User(11111111, 'fakepassword')
        me._login_first_step()
        #assert False
    bodyf.close()
