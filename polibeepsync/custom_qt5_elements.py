from PySide2.QtCore import (QAbstractTableModel, QModelIndex, Qt, Slot,
                            QTimer, QLocale, TreeModel, TreeItem,
                            QEvent, Qt, QPoint, QRect, QLocale, QSize,
                            QMetaObject, QFile)
from PySide2.QtGui import (QTextCursor, QCursor)
from PySide2.QtWidgets import (QWidget, QMenu, QAction, QFileDialog, QLabel,
                               QSystemTrayIcon, qApp, QApplication,
                               QTableView,QStyledItemDelegate,
                               QStyleOptionButton, QStyle, QMainWindow,
                               QHeaderView, QProgressBar, QWidget, QHBoxLayout,
                               QStyleOptionProgressBar, QGridLayout, QLabel,
                               QLineEdit, QSpacerItem, QSizePolicy,
                               QPushButton, QSpinBox, QCheckBox, QTextEdit,
                               QDialogButtonBox)

from PySide2.QtUiTools import QUiLoader



class CoursesListModel(TreeModel):
    def __init__(self, courses):
        super().__init__(self)
        # my object is a mapping, while table model uses an index (so it's
        # more similar to a list
        self.courses = list(courses)
        self._root_element = TreeItem()

    def rowCount(self, parent=QModelIndex()):
        return len(self.courses)

    def columnCount(self, parent=QModelIndex()):
        return 4

    def insertRows(self, position, rows, newcourse, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            self.courses.insert(position, newcourse)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            del self.courses[position]
        self.endRemoveRows()
        return True

    def flags(self, index):
        # Destination save name
        if index.column() == 2:
            flags = Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
            return flags
        # Sync checkbox
        elif index.column() == 1:
            flags = Qt.ItemIsEditable | Qt.ItemIsEnabled | \
                Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
            return flags
        else:
            return Qt.ItemIsEnabled

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            if index.column() == 2:
                other_names = [elem.save_folder_name for elem in self.courses]
                if value not in other_names and value is not "":
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
            if index.column() == 3:
                dw = self.courses[index.row()].downloaded_size
                total = self.courses[index.row()].size
                return (dw, total)
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
            elif col == 3:
                return "Download %"



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


