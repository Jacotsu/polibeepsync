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
        self.subscribed_courses = []
        self.courses_url = ""
        self.available_courses = []

    def visit(self):
        """Visit the login webpage to test for working connection."""
        try:
            self.session.get('https://beep.metid.polimi.it')
        except (requests.ConnectionError, requests.Timeout):
            # re-raise the exception for the moment
            raise

    def get_resource(self, url):
        """Get a page and re-login if the session is expired.

        Returns: a requests.get(url) response
        """
        response = self.session.get(url)
        if len(response.history) > 0:
            # we've been redirected to the login page
            self.session.cookies.clear()
            self.login()
            response = self.session.get(url)
        return response

    def login(self):
        """Try logging in.

        If the login is successful, a session attribute is set on the object.
        If it fails, raises an InvalidLoginError.
        """
        # switch to english version if we're on the italian site
        default_lang_page = self.session.get(self.loginurl)
        lang_soup = BeautifulSoup(default_lang_page.text)
        lang_tag = lang_soup.find('a', attrs={'title': 'English'})
        if lang_tag:
            self.session.get('https://aunicalogin.polimi.it' +
                             lang_tag['href'])
        payload = "login=%s&password=%s" % (self.username, self.password) + \
                  '&evn_conferma%3Devento=Accedi'
        login_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:34.0)\
Gecko/20100101 Firefox/34.0',

            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': len(payload),
            'Accept': 'text/html,application/xhtml+xml,\
            application/xml;q=0.9,*/*;q=0.8'
        }
        login_response = self.session.post(
            'https://aunicalogin.polimi.it:443/aunicalogin/\
aunicalogin/controller/IdentificazioneUnica.do?\
&jaf_currentWFID=main',
            data=payload, headers=login_headers)
        login_soup = BeautifulSoup(login_response.text)
        try:
            parenttag = login_soup.find_all('table')[3]
            parenttag.find('td',
                           text='\n\t\t\t\t\t\n\t\t\t\t\t\t\n\t\t\t\t\
\t\tCode: 14 - Identificazione fallita\n\t\t\t\t\t\n\t\t\t\t')
        except IndexError:
            hidden_fields = BeautifulSoup(login_response.text).find_all(
                'input', attrs={'type': 'hidden'}
            )
            # The SAML response wants '+' replaced by %2B
            relay_state = hidden_fields[0].attrs['value']
            saml_response = hidden_fields[1].attrs['value'].replace('+',
                                                                    '%2B')
            final_request_data = "RelayState=%s&SAMLResponse=%s" % \
                                 (relay_state, saml_response)
            final_headers = {
                'Cookie': "GUEST_LANGUAGE_ID=en_GB; \
COOKIE_SUPPORT=true; polij_device_category=PERSONAL_COMPUTER",
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': len(final_request_data),
            }
            self.session.post(
                'https://beep.metid.polimi.it/Shibboleth.sso/SAML2/POST',
                data=final_request_data,
                headers=final_headers)
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            for key in cookies:
                if key.startswith('_shibsession'):
                    shibsessionstr = "%s=%s" % (key, cookies[key])
            main_headers = {
                'Cookie': "GUEST_LANGUAGE_ID=en_GB; \
COOKIE_SUPPORT=true; polij_device_category=PERSONAL_COMPUTER; %s" % (
                    shibsessionstr)
            }
            mainpage = self.session.get(
                'https://beep.metid.polimi.it/polimi/login',
                headers=main_headers)
            self.courses_url = mainpage.url
            self.logged = True
        else:
            raise InvalidLoginError
            self.logged = False

    def update_available_courses(self):
        coursespage = self.get_resource(self.courses_url)
        courses_soup = BeautifulSoup(coursespage.text)
        raw_courses = courses_soup.find_all('tr',
                                            attrs={'class': 'results-row'})
        raw_courses.pop(0)
        for course in raw_courses:
            firstlink = course.td.a['href']
            name = course.td.a.strong.text
            # If we follow firstlink, we will get to the course web page
            # after two redirects. We call get_resource(), which
            # will follow firstlink, notice the 302 redirects,
            # therefore clear cookies and get a valid session; only
            # at the end, it will return the response.
            # We do this because at this point the session that was valid
            # at the beginning of the function call may be expired by now.
            link = self.get_resource(firstlink).url
            # prima controllare se esistono già, in tal caso solo aggiornare
            # il link
            # available_courses definirci __contains__
            self.available_courses.append({'name': name, 'link': link})

