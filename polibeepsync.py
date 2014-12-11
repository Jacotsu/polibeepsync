from selenium import webdriver
import requests

class InvalidLoginError(Exception):
    pass

class User:
    loginurl = 'https://beep.metid.polimi.it/polimi/login'
    def __init__(self, username, password):
        self.username = username
        self.password = password


    def visit(self):
        """Visit the login webpage to test for working connection."""
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1600, 1200)
        try:
            requests.get(self.loginurl)
        except (requests.ConnectionError, requests.Timeout):
            # re-raise the exception for the moment
            raise
        else:
            self.driver.get(self.loginurl)

    def login(self):
        """Try logging in.

        If the login is successful, a session attribute is set on the object.
        If it fails, raises an InvalidLoginError."""
        self.driver.find_element_by_id('login').send_keys(self.username)
        self.driver.find_element_by_id('password').send_keys(self.password)
        self.driver.find_element_by_xpath('//input[@type="submit" and @name="evn_conferma=evento"]').click()
        try:
            self.driver.find_element_by_xpath('//div[@class="sign-in"]/a').click()
        except selenium.common.exceptions.NoSuchElementException:
            raise InvalidLoginError()
        else:
            cook = {i['name']: i['value'] for i in self.driver.get_cookies()}
            self.driver.quit()
            self.session = requests.get("https://beep.metid.polimi.it", cookies=cook)


