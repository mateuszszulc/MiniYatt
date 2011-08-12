#!/usr/bin/env python

import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui

class SerialCommunicationThread(QtCore.QThread):
    def __init__(self):
        super(QtCore.QThread, self).__init__()
    def run(self):
        while (True):
          self.sleep(1)
          print("Hello From Thread\n")

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(QtGui.QWidget, self).__init__()

        self.curFile = ''
        self.thread = SerialCommunicationThread()
        self.thread.start()
        self.textEdit = QtGui.QTextEdit()
        #self.setCentralWidget(self.textEdit)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.textEdit)
        self.setLayout(self.layout)

        self.readSettings()

    def about(self):
        QtGui.QMessageBox.about(self, "About Application",
                "The <b>Application</b> example demonstrates how to write "
                "modern GUI applications using Qt, with a menu bar, "
                "toolbars, and a status bar.")

    def readSettings(self):
        settings = QtCore.QSettings("REC", "Yatt")
        pos = settings.value("pos", QtCore.QPoint(200, 200))
        size = settings.value("size", QtCore.QSize(400, 400))
        self.resize(size)
        self.move(pos)

    def writeSettings(self):
        settings = QtCore.QSettings("REC", "Yatt")
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

    def maybeSave(self):
        if self.textEdit.document().isModified():
            ret = QtGui.QMessageBox.warning(self, "Application",
                    "The document has been modified.\nDo you want to save "
                    "your changes?",
                    QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                    QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Save:
                return self.save()
            elif ret == QtGui.QMessageBox.Cancel:
                return False
        return True

    def loadFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
               "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return

        inf = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.textEdit.setPlainText(inf.readAll())
        QtGui.QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File loaded", 2000)

    def saveFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
              "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False

        outf = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        outf << self.textEdit.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName);
        self.statusBar().showMessage("File saved", 2000)
        return True

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        self.textEdit.document().setModified(False)
        self.setWindowModified(False)

        if self.curFile:
            shownName = self.strippedName(self.curFile)
        else:
            shownName = 'untitled.txt'

        self.setWindowTitle("%s[*] - Application" % shownName)

    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
