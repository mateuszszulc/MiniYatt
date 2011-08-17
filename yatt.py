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
from PyQt4.QtGui import QAction, QIcon, QActionGroup, QComboBox

from SerialCommunicationThread import *

from AddButtonWidget import *

def radioBand(preferred, allowed):
    return "at^scfg=Radio/band,{0},{1}".format(preferred, allowed)

def pin(pinValue = 9999):
    return "AT+CPIN={0}".format(pinValue)

def cmee2():
    return "AT+CMEE=2"

def smso():
    return "AT^SMSO"

scenarios = { 
'cmu850': 
[ radioBand(4,4), smso(), pin(),radioBand(8,12),radioBand(4,4),radioBand(4,12)],
'cmu850_AllowAll': #with Camp?!
[ radioBand(4,4), smso(), pin(),radioBand(8,15),radioBand(4,4),radioBand(2,15)],
'cmu900': 
[ radioBand(4,4), smso(), pin(),radioBand(1,3),radioBand(4,4),radioBand(2,3)],
'cmu900_AllowAll': #with CAMP?! should camp on 2,2 or 4,4? Another Test Case?
[ radioBand(2,2), smso(), pin(),radioBand(1,15),radioBand(2,2),radioBand(8,15)],
}

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
        self.createActionGroup()
        self.createMenus()
        self.createToolbar()
        
        self.readSettings()
        #self.commands = copy.deepcopy(scenarios['cmu850'])
        #self.commands = copy.deepcopy(scenarios['cmu850_AllowAll'])
        self.commands = copy.deepcopy(scenarios['cmu900'])
        #self.commands = copy.deepcopy(scenarios['cmu900_AllowAll'])

        for key in sorted(scenarios.keys()):
            print(key)
            self.scenarioComboBox.addItem(key)


        self.lineEdit.setText(self.commands[0])

    def selectScenario(self, scenarioName):
        QtCore.qDebug("Hello From SelectScenario")
        QtCore.qDebug(scenarioName)
        self.commands = copy.deepcopy(scenarios[scenarioName])

    def createToolbar(self):
        self.fileToolBar = self.addToolBar("ATCommands Toolbar")
        self.fileToolBar.addAction(self.atAct)
        self.fileToolBar.addAction(self.modelAct)
        self.fileToolBar.addAction(self.pinAct)
        self.fileToolBar.addAction(self.moniAct)
        self.fileToolBar.addAction(self.smsoAct)
        self.fileToolBar.addAction(self.bandsAct)

    def createCentralWidget(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.lineEdit = QtGui.QLineEdit()
        self.textEdit = QtGui.QTextEdit()


        self.scenarioComboBox = QtGui.QComboBox(self)
        #                           currentIndexChanged = self.selectScenario )

#        self.connect(self.scenarioComboBox, 
#                      QtCore.SIGNAL("currentIndexChanged( const QString)"),                                                  self.selectScenario)
#
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.scenarioComboBox)
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
        self.smsoAct = QAction("Shutdown", self,  triggered=self.sendShutdown)

        self.addButtonAct = QAction("Add Button", self,triggered=self.addButton)

        self.quitAct = QAction("Quit", self, shortcut=QKeySequence.Quit,
                                                 triggered=QtGui.qApp.quit)

    def createActionGroup(self):
        self.actionGroup = QActionGroup(self,triggered=self.actionGroupTriggered)
        self.bandsAct = QAction("Bands?", self)
        self.bandsAct.setData("at^scfg=radio/band")
        self.actionGroup.addAction(self.bandsAct)

    def closeEvent(self, event):
        self.writeSettings()
        
    def readSettings(self):
        settings = QtCore.QSettings("REC", "MiniYatt")
        pos = settings.value("pos", QtCore.QPoint(200, 200))
        size = settings.value("size", QtCore.QSize(400, 400))
        self.resize(size)
        self.move(pos)

    def writeSettings(self):
        settings = QtCore.QSettings("REC", "MiniYatt")
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

    def openFile(self):
        QtCore.qDebug("Hello From Open FIle")

    def addButton(self):
        self.addButtonWidget = AddButtonWidget()
        self.addButtonWidget.setWindowModality(QtCore.Qt.ApplicationModal)
        self.addButtonWidget.resize(200,200)
        self.addButtonWidget.show()
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

    def actionGroupTriggered(self, action):
        QtCore.qDebug("Hello from actionGroupTriggered")
        QtCore.qDebug(action.data())
        self.socket.write(str.encode(action.data()) + b"\r\n")
        

    def sendMoni(self):
        self.socket.write(str.encode("at^moni") + b"\r\n")
    def sendPin(self):
        self.socket.write(str.encode("at+cpin=9999") + b"\r\n")
    def sendAt(self):
        self.socket.write(str.encode("at") + b"\r\n")
    def sendModel(self):
        self.socket.write(str.encode("at^siekret=1") + b"\r\n")
    def sendShutdown(self):
        self.socket.write(str.encode("at^smso") + b"\r\n")


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.stdout.write("DDD")
    sys.exit(app.exec_())

#   def playSequence(self):
#       #here comes all the logic
#       self.sequence.play();



#       self.sequence = Sequence(init_band = "AT^SCFG=radio/band,4,4",
#                                       first_band = "AT^SCFG=radio/band,8,8",
#                                      second_band = "AT^SCFG=radio/band,4,12")
#       self.playSequence();


#self.thread.newData.connect(self.textEdit2.setText)


#self.socket.write(b"AT\r\n")
#self.socket.write(b"AT" + b"\r\n")

#self.socket.write(str.encode("AT") + b"\r\n")


#NOT WORKING
#        self.connect(self.textEdit, QtCore.SIGNAL("returnPressed()"), self, QtCore.SLOT("sendData()"))

#WORKING
#        self.connect(self.textEdit, QtCore.SIGNAL("returnPressed()"), self.sendData)


