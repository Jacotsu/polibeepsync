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
                           QGridLayout, QTabWidget, QPlainTextEdit,
                           QMenuBar, QMenu, QStatusBar, QAction,
                           QIcon, QFileDialog, QMessageBox, QFont,
                           QVBoxLayout, QLabel, QLineEdit, )




# http://stackoverflow.com/questions/13299283/folder-browser-dialog-in-qt






    #def aboutBox(self):
    #    '''Popup a box with about message.'''
    #    QMessageBox.about(self, "About poliBeePsync",
    #            """<b>Sync files from BeeP.</b>
    #            <p>Copyright &copy; 2014 Davide Olianas.
    ##            Released under GNU GPLv3+.</p>
    #            <p>poliBeePsync {} - Python {} -  PySide version {} - Qt version {} on\
    #            {}""".format() % (__version__, platform.python_version(),
    #            PySide.__version__,  PySide.QtCore.__version__,
    #            platform.system()))

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
    from appdirs import user_config_dir, user_data_dir
    import os
    import pickle
    import sys
    import configparser
    from ui_main import Ui_MainWindow


    class MainWindow(QMainWindow, Ui_MainWindow):
        def __init__(self, parent=None):
            super(MainWindow, self).__init__(parent)
            self.setupUi(self)


    appname = "poliBeePsync"
    data_fname = 'pbs.data'
    for path in [user_config_dir(appname), user_data_dir(appname)]:
        try:
            os.makedirs(path, exist_ok=True)
        except OSError:
            if not os.path.isdir(path):
                raise

    settings_fname = 'pbs-settings.ini'
    config = configparser.ConfigParser()
    config.read(os.path.join(user_config_dir(appname), settings_fname))
    try:
        mainsection = config['General']
        update_minutes = mainsection['UpdateEvery']
        root_folder = mainsection['RootFolder']
        notify_new = mainsection.getboolean('NotifyNewCourses')
        sync_new = mainsection.getboolean('SyncNewCourses')

        if type(update_minutes) != int:
            update_minutes = 60

        if notify_new:
            notify_new = Qt.Checked
        else:
            notify_new = Qt.Unchecked

        if sync_new:
            sync_new = Qt.Checked
        else:
            sync_new = Qt.Unchecked


    except KeyError:
        print('cant read file')
        pass

# se facessi così, se manca un valore tutti gli altri vanno a default, che non voglio
# poi voglio controllare valori possibili (minuti: intero, e i due boolean
# invece la cartella viene controllata ogni volta che esegue sync
#        update_minutes = 60
#        root_folder = os.path.join(os.path.expanduser('~'), appname)
#        notify_new =

    with open(os.path.join(user_data_dir(appname), data_fname), 'rb') as f:
        try:
            print(update_minutes)
            guy = pickle.load(f)
            for course in guy.available_courses:
                print(course.name)
            app = QApplication(sys.argv)
            frame = MainWindow()
            frame.usercode.setText(str(guy.username))
            frame.password.setText(guy.password)
            frame.readonlyrootfolder.setText(root_folder)
            frame.notifynewcoursescheckbox.setCheckState(notify_new)
            frame.syncnewcoursescheckbox.setCheckState(sync_new)
            frame.spinBox.setValue(update_minutes)
            frame.show()
            sys.exit(app.exec_())
            # popolare gui con  rootfolder, everyminutes, notfiy_new, automatically_add
        except:
            print('An error has occurred.')
            raise