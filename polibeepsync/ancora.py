# Written by Robin Burchell
# No licence specified or required, but please give credit where it's due, and please let me know if this helped you.
# Feel free to contact with corrections or suggestions.
#
from PySide.QtCore import *
from PySide.QtGui import *

import sys

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
        '''
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton or presses
        Key_Space or Key_Select and this cell is editable. Otherwise do nothing.
        '''

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


class MyObject(object):
    def __init__(self, name, other, editable):
        self.name = name
        self.other = other
        self.editable = editable

class SimpleListModel(QAbstractTableModel):
    def __init__(self, mlist):
        QAbstractTableModel.__init__(self)
        self._items = mlist

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def columnCount(self, parent=QModelIndex()):
        return 3

    def flags(self, index):
        if index.column() == 2:
            flags = Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
            return flags
        elif index.column() == 1:
            flags = Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable\
            | Qt.ItemIsUserCheckable
            return flags
        else: return Qt.ItemIsEnabled

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            if index.column() == 2:
                self._items[index.row()].editable = value
                self.dataChanged.emit(index, index)
                return True
            elif index.column() == 1:
                self._items[index.row()].other = value
                self.dataChanged.emit(index, index)
                return True
        return False


    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self._items[index.row()].name
            if index.column() == 1:
                return self._items[index.row()].other
            if index.column() == 2:
                return self._items[index.row()].editable
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

    def print_all(self):
        for elem in self._items:
            print(elem.name, elem.other, elem.editable)

# This widget is our view of the readonly list.
# Obviously, in a real application, this will be more complex, with signals/etc usage, but
# for the scope of this tutorial, let's keep it simple, as always.
#
# For more information, see:
# http://doc.trolltech.com/4.6/qlistview.html
class SimpleListView(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        self.setItemDelegateForColumn(1, CheckBoxDelegate(self))

# Our main application window.
# You should be used to this from previous tutorials.
class MyMainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)

        # main section of the window
        vbox = QVBoxLayout()

        # create a data source:
        self.m = SimpleListModel([MyObject('a',True, 'edit this'), MyObject('b', False, 'edit me')])
        self.m.dataChanged.connect(self.m.print_all)
        # let's add two views of the same data source we just created:
        v = SimpleListView()
        v.setModel(self.m)
        vbox.addWidget(v)
        # set layout on the window
        self.setLayout(vbox)

# set things up, and run it. :)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    app.exec_()
    sys.exit()
