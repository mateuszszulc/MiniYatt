from PyQt4 import QtCore, QtGui
from PyQt4 import Qt
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QWidget, QTextEdit, QLineEdit, QShortcut, QKeySequence
from PyQt4.QtGui import QAction, QIcon, QActionGroup, QComboBox

class AddButtonWidget(QtGui.QWidget):
    def __init__(self):
        super(QtGui.QWidget, self).__init__()
        self.buttonName = QtGui.QLineEdit()
        self.buttonCommand = QtGui.QLineEdit()
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.buttonName)
        self.layout.addWidget(self.buttonCommand)
        self.setLayout(self.layout)
        self.setWindowModality(QtCore.Qt.WindowModal)

    def getButtonName(self):
        return self.buttonName.text()

    def getButtonCommand(self):
        return self.buttonCommand.text()

