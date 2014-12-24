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

from polibeepsync import User
import platform
import PySide
from PySide.QtCore import *
from PySide.QtGui import (QApplication, QMainWindow, QWidget,
                           QMenuBar, QMenu, QStatusBar, QAction,
                           QIcon, QFileDialog, QMessageBox, QFont,
                           QVBoxLayout, QLabel, QLineEdit, QSystemTrayIcon,
                            qApp, QDialog, QPixmap, QTextEdit, QTableView,
                            QStyledItemDelegate, QStyleOptionButton, QStyle)




class CoursesListModel(QAbstractTableModel):
    def __init__(self, courses):
        QAbstractTableModel.__init__(self)
        # il mio è un mapping, mentre con tableview viene più comodo avere indici
        self.courses = list(courses)

    def rowCount(self, parent=QModelIndex()):
        return len(self.courses)

    def columnCount(self, parent=QModelIndex()):
        return 3

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


if __name__ == '__main__':
    from appdirs import user_config_dir, user_data_dir
    import os
    import pickle
    import sys
    from ui_resizable import Ui_Form
    import filesettings

    class MainWindow(QWidget, Ui_Form):
        def __init__(self, parent=None):
            super(MainWindow, self).__init__(parent)
            self.setupUi(self)
            self.w = QWidget()
            self.createTray()
            self.about.clicked.connect(self.about_box)
            self.license.clicked.connect(self.license_box)

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

    app = QApplication(sys.argv)
    frame = MainWindow()
    appname = "poliBeePsync"
    settings_fname = 'pbs-settings.ini'
    data_fname = 'pbs.data'

    for path in [user_config_dir(appname), user_data_dir(appname)]:
        try:
            os.makedirs(path, exist_ok=True)
        except OSError:
            if not os.path.isdir(path):
                raise

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




    #with open(os.path.join(user_data_dir(appname), data_fname), 'rb') as f:
    #    try:
    #guy = pickle.load(f)

    #frame.usercode.setText(str(guy.username))
    #frame.password.setText(guy.password)
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

    with open(os.path.join(user_data_dir(appname), data_fname), 'rb') as f:
        user = pickle.load(f)

    frame.courses_model = CoursesListModel(user.available_courses)
    frame.coursesView.setModel(frame.courses_model)










    frame.show()
    app.exec_()
    #sys.exit(app.exec_())
    # popolare gui con  rootfolder, everyminutes, notfiy_new, automatically_add
    #    except:
    #        print('An error has occurred.')
    #        raise