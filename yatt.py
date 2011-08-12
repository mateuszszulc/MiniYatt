#!/usr/bin/env python

import sip
import sys
import serial

sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QWidget, QTextEdit, QLineEdit, QShortcut, QKeySequence


class SerialCommunicationThread(QtCore.QThread):

    def __init__(self, socket):
        super(QtCore.QThread, self).__init__()
        self.socket = socket
    def run(self):
        while (True):
          linia = self.socket.readline()
          QtCore.qDebug(linia)
          self.emit(QtCore.SIGNAL("newData"), bytes.decode(linia))

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(QtGui.QWidget, self).__init__()

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"));
        self.setWindowTitle("Mini Yatt Player")

        self.socket = serial.Serial(3,115200)
        self.thread = SerialCommunicationThread(self.socket)
        self.thread.start()

        self.textEdit = QtGui.QLineEdit()
        self.textEdit2 = QtGui.QTextEdit()
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.textEdit2)
        self.setLayout(self.layout)

        self.textEdit.returnPressed.connect(self.sendData)
        self.connect(self.thread, QtCore.SIGNAL("newData"), self.readNewData)
				
        self.createShortcuts()

#        self.sequence = Sequence(init_band = "AT^SCFG=radio/band,4,4",
#                                        first_band = "AT^SCFG=radio/band,8,8",
#                                       second_band = "AT^SCFG=radio/band,4,12")
#        self.playSequence();

        self.commands = []
        self.currentCommand = 0
        self.commands.append("AT^SCFG=Radio/Band,4,4")
        self.commands.append("AT+CPIN=9999")
        self.commands.append("AT+CMEE=2")
        self.commands.append("AT^SCFG=Radio/Band,8,12")
        self.commands.append("AT^SCFG=Radio/Band,4,4")
        self.commands.append("AT^SCFG=Radio/Band,4,12")

        self.textEdit.setText(self.commands[self.currentCommand])

#    def playSequence(self):
#        #here comes all the logic
#        self.sequence.play();
 
    def createShortcuts(self):
        self.shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcut.activated.connect(self.openFile)

    def openFile(self):
        QtCore.qDebug("Hello From Open FIle")

    def readNewData(self, data):
        data = data.strip()
        self.textEdit2.append(data)
        #self.textEdit2.append("\n")
        self.textEdit2.moveCursor(QtGui.QTextCursor.End)

    def sendData(self):
        QtCore.qDebug("sendData odpalone!")
        #QtCore.qDebug(self.textEdit.text())
        #self.socket.write(str.encode(self.textEdit.text()) + b"\r\n")
        self.socket.write(str.encode(self.commands[self.currentCommand]) + b"\r\n")
        self.currentCommand += 1
        self.textEdit.setText(self.commands[self.currentCommand])


#str.encode(self.textEdit.text())


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


