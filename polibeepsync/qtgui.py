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

import requests
from appdirs import user_config_dir, user_data_dir
import os
import pickle
import sys

from PySide.QtCore import (QThread, QObject, Signal, QAbstractTableModel,
                           QModelIndex, Qt, Slot, QTimer, QLocale)
from PySide.QtGui import (QApplication, QWidget, QTextCursor,
                          QMenu, QAction, QFileDialog,
                          QVBoxLayout, QLabel, QSystemTrayIcon,
                          qApp, QDialog, QCursor)

from polibeepsync.common import User, InvalidLoginError, Folder, Course, \
    DownloadThread, LoginThread, SyncThread, dump_user_to_disk, \
    load_user_from_disk, resource_path
from polibeepsync.cmdlineparser import create_parser
from polibeepsync.widget import Ui_Form
from polibeepsync import filesettings
import re
import logging
import json
import sys

cert_path = resource_path('cacert.pem')

class AboutTabHandler(logging.Handler):
    def __init__(self, how):
        logging.Handler.__init__(self)
        self.callable = how

    def emit(self, record):
        self.callable(record.getMessage())


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


#__version__ = find_version("polibeepsync/version.py")
__version__ = 'fake'  # until I solve a problem related to cx_freeze

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
                total = self.courses[index.row()].total_file_size
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


