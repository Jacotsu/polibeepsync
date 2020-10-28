# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_course_popup.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import uglytheme_rc

class Ui_AddCoursePopup(object):
    def setupUi(self, AddCoursePopup):
        if not AddCoursePopup.objectName():
            AddCoursePopup.setObjectName(u"AddCoursePopup")
        AddCoursePopup.resize(795, 210)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddCoursePopup.sizePolicy().hasHeightForWidth())
        AddCoursePopup.setSizePolicy(sizePolicy)
        icon = QIcon()
        iconThemeName = u":/root/imgs/icons/polibeepsync.svg"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        AddCoursePopup.setWindowIcon(icon)
        AddCoursePopup.setStyleSheet(u"/* https://github.com/martinrotter/qt-material-stylesheet */\n"
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
"	border: 1px solid #536D79;\n"
"}\n"
"\n"
"QRadioButton::indicator::checked {\n"
"	background-color: qrad"
                        "ialgradient(cx:0.5, cy:0.5, fx:0.25, fy:0.15, radius:0.3, stop:0 #80CBC4, stop:1 #FFFFFF);\n"
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
"}\n"
"\n"
"QTreeView QHeaderView:section {\n"
"	background-color: #FFFFFF;\n"
"	colo"
                        "r: #CFD8DC;\n"
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
"QTreeView::branch:closed:has-children:has-siblings {\n"
"	background: url('./images/righta"
                        "rrowgray.png') center center no-repeat;\n"
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
"    background: #AFBDC4;					/* Slider color */\n"
"    min-width: 16px;\n"
"	border-r"
                        "adius: 5px;\n"
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
"	color: #80CBC4;\n"
"	border-radius: 4px;\n"
"	border-color: #80CBC4;\n"
"}\n"
"\n"
"QLineEdit {\n"
""
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
"	background: transparent;			/* Could change this to #546E7A and reduce the margin top and bottom to 1px */\n"
""
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
"	background: url('./images/downarrowgray.png') center center no-repeat;\n"
"	background-color:"
                        " #FFFFFF;												/* This needs to be set to ensure the other brown arrows don't show */\n"
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
"	background-color: transparent;				/* I don't like how the down arrows in the top menu bar move down when clicked */\n"
"	border: 1px solid transparent;\n"
"}\n"
"\n"
"QToolButton[popupMode=\"1\""
                        "] { /* only for MenuButtonPopup */\n"
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
"QTabWidget::tab-bar {\n"
"	left: 0px; /* Test this out on OS X, it will affect the tabs in the Options Dia"
                        "log, on OS X they are centered */\n"
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
"QTableView::item:hover {\n"
"	border: 1px solid transparent;\n"
"	border-bottom: 1px solid #546E7A;\n"
"	color: #546E7A;\n"
"}")
        self.horizontalLayout = QHBoxLayout(AddCoursePopup)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.CourseUrl = QPlainTextEdit(AddCoursePopup)
        self.CourseUrl.setObjectName(u"CourseUrl")

        self.horizontalLayout.addWidget(self.CourseUrl)

        self.buttonBox = QDialogButtonBox(AddCoursePopup)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy1)
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AddCoursePopup)
        self.buttonBox.accepted.connect(AddCoursePopup.accept)
        self.buttonBox.rejected.connect(AddCoursePopup.reject)

        QMetaObject.connectSlotsByName(AddCoursePopup)
    # setupUi

    def retranslateUi(self, AddCoursePopup):
        AddCoursePopup.setWindowTitle(QCoreApplication.translate("AddCoursePopup", u"Add new course", None))
        self.CourseUrl.setPlaceholderText(QCoreApplication.translate("AddCoursePopup", u"Please insert here the course url", None))
    # retranslateUi

