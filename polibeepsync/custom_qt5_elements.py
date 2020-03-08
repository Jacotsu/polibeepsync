__copyright__ = """Copyright 2020 Davide Olianas (ubuntupk@gmail.com), Di
Campli Raffaele (dcdrj.pub@gmail.com)."""

__license__ = """This f is part of poliBeePsync.
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

from PySide2.QtCore import (QAbstractTableModel, QModelIndex, Qt, Slot,
                            QTimer, QLocale, TreeModel, TreeItem,
                            QEvent, Qt, QPoint, QRect, QLocale, QSize,
                            QMetaObject, QFile)
from PySide2.QtGui import (QTextCursor, QCursor)
from PySide2.QtWidgets import (QWidget, QMenu, QAction, QFileDialog, QLabel,
                               QSystemTrayIcon, qApp, QApplication,
                               QTableView,QStyledItemDelegate, QTreeView,
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
            # Editing save file position
            if index.column() == 2:
                other_names = [elem.save_folder_name for elem in self.courses]
                if value and value not in other_names:
                    self.courses[index.row()].save_folder_name = value
                    self.dataChanged.emit(index, index)
                return True
            # Editing sync checkbox
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


class CoursesListView(QTreeView):
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


