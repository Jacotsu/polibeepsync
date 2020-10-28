# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_gui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import uglytheme_rc

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        if not MainForm.objectName():
            MainForm.setObjectName(u"MainForm")
        MainForm.setWindowModality(Qt.NonModal)
        MainForm.setEnabled(True)
        MainForm.resize(800, 600)
        MainForm.setMinimumSize(QSize(800, 600))
        icon = QIcon()
        icon.addFile(u":/root/imgs/icons/polibeepsync.svg", QSize(), QIcon.Normal, QIcon.Off)
        MainForm.setWindowIcon(icon)
        MainForm.setStyleSheet(u"/* https://github.com/martinrotter/qt-material-stylesheet */\n"
"\n"
"QWidget:window {					/* Borders around the code editor and debug window */\n"
"	border: 0px solid #FFFFFF;\n"
"	background-color: #FFFFFF;\n"
"}\n"
"\n"
"QToolTip {\n"
"	background-color: #80CBC4;\n"
"	color: black;\n"
"    padding: 5px;\n"
"    border-radius: 0;\n"
"    opacity: 200;\n"
"}\n"
"\n"
"/* ==================== Dialog ==================== */\n"
"QLabel {\n"
"	background: transparent;\n"
"	color: #CFD8DC;				/* Not sure about this one */\n"
"}\n"
"\n"
"QDialog, QListView {\n"
"	background-color: #FFFFFF;\n"
"	color: #546E7A;\n"
"	outline: 0;\n"
"	border: 2px solid transparent;\n"
"}\n"
"\n"
"QListView::item:hover {\n"
"	color: #AFBDC4;\n"
"	background: transparent;\n"
"}\n"
"\n"
"\n"
"QListView::item:selected {\n"
"	color: #ffffff;\n"
"	background: transparent;\n"
"}\n"
"\n"
"/* === QTabBar === */\n"
"QTabBar {\n"
"	background: #FFFFFF;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"	background: transparent;	/* Only at the very bottom of t"
                        "he tabs */\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"	background: transparent;\n"
"	border: 0px solid transparent;\n"
"	border-bottom: 2px solid transparent;\n"
"	color: #546E7A;\n"
"	padding-left: 10px;\n"
"	padding-right: 10px;\n"
"	padding-top: 3px;\n"
"	padding-bottom: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"	background-color: transparent;\n"
"	border: 0px solid transparent;\n"
"	border-bottom: 2px solid #80CBC4;\n"
"	color: #AFBDC4;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"	background-color: transparent;\n"
"	border: 0px solid transparent;\n"
"	border-top: none;\n"
"	border-bottom: 2px solid #80CBC4;\n"
"	color: #80CBC4;\n"
"}\n"
"\n"
"QStackedWidget {\n"
"	background: #FFFFFF;	/* This covers a bunch of things, I was thinking about making it transparent, */\n"
"							/* but I would have to find all the other elements... but QTabWidget::pane may be it */\n"
"}\n"
"\n"
"\n"
"/* === QGroupBox === */\n"
"QGroupBox {\n"
"    border: 1px solid transparent;\n"
"    margin-top: 1em;\n"
"}\n"
"\n"
"QGroupBox::titl"
                        "e {\n"
"	color: #80CBC4;\n"
"    subcontrol-origin: margin;\n"
"    left: 6px;\n"
"    padding: 0 3px 0 3px;\n"
"}\n"
"\n"
"QComboBox {\n"
"	color: #546E7A;\n"
"	background-color: transparent;\n"
"	selection-background-color: transparent;\n"
"	outline: 0;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView\n"
"{    \n"
"    selection-background-color: transparent;\n"
"	outline: 0;\n"
"}\n"
"\n"
"/* === QCheckBox === */\n"
"QCheckBox, QRadioButton {\n"
"	color: #546E7A;\n"
"}\n"
"QCheckBox::indicator {\n"
"	height: 18%;\n"
"	width: 18%;\n"
"	margin: 5%;\n"
"}\n"
"\n"
"QCheckBox::indicator::unchecked  {\n"
"	background-color: #FFFFFF;\n"
"	border: 1px solid #536D79;\n"
"}\n"
"\n"
"QRadioButton::indicator::unchecked {\n"
"	background-color: #FFFFFF;\n"
"	border: 1px solid #536D79;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"QCheckBox::indicator::checked, QTreeView::indicator::checked {\n"
"	background-color: qradialgradient(cx:0.5, cy:0.5, fx:0.25, fy:0.15, radius:0.3, stop:0 #80CBC4, stop:1 #FFFFFF);\n"
"	border: 1px solid #"
                        "536D79;\n"
"}\n"
"\n"
"QRadioButton::indicator::checked {\n"
"	background-color: qradialgradient(cx:0.5, cy:0.5, fx:0.25, fy:0.15, radius:0.3, stop:0 #80CBC4, stop:1 #FFFFFF);\n"
"	border: 1px solid #536D79;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"QCheckBox::indicator:disabled, QRadioButton::indicator:disabled, QTreeView::indicator:disabled {\n"
"	background-color: #444444;			/* Not sure what this looks like */\n"
"}\n"
"\n"
"QCheckBox::indicator::checked:disabled, QRadioButton::indicator::checked:disabled, QTreeView::indicator::checked:disabled {  \n"
"	background-color: qradialgradient(cx:0.5, cy:0.5, fx:0.25, fy:0.15, radius:0.3, stop:0 #BBBBBB, stop:1 #444444); /* Not sure what this looks like */\n"
"}\n"
"\n"
"QTreeView {\n"
"	background-color: transparent;\n"
"	color: #546E7A;\n"
"	outline: 0;\n"
"	border: 0;\n"
"}\n"
"\n"
"QTreeView::item:hover {\n"
"	background-color: transparent;\n"
"	color: #AFBDC4;\n"
"}\n"
"\n"
"QTreeView::item:selected {\n"
"	background-color: transparent;\n"
"	color: #FFFFFF;\n"
""
                        "}\n"
"\n"
"QTreeView QHeaderView:section {\n"
"	background-color: #FFFFFF;\n"
"	color: #CFD8DC;\n"
"	border: 0;\n"
"}\n"
"\n"
"QTreeView::indicator:checked {\n"
"	background-color: qradialgradient(cx:0.5, cy:0.5, fx:0.25, fy:0.15, radius:0.3, stop:0 #80CBC4, stop:1 #FFFFFF);\n"
"	border: 1px solid #536D79;\n"
"	selection-background-color: transparent;\n"
"}\n"
"\n"
"QTreeView::indicator:unchecked {			/* This and the one above style the checkbox in the Options -> Keyboard */\n"
"	background-color: #FFFFFF;				/* This is still a hover over in blue I can't get rid of */\n"
"	border: 1px solid #536D79;\n"
"	selection-background-color: transparent;\n"
"}\n"
"\n"
"/*QTreeView QScrollBar {\n"
"	background-color: #FFFFFF\n"
"}*/\n"
"\n"
"QTreeView::branch {\n"
"	/* Skip - applies to everything */\n"
"}\n"
"\n"
"QTreeView::branch:has-siblings:adjoins-item {\n"
"	/* Skip - files */\n"
"}\n"
"\n"
"QTreeView::branch:has-siblings:!adjoins-item {\n"
"	/* Skip - applies to almost all on the left side */\n"
"}\n"
"\n"
"QTreeV"
                        "iew::branch:closed:has-children:has-siblings {\n"
"	background: url('./images/rightarrowgray.png') center center no-repeat;\n"
"}\n"
"\n"
"QTreeView::branch:has-children:!has-siblings:closed {\n"
"	background: url('./images/rightarrowgray.png') center center no-repeat;\n"
"}\n"
"\n"
"QTreeView::branch:!has-children:!has-siblings:adjoins-item {\n"
"	/* Skip - files */\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:has-siblings {\n"
"	background: url('./images/downarrowgray.png') center center no-repeat;\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:!has-siblings {\n"
"	background: url('./images/downarrowgray.png') center center no-repeat;\n"
"}\n"
"\n"
"/* === QScrollBar:horizontal === */\n"
"QScrollBar:horizontal {\n"
"	background: #FFFFFF;				/* Background where slider is not */\n"
"	height: 10px;\n"
"	margin: 0;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"	background: #FFFFFF;				/* Background where slider is not */\n"
"	width: 10px;\n"
"	margin: 0;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"  "
                        "  background: #AFBDC4;					/* Slider color */\n"
"    min-width: 16px;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: #AFBDC4;					/* Slider color */\n"
"    min-height: 16px;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal,\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"	background: none;												/* Removes the dotted background */\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {	/* Hides the slider arrows */\n"
"      border: none;\n"
"      background: none;\n"
"}\n"
"\n"
"QPushButton {\n"
"	background-color: transparent;\n"
"	color: #546E7A;\n"
"	border: 1px solid #546E7A;\n"
"	border-radius: 4px;\n"
"	padding: 4px 22px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	color: #AFBDC4;\n"
"	border-radius: 4px;\n"
"	border-color: #AFBDC4;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	color: #80CBC4;"
                        "\n"
"	border-radius: 4px;\n"
"	border-color: #80CBC4;\n"
"}\n"
"\n"
"QLineEdit {\n"
"	background: transparent;\n"
"	border: 1px solid transparent;\n"
"	border-bottom: 1px solid #546E7A;\n"
"	color: #546E7A;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"	background: transparent;\n"
"	border: 1px solid transparent;\n"
"	border-bottom: 2px solid #80CBC4;\n"
"	color: #546E7A;\n"
"}\n"
"\n"
"QSpinBox {\n"
"	background: transparent;\n"
"	border: 1px solid transparent;\n"
"	color: #546E7A;\n"
"}\n"
"\n"
"/*****************************************************************************\n"
"Main Screen\n"
"*****************************************************************************/\n"
"QTreeView {\n"
"	background-color: #FFFFFF;\n"
"}\n"
"\n"
"QMenu {\n"
"	background-color: #FFFFFF;		/* File Menu Background color */\n"
"	color: #546E7A;\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"	color: #AFBDC4;\n"
"}\n"
"\n"
"QMenu::item:pressed {\n"
"	color: #FFFFFF;\n"
"}\n"
"\n"
"QMenu::separator {\n"
"	height: 1px;\n"
"	background: transpare"
                        "nt;			/* Could change this to #546E7A and reduce the margin top and bottom to 1px */\n"
"	margin-left: 10px;\n"
"	margin-right: 10px;\n"
"	margin-top: 5px;\n"
"	margin-bottom: 5px;\n"
"}\n"
"\n"
"/* === QMenuBar === */\n"
"QMenuBar {\n"
"	background-color: #FFFFFF;\n"
"	color: #546E7A;\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"	background: transparent;\n"
"}\n"
"\n"
"QMenuBar::item:disabled {\n"
"	color: gray;\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"	color: #AFBDC4;\n"
"}\n"
"\n"
"QMenuBar::item:pressed {\n"
"	color: #FFFFFF;\n"
"}\n"
"\n"
"QToolBar {\n"
"	background: #FFFFFF;\n"
"	border: 1px solid transparent;\n"
"}\n"
"\n"
"QToolBar:handle {\n"
"	background: transparent;\n"
"	border-left: 2px dotted #80CBC4;	/* Fix the 4 handle dots so it doesn't look crappy */\n"
"	color: transparent;\n"
"}\n"
"\n"
"QToolBar::separator {\n"
"	border: 0;\n"
"}\n"
"\n"
"/* === QToolButton === */\n"
"QToolButton:hover, QToolButton:pressed {\n"
"	background-color: transparent;\n"
"}\n"
"\n"
"QToolButton::menu-button {\n"
"	back"
                        "ground: url('./images/downarrowgray.png') center center no-repeat;\n"
"	background-color: #FFFFFF;												/* This needs to be set to ensure the other brown arrows don't show */\n"
"}\n"
"\n"
"QToolButton::menu-button:hover, QToolButton::menu-button:pressed {\n"
"	background-color: #FFFFFF;\n"
"}\n"
"\n"
"QStatusBar {\n"
"	background-color: #FFFFFF;\n"
"}\n"
"\n"
"QLabel {\n"
"	color: #546E7A;		/* Text at the bottom right corner of the screen */\n"
"}\n"
"\n"
"QToolButton {	/* I don't like how the items depress */\n"
"	color: #546E7A;\n"
"}\n"
"\n"
"QToolButton:hover, QToolButton:pressed, QToolButton:checked {\n"
"	background-color: #FFFFFF;\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"	color: #AFBDC4;\n"
"\n"
"}\n"
"\n"
"QToolButton:checked, QToolButton:pressed {\n"
"	color: #FFFFFF;\n"
"}\n"
"\n"
"\n"
"QToolButton {\n"
"	border: 1px solid transparent;\n"
"	margin: 1px;\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"	background-color: transparent;				/* I don't like how the down arrows in the top menu bar move down when"
                        " clicked */\n"
"	border: 1px solid transparent;\n"
"}\n"
"\n"
"QToolButton[popupMode=\"1\"] { /* only for MenuButtonPopup */\n"
"	padding-right: 20px; /* make way for the popup button */\n"
"}\n"
"\n"
"QToolButton::menu-button {\n"
"	border-left: 1px solid transparent;\n"
"	background: transparent;\n"
"    width: 16px;\n"
"}\n"
"\n"
"QToolButton::menu-button:hover {\n"
"	border-left: 1px solid transparent;\n"
"	background: transparent;\n"
"    width: 16px;\n"
"}\n"
"\n"
"QStatusBar::item {\n"
"	color: #546E7A;\n"
"	background-color: #FFFFFF;\n"
"}\n"
"\n"
"QAbstractScrollArea  {	/* Borders around the code editor and debug window */\n"
"	border: 0;\n"
"}\n"
"\n"
"/*****************************************************************************\n"
"Play around with these settings\n"
"*****************************************************************************/\n"
"\n"
"/* Force the dialog's buttons to follow the Windows guidelines. */\n"
"QDialogButtonBox {\n"
"    button-layout: 0;\n"
"}\n"
"\n"
"QTabWidget::tab-"
                        "bar {\n"
"	left: 0px; /* Test this out on OS X, it will affect the tabs in the Options Dialog, on OS X they are centered */\n"
"}\n"
"\n"
"\n"
"QTextEdit {\n"
"	color: #546E7A;\n"
"}\n"
"\n"
"QStatusBar {\n"
"	color: #546E7A;\n"
"}\n"
"\n"
"QProgressBar {\n"
"	color: #546E7A;\n"
"}\n"
"\n"
"QProgressBar::chunk:horizontal {\n"
"	background: #80CBC4;\n"
"}\n"
"\n"
"")
        MainForm.setToolButtonStyle(Qt.ToolButtonIconOnly)
        MainForm.setDocumentMode(False)
        self.centralwidget = QWidget(MainForm)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QSize(800, 552))
        self.centralwidget.setAutoFillBackground(False)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.userCode = QLineEdit(self.centralwidget)
        self.userCode.setObjectName(u"userCode")

        self.horizontalLayout_3.addWidget(self.userCode)

        self.horizontalSpacer_2 = QSpacerItem(400, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 10)

        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.password = QLineEdit(self.centralwidget)
        self.password.setObjectName(u"password")
        self.password.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_5.addWidget(self.password)

        self.horizontalSpacer_3 = QSpacerItem(300, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_5.setStretch(0, 5)
        self.horizontalLayout_5.setStretch(1, 5)

        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)

        self.syncNow = QPushButton(self.centralwidget)
        self.syncNow.setObjectName(u"syncNow")

        self.gridLayout.addWidget(self.syncNow, 0, 2, 1, 1)

        self.trylogin = QPushButton(self.centralwidget)
        self.trylogin.setObjectName(u"trylogin")
        self.trylogin.setMinimumSize(QSize(101, 0))

        self.gridLayout.addWidget(self.trylogin, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QSize(0, 0))
        self.tabWidget.setMaximumSize(QSize(16777215, 2000000))
        self.tabWidget.setMouseTracking(True)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.courses_tab = QWidget()
        self.courses_tab.setObjectName(u"courses_tab")
        self.verticalLayout_3 = QVBoxLayout(self.courses_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.courses_layout = QVBoxLayout()
        self.courses_layout.setObjectName(u"courses_layout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.refreshCourses = QPushButton(self.courses_tab)
        self.refreshCourses.setObjectName(u"refreshCourses")

        self.horizontalLayout_2.addWidget(self.refreshCourses)

        self.AddCourse = QPushButton(self.courses_tab)
        self.AddCourse.setObjectName(u"AddCourse")

        self.horizontalLayout_2.addWidget(self.AddCourse)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.courses_layout.addLayout(self.horizontalLayout_2)

        self.coursesView = QTableWidget(self.courses_tab)
        if (self.coursesView.columnCount() < 4):
            self.coursesView.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.coursesView.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.coursesView.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.coursesView.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.coursesView.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.coursesView.rowCount() < 1):
            self.coursesView.setRowCount(1)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.coursesView.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.coursesView.setItem(0, 0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.coursesView.setItem(0, 1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.coursesView.setItem(0, 2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.coursesView.setItem(0, 3, __qtablewidgetitem8)
        self.coursesView.setObjectName(u"coursesView")
        self.coursesView.setMinimumSize(QSize(758, 0))
        self.coursesView.setMaximumSize(QSize(1920, 1080))
        self.coursesView.setLineWidth(1)
        self.coursesView.setMidLineWidth(0)
        self.coursesView.setSortingEnabled(False)
        self.coursesView.horizontalHeader().setVisible(False)
        self.coursesView.horizontalHeader().setCascadingSectionResizes(False)
        self.coursesView.horizontalHeader().setMinimumSectionSize(50)
        self.coursesView.horizontalHeader().setDefaultSectionSize(200)
        self.coursesView.horizontalHeader().setHighlightSections(True)
        self.coursesView.horizontalHeader().setProperty("showSortIndicator", True)
        self.coursesView.horizontalHeader().setStretchLastSection(True)
        self.coursesView.verticalHeader().setVisible(False)
        self.coursesView.verticalHeader().setHighlightSections(False)

        self.courses_layout.addWidget(self.coursesView)


        self.verticalLayout_3.addLayout(self.courses_layout)

        self.tabWidget.addTab(self.courses_tab, "")
        self.status_tab = QWidget()
        self.status_tab.setObjectName(u"status_tab")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.status_tab.sizePolicy().hasHeightForWidth())
        self.status_tab.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.status_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_6.setContentsMargins(0, 0, -1, -1)
        self.check_version = QPushButton(self.status_tab)
        self.check_version.setObjectName(u"check_version")

        self.horizontalLayout_6.addWidget(self.check_version, 0, Qt.AlignLeft)

        self.version_label = QLabel(self.status_tab)
        self.version_label.setObjectName(u"version_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.version_label.sizePolicy().hasHeightForWidth())
        self.version_label.setSizePolicy(sizePolicy2)
        self.version_label.setMinimumSize(QSize(0, 0))
        self.version_label.setFrameShape(QFrame.NoFrame)
        self.version_label.setFrameShadow(QFrame.Plain)
        self.version_label.setTextFormat(Qt.RichText)
        self.version_label.setScaledContents(True)
        self.version_label.setMargin(0)
        self.version_label.setIndent(4)
        self.version_label.setOpenExternalLinks(True)

        self.horizontalLayout_6.addWidget(self.version_label, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)

        self.about = QPushButton(self.status_tab)
        self.about.setObjectName(u"about")

        self.horizontalLayout_6.addWidget(self.about, 0, Qt.AlignRight)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.status = QTextEdit(self.status_tab)
        self.status.setObjectName(u"status")
        self.status.setEnabled(True)
        self.status.setAcceptDrops(False)
        self.status.setAutoFillBackground(False)
        self.status.setFrameShape(QFrame.StyledPanel)
        self.status.setFrameShadow(QFrame.Sunken)
        self.status.setUndoRedoEnabled(False)
        self.status.setReadOnly(True)
        self.status.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout_2.addWidget(self.status)

        self.tabWidget.addTab(self.status_tab, "")
        self.settings_tab = QWidget()
        self.settings_tab.setObjectName(u"settings_tab")
        self.settings_tab.setEnabled(True)
        self.verticalLayout_4 = QVBoxLayout(self.settings_tab)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_4 = QLabel(self.settings_tab)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_7.addWidget(self.label_4)

        self.rootfolder = QLineEdit(self.settings_tab)
        self.rootfolder.setObjectName(u"rootfolder")

        self.horizontalLayout_7.addWidget(self.rootfolder)

        self.changeRootFolder = QPushButton(self.settings_tab)
        self.changeRootFolder.setObjectName(u"changeRootFolder")

        self.horizontalLayout_7.addWidget(self.changeRootFolder)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_5 = QLabel(self.settings_tab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setScaledContents(False)
        self.label_5.setMargin(0)
        self.label_5.setIndent(-1)
        self.label_5.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout_4.addWidget(self.label_5, 0, Qt.AlignLeft)

        self.timerMinutes = QSpinBox(self.settings_tab)
        self.timerMinutes.setObjectName(u"timerMinutes")
        self.timerMinutes.setMaximumSize(QSize(68, 28))
        self.timerMinutes.setFrame(True)
        self.timerMinutes.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.timerMinutes.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.timerMinutes.setAccelerated(False)
        self.timerMinutes.setProperty("showGroupSeparator", False)
        self.timerMinutes.setMaximum(4800)
        self.timerMinutes.setValue(480)

        self.horizontalLayout_4.addWidget(self.timerMinutes, 0, Qt.AlignLeft)

        self.label_6 = QLabel(self.settings_tab)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_4.addWidget(self.label_6, 0, Qt.AlignLeft)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = QLabel(self.settings_tab)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.timeout = QSpinBox(self.settings_tab)
        self.timeout.setObjectName(u"timeout")
        self.timeout.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.timeout.setMaximum(300)
        self.timeout.setValue(10)

        self.horizontalLayout.addWidget(self.timeout)

        self.label_7 = QLabel(self.settings_tab)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout.addWidget(self.label_7)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.addSyncNewCourses = QCheckBox(self.settings_tab)
        self.addSyncNewCourses.setObjectName(u"addSyncNewCourses")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.addSyncNewCourses.sizePolicy().hasHeightForWidth())
        self.addSyncNewCourses.setSizePolicy(sizePolicy3)
        self.addSyncNewCourses.setMinimumSize(QSize(420, 30))
        self.addSyncNewCourses.setMaximumSize(QSize(1920, 40))
        self.addSyncNewCourses.setIconSize(QSize(4, 4))
        self.addSyncNewCourses.setCheckable(True)
        self.addSyncNewCourses.setChecked(False)
        self.addSyncNewCourses.setAutoRepeat(False)
        self.addSyncNewCourses.setTristate(False)

        self.verticalLayout_5.addWidget(self.addSyncNewCourses)

        self.startupSync = QCheckBox(self.settings_tab)
        self.startupSync.setObjectName(u"startupSync")

        self.verticalLayout_5.addWidget(self.startupSync)

        self.verticalSpacer = QSpacerItem(20, 2000, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)


        self.verticalLayout_4.addLayout(self.verticalLayout_5)

        self.tabWidget.addTab(self.settings_tab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainForm.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainForm)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setEnabled(True)
        MainForm.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.userCode)
        self.label_2.setBuddy(self.password)
        self.label_4.setBuddy(self.rootfolder)
        self.label_5.setBuddy(self.timerMinutes)
        self.label_3.setBuddy(self.timeout)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.userCode, self.password)
        QWidget.setTabOrder(self.password, self.syncNow)
        QWidget.setTabOrder(self.syncNow, self.trylogin)
        QWidget.setTabOrder(self.trylogin, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.refreshCourses)
        QWidget.setTabOrder(self.refreshCourses, self.AddCourse)
        QWidget.setTabOrder(self.AddCourse, self.coursesView)
        QWidget.setTabOrder(self.coursesView, self.check_version)
        QWidget.setTabOrder(self.check_version, self.about)
        QWidget.setTabOrder(self.about, self.status)
        QWidget.setTabOrder(self.status, self.rootfolder)
        QWidget.setTabOrder(self.rootfolder, self.changeRootFolder)
        QWidget.setTabOrder(self.changeRootFolder, self.timerMinutes)
        QWidget.setTabOrder(self.timerMinutes, self.addSyncNewCourses)
        QWidget.setTabOrder(self.addSyncNewCourses, self.startupSync)

        self.retranslateUi(MainForm)
        self.userCode.editingFinished.connect(MainForm.set_usercode)
        self.password.editingFinished.connect(MainForm.set_password)
        self.syncNow.clicked.connect(MainForm.sync_files)
        self.trylogin.clicked.connect(MainForm.test_login)
        self.refreshCourses.clicked.connect(MainForm.refresh_courses)
        self.about.clicked.connect(MainForm.show_about)
        self.check_version.clicked.connect(MainForm.check_new_version)
        self.changeRootFolder.clicked.connect(MainForm.choose_rootdir)
        self.timerMinutes.valueChanged.connect(MainForm.updated_minutes)
        self.timeout.valueChanged.connect(MainForm.updated_default_timeout)
        self.rootfolder.textEdited.connect(MainForm.updated_root_folder)
        self.AddCourse.clicked.connect(MainForm.show_add_course_popup)
        self.startupSync.stateChanged.connect(MainForm.sync_on_startup)
        self.addSyncNewCourses.stateChanged.connect(MainForm.sync_new)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainForm)
    # setupUi

    def retranslateUi(self, MainForm):
        MainForm.setWindowTitle(QCoreApplication.translate("MainForm", u"PoliBeePSync", None))
        self.label.setText(QCoreApplication.translate("MainForm", u"User code", None))
        self.label_2.setText(QCoreApplication.translate("MainForm", u"Password", None))
        self.password.setInputMask("")
        self.password.setText("")
        self.syncNow.setText(QCoreApplication.translate("MainForm", u"Sync now", None))
        self.trylogin.setText(QCoreApplication.translate("MainForm", u"Try logging in", None))
        self.refreshCourses.setText(QCoreApplication.translate("MainForm", u"Refresh list", None))
        self.AddCourse.setText(QCoreApplication.translate("MainForm", u"Add Course", None))
        ___qtablewidgetitem = self.coursesView.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainForm", u"Name", None));
        ___qtablewidgetitem1 = self.coursesView.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainForm", u"Sync", None));
        ___qtablewidgetitem2 = self.coursesView.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainForm", u"Save as", None));
        ___qtablewidgetitem3 = self.coursesView.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainForm", u"Download %", None));
        ___qtablewidgetitem4 = self.coursesView.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainForm", u"kek", None));

        __sortingEnabled = self.coursesView.isSortingEnabled()
        self.coursesView.setSortingEnabled(False)
        ___qtablewidgetitem5 = self.coursesView.item(0, 0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainForm", u"ciao", None));
        ___qtablewidgetitem6 = self.coursesView.item(0, 1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainForm", u"si", None));
        ___qtablewidgetitem7 = self.coursesView.item(0, 2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainForm", u"no", None));
        ___qtablewidgetitem8 = self.coursesView.item(0, 3)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainForm", u"10", None));
        self.coursesView.setSortingEnabled(__sortingEnabled)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.courses_tab), QCoreApplication.translate("MainForm", u"Courses", None))
        self.check_version.setText(QCoreApplication.translate("MainForm", u"Check for new version", None))
        self.version_label.setText("")
        self.about.setText(QCoreApplication.translate("MainForm", u"About", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.status_tab), QCoreApplication.translate("MainForm", u"Status", None))
        self.label_4.setText(QCoreApplication.translate("MainForm", u"Root folder", None))
        self.changeRootFolder.setText(QCoreApplication.translate("MainForm", u"Change", None))
        self.label_5.setText(QCoreApplication.translate("MainForm", u"Sync every", None))
        self.timerMinutes.setSpecialValueText("")
        self.timerMinutes.setSuffix("")
        self.timerMinutes.setPrefix("")
        self.label_6.setText(QCoreApplication.translate("MainForm", u"minutes", None))
        self.label_3.setText(QCoreApplication.translate("MainForm", u"Default connection timeout", None))
        self.timeout.setSuffix("")
        self.label_7.setText(QCoreApplication.translate("MainForm", u"seconds", None))
        self.addSyncNewCourses.setText(QCoreApplication.translate("MainForm", u"Automatically add and sync new available courses", None))
        self.startupSync.setText(QCoreApplication.translate("MainForm", u"Sync on startup", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings_tab), QCoreApplication.translate("MainForm", u"Settings", None))
    # retranslateUi

