__copyright__ = """Copyright 2019 Davide Olianas (ubuntupk@gmail.com), Di
Campli Raffaele."""

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

import requests
import os
import pickle
import sys
import logging
import json
import keyring
from polibeepsync.common import (User, Folder, Course, DownloadThread,
                                 LoginThread, find_version, MySignal,
                                 RefreshCoursesThread, SignalLoggingHandler)
from polibeepsync.cmdlineparser import create_parser
from polibeepsync.ui_resizable import Ui_Form
from polibeepsync import filesettings
from appdirs import user_config_dir, user_data_dir

from PySide2.QtCore import (QAbstractTableModel, QModelIndex, Qt, Slot,
                            QTimer, QLocale)
from PySide2.QtGui import (QTextCursor, QCursor)
from PySide2.QtWidgets import (QWidget, QMenu, QAction, QFileDialog, QLabel,
                               QSystemTrayIcon, qApp, QApplication)


__version__ = find_version("__init__.py")
logger = logging.getLogger("polibeepsync.qtgui")
commonlogger = logging.getLogger("polibeepsync.common")


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
        if index.column() == 2:
            flags = Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
            return flags
        elif index.column() == 1:
            flags = Qt.ItemIsEditable | Qt.ItemIsEnabled | \
                Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
            return flags
        else:
            return Qt.ItemIsEnabled

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            if index.column() == 2:
                other_names = [elem.save_folder_name for elem in self.courses]
                if value not in other_names and value is not "":
                    self.courses[index.row()].save_folder_name = value
                    self.dataChanged.emit(index, index)
                return True
            elif index.column() == 1:
                self.courses[index.row()].sync = value
                self.dataChanged.emit(index, index)
                return True
        return False

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self.courses[index.row()].name
            if index.column() == 1:
                return self.courses[index.row()].sync
            if index.column() == 2:
                return self.courses[index.row()].save_folder_name
            if index.column() == 3:
                dw = self.courses[index.row()].downloaded_size
                total = self.courses[index.row()].size
                return (dw, total)
        elif role == Qt.CheckStateRole:
            return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col == 0:
                return "Name"
            elif col == 1:
                return "Sync"
            elif col == 2:
                return "Save as"
            elif col == 3:
                return "Download %"


