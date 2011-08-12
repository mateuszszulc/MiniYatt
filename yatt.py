#!/usr/bin/env python

import sip
import sys
import serial
import copy

sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui
from PyQt4 import Qt
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QWidget, QTextEdit, QLineEdit, QShortcut, QKeySequence
from PyQt4.QtGui import QAction, QIcon


def radioBand(preferred, allowed):
    return "at^scfg=Radio/band,{0},{1}".format(preferred, allowed)

def pin(pinValue = 9999):
    return "AT+CPIN={0}".format(pinValue)

def cmee2():
    return "AT+CMEE=2"

scenarios = { 'cmu850': 
[ radioBand(4,4),pin(),cmee2(),radioBand(8,12),radioBand(4,4),radioBand(4,12)]
}

class SerialCommunicationThread(QtCore.QThread):

    def __init__(self, socket):
        super(QtCore.QThread, self).__init__()
        self.socket = socket
    def run(self):
        while (True):
          linia = self.socket.readline()
          QtCore.qDebug(linia)
          self.emit(QtCore.SIGNAL("newData"), bytes.decode(linia))

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

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(QtGui.QMainWindow, self).__init__()

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"));
        self.setWindowTitle("Mini Yatt")
        
        self.setupSocketThread()
        self.createCentralWidget()


        self.lineEdit.returnPressed.connect(self.sendData)
        self.connect(self.thread, QtCore.SIGNAL("newData"), self.readNewData)
				
        self.createShortcuts()
        self.createActions()
        self.createMenus()
        self.createToolbar()
        
        self.resize(500,400)
#       self.sequence = Sequence(init_band = "AT^SCFG=radio/band,4,4",
#                                       first_band = "AT^SCFG=radio/band,8,8",
#                                      second_band = "AT^SCFG=radio/band,4,12")
#       self.playSequence();

        self.commands = copy.deepcopy(scenarios['cmu850'])

        self.lineEdit.setText(self.commands[0])

    def createToolbar(self):
        self.fileToolBar = self.addToolBar("ATCommands Toolbar")
        self.fileToolBar.addAction(self.atAct)
        self.fileToolBar.addAction(self.modelAct)
        self.fileToolBar.addAction(self.pinAct)
        self.fileToolBar.addAction(self.moniAct)

    def createCentralWidget(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.lineEdit = QtGui.QLineEdit()
        self.textEdit = QtGui.QTextEdit()
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.textEdit)
        centralWidget.setLayout(self.layout)

    def setupSocketThread (self):
        self.socket = serial.Serial(3,115200)
        self.thread = SerialCommunicationThread(self.socket)
        self.thread.start()

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("File")
        self.fileMenu.addAction(self.quitAct)

        self.toolbarMenu = self.menuBar().addMenu("Toolbar")
        self.toolbarMenu.addAction(self.addButtonAct)

    def createShortcuts(self):
        self.shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcut.activated.connect(self.openFile)

    def createActions(self):
        # HOW TO TRIGGER WITH SPECYFIC DATA?
        self.moniAct = QAction("at^moni", self, shortcut=QKeySequence.New, 
                       triggered=self.sendMoni)
        self.pinAct = QAction("at+cpin=9999", self, triggered=self.sendPin)
        self.atAct = QAction("at", self, triggered=self.sendAt)
        self.modelAct = QAction("model", self,  triggered=self.sendModel)

        self.addButtonAct = QAction("Add Button", self,triggered=self.addButton)

        self.quitAct = QAction("Quit", self, shortcut=QKeySequence.Quit,
                                                 triggered=QtGui.qApp.quit)
        
    def openFile(self):
        QtCore.qDebug("Hello From Open FIle")

    def addButton(self):
        addButtonWidget = AddButtonWidget()
        #addButtonWidget.setWindowModality(QtCore.Qt.WindowModal)
        addButtonWidget.resize(200,200)
        addButtonWidget.show()
        QtCore.qDebug("Hello From Add Button")

    def readNewData(self, data):
        data = data.strip()
        self.textEdit.append(data)
        #self.textEdit2.append("\n")
        self.textEdit.moveCursor(QtGui.QTextCursor.End)

    def sendData(self):
        QtCore.qDebug("sendData odpalone!")
        #QtCore.qDebug(self.textEdit.text())
        #self.socket.write(str.encode(self.textEdit.text()) + b"\r\n")
        msg = self.commands.pop(0)
        self.socket.write(str.encode(msg) + b"\r\n")
        self.lineEdit.setText(self.commands[0])

    def sendMoni(self):
        self.socket.write(str.encode("at^moni") + b"\r\n")
    def sendPin(self):
        self.socket.write(str.encode("at+pin=9999") + b"\r\n")
    def sendAt(self):
        self.socket.write(str.encode("at") + b"\r\n")
    def sendModel(self):
        self.socket.write(str.encode("at^siekret=1") + b"\r\n")


#   def playSequence(self):
#       #here comes all the logic
#       self.sequence.play();


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.stdout.write("DDD")
    sys.exit(app.exec_())

#self.thread.newData.connect(self.textEdit2.setText)


#self.socket.write(b"AT\r\n")
#self.socket.write(b"AT" + b"\r\n")

#self.socket.write(str.encode("AT") + b"\r\n")


#NOT WORKING
#        self.connect(self.textEdit, QtCore.SIGNAL("returnPressed()"), self, QtCore.SLOT("sendData()"))

#WORKING
#        self.connect(self.textEdit, QtCore.SIGNAL("returnPressed()"), self.sendData)


