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

__version__ = 0.1

from requests import ConnectionError, Timeout

from polibeepsync.common import User, InvalidLoginError
import platform
import PySide
from PySide.QtCore import *
from PySide.QtGui import (QApplication, QMainWindow, QWidget,
                           QMenuBar, QMenu, QStatusBar, QAction,
                           QIcon, QFileDialog, QMessageBox, QFont,
                           QVBoxLayout, QLabel, QLineEdit, QSystemTrayIcon,
                            qApp, QDialog, QPixmap, QTextEdit, QTableView,
                            QTextCursor)

from ui_resizable import Ui_Form


class MyStream(QObject):
    message = Signal(str)
    def __init__(self, parent=None):
        super(MyStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))

    def flush(self):
        pass

class CoursesListModel(QAbstractTableModel):
    def __init__(self, courses):
        QAbstractTableModel.__init__(self)
        # il mio è un mapping, mentre con tableview viene più comodo avere indici
        self.courses = list(courses)

    def rowCount(self, parent=QModelIndex()):
        return len(self.courses)

    def columnCount(self, parent=QModelIndex()):
        return 3

    def insertRows(self, position, rows, newcourse, parent= QModelIndex()):
        self.beginInsertRows(parent, position, position + rows -1)
        for row in range(rows):
            self.courses.insert(position, newcourse)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent = QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows -1)
        for row in range(rows):
            del self.courses[position]
        self.endRemoveRows()
        return True

    def flags(self, index):
        if index.column() == 2:
            flags = Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
            return flags
        elif index.column() == 1:
            flags = Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable\
            | Qt.ItemIsUserCheckable
            return flags
        else: return Qt.ItemIsEnabled

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            if index.column() == 2:
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

class MainWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.w = QWidget()
        self.createTray()
        self.about.clicked.connect(self.about_box)
        self.license.clicked.connect(self.license_box)



    @Slot(str)
    def myStream_message(self, message):
        self.status.moveCursor(QTextCursor.End)
        self.status.insertPlainText(message + "\n\n")

    def createTray(self):
        restoreAction = QAction("&Restore", self, triggered=self.showNormal)
        quitAction = QAction("&Quit", self, triggered=qApp.quit)
        icon =  PySide.QtGui.QIcon(':/newPrefix/polibeep.svg')
        trayIconMenu = QMenu()
        trayIconMenu.addAction(restoreAction)
        trayIconMenu.addAction(quitAction)
        trayIcon = QSystemTrayIcon(icon, self.w)
        trayIcon.setContextMenu(trayIconMenu)
        trayIcon.show()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def about_box(self):
        Dialog = QDialog()
        Dialog.setObjectName("Dialog")
        Dialog.resize(379, 161)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/newPrefix/polibeep-black.svg"), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        verticalLayout = QVBoxLayout(Dialog)
        verticalLayout.setObjectName("verticalLayout")
        label = QLabel(Dialog)
        label.setTextFormat(Qt.RichText)
        label.setOpenExternalLinks(True)
        label.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        label.setScaledContents(True)
        label.setWordWrap(True)
        label.setObjectName("label")
        verticalLayout.addWidget(label)
        text = "<html><head/><body><p>poliBeePsync version {}.</p><p>poliBeePsync is a program written by Davide Olianas, released under GNU GPLv3+.</p><p><br/></p><p>More information is available on the <a href=\"http://www.davideolianas.com/polibeepsync\"><span style=\" text-decoration: underline; color:#0000ff;\">official website</span></a>.</p></body></html>".format(__version__)
        Dialog.setWindowTitle(QApplication.translate("Dialog", "About poliBeePsync", None, QApplication.UnicodeUTF8))
        label.setText(QApplication.translate("Dialog", text, None, QApplication.UnicodeUTF8))
        Dialog.exec_()

    def license_box(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        par = os.path.abspath(os.path.join(dir, os.pardir))
        lic = os.path.join(par, 'gpl.txt')
        with open(lic, 'rt') as f:
            text = f.read()
        Dialog = QDialog()
        Dialog.resize(600, 500)
        Dialog.setWindowTitle("License")
        layout = QVBoxLayout(Dialog)
        textEdit = QTextEdit(Dialog)
        layout.addWidget(textEdit)
        textEdit.setText(text)
        Dialog.exec_()



if __name__ == '__main__':
    from appdirs import user_config_dir, user_data_dir
    import os
    import pickle
    import sys

    import filesettings

    app = QApplication(sys.argv)
    appname = "poliBeePsync"
    frame = MainWindow()
    frame.show()
    settings_fname = 'pbs-settings.ini'
    data_fname = 'pbs.data'
    myStream = MyStream()
    myStream.message.connect(frame.myStream_message)
    sys.stdout = myStream


    for path in [user_config_dir(appname), user_data_dir(appname)]:
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as err:
            if not os.path.isdir(path):
                frame.myStream_message(str(err))

    settings_path = os.path.join(user_config_dir(appname), settings_fname)
    settings = filesettings.settingsFromFile(settings_path)

    def notifynewslot(state):
        if state == 2:
            settings['NotifyNewCourses'] = 'yes'
        else:
            settings['NotifyNewCourses'] = 'no'
        filesettings.settingsToFile(settings, settings_path)

    def syncnewslot(state):
        if state == 2:
            settings['SyncNewCourses'] = 'yes'
        else:
            settings['SyncNewCourses'] = 'no'
        filesettings.settingsToFile(settings, settings_path)

    def updateminuteslot(minutes):
        settings['UpdateEvery'] = str(minutes)
        filesettings.settingsToFile(settings, settings_path)

    def rootfolderslot(path):
        settings['RootFolder'] = path
        filesettings.settingsToFile(settings, settings_path)

    def chooserootdir():
        currentdir = settings['RootFolder']
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        newroot =  QFileDialog.getExistingDirectory(None,
            "Open Directory", currentdir, flags)
        if newroot != "":
            settings['RootFolder'] = str(newroot)
            filesettings.settingsToFile(settings, settings_path)
            frame.rootfolder.setText(newroot)

    def setusercode():
        newcode = frame.userCode.text()
        user.username = newcode
        try:
            dumpUser()
            frame.myStream_message(
                "User code changed to {}.".format(newcode))
        except Exception as err:
            frame.myStream_message(str(err))


    def setpassword():
        newpass = frame.password.text()
        user.password = newpass
        try:
            dumpUser()
            frame.myStream_message("Password changed.")
        except Exception as err:
            frame.myStream_message(str(err))

    def dumpUser():
        with open(os.path.join(user_data_dir(appname), data_fname), 'wb') as f:
            pickle.dump(user, f)

    def testlogin():
        frame.login_attempt.setStyleSheet("color: rgba(0, 0, 0, 255);")
        try:
            user.logout()
            user.login()
            if user.logged == True:
                frame.login_attempt.setText("Login successful.")
                frame.myStream_message("Logged in.")
        except IndexError:
            frame.login_attempt.setText("You're already logged in.")
            frame.myStream_message("You're already logged in.")
        except InvalidLoginError:
            user.logout()
            frame.login_attempt.setText("Login failed.")
            frame.myStream_message("Login failed.")
        except ConnectionError as err:
            user.logout()
            frame.login_attempt.setText("I can't connect to the server. Is the Internet connection working?")
            #frame.myStream_message(str(err) + "\nThis usually means that the Internet connection is not working.")
        except Timeout as err:
            user.logout()
            frame.login_attempt.setText("The timeout time has been reached. Is the Internet connection working?")
            #frame.myStream_message(str(err) + "\nThis usually means that the Internet connection is not working.")
        except Exception as err:
            frame.login_attempt.setText("An error occurred. See the *status* tab.")
            frame.myStream_message(str(err))

    def refreshcourses():
        testlogin()
        most_recent = user.get_online_courses()
        last = user.available_courses
        new = most_recent -last
        removable = last - most_recent
        print('The following courses have been removed because they '
              'aren\'t available online: {}'.format(removable))
        for course in new:
            course.save_folder_name = course.simplify_name(course.name)
            print('A new course was found: {}'.format(course))
        user.sync_available_courses(most_recent)
        dumpUser()
        for course in new:
            frame.courses_model.insertRows(0, 1, course)
        for course in removable:
            index = frame.courses_model.courses.index(course)
            frame.courses_model.removeRows(index, 1)

    def syncfiles():
        topdir = settings['RootFolder']

        for course in user.available_courses:
            subdir = course.save_folder_name
            if course.sync == True:
                outdir = os.path.join(topdir, subdir)
                os.makedirs(outdir, exist_ok=True)
                rootdir = user.find_files_and_folders(course.documents_url,
                                                      'root')
                user.save_files(rootdir, outdir)
            text = "Synced files for {}".format(course.name)
            frame.myStream_message(text)


    frame.rootfolder.setText(settings['RootFolder'])
    frame.rootfolder.textChanged.connect(rootfolderslot)

    if settings['NotifyNewCourses'] == str(True):
        notify_new = Qt.Checked
    else:
        notify_new = Qt.Unchecked

    if settings['SyncNewCourses'] == str(True):
        sync_new = Qt.Checked
    else:
        sync_new = Qt.Unchecked

    frame.notifyNewCourses.setCheckState(notify_new)
    frame.notifyNewCourses.stateChanged.connect(notifynewslot)

    frame.addSyncNewCourses.setCheckState(sync_new)
    frame.addSyncNewCourses.stateChanged.connect(syncnewslot)

    frame.timerMinutes.setValue(int(settings['UpdateEvery']))
    frame.timerMinutes.valueChanged.connect(updateminuteslot)

    frame.changeRootFolder.clicked.connect(chooserootdir)

    try:
        with open(os.path.join(user_data_dir(appname), data_fname), 'rb') as f:
            user = pickle.load(f)
            frame.myStream_message("Data has been loaded successfully.")
    except FileNotFoundError as err:
        user = User('', '')
        complete_message = str(err) + " ".join([
"\nThis error means that no data can be found in the predefined",
"directory. Ignore this if you're using poliBeePsync for the first",
" time."])
        frame.myStream_message(complete_message)
    except Exception as err:
        user = User('', '')
        frame.myStream_message(str(err))

    frame.userCode.setText(str(user.username))
    frame.userCode.textEdited.connect(setusercode)
    frame.password.setText(user.password)
    frame.password.textEdited.connect(setpassword)
    frame.trylogin.clicked.connect(testlogin)

    frame.courses_model = CoursesListModel(user.available_courses)
    frame.coursesView.setModel(frame.courses_model)
    frame.refreshCourses.clicked.connect(refreshcourses)
    frame.courses_model.dataChanged.connect(dumpUser)
    frame.syncNow.clicked.connect(syncfiles)








    sys.exit(app.exec_())
