# -*- coding: utf-8 -*-

import os

from PySide2.QtGui import QIcon

from PySide2.QtWidgets import (QApplication,QVBoxLayout, QTabWidget,
                               QTableView,QStyledItemDelegate,
                               QStyleOptionButton, QStyle, QMainWindow,
                               QHeaderView, QProgressBar, QWidget, QHBoxLayout,
                               QStyleOptionProgressBar, QGridLayout, QLabel,
                               QLineEdit, QSpacerItem, QSizePolicy,
                               QPushButton, QSpinBox, QCheckBox, QTextEdit,
                               QDialogButtonBox)
from PySide2.QtCore import (QEvent, Qt, QPoint, QRect, QLocale, QSize,
                            QMetaObject, QFile)

from PySide2.QtUiTools import QUiLoader


class CoursesListView(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

        self.progbar = ProgressBarDelegate(self)
        self.setItemDelegateForColumn(1, CheckBoxDelegate(self))
        self.setItemDelegateForColumn(3, self.progbar)


class ProgressBarDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        progressBar = QProgressBar()
        style = """QProgressBar { color: #546E7A; }
        QProgressBar::chunk { background: #80CBC4;
        }"""

        progressBar.setAlignment(Qt.AlignCenter)
        progressBar.setTextVisible(True)

        progressBar.resize(option.rect.size())
        progressBar.setMinimum(0)
        progressBar.setMaximum(100)

        progressBar.setStyleSheet(style)

        dw = index.data()[0]
        tot = index.data()[1]
        if tot != 0:
            progressBar.setValue(round(dw/tot*100, 2))
        else:
            progressBar.setValue(0)
        progressBar.setFormat("{}/{} MB".format(round(dw/(
            1024*1024), 2), round(tot/(1024*1024), 2)))

        painter.save()
        painter.translate(option.rect.topLeft())
        progressBar.render(painter, QPoint(0, 0))
        painter.restore()


class CheckBoxDelegate(QStyledItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox in every
    cell of the column to which it's applied
    """

    def __init__(self, parent):
        QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        return None

    def paint(self, painter, option, index):
        checked = bool(index.data())
        checkbox = QCheckBox()

        if (index.flags() & Qt.ItemIsEditable) > 0:
            checkbox.setEnabled(True)
        else:
            checkbox.setEnabled(False)

        if checked:
            checkbox.setCheckState(Qt.Checked)
        else:
            checkbox.setCheckState(Qt.Unchecked)

        checkbox.rect = self.getCheckBoxRect(option)

        #checkbox.setCheckState(QStyle.State_Enabled)

        style = '''QCheckBox, QRadioButton {
                color: #546E7A;
            }

            QCheckBox::indicator::unchecked  {
                background-color: #FFFFFF;
                border: 1px solid #536D79;
            }

            QCheckBox::indicator::checked, QTreeView::indicator::checked {
                background-color: qradialgradient(cx:0.5, cy:0.5, fx:0.25, fy:0.15, radius:0.3, stop:0 #80CBC4, stop:1 #FFFFFF);
                border: 1px solid #536D79;
            }


            QCheckBox::indicator:disabled, QRadioButton::indicator:disabled, QTreeView::indicator:disabled {
                background-color: #444444;			/* Not sure what this looks like */
            }

            QCheckBox::indicator::checked:disabled, QRadioButton::indicator::checked:disabled, QTreeView::indicator::checked:disabled {  
                background-color: qradialgradient(cx:0.5, cy:0.5, fx:0.25, fy:0.15, radius:0.3, stop:0 #BBBBBB, stop:1 #444444); /* Not sure what this looks like */
            }

            '''
        checkbox.setStyleSheet(style)

        painter.save()
        painter.translate(option.rect.topLeft())
        checkbox.render(painter, QPoint(0, 0))
        painter.restore()


    def editorEvent(self, event, model, option, index):
        if not (index.flags() & Qt.ItemIsEditable) > 0:
            return False

        # Do not change the checkbox-state
        if event.type() == QEvent.MouseButtonPress:
            return False
        if event.type() == QEvent.MouseButtonRelease or event.type() == QEvent.MouseButtonDblClick:
            if event.button() != Qt.LeftButton or not self.getCheckBoxRect(
                    option).contains(event.pos()):
                return False
            if event.type() == QEvent.MouseButtonDblClick:
                return True
        elif event.type() == QEvent.KeyPress:
            if event.key() != Qt.Key_Space and event.key() != Qt.Key_Select:
                return False
            else:
                return False

        # Change the checkbox-state
        self.setModelData(None, model, index)
        return True

    def setModelData(self, editor, model, index):
        newValue = not bool(index.data())
        model.setData(index, newValue, Qt.EditRole)

    def getCheckBoxRect(self, option):
        check_box_style_option = QStyleOptionButton()
        check_box_rect = QApplication.style().subElementRect(
            QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QPoint(option.rect.x() +
                                 option.rect.width() / 2 -
                                 check_box_rect.width() / 2,
                                 option.rect.y() +
                                 option.rect.height() / 2 -
                                 check_box_rect.height() / 2)
        return QRect(check_box_point, check_box_rect.size())


class Ui_Form(QMainWindow):
    def setupUi(self, Form):
        path = f"{os.path.dirname(__file__)}/new_gui.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self._window = loader.load(ui_file)

        # Need to fix this courses list view
        self._window.coursesView = CoursesListView(self._window.courses_tab)
        self._window.courses_layout.addWidget(self._window.coursesView)
        self._window.coursesView.setObjectName("coursesView")
        self._window.coursesView2.deleteLater()

        self.icon = QIcon(":/icons/uglytheme/polibeepsync.svg")

        self.retranslateUi(self._window)
        self._window.tabWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(self._window)

    def show(self):
        self._window.show()

    def retranslateUi(self, Form):
        self._window.label_2.setText(QApplication.translate("Form", "Password",
                                                            None))
        self._window.label.setText(QApplication.translate("Form", "User code",
                                                          None))
        self._window.trylogin.setText(
            QApplication.translate("Form", "Try logging in", None))
        self._window.check_version.setText(
            QApplication.translate("Form", "Check for new version", None))
        self._window.statusbar.showMessage(
            QApplication.translate("Form", "Login successful", None))
        self._window.label_4.setText(
            QApplication.translate("Form", "Root folder", None))
        self._window.changeRootFolder.setText(
            QApplication.translate("Form", "Change", None))
        self._window.label_5.setText(QApplication.translate("Form",
                                                            "Sync every",
                                                            None))
        self._window.label_6.setText(QApplication.translate("Form",
                                                            "minutes", None))
        self._window.syncNow.setText(QApplication.translate("Form",
                                                            "Sync now", None))
        self._window.addSyncNewCourses.setText(QApplication.translate("Form",
                                                              "Automatically add and sync new available courses",
                                                              None))
        self._window.tabWidget.setTabText(self._window.tabWidget.indexOf(self._window.settings_tab),
                                  QApplication.translate("Form",
                                                         "Settings",
                                                         None))
        self._window.refreshCourses.setText(
            QApplication.translate("Form", "Refresh list", None))
        self._window.tabWidget.setTabText(self._window.tabWidget.indexOf(self._window.courses_tab),
                                  QApplication.translate("Form", "Courses",
                                                         None))
        self._window.about.setText(QApplication.translate("Form", "About", None))
        self._window.tabWidget.setTabText(self._window.tabWidget.indexOf(self._window.status_tab),
                                  QApplication.translate("Form", "Status",
                                                         None))
        self._window.tabWidget.setTabText(self._window.tabWidget.indexOf(self._window.plugins_tab),
                                  QApplication.translate("Form", "Plugins",
                                                         None))



from polibeepsync import icone_rc
