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
from datetime import datetime, timedelta, tzinfo
import requests
import os
import logging


class InvalidLoginError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


class GMT1(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=1) + self.dst(dt)

    def dst(self, dt):
        # DST starts last Sunday in March
        d = datetime(dt.year, 4, 1)   # ends last Sunday in October
        self.dston = d - timedelta(days=d.weekday() + 1)
        d = datetime(dt.year, 11, 1)
        self.dstoff = d - timedelta(days=d.weekday() + 1)
        if self.dston <= dt.replace(tzinfo=None) < self.dstoff:
            return timedelta(hours=1)
        else:
            return timedelta(0)

    def tzname(self, dt):
        return "GMT +1"


class GenericSet(object):
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
    def __init__(self, name, documents_url, sync=False):
        logging.debug('Creating course with name={},'
                      ' documents_url={}, sync={}'
                      .format(name, documents_url, sync))
        super(Course, self).__init__()
        self.name = name
        self.documents_url = documents_url
        self.sync = sync
        self.documents = ""
        self.save_folder_name = ""

    def simplify_name(self, name):
        upper = name
        try:
            rmleftbrackets = "".join(name.split('[')[1:-1])
            upper = rmleftbrackets.split("]")[1].lstrip(' - ').rstrip(" ")
            #upper = name.split('[')[1].split(']')[1].rstrip(" ").lstrip(' - ')
        except Exception as err:
            logging.error('Failed to simplify course name {}'.format(name))
            logging.error(str(err))
        return upper.title()

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


class CourseFile(object):
    def __init__(self, name, url, last_online_edit_time):
        gmt1 = GMT1()
        self.name = name
        self.url = url
        self.last_online_edit_time = last_online_edit_time
        self.local_creation_time = datetime(1990, 1, 1, 1, 1,
                                     tzinfo=gmt1)

    def __hash__(self):
        return hash(self.name)


