#!/usr/bin/env python

import sip
import sys
import serial
from serial import SerialException
from copy import deepcopy
import socket

sip.setapi('QVariant', 2)

from PyQt4.QtCore import QThread
from PyQt4.QtGui import QWidget, QTextEdit, QLineEdit, QShortcut, QKeySequence
from PyQt4.QtGui import QAction, QIcon, QActionGroup, QComboBox

from SerialCommunicationThread import *
from AddButtonWidget import *
from SequenceFactory import *
from SocketMock import *

class MainWindow(QtGui.QMainWindow):
    class MODES:
      MODE_MANUAL = 1
      MODE_SEQUENCE_PLAYER = 2
    def __init__(self, mock = None):
        super(QtGui.QMainWindow, self).__init__()

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"));
        self.setWindowTitle("Mini Yatt")
        self.mock = mock

        self.mode = self.MODES.MODE_SEQUENCE_PLAYER

        self.currentCmd = 0 

        self.setupSocketThread()
        self.createCentralWidget()

        self.lineEdit.returnPressed.connect(self.sendData)
        self.connect(self.thread, QtCore.SIGNAL("newData"), self.readNewData)
				
        self.createShortcuts()
        self.createActions()
        self.createToolbar()
        self.createActionGroup()
        self.createMenus()
        
        self.readSettings()
        self.connect(self.scenarioComboBox, 
                      QtCore.SIGNAL("currentIndexChanged( const QString)"),                                                  self.selectScenario)

        for sequenceName in sorted(SequenceFactory().getAllSequenceNames()):
            print(sequenceName)
            self.scenarioComboBox.addItem(sequenceName)

    def createToolbar(self):
        self.fileToolBar = self.addToolBar("ATCommands Toolbar")
        self.fileToolBar.addAction(self.addAct)

    def createCentralWidget(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.lineEdit = QtGui.QLineEdit()
        self.textEdit = QtGui.QTextEdit()


        self.scenarioComboBox = QtGui.QComboBox(self)
        #                           currentIndexChanged = self.selectScenario )

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.scenarioComboBox)
        centralWidget.setLayout(self.layout)

    def actionFactory(self, actionName, atCmd):
        newActionObject = QAction(actionName, self)
        newActionObject.setData(atCmd)
        return newActionObject

    def setupSocketThread (self):
        self.socket = None
        
        if self.mock == True:
            QtCore.qDebug("MOCK MODE ON")
            self.socket = SocketMock()
        else:
          try:
              self.socket = serial.Serial(3,115200)
          except SerialException as e:
              QtCore.qDebug("Exception catched!")
              QtGui.QMessageBox.about(self, "Error", "Socket in use")

        self.thread = SerialCommunicationThread(self.socket)
        self.thread.start()
            

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("File")
        self.fileMenu.addAction(self.quitAct)

        #self.toolbarMenu = self.menuBar().addMenu("Toolbar")
        #self.toolbarMenu.addAction(self.addButtonAct)

    def createShortcuts(self):
        self.shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcut.activated.connect(self.openFile)

        self.upArrow = QShortcut(QKeySequence("Up"), self)
        self.upArrow.activated.connect(self.previousCmd)

        self.downArrow = QShortcut(QKeySequence("Down"), self)
        self.downArrow.activated.connect(self.nextCmd)

    def previousCmd(self):
        QtCore.qDebug("Hello From Up")
        self.currentCmd -= 1

    def nextCmd(self):
        QtCore.qDebug("Hello From Down")
        self.currentCmd += 1
        
    def createActions(self):
        self.addAct = QAction(QIcon("addIcon16.png"), "Add", self, 
                                                triggered=self.addButton)

        #self.addButtonAct = QAction("Add Button",self,triggered=self.addButton)

        self.quitAct = QAction("Quit", self, shortcut=QKeySequence.Quit,
                                                 triggered=QtGui.qApp.quit)

    def createActionGroup(self):
        self.actionGroup=QActionGroup(self,triggered=self.actionGroupTriggered)

        allActionsItemList = []
        allActionsItemList.append(["Bands?", "at^scfg=radio/band"])
        allActionsItemList.append(["at^moni", "at^moni"])
        allActionsItemList.append(["PIN","at+cpin=9999"])
        allActionsItemList.append(["PIN?","at+cpin?"])
        allActionsItemList.append(["AT", "AT"])
        allActionsItemList.append(["Model","at^siekret=1"])
        allActionsItemList.append(["Shutdown","at^smso"])

        for actionItem in allActionsItemList:
            newActionObject = self.actionFactory(actionItem[0], actionItem[1])
            self.actionGroup.addAction(newActionObject)
            self.fileToolBar.addAction(newActionObject)

    def selectScenario(self, sequenceName):
        QtCore.qDebug("Hello From SelectScenario")
        QtCore.qDebug(sequenceName)
        self.commands = deepcopy(SequenceFactory().getSequence(sequenceName))
        self.currentCmd = 0
        self.lineEdit.setText(self.commands[0])

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
        msg = self.lineEdit.text()
        self.socket.write(str.encode(msg) + b"\r\n")

        if self.mode == self.MODES.MODE_SEQUENCE_PLAYER:
            self.currentCmd += 1
            self.lineEdit.setText(self.commands[self.currentCmd])
        else:
            addHistory(msg)
            self.lineEdit.setText("")

    def actionGroupTriggered(self, action):
        QtCore.qDebug("Hello from actionGroupTriggered")
        QtCore.qDebug(action.data())
        self.socket.write(str.encode(action.data()) + b"\r\n")
        
if __name__ == '__main__':

    import sys
    import platform

    app = QtGui.QApplication(sys.argv)
    
    mainWin = MainWindow(platform.node() == "vermont")

    mainWin.show()
    sys.exit(app.exec_())

# senddata
#QtCore.qDebug(self.textEdit.text())
#self.socket.write(str.encode(self.textEdit.text()) + b"\r\n")

######## Dodawanie przycisku do toolbara akcji
#self.actionGroup.addAction("at^moni", "at^moni") #QKeySequence.New!


#self.pinAct = QAction("at+cpin=9999", self, triggered=self.sendPin)
#self.atAct = QAction("at", self, triggered=self.sendAt)
#self.modelAct = QAction("model", self,  triggered=self.sendModel)
#self.smsoAct = QAction("Shutdown", self,  triggered=self.sendShutdown)
#####################


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


        #self.commands = copy.deepcopy(scenarios['cmu850'])
        #self.commands = copy.deepcopy(scenarios['cmu850_AllowAll'])
        #self.commands = copy.deepcopy(scenarios['cmu900'])
        #self.commands = copy.deepcopy(scenarios['cmu900_AllowAll'])

