__copyright__ = """Copyright 2020 Davide Olianas (ubuntupk@gmail.com), Di
Campli Raffaele (dcdrj.pub@gmail.com)."""

__license__ = """This f is part of poliBeePsync.
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

from lxml import etree
from urllib.parse import urlparse, parse_qs, quote_plus, unquote
from datetime import datetime, timedelta, tzinfo
from dateutil.parser import parse
from functools import partial
import requests
from urllib.parse import urlsplit
from polibeepsync.utils import raw_date_to_datetime, debug_dump,\
    debug_dump_request_response
import os
import logging
import re
from PySide2.QtCore import QThread, QObject, Signal, QRunnable, QThreadPool,\
        Slot
from pyparsing import (Word, alphanums, alphas8bit, alphas, nums, Group,
                       OneOrMore, ParseException, ZeroOrMore, Suppress,
                       Optional, CaselessLiteral)
from signalslot import Signal as sSignal
from polibeepsync.std_dicts import std_file_dict


commonlogger = logging.getLogger("polibeepsync.common")


# --- Custom Exceptions --- #

class InvalidLoginError(Exception):
    """Exception raised when user code, password or both are wrong."""
    def __init__(self):
        pass


# --- Custom Threads --- #
class QThreadPoolContexted(QThreadPool):
    def __init__(self, max_threads=4, wait=True, parent=None):
        super(QThreadPoolContexted, self).__init__(parent)
        self.wait = wait
        self.setMaxThreadCount(max_threads)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.wait:
            self.waitForDone()


class RefreshCoursesThread(QThread):
    def __init__(self, user, parent=None):
        super(RefreshCoursesThread, self).__init__(parent)
        self.dumpuser = MySignal()
        self.newcourses = CoursesSignal()
        self.removable = CoursesSignal()
        self.user = user

    def run(self):
        most_recent = self.user.get_online_courses()
        for course in self.user.available_courses:
            if course.manually_added:
                most_recent.append(course)
        last = self.user.available_courses
        new = most_recent - last
        removable = last - most_recent
        if removable:
            commonlogger.info('The following courses have'
                              ' been removed because they '
                              'aren\'t available online: {}'
                              .format(removable))
        for course in new:
            course.save_folder_name = course.simplify_name(course.name)
            commonlogger.info('A new course '
                              'was found: {}'.format(course))
        if not new:
            commonlogger.info('No new courses found.')
        self.user.sync_available_courses(most_recent)
        self.newcourses.sig.emit(new)
        self.removable.sig.emit(removable)
        self.dumpuser.sig.emit('')


class LoginThread(QThread):
    def __init__(self, user, parent=None):
        super(LoginThread, self).__init__(parent)
        self.signal_ok = MySignal()
        self.signal_error = MySignal()
        self.user = user

    def run(self):
        try:
            commonlogger.info('Logging in.')
            self.user.logout()
            self.user.login()
            if self.user.logged is True:
                commonlogger.info('Successful login.')
                self.signal_ok.sig.emit('Successful login')
        except (InvalidLoginError, requests.exceptions.MissingSchema):
            commonlogger.error('Login failed.', exc_info=True)
            self.signal_error.sig.emit('Login failed')
        except requests.exceptions.SSLError as ssl_error:
            commonlogger.error(f'Connection SSL error: {ssl_error}',
                               exc_info=True)
            self.signal_error.sig.emit('Connection SSL error')
        except requests.ConnectionError as conn_err:
            commonlogger.error(f'Connection error: {conn_err}',
                               exc_info=True)
            self.signal_error.sig.emit('Connection error')
        except requests.Timeout:
            commonlogger.error('Connection timeout error.', exc_info=True)
            self.signal_error.sig.emit('Connection timeout error')


class DownloadThread(QThread):
    def __init__(self, user, topdir, parent=None):
        super(DownloadThread, self).__init__(parent)
        self.user = user
        self.topdir = topdir
        self.start_download_s = MySignal()
        self.start_download_s.sig.connect(self._work)
        if parent:
            self.status_signal = MySignal()
            self.status_signal.sig.connect(parent.update_status_bar)
        self.dumpuser = MySignal()
        self.download_signal = sSignal(args=['course'])
        self.initial_sizes = sSignal(args=['course'])
        self.date_signal = sSignal(args=['data'])

    def run(self):
        self.start_download_s.sig.emit('')

    def notify_finished(self):
        self.dumpuser.sig.emit('')
        commonlogger.info('Syncing finished')
        if self.status_signal:
            self.status_signal.sig.emit('Syncing finished')

    def _threaded_syncer(self):
        with QThreadPoolContexted(wait=True) as TExec:
            for course in self.user.available_courses:
                if course.sync:
                    commonlogger.debug(f'Syncing {course}')
                    TExec.start(func_runnable(self, self.sync_course, course),
                                QThread.LowPriority)
        self.notify_finished()

    @Slot()
    def _work(self):
        # We disable multithreading while debugging
        if commonlogger.getEffectiveLevel() == logging.DEBUG:
            for course in self.user.available_courses:
                if course.sync:
                    commonlogger.debug(f'Syncing {course}')
                    self.sync_course(course)
            self.notify_finished()
        else:
            with QThreadPoolContexted(wait=False, parent=self) as TExec:
                TExec.start(func_runnable(self, self._threaded_syncer),
                            QThread.LowPriority)

    def sync_course(self, course):
        try:
            subdir = course.save_folder_name
            outdir = os.path.join(self.topdir, subdir)
            os.makedirs(outdir, exist_ok=True)
            self.user.update_course_files(course)
            savedhere = os.path.join(self.topdir,
                                     course.save_folder_name)
            needsync = need_syncing(course.documents,
                                    savedhere)

            syncsize = total_size(needsync)
            commonlogger.info(f'****SYNCSIZE: {sizeof_fmt(syncsize)}')
            alreadysynced = course.size - syncsize
            commonlogger.info(f'****ALREADYSYNCED {sizeof_fmt(alreadysynced)}')
            course.downloaded_size = alreadysynced
            commonlogger.info('****DOWNLOADED SIZE setting to '
                              f'{sizeof_fmt(course.downloaded_size)}')
            self.initial_sizes.emit(course=course)
            self.user.save_files(course, needsync, self.download_signal)
            # adesso ogni f di syncthese ha la data di download
            # aggiornata, ma deve essere scritto su f
            commonlogger.info(f'Synced files for {course.name}')
        except InvalidLoginError:
            self.user.logout()
            commonlogger.info('Login failed.', exc_info=True)
        except requests.ConnectionError:
            self.user.logout()
            commonlogger.error('Connection error.', exc_info=True)
        except requests.Timeout:
            self.user.logout()
            commonlogger.error("Timeout error.", exc_info=True)


# --- "Core" classes here --- #
class GMT1(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=1) + self.dst(dt)

    def dst(self, dt):
        # DST starts last Sunday in March
        d = datetime(dt.year, 4, 1)  # ends last Sunday in October
        self.dston = d - timedelta(days=d.weekday() + 1)
        d = datetime(dt.year, 11, 1)
        self.dstoff = d - timedelta(days=d.weekday() + 1)
        if self.dston <= dt.replace(tzinfo=None) < self.dstoff:
            return timedelta(hours=1)
        else:
            return timedelta(0)

    def tzname(self, dt):
        return "GMT +1"


class GenericSet():
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
    def __init__(self, course_dict, sync=False):
        commonlogger.debug(f'Creating course with name={course_dict["name"]},'
                           f' documents_url={course_dict["friendlyUrl"]}, '
                           f'sync={sync}')
        super(Course, self).__init__()
        self._course_dict = course_dict
        self.documents = Folder({'name': 'root'})

    @property
    def manually_added(self):
        return self._course_dict['ManuallyAdded']

    @manually_added.setter
    def manually_added(self, val: bool):
        self._course_dict['ManuallyAdded'] = val

    @property
    def save_folder_name(self):
        return self._course_dict['saveFolderName']

    @save_folder_name.setter
    def save_folder_name(self, save: str):
        self._course_dict['saveFolderName'] = save

    @property
    def sync(self):
        return self._course_dict['sync']

    @sync.setter
    def sync(self, do_sync: bool):
        self._course_dict['sync'] = do_sync

    @property
    def size(self):
        # in bytes
        return self._course_dict['size']

    @size.setter
    def size(self, new_size):
        # in bytes
        self._course_dict['size'] = new_size

    @property
    def downloaded_size(self):
        # in bytes
        return self._course_dict['downloadedSize']

    @downloaded_size.setter
    def downloaded_size(self, new_size: int):
        # in bytes
        self._course_dict['downloadedSize'] = new_size

    @property
    def documents_url(self):
        return 'https://beep.metid.polimi.it/web/' \
            f'{self._course_dict["friendlyUrl"]}/documenti-e-media'

    @property
    def name(self):
        return self._course_dict['name']

    def simplify_name(self, name):
        simple = name
        year = Group(ZeroOrMore("[" + Word(nums, exact=4) +
                                "-" + Word(nums, exact=2) + "]"))
        iol = Group(ZeroOrMore(CaselessLiteral("[IOL]")))
        iol_literal = Group(ZeroOrMore("-" + Word(alphas) + "-"))
        dash_with_student_code = Group(ZeroOrMore("-" + Word(nums)))
        personal_names = OneOrMore(Word(alphas + ',.;:/'))
        course_name = Group(
            OneOrMore(
                Word(alphanums + alphas8bit + ',.;:/|\'"')
            )
        ).setResultsName('course_name')
        course_extra_specs = Group(
            ZeroOrMore('(' + ZeroOrMore(Word(alphanums + ',.:;/\'')) + ')')
        )
        # Some courses specifies the professor name like this
        # [2019/20] COURSE MEMEOLOGY - George Miller
        # Most of the courses like this
        # [2019/20] COURSE MEMEOLOGY [ George Miller ]
        prof_name = Group(Optional(
            Suppress('[') + personal_names + Suppress(']') ^
            Suppress('-') + personal_names)) \
            .setResultsName('prof_name')

        try:
            grammar = iol.suppress() + year.suppress() + \
                    iol_literal.suppress() + \
                    dash_with_student_code.suppress() + \
                    Suppress(ZeroOrMore('-')) + course_name +\
                    course_extra_specs.suppress() + prof_name
            parsed_name_tokens = grammar.parseString(name)

            simple = f"{' '.join(parsed_name_tokens['course_name'])} "
            # Append professor names only if present
            if parsed_name_tokens['prof_name']:
                # Replace `/` with `;`
                safe_names = ' '.join(parsed_name_tokens['prof_name'])\
                    .replace(' /', ';')
                simple += f"[{safe_names}]"

        except ParseException:
            commonlogger.error(f'Failed to simplify course name {name}',
                               exc_info=True)
        return simple.title().strip()

    def __hash__(self):
        return hash(f"{self._course_dict['classPK']}"
                    f"{self._course_dict['name']}")

    def __repr__(self):
        return 'Course {}'.format(self._course_dict['name'])

    def __contains__(self, key):
        if key.name in self._elements_names():
            return True
        else:
            return False

    def __eq__(self, other):
        if int(self._course_dict['classPK']) ==\
           int(other._course_dict['classPK']):
            return True
        else:
            return False


class CourseFile():
    def __init__(self, file_dict):
        self.gmt1 = GMT1()
        self._file_dict = {**std_file_dict, **file_dict}

    @property
    def sync(self):
        return self._file_dict['sync']

    @sync.setter
    def sync(self, val: bool):
        self._file_dict['sync'] = val

    @property
    def local_creation_time(self):
        if self._file_dict["localCreationTime"]:
            return datetime.fromtimestamp(
                self._file_dict["localCreationTime"]/1000, self.gmt1
            )
        else:
            return None

    @local_creation_time.setter
    def local_creation_time(self, time: 'datetime'):
        self._file_dict['localCreationTime'] = time.timestamp()*1000

    @property
    def extension(self):
        return self._file_dict['extension']

    @property
    def version(self):
        return self._file_dict['version']

    @property
    def id(self):
        return self._file_dict['fileEntryId']

    @property
    def name(self):
        return self._file_dict["title"]

    @property
    def url(self):
        return 'https://beep.metid.polimi.it/documents/' \
                f'{self._file_dict["groupId"]}/{self._file_dict["uuid"]}'

    @property
    def last_online_edit_time(self):
        # Beep's timestamp is an epoch with millisecond resolution
        return datetime.fromtimestamp(self._file_dict["modifiedDate"]/1000,
                                      self.gmt1)

    @property
    def downloaded_size(self):
        # in bytes
        return self._file_dict["downloadedSize"]

    @downloaded_size.setter
    def downloaded_size(self, val):
        self._file_dict["downloadedSize"] = val

    @property
    def size(self):
        # in bytes
        return self._file_dict["size"]

    @size.setter
    def size(self, val):
        self._file_dict["size"] = val

    def __hash__(self):
        return hash(self._file_dict["title"])

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if os.path.splitext(self.name)[0] == os.path.splitext(other.name)[0]:
            return True
        else:
            return False


class Folder():
    def __init__(self, folder_dict):
        self._folder_dict = folder_dict
        if 'folderId' not in folder_dict:
            # Folder not existant on BeeP
            self._folder_dict['folderId'] = -1
        self.files = []
        self.folders = []

    @property
    def name(self):
        return self._folder_dict['name']

    @property
    def id(self):
        return self._folder_dict['folderId']

    @property
    def group_id(self):
        return self._folder_dict['groupId']

    def __repr__(self):
        return f'{self.name} folder'

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False


def total_size(listoffiles):
    total = 0
    for f, path in listoffiles:
        commonlogger.debug(f'Size of {f.name}: {f.size} bytes')
        total += f.size
    commonlogger.debug('Total size: {}'.format(total))
    return total


def folder_total_size(parentfolder, sizes):
    for f in parentfolder.files:
        commonlogger.debug(f'il {f.name}, pesa {f.size}')
        sizes.append(f.size)
    for folder in parentfolder.folders:
        commonlogger.debug('sto controllando la dimensione della sottocartella'
                           f' {folder.name}')
        folder_total_size(folder, sizes)
        # viene passata sempre la stessa dimensione della cartella più in alto
    return sizes

def synclocalwithonline(local, online):
    """Modifies local in order to reflect changes from online"""
    for f in online.files:
        if f not in local.files:
            local.files.append(f)
        else:
            ind = local.files.index(f)
            local.files[ind]._file_dict["modifiedDate"] = \
                f._file_dict["modifiedDate"]
    oldfiles = [f for f in local.files if f not in online.files]
    cleanfiles = [f for f in local.files if f not in oldfiles]
    local.files = cleanfiles
    old = [f for f in local.folders if f not in online.folders]
    clean = [f for f in local.folders if f not in old]
    local.folders = clean
    for folder in online.folders:
        if folder not in local.folders:
            local.folders.append(folder)
    for folder in online.folders:
        ind = local.folders.index(folder)
        synclocalwithonline(local.folders[ind], folder)
    return local


def need_syncing(folder, parent_folder):
    """Return a flat list with files to download

    Each element is a tuple like this
    (f, path)

    filename is the f as scraped from the web (its name can be with or
    without the extension)
    path is the absolute path of the folder in which the f should be
    downloaded
    """
    syncthese = []
    commonlogger.debug(f'calling with folder={folder.name}, parent '
                       f'folder={parent_folder}')
    # basenames contains the names of files without extension (this is used
    # later because the website sometimes doesn't show the f extension)
    basenames = []
    if os.path.exists(parent_folder):
        basenames = [os.path.splitext(os.path.basename(f))[0]
                     for f in os.listdir(parent_folder)
                     if os.path.isfile(os.path.join(parent_folder, f))]
    commonlogger.debug(basenames)
    for f in folder.files:
        simplename = os.path.join(parent_folder, f.name)
        commonlogger.debug(f)
        if f.local_creation_time is None:
            commonlogger.debug(f'No local creation time: {f}')
            syncthese.append((f, parent_folder))
        elif f.local_creation_time < f.last_online_edit_time:
            commonlogger.info(f'Outdated local file: {f} '
                              f'{f.local_creation_time} '
                              f'{f.last_online_edit_time}')
            syncthese.append((f, parent_folder))
        elif not os.path.exists(simplename) and f.name not in basenames:
            # Manages extensionless files
            syncthese.append((f, parent_folder))
    for f in folder.folders:
        new_parent = os.path.join(parent_folder, f.name)
        syncthese += need_syncing(f, new_parent)
    return syncthese


class User():
    loginurl = 'https://beep.metid.polimi.it/polimi/login'
    user_courses_url = 'https://beep.metid.polimi.it/api/secure/jsonws/'\
        'group/get-user-sites'
    get_folders_url = 'https://beep.metid.polimi.it/api/secure/jsonws/dlapp/'\
        'get-folders'
    get_files_url = 'https://beep.metid.polimi.it/api/secure/jsonws/dlapp/'\
        'get-file-entries'
    gmt1 = GMT1()

    def __init__(self, username, password,
                 use_json_endpoint=False, default_timeout=10):
        self.username = username
        self.password = password
        self._use_json_endpoint = use_json_endpoint
        self.max_redirects = 10
        self.session = requests.Session()
        self.default_timeout = default_timeout
        self.logged = False
        self.courses_url = ""
        self.available_courses = Courses()
        self.root_save_folder = ""
        self.chunk_download = sSignal(args=['course'])
        # self.chunk_download.connect(self.print_chunk)

        # We manually load this certficate because sometimes the beep's one
        # is malformed and it's not accepted by openssl
        # ENABLE ONLY IF MALFORMED CERTS ARE SERVED
        # self.session.verify = f'{os.path.dirname(__file__)}/beep.pem'
        self.session.max_redirects = self.max_redirects
        cookie_obj = requests.cookies.create_cookie(
            domain='beep.metid.polimi.it',
            name='GUEST_LANGUAGE_ID',
            value='en_GB'
        )
        self.session.cookies.set_cookie(cookie_obj)

    def logout(self):
        """Logout.

        It re-creates a session and sets :attr:`logged` to ``False``."""
        del self.session
        self.session = requests.Session()
        self.session.max_redirects = self.max_redirects
        cookie_obj = requests.cookies.create_cookie(
            domain='beep.metid.polimi.it',
            name='GUEST_LANGUAGE_ID',
            value='en_GB'
        )
        self.session.cookies.set_cookie(cookie_obj)

        # ENABLE ONLY IF MALFORMED CERTS ARE SERVED
        #self.session.verify = f'{os.path.dirname(__file__)}/beep.pem'
        self.logged = False

    def get_headers(self, url, params=None):
        """Use this method to get a webpage headers.

        It will check if the session is expired, and relogin if necessary.

        Returns:
            response (:class:`requests.Response`): a :class:`requests.Response`
            instance
        """
        headers = {'Accept-Encoding': 'identity'}
        response = self.session.head(
            url, params=params, headers=headers,
            timeout=self.default_timeout)
        response_tree = etree.HTML(response.text)
        if response_tree and (response.status_code == 401 or\
           response_tree.xpath('//input[contains(@id, "login")]')):
            commonlogger.info('The session has expired. Logging-in again...')
            self.login()
            response = self.session.head(
                url,
                params=params,
                headers=headers,
                timeout=self.default_timeout
            )
        response.raise_for_status()
        return response


    def get_page(self, url, params=None):
        """Use this method to get a webpage.

        It will check if the session is expired, and relogin if necessary.

        Returns:
            response (:class:`requests.Response`): a :class:`requests.Response`
            instance
        """
        response = self.session.get(url, params=params,
                                    timeout=self.default_timeout)
        response_tree = etree.HTML(response.text)
        if response.status_code == 401 or\
           response_tree.xpath('//input[contains(@id, "login")]'):
            commonlogger.info('The session has expired. Logging-in again...')
            self.login()
            response = self.session.get(url, params=params,
                                        timeout=self.default_timeout)
        response.raise_for_status()
        return response

    def get_file(self, url, params=None):
        """Use this method to get a f.

        It will check if the session is expired, and re-login if necessary.
        The f bytes can be accessed with the :attr:`content` attribute

        >>> user = User('username', 'password')
        >>> response = user.get_file('url_to_file', timeout=10)
        >>> with open('outfile','wb') as f:
        ...    f.write(response.content)

        Returns:
            response (requests.Response): a :class:`requests.Response` object
        """
        response = self.session.get(url, params=params,
                                    timeout=self.default_timeout, stream=True)
        if len(response.history) > 0:
            # it means that we've been redirected to the login page
            commonlogger.info('The session has expired. Logging-in again...')
            self.logout()
            self.login()
            response = self.session.get(url, params=params,
                                        timeout=self.default_timeout,
                                        stream=True)
        return response

    def _login_first_step(self):
        default_lang_page = self.session.get(self.loginurl,
                                             timeout=self.default_timeout)
        response_tree = etree.HTML(default_lang_page.text)
        lang_tag = response_tree\
            .xpath('//a[contains(@title, "English")]/@href')

        if lang_tag:
            self.session.get('https://aunicalogin.polimi.it' +
                             lang_tag[0], timeout=self.default_timeout)
        payload = {'login': self.username,
                   'password': self.password,
                   'evn_conferma': ''
                   }
        login_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:34.0)'
                          'Gecko/20100101 Firefox/34.0',
        }
        login_response = self.session\
            .post('https://aunicalogin.polimi.it:443/aunicalogin/aunicalogin'
                  '/controller/IdentificazioneUnica.do?&jaf_currentWFID=main',
                  data=payload, headers=login_headers,
                  timeout=self.default_timeout)
        if re.search(
            'Identificazione fallita|Identification error',
            login_response.text
        ):
            raise InvalidLoginError
        return login_response

    def _do_shibboleth(self, first_response):
        first_response_tree = etree.HTML(first_response.text)
        hidden_inputs = first_response_tree.xpath(
            '//input[contains(@type, "hidden")]/@value'
        )
        relay_state = hidden_inputs[0]
        saml_response = quote_plus(hidden_inputs[1])
        final_request_data = f'RelayState={relay_state}&'\
            f'SAMLResponse={saml_response}'
        final_headers = {
            'Cookie': 'GUEST_LANGUAGE_ID=en_GB; COOKIE_SUPPORT=true; '
            'polij_device_category=PERSONAL_COMPUTER',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.session.post(
            'https://beep.metid.polimi.it/Shibboleth.sso/SAML2/POST',
            data=final_request_data,
            headers=final_headers,
            timeout=self.default_timeout)
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        for key in cookies:
            if key.startswith('_shibsession'):
                shibsessionstr = f"{key}={cookies[key]}"
        main_headers = {
            'Cookie': 'GUEST_LANGUAGE_ID=en_GB; COOKIE_SUPPORT=true; '
            f'polij_device_category=PERSONAL_COMPUTER; {shibsessionstr}'
        }
        mainpage = self.session.get(
            'https://beep.metid.polimi.it/polimi/login',
            headers=main_headers, timeout=self.default_timeout)
        return mainpage

    def login(self):
        """Try logging in.

        If the login is successful, :attr:`logged` is set to ``True``.
        If it fails, :attr:`logged` is set to ``False`` and raises an
        :class:`InvalidLoginError`.

        Raises:
            InvalidLoginError: when the login fails
        """
        login_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:34.0)'
                          'Gecko/20100101 Firefox/34.0',
        }
        # switch to english version if we're on the italian site
        first_response = self._login_first_step()
        response_tree = etree.HTML(first_response.text)
        try:
            form = response_tree.xpath('//form')[0]
        except:
            commonlogger.critical('Something went wront with the login method')
            debug_dump_request_response(first_response, commonlogger)
            if form:
                debug_dump(form.encode(), commonlogger)
            else:
                commonlogger.critical('No login form found')

        # If password change prompt is shown handle this special case
        if form.xpath('button[contains(@name, "evn_pwd_change")]'):
            commonlogger.warning('Your password is about to expire, '
                                 'change it ASAP')
            uri = urlsplit(first_response.url)
            url = f'{uri.scheme}://{uri.netloc}{form["action"]}'
            pwd_change_res = self.session.post(url,
                                               data={'evn_continua': ''},
                                               headers=login_headers,
                                               timeout=self.default_timeout)
            first_response = self._do_shibboleth(pwd_change_res)
            response_tree = etree.HTML(first_response.text)
            form = None
            try:
                form = response_tree.xpath('//form')[0]
            except:
                debug_dump_request_response(first_response, commonlogger)
                debug_dump(form.encode(), commonlogger)

        action_url = form.xpath('@action')[0]
        parsed_action_url = urlparse(action_url)._replace(
            scheme='https',
            netloc='aunicalogin.polimi.it'
        )
        url = parsed_action_url.geturl()

        commonlogger.debug(f'Login url {url}')

        payload = {}
        for x in form.xpath('//input'):
            try:
                payload[x.xpath('@name')[0]] = x.xpath('@value')[0]
            except IndexError:
                pass

        # 1m as minimum timeout time because if the password is about
        # to expire, beep's login response becomes significantly slower
        second_response = self.session.post(url,
                                            data=payload,
                                            headers=login_headers,
                                            timeout=60 + self.default_timeout)

        try:
            login_tree = etree.HTML(second_response.text)
            debug_dump_request_response(second_response, commonlogger)
            parenttag = login_tree.xpath('table')[3]
            if parenttag.xpath(
                    'td[contains(text(), "Identificazione fallita") or '
                    'contains(text(), "Identification error")]'):
                self.logged = False
                raise InvalidLoginError
        except IndexError:
            # Usercode and password are ok
            # continue with Shibboleth
            mainpage = self._do_shibboleth(first_response)
            self.courses_url = mainpage.url
            self.logged = True

    def get_online_courses(self):
        """Return the courses available online.

        Returns:
            online_courses (:class:`Courses`): a :class:`Courses` container of
            all courses available online."""
        commonlogger.info('Looking for new courses.')

        parsed_courses = []
        if self._use_json_endpoint:
            res = self.session.get(self.user_courses_url,
                                   timeout=self.default_timeout)
            parsed_courses = filter(lambda x: x["type"] == 2, res.json())
        else:
            coursespage = self.get_page(self.courses_url)
            parsed_courses = self._courses_scraper(coursespage.text)

        courses = Courses()
        for elem in parsed_courses:
            courses.append(Course(elem))
        return courses

    def scrape_course_main_page(self, friendly_url):
        url = f'https://beep.metid.polimi.it/web/{friendly_url}'
        commonlogger.debug(f'Downloading page {url}')
        text = self.get_page(url).text
        course_tree = etree.HTML(text)

        info_a_xpath = '//div[@id="heading"]//a[@class="logo custom-logo"]'
        course_name_xpath = 'img/@alt'
        course_url_xpath = '@href'

        info_anchor = course_tree.xpath(info_a_xpath)[0]
        course_full_url = info_anchor.xpath(course_url_xpath)[0]
        name = info_anchor.xpath(course_name_xpath)[0]

        parse_course_url = urlparse(course_full_url)
        groupId = parse_qs(parse_course_url.query)['_49_groupId'][0]

        course_dict = {
            # Corresponds to the groupId or the course name
            # fortunately the groupId resolving works anyway
            'friendlyUrl': friendly_url,
            # Course name
            'name': name,
            # Course ID, usually it's the same as group id
            'classPK': groupId,
            # Same as Course ID
            'groupId': groupId,
            # Courses have folderId 0
            'folderId': 0,
            'ManuallyAdded': False,
            'size': 0,
            'downloadedSize': 0,
            'sync': False
        }
        return course_dict


    def _courses_scraper(self, text):
        """
        This function scrapes the main beep page to look for newcourses
        the returned dictionaries have the following structure:
            - name: The name of the course
            - friendlyUrl: The URL of the course
            - classPK: The unique groupID assigned from liferay
        :return: A list of dictionaries with the scraped courses
        :rtype: List
        """

        courses_tree = etree.HTML(text)
        courses_link_xpath = '//tr[contains(@class, "results-row")]/'\
            'td[1]/a/@href'
        courses_name_xpath = '//tr[contains(@class, "results-row")]/'\
            'td[1]/a//text()'
        courses_links = courses_tree.xpath(courses_link_xpath)
        courses_names = courses_tree.xpath(courses_name_xpath)
        scraped_courses_list = zip(courses_names, courses_links)

        # online_courses = Courses()
        # we iterate over the tags
        # we only need year or [IOL] to parse for real courses
        year_or_iol = Group(
            "[" + ZeroOrMore(Word(nums, exact=4) + "-" + Word(nums, exact=2)) +
            ZeroOrMore(CaselessLiteral("IOL")) + "]"
        )

        # bracketed = Group("[" + OneOrMore(Word(printables, " ")) + "]")
        # middle = ~bracketed + OneOrMore(Word(alphas))
        # grammar = year.suppress() + Literal("-").suppress() + middle
        grammar = year_or_iol

        temporary_courses = []
        for course in scraped_courses_list:
            parsed_link = urlparse(course[1])
            parsed_query_str = parse_qs(parsed_link.query)

            try:
                grammar.parseString(course[0])
                course_dict = {
                    # Corresponds to the groupId or the course name
                    # fortunately the groupId resolving works anyway
                    'friendlyUrl': parsed_query_str['_29_groupId'][0],
                    # Course name
                    'name': course[0],
                    # Course ID, usually it's the same as group id
                    'classPK': parsed_query_str['_29_groupId'][0],
                    # Same as Course ID
                    'groupId': parsed_query_str['_29_groupId'][0],
                    # Courses have folderId 0
                    'folderId': 0,
                    'ManuallyAdded': False,
                    'size': 0,
                    'downloadedSize': 0,
                    'sync': False
                }
                temporary_courses.append(course_dict)
            except ParseException:
                pass

        return temporary_courses

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
            commonlogger.debug(f'Comparing course {elem.name} with the local '
                               'copy of courses')
            if elem not in self.available_courses:
                commonlogger.debug("It's not present in the local copy;"
                                   " adding it")
                self.available_courses.append(elem)
        # now do the opposite: if a course has been deleted,
        # do the same with the local copy
        for elem in self.available_courses:
            commonlogger.debug(f'Comparing course {elem.name} from the local '
                               'data to the new list.')
            if elem not in master_courses:
                commonlogger.debug("It's not present in the new list, "
                                   "therefore we remove it from the local"
                                   " data")
                self.available_courses.remove(elem)

    def update_course_files(self, course):
        online = self.find_files_and_folders(course._course_dict)
        synclocalwithonline(course.documents, online)
        sizes = []
        course.size = sum(folder_total_size(course.documents, sizes))
        human_total_size = sizeof_fmt(course.size)
        commonlogger.info(f'****DIMENSIONE TOTALE: {human_total_size}')

    def find_files_and_folders(self, folder_dict):
        folder = Folder(folder_dict)
        if self._use_json_endpoint:
            commonlogger.debug('Using JSON endpoint method')
            query_params_files = {'repositoryId': folder.group_id,
                                  'folderId': 0}
            query_params_folder = {'repositoryId': folder.group_id,
                                   'parentFolderId': 0}
            if folder_dict['folderId'] != -1:
                query_params_files['folderId'] = folder_dict['folderId']
                query_params_folder['parentFolderId'] = folder_dict['folderId']

            subfolders_dict = self.get_page(self.get_folders_url,
                                            params=query_params_folder).json()

            files_dict = self.get_page(self.get_files_url,
                                       params=query_params_files).json()

            for elem in subfolders_dict:
                commonlogger.debug(f'Added {elem} to \n{folder}')
                subfolder = self.find_files_and_folders(elem)
                folder.folders.append(subfolder)

            for elem in files_dict:
                commonlogger.debug(f'Added {elem} to \n{folder}')
                course_file = CourseFile(elem)
                folder.files.append(course_file)
        else:
            commonlogger.debug('Falling back to webscraper method')

            weird_parameters = {
                '_20_folderId': folder_dict['folderId'],
                '_20_displayStyle': 'list',
                '_20_viewEntries': '0',
                '_20_viewFolders': '0',
                '_20_entryEnd': '500',
                '_20_entryStart': '0',
                '_20_folderEnd': '500',
                '_20_folderStart': '0',
                '_20_viewEntriesPage': '1',
                'p_p_id': '20',
                'p_p_lifecycle': '0'
            }
            commonlogger.debug(folder_dict)
            try:
                response = self.get_page(
                    "https://beep.metid.polimi.it/web/"
                    f"{folder_dict['groupId']}/documenti-e-media",
                    weird_parameters)
            except requests.exceptions.HTTPError:
                try:
                    response = self.get_page(
                        "https://beep.metid.polimi.it/web/"
                        f"{folder_dict['friendly_url']}/documenti-e-media",
                        weird_parameters)
                except requests.exceptions.HTTPError:
                    commonlogger.error(
                        'Can\'t find the documents and media folde of '
                        f'"{folder_dict["name"]}" , so it won\'t be '
                        'downloaded',
                        exc_info=True
                    )
                    return folder

            page_tree = etree.HTML(response.text)
            debug_dump_request_response(response, commonlogger)

            entry_xpath = '//div[contains(@id, "SearchContainer")]//'\
                'tr[contains(@class, "document-display-style")]'

            title_xpath = 'td[contains(@class, "col-2")]//span[1]'\
                '/text()'
            is_folder_xpath = '@data-folder'
            folder_id_xpath = '@data-folder-id'
            date_xpath = 'td[contains(@class, "col-5")]/text()'
            size_xpath = 'td[contains(@class, "col-3")]/text()'

            for entry in page_tree.xpath(entry_xpath):
                title = entry.xpath(title_xpath)[1]
                raw_date = entry.xpath(date_xpath)[0]
                is_folder = entry.xpath(is_folder_xpath)
                raw_size = entry.xpath(size_xpath)[0]

                date = raw_date_to_datetime(raw_date, self.gmt1)

                if is_folder:
                    folder_dict_sub = {
                        'folderId': entry.xpath(folder_id_xpath)[0],
                        # Don't remove the *1000, this necessary to keep the
                        # timestamp consistent with liferay precision (1/1000s)
                        'lastPostDate': date.timestamp()*1000,
                        'name': title.replace('UTF-8\'\'', ''),
                        'groupId': folder_dict['groupId'],
                    }

                    subfolder = self.find_files_and_folders(folder_dict_sub)
                    folder.folders.append(subfolder)
                else:
                    file_page_xpath = 'td[contains(@class, "col-2")]//span[1]'\
                        '//a/@href'
                    file_version_xpath = '//div[contains(@class,'\
                        '"lfr-search-container")]//tr[contains(@class,'\
                        'results-row)]//td[1]/text()'
                    url_xpath = '//div[contains(@class, "url-file-container")'\
                        ']//input/@value'

                    parsed_link = urlparse(entry.xpath(file_page_xpath)[0])
                    parsed_query_str = parse_qs(parsed_link.query)

                    file_download_page = self.get_page(parsed_link.geturl())
                    download_page_tree = etree.HTML(file_download_page.text)

                    uuid = download_page_tree.xpath(url_xpath)[0]\
                        .split("/")[-1]
                    # Server: nginx/1.10.3
                    # Date: Wed, 16 Dec 2020 10:38:28 GMT
                    # Content-Type: application/pdf
                    # Content-Length: 43228
                    # Connection: keep-alive
                    # Last-Modified: Sun, 10 Sep 2017 17:49:11 GMT
                    # Cache-Control: public
                    # Pragma: public
                    # Content-Disposition: attachment; filename="170829 AM1 ELN risultati.pdf"
                    # Vary: Accept-Encoding
                    file_info = ''
                    complete_filename = ''
                    size = 0
                    last_online_edit_time = datetime(1980, 1, 1)
                    for _ in range(10):
                        file_info = self.get_headers(
                            'https://beep.metid.polimi.it/documents/'
                            f'{folder_dict["groupId"]}/{uuid}')
                        try:
                            size = file_info.headers['Content-Length']
                            complete_filename = re.search(
                                '(?<=filename=\")(.*)(?=\")|'
                                '(?<=filename\\*=UTF-8\'\')(.*)',
                                file_info.headers['Content-Disposition']
                            ).group()
                            last_online_edit_time = \
                                parse(file_info.headers['Last-Modified'])
                            break
                        except KeyError:
                            pass
                    filename, _, extension = complete_filename.rpartition('.')
                    file_version = None
                    try:
                        file_version = download_page_tree\
                                .xpath(file_version_xpath)[0]
                    except IndexError:
                        commonlogger.warning(f'{filename} is missing its'
                                             ' version')
                        file_version = 0

                    file_entry_id = None
                    try:
                        file_version = parsed_query_str['_20_fileEntryId'][0]
                    except (KeyError, IndexError):
                        commonlogger.warning(f'{filename} is missing its'
                                             ' entry id')
                        file_entry_id = 0

                    try:
                        file_dict = {
                            'extension': extension,
                            'version': file_version,
                            'fileEntryId': file_entry_id,
                            'title': filename,
                            'groupId': folder_dict['groupId'],
                            'uuid': uuid,
                            'modifiedDate': last_online_edit_time
                            .timestamp()*1000,
                            'size': int(size),
                            'localCreationTime': None
                        }
                        folder.files.append(CourseFile(file_dict))
                    except IndexError:
                        # uuid is missing or malformed
                        commonlogger.error('Can\'t download '
                                           f'{filename} please proceed to '
                                           'download it manually')
                        commonlogger.error(download_page_tree.xpath(url_xpath))

        return folder

    def save_files(self, course, needsync, downloadsignal,
                   chunk_size=512 * 1024):
        with QThreadPoolContexted(wait=False) as TExec:
            for coursefile, path in needsync:
                TExec.start(func_runnable(self, self.download_file, course,
                                          path, coursefile, needsync,
                                          downloadsignal, chunk_size),
                            QThread.LowPriority)

    def download_file(self, course, path, coursefile, needsync, downloadsignal,
                      chunk_size):
        result = self.get_file(coursefile.url)
        commonlogger.debug(coursefile.url)
        complete_basename = f'{coursefile.name}.{coursefile.extension}'
        complete_name = os.path.join(path, unquote(complete_basename))
        os.makedirs(path, exist_ok=True)
        with open(complete_name, 'wb') as f:
            commonlogger.info('writing into {}'.format(complete_name))
            for chunk in result.iter_content(chunk_size):
                bytes_written = f.write(chunk)
                course.downloaded_size += bytes_written
                coursefile.downloaded_size += bytes_written
                downloadsignal.emit(course=course)
            coursefile.local_creation_time = datetime.now(self.gmt1)

# --- Utils ---#
class func_runnable(QRunnable):
    def __init__(self, parent, function, *args, **kwargs):
        super(func_runnable, self).__init__(parent)
        self.run = partial(function, *args, **kwargs)


def read(*names, **kwargs):
    with open(
            os.path.join(os.path.dirname(__file__), *names),
            encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


class MySignal(QObject):
    sig = Signal(str)


class CoursesSignal(QObject):
    sig = Signal(list)


class DownloadChunkSignal(QObject):
    sig = Signal(Course, int)


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


class SignalLoggingHandler(logging.Handler):
    def __init__(self, signal, forward_file_descriptor=None):
        super(SignalLoggingHandler, self).__init__()

        if forward_file_descriptor:
            self.forward_fd = forward_file_descriptor

        def sig_emit(record):
            if isinstance(record, str):
                signal.sig.emit(record)
            else:
                signal.sig.emit(record.msg)
        self.emit = sig_emit

    def write(self, message):
        if self.forward_fd:
            self.forward_fd.write(message)
        self.emit(message)

    def flush(self):
        self.forward_fd.flush()
