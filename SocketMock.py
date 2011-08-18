from threading import Event
from PyQt4 import QtCore

class SocketMock():
    def __init__(self):
        self.newDataNotify = Event()
#        QtCore.qDebug("MOCK INIT")
    def readline(self):
#        QtCore.qDebug("MOCK WAIT")
        self.newDataNotify.wait()
#        QtCore.qDebug("MOCK CLEAR")
        self.newDataNotify.clear()
        return str.encode(bytes.decode(self.newData) + "\n" + "OK")

    def write(self, writeData):
#        QtCore.qDebug("MOCK SET")
        self.newData = writeData
        self.newDataNotify.set()


