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
                               QDialogButtonBox, QPlainTextEdit)
from PySide2.QtCore import (QEvent, Qt, QPoint, QRect, QLocale, QSize,
                            QMetaObject, QFile, Slot)

from PySide2.QtUiTools import QUiLoader

from polibeepsync.utils import fps_limiter

FPS = 60

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
        if fps_limiter(FPS, 'progress_bars'):
            progressBar = QProgressBar()

            progressBar.setAlignment(Qt.AlignCenter)
            progressBar.setTextVisible(True)

            progressBar.resize(option.rect.size())
            progressBar.setMinimum(0)
            progressBar.setMaximum(100)

            if self.parent():
                progressBar.setStyleSheet(self.parent().styleSheet())

            dw, tot = index.data()
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
        if fps_limiter(FPS, 'checkboxes'):
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
