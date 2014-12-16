from bs4 import BeautifulSoup
import requests


class InvalidLoginError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


class GenericSet:
    def __init__(self):
        self.elements = []

    def _elements_names(self):
        return [elem.name for elem in self.elements]

    def __eq__(self, other):
        this_elements = set(self.elements)
        other_elements = set(other.elements)
        if this_elements == other_elements:
            return True
        else:
            return False

    def __contains__(self, key):
        if key.name in self._elements_names():
            return True
        else:
            return False

    def __getitem__(self, key):
        if key in self._elements_names():
            for elem in self.elements:
                if elem.name == key:
                    return elem
        else:
            raise KeyError

    def __iter__(self):
        return iter(self.elements)

    def __sub__(self, other):
        return list(set(self.elements) - set(other.elements))

    def append(self, *args):
        print('now self.elements are {}'.format(self.elements))
        for elem in args:
            print('getting {}'.format(elem))
            if not self.__contains__(elem):
                self.elements.append(elem)


class Courses(GenericSet):
    def __hash__(self):
        unordered_name = self._elements_names()
        return hash("".join(sorted(unordered_name)))


class Course(GenericSet):
    def __init__(self, name, documents_url, sync=True):
        self.name = name
        self.documents_url = documents_url
        self.sync = sync
        self.elements = []

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return 'Course {}'.format(self.name)


class CourseFile:
    def __init__(self, name, last_online_edit_time):
        self.name = name
        self.last_online_edit_time = last_online_edit_time

    def __hash__(self):
        return hash(self.name)


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

    def logout(self):
        self.session.cookies.clear()
        self.logged = False

    def get_page(self, url):
        """Use this method to get a webpage.

        It will check if the session is expired, and relogin if necessary.

        Returns: a requests.get(url) response
        """
        response = self.session.get(url)
        soup = BeautifulSoup(response.text)
        login_tag = soup.find('input', attrs={'id': 'login'})
        if login_tag is not None:
            self.logout()
            self.login()
            response = self.session.get(url)
        return response

    def get_file(self, url):
        """Use this method to get a file.

        It will check if the session is expired, and relogin if necessary.

        Returns: a requests.get(url) response
        """
        response = self.session.get(url)
        if len(response.history) > 0:
            # it means that we've been redirected to the login page
            self.logout()
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
            self.logged = False
            raise InvalidLoginError

    def update_available_courses(self):
        coursespage = self.get_page(self.courses_url)
        courses_soup = BeautifulSoup(coursespage.text)
        raw_courses = courses_soup.find_all('tr',
                                            attrs={'class': 'results-row'})
        raw_courses.pop(0)
        for course in raw_courses:
            firstlink = course.td.a['href']
            name = course.td.a.strong.text
            link = self.get_page(firstlink).url
            # prima controllare se esistono già, in tal caso solo aggiornare
            # il link
            # available_courses definirci __contains__
            self.available_courses.append({'name': name, 'link': link})

    def update_course_files_list(self, course_name):
        names = [elem['name'] for elem in self.subscribed_courses]
        if course_name in names:
            url = [elem['link'] for elem in self.subscribed_courses
                   if elem['name'] == course_name][0]
            files_page = self.get_page(url)
            files_soup = BeautifulSoup(files_page.text)
            # here we should check if the session is valid
            links = []
            for tag in files_soup.find_all('a'):
                if tag.text.startswith('  Download ('):
                    links.append(tag['href'])
            rawnames = files_soup.find_all('span',
                                           attrs={'class': 'taglib-text'})
            rawnames.pop(0)
            rawnames.pop(0)
            names = [elem.text for elem in rawnames if elem.text != ""]
            files = [{'link': v, 'name': names[i]} for i, v in
                     enumerate(links)]
        else:
            raise CourseNotFoundError
