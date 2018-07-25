# -*- coding: utf-8 -*-

pysideVersion = '0.0.0'
try:
    from PySide.QtGui import (QTableView, QStyledItemDelegate, QStyleOptionButton,
                              QStyle, QApplication, QIcon, QVBoxLayout, QTabWidget,
                              QWidget, QHBoxLayout, QStyleOptionProgressBarV2,
                              QGridLayout, QLabel, QLineEdit, QSpacerItem,
                              QSizePolicy, QPushButton,
                              QSpinBox, QCheckBox, QTextEdit, QDialogButtonBox)
    from PySide.QtCore import (QEvent, Qt, QPoint, QRect, QLocale, QSize,
                               QMetaObject)
    import PySide
    pysideVersion = PySide.__version__
except ImportError:
    from PySide2.QtGui import (   QIcon, )

    from PySide2.QtWidgets import (QApplication,QVBoxLayout, QTabWidget,QTableView,QStyledItemDelegate, QStyleOptionButton,
                              QStyle,
                              QWidget, QHBoxLayout, QStyleOptionProgressBar,
                              QGridLayout, QLabel, QLineEdit, QSpacerItem,
                              QSizePolicy, QPushButton,
                              QSpinBox, QCheckBox, QTextEdit, QDialogButtonBox)
    from PySide2.QtCore import (QEvent, Qt, QPoint, QRect, QLocale, QSize,
                               QMetaObject)
    import PySide2
    pysideVersion = PySide2.__version__


