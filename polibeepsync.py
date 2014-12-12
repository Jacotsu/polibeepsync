from bs4 import BeautifulSoup
import requests



class InvalidLoginError(Exception):
    pass


class User:
    loginurl = 'https://beep.metid.polimi.it/polimi/login'
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.logged = False

    def visit(self):
        """Visit the login webpage to test for working connection."""
        try:
            self.session.get(self.loginurl)
        except (requests.ConnectionError, requests.Timeout):
            # re-raise the exception for the moment
            raise

    def login(self):
        """Try logging in.

        If the login is successful, a session attribute is set on the object.
        If it fails, raises an InvalidLoginError.

        If possible, this method should be rewritten using only requests."""
        # make sure to use the english webpage
        pass

    def get_available_courses(self):
        pass

