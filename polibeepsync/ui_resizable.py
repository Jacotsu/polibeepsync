# -*- coding: utf-8 -*-

import os

from PySide2.QtGui import QIcon, QRegion

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
        if parent:
            self.setStyleSheet(parent.styleSheet())
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        header.setStyleSheet(self.styleSheet())

        self.setItemDelegateForColumn(1, CheckBoxDelegate(self))
        self.setItemDelegateForColumn(3, ProgressBarDelegate(self))


class ProgressBarDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        progressBar = QProgressBar()

        progressBar.setAlignment(Qt.AlignCenter)
        progressBar.setTextVisible(True)

        progressBar.resize(option.rect.size())
        progressBar.setMinimum(0)
        progressBar.setMaximum(100)

        if self.parent():
            progressBar.setStyleSheet(self.parent().styleSheet())

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

        # Implement tristate checkboxe for folder nodes
        if checked:
            checkbox.setCheckState(Qt.Checked)
        else:
            checkbox.setCheckState(Qt.Unchecked)

        if self.parent():
            checkbox.setStyleSheet(self.parent().styleSheet())

        width = option.widget.columnWidth(1)
        height = option.widget.rowHeight(0)

        painter.save()
        painter.translate(option.rect.topLeft())
        checkbox.rect = option.rect
        checkbox.setFixedSize(width, height)
        checkbox.render(painter, QPoint(0, 0))
        painter.restore()

    def editorEvent(self, event, model, option, index):
        if index.flags() & Qt.ItemIsEditable:
            if event.type() == QEvent.MouseButtonRelease:
                self.setModelData(None, model, index)
                return True
            elif event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key_Space:
                    self.setModelData(None, model, index)
                    return True

        return False

    # Toggles the checkbox
    def setModelData(self, editor, model, index):
        newValue = not bool(index.data())
        model.setData(index, newValue, Qt.EditRole)


class Ui_Form(QMainWindow):
    def setupUi(self, Form):
        path = f"{os.path.dirname(__file__)}/new_gui.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self._window = loader.load(ui_file)

        # Set courses_tab stylesheet so that delegates can inherit it
        self._window.courses_tab.setStyleSheet(self._window.styleSheet())

        # Need to fix this courses list view
        self._window.coursesView = CoursesListView(self._window.courses_tab)
        self._window.courses_layout.addWidget(self._window.coursesView)
        self._window.coursesView.setObjectName("coursesView")
        self._window.coursesView2.deleteLater()

        self.icon = QIcon(":/root/imgs/icons/polibeepsync.svg")

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
        #self._window.tabWidget.setTabText(self._window.tabWidget.indexOf(self._window.plugins_tab),
        #                          QApplication.translate("Form", "Plugins",
        #                                                 None))



from polibeepsync import icone_rc
