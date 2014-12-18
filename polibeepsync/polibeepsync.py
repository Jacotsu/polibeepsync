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
        for elem in args:
            if not self.__contains__(elem):
                self.elements.append(elem)

    def remove(self, arg):
        if arg in self.elements:
            self.elements.remove(arg)
            print('removing {}'.format(arg))
            print('now elements are {}'.format(self.elements))

    def __len__(self):
        return len(self.elements)


class Courses(GenericSet):
    def __hash__(self):
        unordered_name = self._elements_names()
        return hash("".join(sorted(unordered_name)))

    def __repr__(self):
        before = "Courses collection:\n"
        texts = [elem.name for elem in self.elements]
        joined_texts = "\n".join(texts)
        return before + joined_texts


class Course(GenericSet):
    def __init__(self, name, documents_url, sync=True):
        super(Course, self).__init__()
        self.name = name
        self.documents_url = documents_url
        self.sync = sync

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return 'Course {}'.format(self.name)

    def __contains__(self, key):
        if key.name in self._elements_names():
            return True
        else:
            return False

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False

    @property
    def files(self):
        return self.elements

    @files.setter
    def files(self, value):
        if isinstance(value, Courses):
            self.elements = value
        else:
            raise TypeError

    @files.deleter
    def files(self):
        self.elements = []


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
        self.available_courses = Courses()

    def visit(self):
        """Visit the login webpage to test for working connection."""
        try:
            self.session.get('https://beep.metid.polimi.it')
        except (requests.ConnectionError, requests.Timeout):
            # re-raise the exception for the moment
            raise

    def logout(self):
        """Logout.

        It clears session cookies and sets :attr:`logged` to ``False``."""
        self.session.cookies.clear()
        self.logged = False

    def get_page(self, url):
        """Use this method to get a webpage.

        It will check if the session is expired, and relogin if necessary.

        Returns:
            response (:class:`requests.Response`): a :class:`requests.Response`
            instance
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

        It will check if the session is expired, and re-login if necessary.
        The file bytes can be accessed with the :attr:`content` attribute

        >>> user = User('username', 'password')
        >>> response = user.get_file('url_to_file')
        >>> with open('outfile','wb') as f:
        ...    f.write(response.content)

        Returns:
            response (requests.Response): a :class:`requests.Response` object
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

        If the login is successful, :attr:`logged` is set to ``True``.
        If it fails, :attr:`logged` is set to ``False`` and raises an
        :class:`InvalidLoginError`.

        Raises:
            InvalidLoginError: when the login fails
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

    def get_online_courses(self):
        """Return the courses available online.

        Returns:
            online_courses (:class:`Courses`): a :class:`Courses` container of
            all courses available online."""
        coursespage = self.get_page(self.courses_url)
        courses_soup = BeautifulSoup(coursespage.text)
        raw_courses = courses_soup.find_all('tr',
                                            attrs={'class': 'results-row'})
        # the first tag is not a course
        raw_courses.pop(0)
        online_courses = Courses()
        # we iterate over the tags
        for course in raw_courses:
            firstlink = course.td.a['href']
            name = course.td.a.strong.text
            # the real link is found after a redirect
            link = self.get_page(firstlink).url
            link = link.rstrip('attivita-online-e-avvisi')
            link = link + 'documenti-e-media'
            # we ignore BeeP channel
            if str(name) != "BeeP channel":
                course = Course(name, link)
                online_courses.append(course)
        return online_courses

    def sync_available_courses(self, master_courses):
        """Sync :attr:`available_courses` to :attr:`master_courses`.

        This function will compare the courses in master_courses; if some of
        them are not present in the available_courses instance attribute, they
        will be added to available_courses; if any course is present in
        self.available_courses but not in master_courses, it will be
        removed from self.available_courses.

        A typical usage would be the following

        >>> user = User('fakeid', 'fakepwd')
        >>> user.login()
        >>> online = user.get_online_courses()
        >>> user.sync_available_courses(online)

        Args:
            master_courses (Courses): The updated :class:`Courses` instance
        """
        # New courses should be added.
        # the "if not in" check is not really needed, since the append
        # function doesn't allow duplicates.
        for elem in master_courses:
            if elem not in self.available_courses:
                print('adding')
                self.available_courses.append(elem)
        # now do the opposite: if a course has been deleted,
        # do the same with the local copy
        for elem in self.available_courses:
            if elem not in master_courses:
                print('removing')
                self.available_courses.remove(elem)
