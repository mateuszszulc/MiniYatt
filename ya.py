#!/usr/bin/env python

import sip
import sys
import serial

sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui

class SerialCommunicationThread(QtCore.QThread):
    def __init__(self, socket):
        super(QtCore.QThread, self).__init__()
        self.socket = socket
    def run(self):
        while (True):
          linia = self.socket.readline()
          QtCore.qDebug(linia)
          self.emit(QtCore.SIGNAL("newData"), str(linia))
          #sys.stdout.write("Testsssss\n")

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(QtGui.QWidget, self).__init__()

        self.curFile = ''
        self.socket = serial.Serial(3,115200)
        self.thread = SerialCommunicationThread(self.socket)
        self.thread.start()
        self.textEdit = QtGui.QLineEdit()
        self.textEdit2 = QtGui.QLineEdit()
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.textEdit2)
        self.setLayout(self.layout)

        self.textEdit.returnPressed.connect(self.sendData)
        self.connect(self.thread, QtCore.SIGNAL("newData"), self.textEdit2.setText)
    def sendData2(self, napis):
        QtCore.qDebug(napis)

    def sendData(self):
        QtCore.qDebug(self.textEdit.text())
        self.socket.write(str.encode(self.textEdit.text()) + b"\r\n")

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.stdout.write("DDD")
    sys.exit(app.exec_())
