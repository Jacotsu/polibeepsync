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
from PySide.QtCore import QRect, QMetaObject, QObject
from PySide.QtGui  import (QApplication, QMainWindow, QWidget,
                           QGridLayout, QTabWidget, QPlainTextEdit,
                           QMenuBar, QMenu, QStatusBar, QAction,
                           QIcon, QFileDialog, QMessageBox, QFont,
                           QVBoxLayout, QLabel, QLineEdit, )


import sys
#import os

# http://stackoverflow.com/questions/13299283/folder-browser-dialog-in-qt

guy = User('111','111')

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(1000, 600)
        centralwidget = QWidget(self)
        gridLayout = QGridLayout(centralwidget)
        tabWidget = QTabWidget(centralwidget)
        tab = QWidget()
        #font = QFont()
        #font.setFamily("Courier 10 Pitch")
        #font.setPointSize(12)
        #self.tab.setFont(font)
        tabWidget.addTab(tab, "")
        tab_2 = QWidget()
        #self.tab_2.setFont(font)
        tablayout = QVBoxLayout(tab)
        userlabel = QLabel()
        userlabel.setText("User code")
        passwordlabel = QLabel()
        passwordlabel.setText("Password")
        usertext = QLineEdit()
        passwordtext = QLineEdit()
        passwordtext.setEchoMode(QLineEdit.Password)
        loginlayout = QGridLayout()
        loginlayout.addStre
        loginlayout.addWidget(userlabel, 0, 0)
        loginlayout.addWidget(passwordlabel, 1, 0)
        loginlayout.addWidget(usertext, 0, 1)
        loginlayout.addWidget(passwordtext, 1,1)
        tablayout.addLayout(loginlayout)


        gridLayout_2 = QGridLayout(tab_2)
        tabWidget.addTab(tab_2, "")
        gridLayout.addWidget(tabWidget, 0, 0, 1, 1)
        self.setCentralWidget(centralwidget)
        self.setWindowTitle("poliBeePsync")
        tabWidget.setTabText(tabWidget.indexOf(tab),\
                                   "General")
        tabWidget.setTabText(tabWidget.indexOf(tab_2),\
                                   "Courses")


        #menu_File.setTitle("&File")
        #self.menu_Solve.setTitle("&Solve")
        #self.menu_Help.setTitle("&Help")
        #self.tabWidget.setCurrentIndex(0)
        #self.action_New.setText("&New")
        #self.action_Open.setText("&Open")
        #self.actionSave_As.setText("Save &As")
        #self.action_Save.setText("&Save")
        #self.action_Quit.setText("&Quit")
        #self.action_Solve.setText("&Solve")
        #self.action_About.setText("&About")
        #self.action_CCPL.setText("&CCPL")
        #self.action_Help.setText("&Help")
        #self.action_Quit.triggered.connect(self.close)
        #allToolBar = self.addToolBar("AllToolBar")
        #allToolBar.setObjectName("AllToolBar")
        #self.addActions(allToolBar, (self.action_Open, self.actionSave_As,\
        #                self.action_Save, self.action_Solve,\
        #                self.action_Quit ))
        #self.action_New.triggered.connect(self.fileNew)
        #self.action_Open.triggered.connect(self.fileOpen)
        #self.actionSave_As.triggered.connect(self.fileSaveAs)
        #self.action_Save.triggered.connect(self.fileSave)
        #self.action_Solve.triggered.connect(self.trussSolve)
        #self.action_About.triggered.connect(self.aboutBox)
        #self.action_CCPL.triggered.connect(self.displayCCPL)

#    def okToContinue(self):
#        if self.dirty:
#            reply = QMessageBox.question(self,
#                    "Data Loader - Unsaved Changes",
#                    "Save unsaved changes?",
#                    QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
##            if reply == QMessageBox.Cancel:
#                return False
#            elif reply == QMessageBox.Yes:
#                self.clearDirty()
#                return self.fileSave()
#        return True



    def aboutBox(self):
        '''Popup a box with about message.'''
        QMessageBox.about(self, "About poliBeePsync",
                """<b>Sync files from BeeP.</b>
                <p>Copyright &copy; 2014 Davide Olianas.
                Released under GNU GPLv3+.</p>
                <p>poliBeePsync {} - Python {} -  PySide version {} - Qt version {} on\
                {}""".format() % (__version__, platform.python_version(),
                PySide.__version__,  PySide.QtCore.__version__,
                platform.system()))

    #def display_license(self):
        #with open('') as f:
            #self.plainTextEdit.setPlainText(open('CCPL.txt').read())
            #self.filename = 'LICENSE.txt'
            #self.updateStatus('License displayed.')


# aggiorna titolo e barra di stato
#    def updateStatus(self, message):
#        '''Keep status current.'''
#        if self.filename is not None:
#            flbase = os.path.basename(self.filename)
#            self.setWindowTitle(unicode("Truss Analysis - " +\
#                                         flbase + "[*]") )
#            self.statusBar().showMessage(message, 5000)
#            self.setWindowModified(self.dirty)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    sys.exit(app.exec_())