class MainWindow(Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.appname = "poliBeePsync"
        self.settings_fname = 'pbs-settings.ini'
        self.data_fname = 'pbs.data'
        self.setupUi(self)
        self.w = QWidget()

        self.status_signal = MySignal()
        self.status_signal.sig.connect(self.update_status_bar)

        self.logging_signal = MySignal()
        self.logging_signal.sig.connect(self.myStream_message)
        logging_console_hdl = SignalLoggingHandler(self.logging_signal)
        logger.addHandler(logging_console_hdl)
        commonlogger.addHandler(logging_console_hdl)

        self.about_text()
        self.timer = QTimer(self)

        # settings_path is a string containing the path to settings
        self.settings_path = None
        # settings is a dictionary of settings
        self.settings = None
        # load_settings() sets settings_path and settings
        self.load_settings()
        self.load_data()

        self.timer.timeout.connect(self.syncfiles)
        self.timer.start(1000 * 60 * int(self.settings['UpdateEvery']))

        self.loginthread = LoginThread(self.user, self)
        self.loginthread.signal_error.sig.connect(self.update_status_bar)
        self.loginthread.signal_ok.sig.connect(self.update_status_bar)

        self.refreshcoursesthread = RefreshCoursesThread(self.user, self)
        self.refreshcoursesthread.dumpuser.sig.connect(self.dumpUser)
        self.refreshcoursesthread.newcourses.sig.connect(self.addtocoursesview)
        self.refreshcoursesthread.newcourses.sig.connect(self.syncnewcourses)
        self.refreshcoursesthread.removable.sig.connect(self.rmfromcoursesview)

        self.downloadthread = DownloadThread(self.user,
                                             self.settings['RootFolder'],
                                             self)
        self.downloadthread.dumpuser.sig.connect(self.dumpUser)
        self.downloadthread.download_signal.connect(
            self.update_course_download)
        self.downloadthread.initial_sizes.connect(self.setinizialsizes)
        self.downloadthread.date_signal.connect(self.update_file_localtime)

        self._window.userCode.setText(str(self.user.username))
        self._window.userCode.editingFinished.connect(self.setusercode)
        self._window.password.setText(self.user.password)
        self._window.password.editingFinished.connect(self.setpassword)
        self._window.trylogin.clicked.connect(self.testlogin)

        self._window.courses_model = CoursesListModel(self.user.
                                                      available_courses)
        self._window.coursesView.setModel(self._window.courses_model)
        self._resizeview()
        self._window.refreshCourses.clicked.connect(self.refreshcourses)

        self._window.syncNow.clicked.connect(self.syncfiles)

        if self.settings['SyncNewCourses'] == str(True):
            self._window.sync_new = Qt.Checked
        else:
            self._window.sync_new = Qt.Unchecked

        self._window.rootfolder.setText(self.settings['RootFolder'])
        self._window.rootfolder.textChanged.connect(self.rootfolderslot)

        self._window.addSyncNewCourses.setCheckState(self._window.sync_new)
        self._window.addSyncNewCourses.stateChanged.connect(self.syncnewslot)

        self._window.timerMinutes.setValue(int(self.settings['UpdateEvery']))
        self._window.timerMinutes.valueChanged.connect(self.updateminuteslot)

        self._window.changeRootFolder.clicked.connect(self.chooserootdir)
        self._window.version_label.setText("Current version: {}."
                                           .format(__version__))
        self._window.check_version.clicked.connect(self.checknewversion)

        self.trayIconMenu = QMenu()
        self.trayIcon = QSystemTrayIcon(self.icon, self.w)
        self.trayIcon.activated.connect(self._activate_traymenu)
        self.createTray()

    @Slot()
    def _resizeview(self, **kwargs):
        self._window.coursesView.setColumnWidth(3, 160)
        self._window.coursesView.resizeColumnToContents(1)
        self._window.coursesView.setColumnWidth(0, 320)

    def checknewversion(self):
        rawdata = requests.get('https://pypi.python.org/pypi/'
                               'poliBeePsync/json')
        latest = json.loads(rawdata.text)['info']['version']
        self._window.version_label.setTextFormat(Qt.RichText)
        self._window.version_label.setOpenExternalLinks(True)
        self._window.version_label.setLocale(QLocale(QLocale.English,
                                                     QLocale.UnitedStates))
        self._window.version_label.setScaledContents(True)
        self._window.version_label.setWordWrap(True)
        if latest != __version__:
            newtext = """<p>Current version: {}.<br>
Latest version: {}. </p>
<p>Visit <a
href='https://jacotsu.github.io/polibeepsync/dirhtml/index.html\
        #how-to-install-upgrade-remove'>here</a> to find out how to upgrade.
""".format(__version__, latest)
        else:
            newtext = "Current version: {} up-to-date.".format(__version__)
        self._window.version_label.setText(newtext)

    def _update_time(self, folder, file, path_list):
        logger.debug(f'inside {folder.name}')
        for path in path_list:
            logger.debug(f'namegoto: {path}')
            folder_dict = {'name': path}
            fakefolder = Folder(folder_dict)
            logger.debug(f'contained folders:  {folder.folders}')
            ind = folder.folders.index(fakefolder)
            goto = folder.folders[ind]
            self._update_time(goto, file, path_list)

        if file in folder.files:
            ind = folder.files.index(file)
            thisfile = folder.files[ind]
            thisfile.local_creation_time = file.local_creation_time

    @Slot(tuple)
    def update_file_localtime(self, data, **kwargs):
        course, coursefile, path = data
        rootpath = os.path.join(self.settings['RootFolder'],
                                course.save_folder_name)
        if path.startswith(rootpath):
            partial = path[len(rootpath):]
        path_list = filter(None, partial.split(os.path.sep))
        self._update_time(course.documents, coursefile, path_list)

    @Slot(Course)
    def update_course_download(self, course, **kwargs):
        if course in self.user.available_courses:
            updating = self.user.available_courses[course.name]
            updating.downloaded_size = course.downloaded_size
            row = self._window.courses_model.courses.index(updating)
            where = self._window.courses_model.index(row, 3)
            self._window.courses_model.dataChanged.emit(where, where)

    @Slot(Course)
    def setinizialsizes(self, course, **kwargs):
        if course in self.user.available_courses:
            updating = self.user.available_courses[course.name]
            updating.downloaded_size = course.downloaded_size
            updating.size = course.size
            row = self._window.courses_model.courses.index(updating)
            where = self._window.courses_model.index(row, 3)
            self._window.courses_model.dataChanged.emit(where, where)
            self.dumpUser()

    @Slot(list)
    def syncnewcourses(self, newlist):
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
                                " poliBeePsync with --debug "
                                "error to get more details.")
        self.settings_path = os.path.join(user_config_dir(self.appname),
                                          self.settings_fname)
        defaults = {
            'UpdateEvery': '60',
            'RootFolder': os.path.join(os.path.expanduser('~'), self.appname),
            'SyncNewCourses': 'False'
        }
        self.settings = filesettings.settingsFromFile(self.settings_path,
                                                      defaults)

    def load_data(self):
        try:
            with open(os.path.join(user_data_dir(self.appname),
                                   self.data_fname), 'rb') as f:
                self.user = pickle.load(f)
                self.user.password = keyring\
                        .get_password('beep.metid.polimi.it',
                                      self.user.username)
                logger.info("Data has been loaded successfully.")
        except (EOFError, pickle.PickleError):
            logger.error('Settings corrupted', exc_info=True)
            self.user = User('', '')

        except FileNotFoundError:
            logger.error('Settings file not found.')
            self.user = User('', '')
            logger.error("I couldn't find data in the"
                         " predefined directory. Ignore this"
                         "message if you're using poliBeePsync"
                         " for the first time.")

    @Slot(str)
    def update_status_bar(self, status):
        self._window.statusbar.showMessage(status)

    @Slot(int)
    def syncnewslot(self, state):
        if state == 2:
            self.settings['SyncNewCourses'] = 'True'
        else:
            self.settings['SyncNewCourses'] = 'False'
        filesettings.settingsToFile(self.settings, self.settings_path)

    @Slot(int)
    def updateminuteslot(self, minutes):
        self.settings['UpdateEvery'] = str(minutes)
        filesettings.settingsToFile(self.settings, self.settings_path)
        self.timer.start(1000 * 60 * int(self.settings['UpdateEvery']))

    @Slot(str)
    def rootfolderslot(self, path):
        self.settings['RootFolder'] = path
        filesettings.settingsToFile(self.settings, self.settings_path)

    @Slot()
    def chooserootdir(self):
        currentdir = self.settings['RootFolder']
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        newroot = QFileDialog.getExistingDirectory(None,
                                                   "Open Directory",
                                                   currentdir, flags)
        if newroot != "" and str(newroot) != currentdir:
            self.settings['RootFolder'] = str(newroot)
            filesettings.settingsToFile(self.settings, self.settings_path)
            self._window.rootfolder.setText(newroot)
            # we delete the already present downloadthread and recreate it
            # because otherwise it uses the old download folder. I don't know
            # if there's a cleaner approach
            del self.downloadthread
            self.downloadthread = DownloadThread(self.user,
                                                 self.settings['RootFolder'],
                                                 self)
            self.downloadthread.dumpuser.sig.connect(self.dumpUser)
            self.dumpUser()

    @Slot()
    def setusercode(self):
        newcode = self._window.userCode.text()
        try:
            if len(newcode) == 8:
                self.user.username = newcode
                logger.info(f'User code changed to {newcode}.')
                keyring.set_password('beep.metid.polimi.it',
                                     self.user.username,
                                     self.user.password)
        except OSError:
            logger.critical("I couldn't save data to disk. Run"
                            " poliBeePsync with option --debug"
                            " error to get more details.")
            logger.error('OSError raised while trying to write the User'
                         'instance to disk.', exc_info=True)

    @Slot()
    def setpassword(self):
        newpass = self._window.password.text()
        self.user.password = newpass
        try:
            keyring.set_password('beep.metid.polimi.it',
                                 self.user.username,
                                 self.user.password)
            logger.info("Password changed.")
        except OSError:
            logger.critical("I couldn't save data to disk. Run"
                            " poliBeePsync with option --debug"
                            " error to get more details.")
            logger.error('OSError raised while trying to write the User'
                         'instance to disk.', exc_info=True)

    @Slot()
    def testlogin(self):
        if not self.loginthread.isRunning():
            self.loginthread.exiting = False
            self.loginthread.start()
            self.status_signal.sig.emit("Logging in, please wait.")

    @Slot(list)
    def addtocoursesview(self, addlist):
        for elem in addlist:
            self._window.courses_model.insertRows(0, 1, elem)

    @Slot(list)
    def rmfromcoursesview(self, removelist):
        for elem in removelist:
            index = self._window.courses_model.courses.index(elem)
            self._window.courses_model.removeRows(index, 1)

    @Slot()
    def dumpUser(self):
        # we don't use the message...
        with open(os.path.join(user_data_dir(self.appname),
                               self.data_fname), 'wb') as f:
            tmp_pw = self.user.password
            self.user.password = ''
            pickle.dump(self.user, f)
            self.user.password = tmp_pw

    @Slot()
    def refreshcourses(self):
        self.status_signal.sig.emit('Searching for online updates...'
                                'this may take a while.')
        if not self.loginthread.isRunning():
            self.loginthread.exiting = False
            self.loginthread.signal_ok.sig.connect(self.do_refreshcourses)
            self.loginthread.start()

    def do_refreshcourses(self):
        self.loginthread.signal_ok.sig.disconnect(self.do_refreshcourses)
        if not self.refreshcoursesthread.isRunning():
            self.refreshcoursesthread.start()

    @Slot()
    def syncfiles(self):
        # we delete the already present downloadthread and recreate it
        # because otherwise it uses the old download folder. I don't know
        # if there's a cleaner approach
        del self.downloadthread
        self.downloadthread = DownloadThread(self.user,
                                             self.settings['RootFolder'],
                                             self)
        self.downloadthread.dumpuser.sig.connect(self.dumpUser)

        self.refreshcoursesthread.finished.connect(self.do_syncfiles)
        self.refreshcourses()

    @Slot()
    def do_syncfiles(self):
        self.refreshcoursesthread.finished.disconnect(self.do_syncfiles)
        self.status_signal.sig.emit('Started syncing.')
        self.downloadthread.start()

    @Slot(str)
    def myStream_message(self, message):
        self._window.status.moveCursor(QTextCursor.End)
        self._window.status.insertPlainText(message + "\n")

    def restore_window(self):
        self._window.setWindowState(self.windowState() & ~Qt.WindowMinimized |
                                Qt.WindowActive)
        self._window.show()

    def createTray(self):
        restoreAction = QAction("&Restore", self, triggered=self.restore_window)
        quitAction = QAction("&Quit", self, triggered=qApp.quit)
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
        self._window.hide()
        event.ignore()

    def about_text(self):
        self._window.label_3 = QLabel()
        self._window.label_3.setTextFormat(Qt.RichText)
        self._window.label_3.setOpenExternalLinks(True)
        self._window.label_3.setLocale(QLocale(QLocale.English,
                                               QLocale.UnitedStates))
        self._window.label_3.setScaledContents(True)
        self._window.label_3.setWordWrap(True)
        text = """
<html>
<head/>
<body>
  <p>poliBeePsync is a program written by Davide Olianas,
released under GNU GPLv3+.</p>
  <p>Feel free to contact me at <a
  href=\"mailto:ubuntupk@gmail.com\">ubuntupk@gmail.com</a> for
  suggestions and bug reports.</p>
  <p>More information is available on the
  <a href=\"http://www.davideolianas.com/polibeepsync\">
  <span style=\" text-decoration: underline; color:#0000ff;\">
  official website</span></a>.
  </p>
</body>
</html>
"""

        self._window.label_3.setText(QApplication.translate("Form", text,
                                                            None))


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
    if args.debug:
        level_name = args.debug
    level = LEVELS.get(level_name, logging.INFO)

    # now get the logger used in the common module and set its level to what
    # we get from sys.argv
    commonlogger.setLevel(level)
    logger.setLevel(level)

    formatter = logging.Formatter('[%(levelname)s] %(name)s %(message)s')

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    commonlogger.addHandler(handler)

    app = QApplication(sys.argv)

    frame = MainWindow()
    # args is defined at the top of this module
    if not args.hidden:
        # Need to fix showing wrong window
        frame.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
