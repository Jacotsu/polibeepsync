# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/davide/qwidgetresizegiusto.ui'
#
# Created: Wed Dec 24 12:30:44 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from PySide.QtGui import *
from PySide.QtCore import *


class CoursesListView(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        self.setItemDelegateForColumn(1, CheckBoxDelegate(self))


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
        check_box_style_option = QStyleOptionButton()

        if (index.flags() & Qt.ItemIsEditable) > 0:
            check_box_style_option.state |= QStyle.State_Enabled
        else:
            check_box_style_option.state |= QStyle.State_ReadOnly

        if checked:
            check_box_style_option.state |= QStyle.State_On
        else:
            check_box_style_option.state |= QStyle.State_Off

        check_box_style_option.rect = self.getCheckBoxRect(option)

        check_box_style_option.state |= QStyle.State_Enabled

        QApplication.style().drawControl(QStyle.CE_CheckBox, check_box_style_option, painter)

    def editorEvent(self, event, model, option, index):
        if not (index.flags() & Qt.ItemIsEditable) > 0:
            return False

        # Do not change the checkbox-state
        if event.type() == QEvent.MouseButtonPress:
          return False
        if event.type() == QEvent.MouseButtonRelease or event.type() == QEvent.MouseButtonDblClick:
            if event.button() != Qt.LeftButton or not self.getCheckBoxRect(option).contains(event.pos()):
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
        check_box_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QPoint (option.rect.x() +
                            option.rect.width() / 2 -
                            check_box_rect.width() / 2,
                            option.rect.y() +
                            option.rect.height() / 2 -
                            check_box_rect.height() / 2)
        return QRect(check_box_point, check_box_rect.size())



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(598, 450)
        self.icon = QIcon(":/icons/uglytheme/48x48/polibeepsync.png")
        Form.setWindowIcon(self.icon)
        Form.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout = QtGui.QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.password = QtGui.QLineEdit(self.tab)
        self.password.setMaximumSize(QtCore.QSize(139, 16777215))
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 3, 1, 1, 1)
        self.userCode = QtGui.QLineEdit(self.tab)
        self.userCode.setMaximumSize(QtCore.QSize(139, 16777215))
        self.userCode.setText("")
        self.userCode.setObjectName("userCode")
        self.gridLayout.addWidget(self.userCode, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.trylogin = QtGui.QPushButton(self.tab)
        self.trylogin.setMaximumSize(QtCore.QSize(154, 16777215))
        self.trylogin.setObjectName("trylogin")
        self.verticalLayout_2.addWidget(self.trylogin)
        self.login_attempt = QtGui.QLabel(self.tab)
        self.login_attempt.setText("Logging in, please wait.")
        self.login_attempt.setStyleSheet("color: rgba(0, 0, 0, 0);")
        self.login_attempt.setObjectName("login_attempt")
        self.verticalLayout_2.addWidget(self.login_attempt)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.rootfolder = QtGui.QLineEdit(self.tab)
        self.rootfolder.setMinimumSize(QtCore.QSize(335, 0))
        self.rootfolder.setMaximumSize(QtCore.QSize(335, 16777215))
        self.rootfolder.setInputMask("")
        self.rootfolder.setReadOnly(True)
        self.rootfolder.setObjectName("rootfolder")
        self.horizontalLayout_3.addWidget(self.rootfolder)
        self.changeRootFolder = QtGui.QPushButton(self.tab)
        self.changeRootFolder.setObjectName("changeRootFolder")
        self.horizontalLayout_3.addWidget(self.changeRootFolder)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.timerMinutes = QtGui.QSpinBox(self.tab)
        self.timerMinutes.setObjectName("timerMinutes")
        self.horizontalLayout_5.addWidget(self.timerMinutes)
        self.label_6 = QtGui.QLabel(self.tab)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.syncNow = QtGui.QPushButton(self.tab)
        self.syncNow.setObjectName("syncNow")
        self.horizontalLayout_5.addWidget(self.syncNow)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.addSyncNewCourses = QtGui.QCheckBox(self.tab)
        self.addSyncNewCourses.setObjectName("addSyncNewCourses")
        self.verticalLayout_2.addWidget(self.addSyncNewCourses)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.refreshCourses = QtGui.QPushButton(self.tab_2)
        self.refreshCourses.setObjectName("refreshCourses")
        self.horizontalLayout_6.addWidget(self.refreshCourses)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.coursesView = CoursesListView(self.tab_2)
        self.coursesView.setObjectName("coursesView")
        self.verticalLayout_3.addWidget(self.coursesView)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.tab_3)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.about = QtGui.QPushButton(self.tab_3)
        self.about.setObjectName("about")
        self.horizontalLayout_8.addWidget(self.about)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem5)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.status = QtGui.QTextEdit(self.tab_3)
        self.status.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.status.setObjectName("status")
        self.verticalLayout_4.addWidget(self.status)
        self.horizontalLayout_7.addLayout(self.verticalLayout_4)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.okButton = QtGui.QDialogButtonBox(Form)
        self.okButton.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.okButton.setObjectName("okButton")
        self.okButton.clicked.connect(self.hide)
        self.verticalLayout.addWidget(self.okButton)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("poliBeePsync")
        self.label_2.setText(QtGui.QApplication.translate("Form", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "User code", None, QtGui.QApplication.UnicodeUTF8))
        self.trylogin.setText(QtGui.QApplication.translate("Form", "Try login credentials", None, QtGui.QApplication.UnicodeUTF8))
        self.login_attempt.setText(QtGui.QApplication.translate("Form", "Login successful", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Root folder", None, QtGui.QApplication.UnicodeUTF8))
        self.changeRootFolder.setText(QtGui.QApplication.translate("Form", "Change", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Sync every", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Form", "minutes", None, QtGui.QApplication.UnicodeUTF8))
        self.syncNow.setText(QtGui.QApplication.translate("Form", "Sync now", None, QtGui.QApplication.UnicodeUTF8))
        self.addSyncNewCourses.setText(QtGui.QApplication.translate("Form", "Automatically add and sync new available courses", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Form", "General settings", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshCourses.setText(QtGui.QApplication.translate("Form", "Refresh list", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Form", "Courses", None, QtGui.QApplication.UnicodeUTF8))
        self.about.setText(QtGui.QApplication.translate("Form", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("Form", "Status", None, QtGui.QApplication.UnicodeUTF8))

from polibeepsync import icone_rc