class Folder(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.files = []
        self.folders = []


class User(object):
    loginurl = 'https://beep.metid.polimi.it/polimi/login'
    gmt1 = GMT1()

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.logged = False
        self.subscribed_courses = []
        self.courses_url = ""
        self.available_courses = Courses()
        self.root_save_folder = ""


    def logout(self):
        """Logout.

        It re-creates a session and sets :attr:`logged` to ``False``."""
        del(self.session)
        self.session = requests.Session()
        #self.session.cookies.clear()
        self.logged = False

    def get_page(self, url):
        """Use this method to get a webpage.

        It will check if the session is expired, and relogin if necessary.

        Returns:
            response (:class:`requests.Response`): a :class:`requests.Response`
            instance
        """
        response = self.session.get(url, timeout=5, verify=True)
        soup = BeautifulSoup(response.text)
        login_tag = soup.find('input', attrs={'id': 'login'})
        if login_tag is not None:
            logging.info("The session has expired. Logging-in again...")
            self.logout()
            self.login()
            response = self.session.get(url, timeout=5, verify=True)
        return response

    def get_file(self, url):
        """Use this method to get a file.

        It will check if the session is expired, and re-login if necessary.
        The file bytes can be accessed with the :attr:`content` attribute

        >>> user = User('username', 'password')
        >>> response = user.get_file('url_to_file', timeout=5, verify=True)
        >>> with open('outfile','wb') as f:
        ...    f.write(response.content)

        Returns:
            response (requests.Response): a :class:`requests.Response` object
        """
        response = self.session.get(url, timeout=5, verify=True)
        if len(response.history) > 0:
            # it means that we've been redirected to the login page
            logging.info("The session has expired. Logging-in again...")
            self.logout()
            self.login()
            response = self.session.get(url, timeout=5, verify=True)
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
        default_lang_page = self.session.get(self.loginurl, timeout=5, verify=True)
        lang_soup = BeautifulSoup(default_lang_page.text)
        lang_tag = lang_soup.find('a', attrs={'title': 'English'})
        if lang_tag:
            self.session.get('https://aunicalogin.polimi.it' +
                             lang_tag['href'], timeout=5, verify=True)
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
                headers=main_headers, timeout=5, verify=True)
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
            weird_parameters = ['_20_folderId=0',
                                '_20_displayStyle=list',
                                '_20_viewEntries=0',
                                '_20_viewFolders=0',
                                '_20_entryEnd=500',
                                '_20_entryStart=0',
                                '_20_folderEnd=500',
                                '_20_folderStart=0',
                                '_20_viewEntriesPage=1',
                                'p_p_id=20',
                                'p_p_lifecycle=0'
                                ]
            link = link + 'documenti-e-media?' + "&".join(weird_parameters)
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
                self.available_courses.append(elem)
        # now do the opposite: if a course has been deleted,
        # do the same with the local copy
        for elem in self.available_courses:
            if elem not in master_courses:
                self.available_courses.remove(elem)

    def update_course_files(self, course):
        rootfolder = self.find_files_and_folders(course.documents_url,
                                                 'rootfolder')
        course.documents = rootfolder

    def find_files_and_folders(self, link, thisfoldername):
        response = self.get_page(link)
        soup = BeautifulSoup(response.text)
        tags = soup.find_all('span', attrs={'class': 'taglib-text'})
        tags = [elem for elem in tags if elem.text != ""]

        tags.pop(0)
        tags.pop(0)

        rawdates = [elem.parent.parent.parent.next_sibling.next_sibling.
                    next_sibling.next_sibling.next_sibling.next_sibling
                    for elem in tags]
        last_column = [elem.next_sibling.next_sibling.next_sibling.
                       next_sibling for elem in rawdates]

        folder = Folder(thisfoldername, response.url)

        for i, v in enumerate(tags):
            name = v.text
            rawdate = rawdates[i]
            day = int(rawdate.text.split(' ')[1].split('/')[0])
            month = int(rawdate.text.split(' ')[1].split('/')[1])
            year = int(rawdate.text.split(' ')[1].split('/')[2])
            hour = int(rawdate.text.split(' ')[2].split('.')[0])
            minute = int(rawdate.text.split(' ')[2].split('.')[1])
            complete_date = datetime(year, month, day, hour, minute,
                                     tzinfo=self.gmt1)
            download_link = last_column[i].find_all('a')
            elem = download_link[2]
            if elem.text.startswith('  Download ('):
                link = elem['href']
                complete_file = CourseFile(name, link, complete_date)
                folder.files.append(complete_file)

            else:
                link = v.parent['href']
                subfolder = self.find_files_and_folders(link, name)
                folder.folders.append(subfolder)
        return folder


    def save_files(self, masterfolder, out_rootfolder):
        for coursefile in masterfolder.files:
            fname = os.path.join(out_rootfolder, coursefile.name)
            basenames = [os.path.splitext(os.path.basename(f))[0]
                         for f in os.listdir(out_rootfolder)
                         if os.path.isfile(os.path.join(out_rootfolder, f))]

            if os.path.exists(fname) and\
                coursefile.local_creation_time < \
                coursefile.last_online_edit_time:
                result = self.get_file(coursefile.url)
                complete_basename = result.headers['Content-Disposition']\
                .split("; ")[1].split("=")[1].strip('"')
                complete_name = os.path.join(out_rootfolder, complete_basename)
                with open(complete_name, 'wb') as f:
                    f.write(result.content)
                coursefile.local_creation_time = datetime.now(self.gmt1)
            elif fname in basenames and\
                coursefile.local_creation_time < \
                coursefile.last_online_edit_time:
                result = self.get_file(coursefile.url)
                complete_basename = result.headers['Content-Disposition']\
                .split("; ")[1].split("=")[1].strip('"')
                complete_name = os.path.join(out_rootfolder, complete_basename)
                with open(complete_name, 'wb') as f:
                    f.write(result.content)
                coursefile.local_creation_time = datetime.now(self.gmt1)
            elif not (os.path.exists(fname) and fname in basenames):
                result = self.get_file(coursefile.url)
                complete_basename = result.headers['Content-Disposition']\
                .split("; ")[1].split("=")[1].strip('"')
                complete_name = os.path.join(out_rootfolder, complete_basename)
                with open(complete_name, 'wb') as f:
                    f.write(result.content)
                coursefile.local_creation_time = datetime.now(self.gmt1)
        if masterfolder.name == "rootfolder":
            for folder in masterfolder.folders:
                path = os.path.join(out_rootfolder, folder.name)
                os.makedirs(path, exist_ok=True)
                self.save_files(folder, path)
        else:
            for folder in masterfolder.folders:
                path = os.path.join(out_rootfolder, folder.name)
                os.makedirs(path, exist_ok=True)
                self.save_files(folder, path)