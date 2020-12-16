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

import requests
import os
import pickle
import sys
import logging
import json
import keyring
from packaging import version
from appdirs import user_config_dir, user_data_dir
from PySide2.QtCore import (QAbstractTableModel, QModelIndex, Qt, Slot, QTimer)
from PySide2.QtGui import (QTextCursor, QCursor, QIcon)
from PySide2.QtWidgets import (QWidget, QMenu, QAction, QFileDialog,
                               QMainWindow, QSystemTrayIcon, QApplication,
                               QMessageBox, QSizePolicy, QDialog)
from polibeepsync.common import (User, Folder, Course, DownloadThread,
                                 LoginThread, find_version, MySignal,
                                 RefreshCoursesThread, SignalLoggingHandler)
from polibeepsync.cmdlineparser import create_parser
from polibeepsync.ui_resizable import CoursesListView
from polibeepsync import filesettings
from polibeepsync.utils import init_checkbox, check_course_url
from polibeepsync.ui.ui_main_form import Ui_MainForm
from polibeepsync.ui.ui_add_course_popup import Ui_AddCoursePopup
from polibeepsync.database_manager import DatabaseManager


__version__ = find_version("__init__.py")
logger = logging.getLogger("polibeepsync.qtgui")
commonlogger = logging.getLogger("polibeepsync.common")
database_logger = logging.getLogger("polibeepsync.database")


