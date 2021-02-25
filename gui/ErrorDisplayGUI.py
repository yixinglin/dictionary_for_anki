from aqt.qt import QApplication, QListWidget, QAbstractItemView, QDialog
from english_chinese_tts.gui.GUIEvent import *
from aqt.qt import QPushButton, QLabel, QLineEdit, QComboBox
import aqt.qt as qt
import sys

class ErrorDisPlayGUI(QDialog):

  def __init__(self):
    super().__init__()
    #self.setSelectionMode(QAbstractItemView.MultiSelection)
    self.show()

  def update_list(self, items):
    self.addItems(items)

  def append(self, item):
    self.addItem(item)

if __name__ == '__main__':

    app = QApplication(sys.argv)

    listWidget = ErrorDisPlayGUI()

    ls = ['test', 'test2', 'test3']

    listWidget.update_list(ls)

    sys.exit(app.exec_())