class MainWindow(QWidget, Ui_Form):
    def __init__(self, debuglevel, parent=None):
        super(MainWindow, self).__init__(parent)
        self.appname = "poliBeePsync"
        self.settings_fname = 'pbs-settings.ini'
        self.data_fname = 'pbs.data'
        self.setupUi(self)
        self.w = QWidget()

        self.about_text()
        self.timer = QTimer(self)

        self.logger = logging.getLogger("polibeepsync.qtgui")
        self.logger.setLevel(debuglevel)
        # now get the logger used in the common module and set its level to what
        # we get from sys.argv
        self.commonlogger = logging.getLogger("polibeepsync.common")
        self.commonlogger.setLevel(debuglevel)

        formatter = logging.Formatter('[%(levelname)s] %(name)s %(message)s')

        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        aboutabhandler = AboutTabHandler(self.myStream_message)
        aboutabhandler.setFormatter(formatter)
        aboutabhandler.setLevel(logging.INFO)

        self.logger.addHandler(handler)
        self.commonlogger.addHandler(handler)

        self.logger.addHandler(aboutabhandler)
        self.commonlogger.addHandler(aboutabhandler)

        # settings_path is a string containing the path to settings
        self.settings_path = None
        # settings is a dictionary of settings
        self.settings = None
        # load_settings() sets settings_path and settings
        self.load_settings()
        self.user = User('', '')
        self.load_data()

        self.timer.timeout.connect(self.syncfiles)
        self.timer.start(1000 * 60 * int(self.settings['UpdateEvery']))

        self.loginthread = LoginThread(self.user)
        self.loginthread.login_status.connect(self.loginstatus)


        self.refreshcoursesthread = SyncThread(self.user)

        self.refreshcoursesthread.new.connect(self.addtocoursesview)
        self.refreshcoursesthread.new.connect(self.syncnewcourses)
        # TODO: quelli passati a syncnewcourses poi dove finiscono? oppure
        # in memoria fanno sempre riferimento agli stessi oggetti quindi in
        # effetti ottengono il valore giusto anche quelli passati a
        # completedrefreshedcourses? -> SI lo ottengono
        # quindi fra le altre cose...i corsi vecchi vengono eliminati? -> su
        #  questo non lo so (si riesce a fare test?)
        self.refreshcoursesthread.complete.connect(
            self.completedrefreshcourses)
        self.refreshcoursesthread.old.connect(self.rmfromcoursesview)

        self.downloadthread = DownloadThread(self.user,
                                             self.settings['RootFolder'])
        self.downloadthread.download_signal.connect(
            self.update_course_download)
        self.downloadthread.initial_sizes.connect(self.setinizialsizes)
        self.downloadthread.data_signal.connect(self.update_file_localtime)
        self.downloadthread.infosignal.connect(self._coursestabinfo)

        self.userCode.setText(str(self.user.username))
        self.userCode.textEdited.connect(self.setusercode)
        self.password.setText(self.user.password)
        self.password.textEdited.connect(self.setpassword)
        self.trylogin.clicked.connect(self.testlogin)

        self.courses_model = CoursesListModel(self.user.available_courses)
        self.coursesView.setModel(self.courses_model)
        self._resizeview()
        self.refreshCourses.clicked.connect(self.refreshcourses)

        self.courses_model.dataChanged.connect(self.dumpUser)
        self.syncNow.clicked.connect(self.syncfiles)
        self.pushButton.clicked.connect(self.syncfiles)
        self.pushButton.clicked.connect(self.inittextincourses)

        if self.settings['SyncNewCourses'] == str(True):
            self.sync_new = Qt.Checked
        else:
            self.sync_new = Qt.Unchecked

        self.rootfolder.setText(self.settings['RootFolder'])
        self.rootfolder.textChanged.connect(self.rootfolderslot)

        self.addSyncNewCourses.setCheckState(self.sync_new)
        self.addSyncNewCourses.stateChanged.connect(self.syncnewslot)

        self.timerMinutes.setValue(int(self.settings['UpdateEvery']))
        self.timerMinutes.valueChanged.connect(self.updateminuteslot)

        self.changeRootFolder.clicked.connect(self.chooserootdir)

        self.version_label.setText("Current version: {}.".format(__version__))
        self.pushButton_2.clicked.connect(self.checknewversion)

        self.trayIconMenu = QMenu()
        self.trayIcon = QSystemTrayIcon(self.icon, self.w)
        self.trayIcon.activated.connect(self._activate_traymenu)
        self.createTray()

        self.user.errorsignal.connect(self._coursestaberror)

    def _coursestabinfo(self, info, **kwargs):
        self.label_7.setText(info)

    def _coursestaberror(self, **kwargs):
        self.label_7.setText('An error occured, look at the Status tab')

    def _resizeview(self, **kwargs):
        self.coursesView.setColumnWidth(3, 160)
        self.coursesView.resizeColumnToContents(1)
        self.coursesView.setColumnWidth(0, 320)

    def inittextincourses(self):
        self.label_7.setText('Started syncing.')

    def checknewversion(self):
        jsonurl = 'https://pypi.python.org/pypi/poliBeePsync/json'
        rawdata = requests.get(jsonurl, verify=cert_path)
        latest = json.loads(rawdata.text)['info']['version']
        self.version_label.setTextFormat(Qt.RichText)
        self.version_label.setOpenExternalLinks(True)
        self.version_label.setLocale(QLocale(QLocale.English,
                                             QLocale.UnitedStates))
        self.version_label.setScaledContents(True)
        self.version_label.setWordWrap(True)
        if latest != __version__:
            newtext = """<p>Current version: {}.<br>
Latest version: {}. </p>
<p>Visit <a href='http://www.davideolianas.com/polibeepsync/index.html#how-to\
-install-upgrade-remove'>here</a> to find out how to upgrade.
""".format(__version__, latest)
        else:
            newtext = "Current version: {} up-to-date.".format(__version__)
        self.version_label.setText(newtext)

    def _update_time(self, folder, file, path_list):
        print('inside ', folder.name)
        print('path_list: ', path_list)
        while len(path_list) > 0:
            namegoto = path_list.pop(0)
            print('namegoto: ', namegoto)
            # perché a volte è vuoto?
            if namegoto != "":
                fakefolder = Folder(namegoto, 'fake')
                print('contained folders: ', folder.folders)
                ind = folder.folders.index(fakefolder)
                goto = folder.folders[ind]
                self._update_time(goto, file, path_list)
        if file in folder.files:
            ind = folder.files.index(file)
            thisfile = folder.files[ind]
            thisfile.local_creation_time = file.local_creation_time
            self.dumpUser()

    def update_file_localtime(self, data, **kwargs):
        course, coursefile, path = data
        rootpath = os.path.join(self.settings['RootFolder'],
                                course.save_folder_name)
        if path.startswith(rootpath):
            partial = path[len(rootpath):]
        path_list = partial.split(os.path.sep)
        self._update_time(course.documents, coursefile, path_list)

    def update_course_download(self, course, **kwargs):
        self.logger.debug('download size updated')
        if course in self.user.available_courses:
            updating = self.user.available_courses[course.name]
            updating.downloaded_size = course.downloaded_size
            row = self.courses_model.courses.index(updating)
            where = self.courses_model.index(row, 3)
            self.courses_model.dataChanged.emit(where, where)
            self.dumpUser()

    def setinizialsizes(self, course, **kwargs):
        if course in self.user.available_courses:
            updating = self.user.available_courses[course.name]
            updating.downloaded_size = course.downloaded_size
            updating.total_file_size = course.total_file_size
            row = self.courses_model.courses.index(updating)
            where = self.courses_model.index(row, 3)
            self.courses_model.dataChanged.emit(where, where)
            self.dumpUser()

    def syncnewcourses(self, course, **kwargs):
        if self.settings['SyncNewCourses'] == 'True':
            course.sync = True

    def load_settings(self):
        for path in [user_config_dir(self.appname),
                     user_data_dir(self.appname)]:
            try:
                os.makedirs(path, exist_ok=True)
            except OSError:
                self.logger.critical('OSError while calling os.makedirs.',
                                exc_info=True)
                self.myStream_message("I couldn't create {}.\nStart"
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
        path = os.path.join(user_data_dir(self.appname), self.data_fname)
        self.user = load_user_from_disk(path)

    def loginstatus(self, message, **kwargs):
        self.login_attempt.setText(message)

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

    def chooserootdir(self):
        currentdir = self.settings['RootFolder']
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        newroot = QFileDialog.getExistingDirectory(None,
                                                   "Open Directory",
                                                   currentdir, flags)
        if newroot != "" and str(newroot) != currentdir:
            self.settings['RootFolder'] = str(newroot)
            filesettings.settingsToFile(self.settings, self.settings_path)
            self.rootfolder.setText(newroot)
            # we delete the already present downloadthread and recreate it
            # because otherwise it uses the old download folder. I don't know
            # if there's a cleaner approach
            del self.downloadthread
            self.downloadthread = DownloadThread(self.user,
                                                 self.settings['RootFolder'])
            self.downloadthread.download_signal.connect(
                self.update_course_download)
            self.downloadthread.initial_sizes.connect(self.setinizialsizes)
            self.downloadthread.data_signal.connect(self.update_file_localtime)
            self.downloadthread.infosignal.connect(self._coursestabinfo)

    def setusercode(self):
        newcode = self.userCode.text()
        self.user.username = newcode
        self.dumpUser()

    def setpassword(self):
        newpass = self.password.text()
        self.user.password = newpass
        self.dumpUser()

    def testlogin(self):
        self.loginthread.start()
        self.login_attempt.setStyleSheet("color: rgba(0, 0, 0, 255);")
        self.login_attempt.setText("Logging in, please wait.")

    def addtocoursesview(self, course, **kwargs):
        self.courses_model.insertRows(0, 1, course)

    def rmfromcoursesview(self, course, **kwargs):
        index = self.courses_model.courses.index(course)
        self.courses_model.removeRows(index, 1)

    def dumpUser(self):
        path = os.path.join(user_data_dir(self.appname), self.data_fname)
        dump_user_to_disk(self.user, path)

    def refreshcourses(self):
        self.label_7.setText('Searching for online updates...this may take a'
                             ' while.')
        self.refreshcoursesthread.start()

    def completedrefreshcourses(self, courses, **kwargs):
        self.user.available_courses = courses
        self.dumpUser()
        self.label_7.setText('Synced with online courses list.')

    @Slot()
    def syncfiles(self):
        # chiamare refreshcoursesthread e quando ha finito lui con i
        # suoi segnali, scaricare
        #self.refreshcoursesthread.start()
        #self.refreshcoursesthread.join()  # ma il join non basta...perché
        #  ci sono gli slot collegati che devono operare prima di poter
        # iniziare il download
        # faccio prima a togliere l'opzione
        self.downloadthread.start()

    @Slot(str)
    def myStream_message(self, message):
        self.status.moveCursor(QTextCursor.End)
        self.status.insertPlainText(message + "\n\n")

    def createTray(self):
        restoreAction = QAction("&Restore", self, triggered=self.showNormal)
        quitAction = QAction("&Quit", self, triggered=qApp.quit)
        self.trayIconMenu.addAction(restoreAction)
        self.trayIconMenu.addAction(quitAction)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.show()


    def _activate_traymenu(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showNormal()
        else:
            self.trayIconMenu.activateWindow()
            self.trayIconMenu.popup(QCursor.pos())

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def about_text(self):
        self.label_3.setTextFormat(Qt.RichText)
        self.label_3.setOpenExternalLinks(True)
        self.label_3.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.label_3.setScaledContents(True)
        self.label_3.setWordWrap(True)
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
        self.label_3.setText(QApplication.translate("Form", text, None,
                                                    QApplication.UnicodeUTF8))


def main():
    # set debug levels
    LEVELS = {
        'notset': logging.NOTSET,
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }
    parser = create_parser()
    args = parser.parse_args()
    level_name = 'info'
    if args.debug:
        level_name = args.debug
    level = LEVELS.get(level_name, logging.NOTSET)

    app = QApplication(sys.argv)
    frame = MainWindow(level)
    if not args.hidden:
        frame.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
