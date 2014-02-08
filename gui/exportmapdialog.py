# -*- coding: utf8 -*-

from PyQt4 import QtGui


class exportMapDialog(QtGui.QDialog):
	_thread = None

	def __init__(self, parent):
		QtGui.QDialog.__init__(self, parent)
		self.initUI()
		self.setWindowTitle('Export map')
		self.show()

	def setThread(self, thread):
		self._thread = thread
		self._thread.notifyProgressLocal.connect(self.onProgressLocal)
		self._thread.notifyProgressMain.connect(self.onProgressMain)

	def initUI(self):
		vbox = QtGui.QVBoxLayout()

		self.messageLabel = QtGui.QLabel()
		self.progressBarLocal = QtGui.QProgressBar(self)
		self.progressBarLocal.setRange(0,100)
		self.progressBarMain = QtGui.QProgressBar(self)
		self.progressBarMain.setRange(0,100)

		vbox.addWidget(self.messageLabel)
		vbox.addWidget(self.progressBarLocal)
		vbox.addWidget(self.progressBarMain)

		self.setLayout(vbox)

	def onProgressLocal(self, i, message):
		self.progressBarLocal.setValue(i)
		self.messageLabel.setText(message)

	def onProgressMain(self, i, message):
		self.progressBarMain.setValue(i)
		self.messageLabel.setText(message)
