#!/usr/bin/env python

import sip
import sys
import serial

sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QWidget, QTextEdit, QLineEdit, QShortcut, QKeySequence



#Seq44_88_315 = {'start' : (4,4), 'command' : (8,8) }

#command = {'comand' : (4,4), 'expected' : (8,8), 'timeout' : 5 }

class TestingSequence:
    def __init__(self, command, expected, timeout):
        self.command = command
        self.expected = expected
        self.timeout = timeout
        #self.delay = delay


class Sequence:
    def __init__(self, init_band, first_band, second_band):
        self.seq = []

				#INIT
        self.seq.append(TestingSequence("AT^SMSO", "SYSTART", 0)) #0 czeka bezwzl
        self.seq.append(TestingSequence(init_band, "OK", 2))
        self.seq.append(TestingSequence("AT^SMSO", "SYSTART", 3))

        self.seq.append(TestingSequence("AT+CPIN=2","CREG 0;CREG 2;CREG 0", 3))

        self.seq.append(TestingSequence(first_band, "OK", 3))
        self.seq.append(TestingSequence("", "CREG 5", 10))

        self.seq.append(TestingSequence(second_band, "OK", 3))
        self.seq.append(TestingSequence("", "CREG 5", 10))

    def play(self):
        while ( len(self.seq) > 0 ) :
            next = self.seq.pop(0)
            print(next.command)
            
class SequencePlayer:
    def __init__(self, socket, seq):
        self.socket = socket
        self.seq = seq
        self.play()
    def play(self):
        self.socket.write(seq.command)
				try 
				{
					sleep(5)
          print("nie dostalem danych")
				}
        catch
        {
            print("Obsluga danych")

        }
    def dataReceived(self):
        #....

        # teraz czekaj na timeout lub na sygnal w zaleznosci od tego,
        # co bedzie wczesniej


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

        self.sequence = Sequence(init_band = "AT^SCFG=radio/band,4,4",
                                        first_band = "AT^SCFG=radio/band,8,8",
                                       second_band = "AT^SCFG=radio/band,4,12")
        self.playSequence();
    def playSequence(self):
        #here comes all the logic
        self.sequence.play();
 
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
        QtCore.qDebug("ALa ma kota")
        QtCore.qDebug(self.textEdit.text())
        #self.socket.write(b"AT\r\n")
        #self.socket.write(b"AT" + b"\r\n")

        #self.socket.write(str.encode("AT") + b"\r\n")
        self.socket.write(str.encode(self.textEdit.text()) + b"\r\n")

#str.encode(self.textEdit.text())


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.stdout.write("DDD")
    sys.exit(app.exec_())

#self.thread.newData.connect(self.textEdit2.setText)



#NOT WORKING
#        self.connect(self.textEdit, QtCore.SIGNAL("returnPressed()"), self, QtCore.SLOT("sendData()"))

#WORKING
#        self.connect(self.textEdit, QtCore.SIGNAL("returnPressed()"), self.sendData)


#    def about(self):
#        QtGui.QMessageBox.about(self, "About Application",
#                "The <b>Application</b> example demonstrates how to write "
#                "modern GUI applications using Qt, with a menu bar, "
#                "toolbars, and a status bar.")
#
#    def readSettings(self):
#        settings = QtCore.QSettings("REC", "Yatt")
#        pos = settings.value("pos", QtCore.QPoint(200, 200))
#        size = settings.value("size", QtCore.QSize(400, 400))
#        self.resize(size)
#        self.move(pos)
#
#    def writeSettings(self):
#        settings = QtCore.QSettings("REC", "Yatt")
#        settings.setValue("pos", self.pos())
#        settings.setValue("size", self.size())
#
#    def maybeSave(self):
#        if self.textEdit.document().isModified():
#            ret = QtGui.QMessageBox.warning(self, "Application",
#                    "The document has been modified.\nDo you want to save "
#                    "your changes?",
#                    QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
#                    QtGui.QMessageBox.Cancel)
#            if ret == QtGui.QMessageBox.Save:
#                return self.save()
#            elif ret == QtGui.QMessageBox.Cancel:
#                return False
#        return True
#
#    def loadFile(self, fileName):
#        file = QtCore.QFile(fileName)
#        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
#            QtGui.QMessageBox.warning(self, "Application",
#               "Cannot read file %s:\n%s." % (fileName, file.errorString()))
#            return
#
#        inf = QtCore.QTextStream(file)
#        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
#        self.textEdit.setPlainText(inf.readAll())
#        QtGui.QApplication.restoreOverrideCursor()
#
#        self.setCurrentFile(fileName)
#        self.statusBar().showMessage("File loaded", 2000)
#
#    def saveFile(self, fileName):
#        file = QtCore.QFile(fileName)
#        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
#            QtGui.QMessageBox.warning(self, "Application",
#              "Cannot write file %s:\n%s." % (fileName, file.errorString()))
#            return False
#
#        outf = QtCore.QTextStream(file)
#        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
#        outf << self.textEdit.toPlainText()
#        QtGui.QApplication.restoreOverrideCursor()
#
#        self.setCurrentFile(fileName);
#        self.statusBar().showMessage("File saved", 2000)
#        return True