class CoursesListView(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        self.progbar = ProgressBarDelegate(self)
        self.setItemDelegateForColumn(1, CheckBoxDelegate(self))
        self.setItemDelegateForColumn(3, self.progbar)


class ProgressBarDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        progressBar = None
        if pysideVersion == '1.2.2':
            progressBar = QStyleOptionProgressBarV2()
            progressBar.state = QStyle.State_Enabled
        else:
            progressBar = QStyleOptionProgressBar()
            progressBar.state = QStyle.State_Enabled
        progressBar.direction = QApplication.layoutDirection()
        progressBar.fontMetrics = QApplication.fontMetrics()
        progressBar.rect = option.rect
        progressBar.minimum = 0
        progressBar.maximum = 100
        progressBar.textAlignment = Qt.AlignCenter
        progressBar.textVisible = True
        dw = index.data()[0]
        tot = index.data()[1]
        if tot != 0:
            progressBar.progress = round(dw/tot*100, 2)
        else:
            progressBar.progress = 0
        progressBar.text = "{} MB of {} MB".format(round(dw/(
            1024*1024), 2), round(tot/(1024*1024), 2))
        QApplication.style().drawControl(QStyle.CE_ProgressBar, progressBar,
                                     painter)


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

        QApplication.style().drawControl(QStyle.CE_CheckBox,
                                         check_box_style_option, painter)

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


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(598, 450)
        self.icon = QIcon(":/icons/uglytheme/48x48/polibeepsync.png")
        Form.setWindowIcon(self.icon)
        Form.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")

        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")

        # Tab General Settings
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout = QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label = QLabel(self.tab)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.password = QLineEdit(self.tab)
        self.password.setMaximumSize(QSize(139, 16777215))
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 3, 1, 1, 1)
        self.userCode = QLineEdit(self.tab)
        self.userCode.setMaximumSize(QSize(139, 16777215))
        self.userCode.setText("")
        self.userCode.setObjectName("userCode")
        self.gridLayout.addWidget(self.userCode, 1, 1, 1, 1)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding,
                                 QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.trylogin = QPushButton(self.tab)
        self.trylogin.setMaximumSize(QSize(154, 16777215))
        self.trylogin.setObjectName("trylogin")
        self.verticalLayout_2.addWidget(self.trylogin)
        self.login_attempt = QLabel(self.tab)
        self.login_attempt.setText("Logging in, please wait.")
        self.login_attempt.setStyleSheet("color: rgba(0, 0, 0, 0);")
        self.login_attempt.setObjectName("login_attempt")
        self.verticalLayout_2.addWidget(self.login_attempt)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum,
                                  QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.rootfolder = QLineEdit(self.tab)
        self.rootfolder.setMinimumSize(QSize(335, 0))
        self.rootfolder.setMaximumSize(QSize(335, 16777215))
        self.rootfolder.setInputMask("")
        self.rootfolder.setReadOnly(True)
        self.rootfolder.setObjectName("rootfolder")
        self.horizontalLayout_3.addWidget(self.rootfolder)
        self.changeRootFolder = QPushButton(self.tab)
        self.changeRootFolder.setObjectName("changeRootFolder")
        self.horizontalLayout_3.addWidget(self.changeRootFolder)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding,
                                  QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.timerMinutes = QSpinBox(self.tab)
        self.timerMinutes.setObjectName("timerMinutes")
        self.horizontalLayout_5.addWidget(self.timerMinutes)
        self.label_6 = QLabel(self.tab)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.syncNow = QPushButton(self.tab)
        self.syncNow.setObjectName("syncNow")
        self.horizontalLayout_5.addWidget(self.syncNow)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding,
                                  QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.addSyncNewCourses = QCheckBox(self.tab)
        self.addSyncNewCourses.setObjectName("addSyncNewCourses")
        self.verticalLayout_2.addWidget(self.addSyncNewCourses)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.tabWidget.addTab(self.tab, "")

        # Tab Courses
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_2 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.refreshCourses = QPushButton(self.tab_2)
        self.refreshCourses.setObjectName("refreshCourses")
        self.horizontalLayout_6.addWidget(self.refreshCourses)
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding,
                                  QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.coursesView = CoursesListView(self.tab_2)
        self.coursesView.setObjectName("coursesView")
        self.verticalLayout_3.addWidget(self.coursesView)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tab_2, "")

        # Tab Status
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_7 = QHBoxLayout(self.tab_3)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.about = QPushButton(self.tab_3)
        self.about.setObjectName("about")
        self.horizontalLayout_8.addWidget(self.about)
        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding,
                                  QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem5)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.status = QTextEdit(self.tab_3)
        self.status.setTextInteractionFlags(
            Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)
        self.status.setObjectName("status")
        self.verticalLayout_4.addWidget(self.status)
        self.horizontalLayout_7.addLayout(self.verticalLayout_4)
        self.tabWidget.addTab(self.tab_3, "")

        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout.addWidget(self.tabWidget)

        self.okButton = QDialogButtonBox(Form)
        self.okButton.setStandardButtons(QDialogButtonBox.Ok)
        self.okButton.setObjectName("okButton")
        self.okButton.clicked.connect(self.hide)
        self.verticalLayout.addWidget(self.okButton)

        self.statusLabel = QLabel(Form)
        self.statusLabel.setObjectName("statusLabel")
        self.verticalLayout.addWidget(self.statusLabel)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("poliBeePsync")
        if pysideVersion == '1.2.2':
            self.label_2.setText(QApplication.translate("Form", "Password", None,
                                                        QApplication.UnicodeUTF8))
            self.label.setText(QApplication.translate("Form", "User code", None,
                                                      QApplication.UnicodeUTF8))
            self.trylogin.setText(
                QApplication.translate("Form", "Try login credentials", None,
                                       QApplication.UnicodeUTF8))
            self.login_attempt.setText(
                QApplication.translate("Form", "Login successful", None,
                                       QApplication.UnicodeUTF8))
            self.label_4.setText(
                QApplication.translate("Form", "Root folder", None,
                                       QApplication.UnicodeUTF8))
            self.changeRootFolder.setText(
                QApplication.translate("Form", "Change", None,
                                       QApplication.UnicodeUTF8))
            self.label_5.setText(QApplication.translate("Form", "Sync every", None,
                                                        QApplication.UnicodeUTF8))
            self.label_6.setText(QApplication.translate("Form", "minutes", None,
                                                        QApplication.UnicodeUTF8))
            self.syncNow.setText(QApplication.translate("Form", "Sync now", None,
                                                        QApplication.UnicodeUTF8))
            self.addSyncNewCourses.setText(QApplication.translate("Form",
                                                                  "Automatically add and sync new available courses",
                                                                  None,
                                                                  QApplication.UnicodeUTF8))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),
                                      QApplication.translate("Form",
                                                             "General settings",
                                                             None,
                                                             QApplication.UnicodeUTF8))
            self.refreshCourses.setText(
                QApplication.translate("Form", "Refresh list", None,
                                       QApplication.UnicodeUTF8))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                      QApplication.translate("Form", "Courses",
                                                             None,
                                                             QApplication.UnicodeUTF8))
            self.about.setText(QApplication.translate("Form", "About", None,
                                                      QApplication.UnicodeUTF8))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3),
                                      QApplication.translate("Form", "Status",
                                                             None,
                                                             QApplication.UnicodeUTF8))
        else:
            self.label_2.setText(QApplication.translate("Form", "Password", None))
            self.label.setText(QApplication.translate("Form", "User code", None))
            self.trylogin.setText(
                QApplication.translate("Form", "Try login credentials", None))
            self.login_attempt.setText(
                QApplication.translate("Form", "Login successful", None))
            self.label_4.setText(
                QApplication.translate("Form", "Root folder", None))
            self.changeRootFolder.setText(
                QApplication.translate("Form", "Change", None))
            self.label_5.setText(QApplication.translate("Form", "Sync every", None))
            self.label_6.setText(QApplication.translate("Form", "minutes", None))
            self.syncNow.setText(QApplication.translate("Form", "Sync now", None))
            self.addSyncNewCourses.setText(QApplication.translate("Form",
                                                                  "Automatically add and sync new available courses",
                                                                  None))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),
                                      QApplication.translate("Form",
                                                             "General settings",
                                                             None))
            self.refreshCourses.setText(
                QApplication.translate("Form", "Refresh list", None))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                      QApplication.translate("Form", "Courses",
                                                             None))
            self.about.setText(QApplication.translate("Form", "About", None))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3),
                                      QApplication.translate("Form", "Status",
                                                             None))


from polibeepsync import icone_rc