class CoursesListModel(QAbstractTableModel):
    def __init__(self, courses):
        QAbstractTableModel.__init__(self)
        # my object is a mapping, while table model uses an index (so it's
        # more similar to a list
        self.courses = list(courses)

    def rowCount(self, parent=QModelIndex()):
        return len(self.courses)

    def columnCount(self, parent=QModelIndex()):
        return 4

    def insertRows(self, position, rows, newcourse, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            self.courses.insert(position, newcourse)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            del self.courses[position]
        self.endRemoveRows()
        return True

    def flags(self, index):
        try:
            flags_dict = {
                1: Qt.ItemIsEditable | Qt.ItemIsEnabled |
                Qt.ItemIsSelectable | Qt.ItemIsUserCheckable,
                2: Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
            }
            return flags_dict[index.column()]
        except KeyError:
            return Qt.ItemIsEnabled

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            column = index.column()
            if column == 2:
                other_names = [elem.save_folder_name for elem in self.courses]
                if value not in other_names and value != "":
                    self.courses[index.row()].save_folder_name = value
                    self.dataChanged.emit(index, index)
            elif column == 1:
                self.courses[index.row()].sync = value
                self.dataChanged.emit(index, index)
            return True
        return False

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            course = self.courses[index.row()]
            dw = course.downloaded_size
            total = course.size
            data_array = [
                course.name,
                course.sync,
                course.save_folder_name,
                (dw, total)
            ]
            return data_array[index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            headers_list = [
                "Name",
                "Sync",
                "Save as",
                "Download %"
            ]
            return headers_list[col]

class MainWindow(QMainWindow, Ui_MainForm):
    def __init__(self, parent=None, args=None):
        super().__init__(parent)
        self.appname = "poliBeePsync"
        self.settings_fname = 'pbs-settings.ini'
        self.data_fname = 'pbs.sqlite3'
        self.settings_path = None
        self.settings = None
        self.icon = QIcon(":/root/imgs/icons/polibeepsync.svg")
        self.db_mgr = None

        self.status_signal = MySignal()
        self.logging_signal = MySignal()

        logging_console_hdl = SignalLoggingHandler(
            self.logging_signal, sys.stderr
        )
        sys.stderr = logging_console_hdl

        logger.addHandler(logging_console_hdl)
        commonlogger.addHandler(logging_console_hdl)
        database_logger.addHandler(logging_console_hdl)

        # load_settings() sets settings_path and settings
        self.load_settings()
        self.load_data()
        if args.default_timeout:
            self.user.default_timeout = args.default_timeout

        self.setupUi(self)

        self.w = QWidget()
        self.timer = QTimer(self)
        self.loginthread = LoginThread(self.user, self)
        self.refreshcoursesthread = RefreshCoursesThread(self.user, self)
        self.downloadthread = DownloadThread(self.user,
                                             self.settings['RootFolder'],
                                             self)

        self.add_course_popup = AddCoursePopup(self)

        self.userCode.setText(str(self.user.username))
        self.password.setText(self.user.password)
        self.courses_model = CoursesListModel(self.user.available_courses)

        self.coursesView.deleteLater()
        self.coursesView = CoursesListView(self.courses_tab)
        self.coursesView.setStyleSheet(self.styleSheet())
        self.courses_layout.addWidget(self.coursesView)
        self.coursesView.setObjectName("coursesView")

        self.coursesView.setModel(self.courses_model)

        self._resizeview()

        self.rootfolder.setText(self.settings['RootFolder'])

        init_checkbox(self.addSyncNewCourses, self.settings, 'SyncNewCourses')

        init_checkbox(self.startupSync, self.settings, 'SyncOnStartup')

        self.timerMinutes.setValue(int(self.settings['UpdateEvery']))
        self.timeout.setValue(int(self.settings['DefaultTimeout']))

        self.version_label.setText(f"Current version: {__version__}")

        self.trayIconMenu = QMenu()
        self.trayIcon = QSystemTrayIcon(self.icon, self.w)
        self.createTray()

        self.__connect_signals()
        self.timer.start(1000 * 60 * int(self.settings['UpdateEvery']))

        try:
            if args.sync_on_startup or \
               self.settings['SyncOnStartup'] == str(True):
                self.sync_files()
        except KeyError:
            pass
        if args.sync_interval:
            logger.info('Sync interval overridden with '
                        f'{args.sync_interval} minutes')
            self.timer.start(1000 * 60 * args.sync_interval)
        self.user.login()

    @Slot()
    def show_add_course_popup(self):
        self.add_course_popup.show()

    def __connect_signals(self):
        self.status_signal.sig.connect(self.update_status_bar)
        self.logging_signal.sig.connect(self.myStream_message)
        self.timer.timeout.connect(self.sync_files)

        self.loginthread.signal_error.sig.connect(self.update_status_bar)
        self.loginthread.signal_ok.sig.connect(self.update_status_bar)

        self.refreshcoursesthread.dumpuser.sig.connect(self.dumpUser)
        self.refreshcoursesthread.newcourses.sig.connect(self.addtocoursesview)
        self.refreshcoursesthread.newcourses.sig\
            .connect(self.sync_new_courses)
        self.refreshcoursesthread.removable.sig.connect(self.rmfromcoursesview)

        self.downloadthread.dumpuser.sig.connect(self.dumpUser)
        self.downloadthread.download_signal.connect(
            self.update_course_downloaded_sizes)
        self.downloadthread.initial_sizes\
            .connect(self.update_course_downloaded_sizes)

        self.trayIcon.activated.connect(self._activate_traymenu)

    @Slot()
    def show_about(self, **kwargs):
        msgBox = QMessageBox(self)
        msgBox.setTextFormat(Qt.RichText)
        msgBox.setWindowTitle('About poliBeePSync')
        text = """
<html>
<head/>
<body>
  <p>
    poliBeePsync is a program written by Davide Olianas and Raffaele Di Campli
    released under GNU GPLv3+.
    More information is available on the
    <a href=\"https://github.com/Jacotsu/polibeepsync\">
    <span style=\" text-decoration: underline; color:#0000ff;\">
    official github</span></a>.
    Feel free to contact us at
    <a href=\"mailto:dcdrj.pub@gmail.com\">dcdrj.pub@gmail.com</a> for
    suggestions and bug reports.
  </p>
  <p>
  Want to learn how to make softwares like this? Then join <br>
    <a href='https://poul.org/'>
      <img src=':/root/imgs/PinguiniStilNovoFullLogoBlack.svg'>
    </a>
  </p>
  <p>
    <a href='https://liberapay.com/jacotsu/donate'>
        Want to offer me a sandwich?
    </a>
  </p>
</body>
</html>
"""
        msgBox.setInformativeText(text)
        msgBox.exec()

    @Slot()
    def _resizeview(self, **kwargs):
        self.coursesView.setColumnWidth(3, 160)
        self.coursesView.resizeColumnToContents(1)
        self.coursesView.setColumnWidth(0, 320)

    def check_new_version(self):
        rawdata = requests.get('https://pypi.python.org/pypi/'
                               'poliBeePsync/json')
        latest = json.loads(rawdata.text)['info']['version']
        if version.parse(latest) > version.parse(__version__):
            newtext = 'Current version: {}. Latest version: {}. '\
                'Click <a href="https://jacotsu.github.io/polibeepsync/build/'\
                'html/installation.html">here</a>'\
                ' to find out how to upgrade'.format(__version__, latest)
        else:
            newtext = "Current version: {} up-to-date.".format(__version__)
        self.version_label.setText(newtext)

    @Slot(Course)
    def update_course_downloaded_sizes(self, course, **kwargs):
        row = self.courses_model.courses.index(course)
        where = self.courses_model.index(row, 3)
        self.courses_model.dataChanged.emit(where, where)

    @Slot(list)
    def sync_new_courses(self, newlist):
        if self.settings['SyncNewCourses'] == 'True':
            for elem in newlist:
                elem.sync = True

    def load_settings(self):
        for path in [user_config_dir(self.appname),
                     user_data_dir(self.appname)]:
            try:
                os.makedirs(path, exist_ok=True)
            except OSError:
                logger.critical('OSError while calling os.makedirs.',
                                exc_info=True)
                logger.critical(f"I couldn't create {path}.\nStart"
                                " poliBeePsync with --log-level=debug "
                                "error to get more details.")
        self.settings_path = os.path.join(user_config_dir(self.appname),
                                          self.settings_fname)
        defaults = {
            # Update every 8 hours
            'UpdateEvery': '480',
            'RootFolder': os.path.join(os.path.expanduser('~'), self.appname),
            'SyncNewCourses': 'True',
            'SyncOnStartup': 'False',
            'DefaultTimeout': '10'
        }
        self.settings = filesettings.settingsFromFile(self.settings_path,
                                                      defaults)

    def load_data(self):
        self.db_mgr = DatabaseManager(
            os.path.join(user_data_dir(self.appname), self.data_fname),
            os.path.join(user_data_dir(self.appname), 'pbs.data')
        )
        try:
            username = self.db_mgr.get_key('username')
            self.user = User(
                username,
                keyring.get_password('beep.metid.polimi.it', username)
            )
            self.user.available_courses = self.db_mgr.get_courses()
            logger.info("Data has been loaded successfully.")
        except LookupError:
            self.user = User('', '')

    @Slot(str)
    def update_status_bar(self, status):
        self.statusbar.showMessage(status)

    @Slot(int)
    def sync_new(self, state):
        if state == 2:
            self.settings['SyncNewCourses'] = 'True'
            logger.info('New courses will now be automatically synced')
        else:
            self.settings['SyncNewCourses'] = 'False'
            logger.info('New courses will NOT be automatically synced')
        filesettings.settingsToFile(self.settings, self.settings_path)

    @Slot(int)
    def sync_on_startup(self, state):
        if state == 2:
            self.settings['SyncOnStartup'] = 'True'
            logger.info('All courses will be synced at startup')
        else:
            self.settings['SyncOnStartup'] = 'False'
            logger.info('No course will be synced at startup')
        filesettings.settingsToFile(self.settings, self.settings_path)

    @Slot(int)
    def updated_minutes(self, minutes):
        self.settings['UpdateEvery'] = str(minutes)
        filesettings.settingsToFile(self.settings, self.settings_path)
        self.timer.start(1000 * 60 * int(self.settings['UpdateEvery']))
        logger.info('All courses will be automatically synced every '
                    f'{self.settings["UpdateEvery"]} minutes')

    @Slot(int)
    def updated_default_timeout(self, seconds):
        self.settings['DefaultTimeout'] = str(seconds)
        filesettings.settingsToFile(self.settings, self.settings_path)
        self.user.default_timeout = seconds
        logger.info(f'Connection timeout set to {seconds} seconds')

    @Slot(str)
    def updated_root_folder(self, path):
        self.settings['RootFolder'] = path
        filesettings.settingsToFile(self.settings, self.settings_path)
        logger.info(f'Root folder set to: {path}')

    @Slot()
    def choose_rootdir(self):
        currentdir = self.settings['RootFolder']
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        newroot = QFileDialog.getExistingDirectory(None,
                                                   "Open Directory",
                                                   currentdir, flags)
        if newroot != "" and str(newroot) != currentdir:
            logger.info(f'Root folder set to: {newroot}')
            self.settings['RootFolder'] = str(newroot)
            filesettings.settingsToFile(self.settings, self.settings_path)
            self.rootfolder.setText(newroot)
            self.downloadthread.topdir = self.settings['RootFolder']

    @Slot()
    def set_usercode(self):
        newcode = self.userCode.text()
        try:
            if len(newcode) == 8:
                self.user.username = newcode
                self.db_mgr.set_key('username', newcode)
                logger.info(f'User code changed to {newcode}.')
                keyring.set_password('beep.metid.polimi.it',
                                     self.user.username,
                                     self.user.password)
        except OSError:
            logger.critical("I couldn't save data to disk. Run"
                            " poliBeePsync with option --log-level=debug"
                            " error to get more details.")
            logger.error('OSError raised while trying to write the User'
                         'instance to disk.', exc_info=True)

    @Slot()
    def set_password(self):
        newpass = self.password.text()
        self.user.password = newpass
        try:
            keyring.set_password('beep.metid.polimi.it',
                                 self.user.username,
                                 self.user.password)
            logger.info("Password changed.")
        except OSError:
            logger.critical("I couldn't save data to disk. Run"
                            " poliBeePsync with option --log-level=debug"
                            " error to get more details.")
            logger.error('OSError raised while trying to write the User'
                         'instance to disk.', exc_info=True)

    @Slot()
    def test_login(self):
        if not self.loginthread.isRunning():
            self.loginthread.start()
            self.status_signal.sig.emit("Logging in, please wait.")

    @Slot(list)
    def addtocoursesview(self, addlist):
        for elem in addlist:
            self.courses_model.insertRows(0, 1, elem)

    @Slot(list)
    def rmfromcoursesview(self, removelist):
        for elem in removelist:
            index = self.courses_model.courses.index(elem)
            self.courses_model.removeRows(index, 1)

    @Slot()
    def dumpUser(self):
        self.db_mgr.store_courses(self.user.available_courses)

    @Slot()
    def refresh_courses(self):
        self.status_signal.sig.emit('Searching for online updates...'
                                    'this may take a while.')
        if not self.loginthread.isRunning():
            self.loginthread.signal_ok.sig.connect(self.do_refresh_courses)
            self.loginthread.start()

    def do_refresh_courses(self):
        self.loginthread.signal_ok.sig.disconnect(self.do_refresh_courses)
        if not self.refreshcoursesthread.isRunning():
            self.refreshcoursesthread.start()

    @Slot()
    def sync_files(self):
        self.downloadthread.topdir = self.settings['RootFolder']
        self.refreshcoursesthread.finished.connect(self.do_sync_files)
        self.refresh_courses()

    @Slot()
    def do_sync_files(self):
        self.refreshcoursesthread.finished.disconnect(self.do_sync_files)
        self.status_signal.sig.emit('Started syncing.')
        self.downloadthread.start()

    @Slot(str)
    def myStream_message(self, message):
        self.status.appendPlainText(f'{message}')

    def restore_window(self):
        self.setWindowState(
            self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive
        )
        self.show()

    def createTray(self):
        restoreAction = QAction(
            "&Restore", self, triggered=self.restore_window
        )
        quitAction = QAction(
            "&Quit", self, triggered=QApplication.instance().quit
        )
        self.trayIconMenu.addAction(restoreAction)
        self.trayIconMenu.addAction(quitAction)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.show()

    @Slot(str)
    def _activate_traymenu(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.restore_window()
        else:
            self.trayIconMenu.activateWindow()
            self.trayIconMenu.popup(QCursor.pos())

    def closeEvent(self, event):
        self.hide()
        event.ignore()


class AddCoursePopup(QDialog, Ui_AddCoursePopup):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    @Slot()
    def accept(self):
        url = self.CourseUrl.toPlainText()
        parent = self.parent()
        logger.debug(f'Inserted course url {url}')
        friendly_url = check_course_url(parent.user, url)
        if friendly_url:
            parent.update_status_bar(f'Added course from {url}')
            logger.info(f'Added course from {url}')
            course_dict = parent.user.scrape_course_main_page(friendly_url)
            course_dict['ManuallyAdded'] = True
            course = Course(course_dict, parent.settings['SyncNewCourses'])
            if course not in parent.user.available_courses:
                course.save_folder_name = course.simplify_name(course.name)
                parent.user.available_courses.append(course)
                parent.addtocoursesview([course])
            else:
                parent.update_status_bar(f'{course} already registered')
                logger.error(f'{course} already registered')
        else:
            parent.update_status_bar(f'Invalid course url {url}')
            logger.error(f'Invalid course url {url}')

        self.CourseUrl.clear()
        self.hide()

    @Slot()
    def reject(self):
        self.CourseUrl.clear()
        self.hide()


def main():
    # load options from cmdline
    parser = create_parser()
    args = parser.parse_args()

    # set debug levels
    LEVELS = {
        'notset': logging.NOTSET,
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }

    level_name = 'info'
    if args.log_level:
        level_name = args.log_level
    level = LEVELS.get(level_name, logging.INFO)

    # now get the logger used in the common module and set its level to what
    # we get from sys.argv
    commonlogger.setLevel(level)
    database_logger.setLevel(level)
    logger.setLevel(level)

    formatter = logging.Formatter('[%(levelname)s] %(name)s %(message)s')

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    commonlogger.addHandler(handler)
    database_logger.addHandler(handler)

    # Fixes PyQt5 startup hang on Os X big sur
    os.environ["QT_MAC_WANTS_LAYER"] = "1"
    app = QApplication(sys.argv)

    frame = MainWindow(args=args)
    # args is defined at the top of this module
    if not args.hidden:
        # Need to fix showing wrong window
        frame.show()

    exit_code = app.exec_()
    frame.dumpUser()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
