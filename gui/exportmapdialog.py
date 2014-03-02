# -*- coding: utf8 -*-

from PyQt4 import QtGui
from core.localisation import _


class exportMapDialog(QtGui.QDialog):
	"""
	Class displaying the progression of a map export.
	"""
	_thread = None

	def __init__(self, parent):
		"""
		Window initialisation.
		Creates the GUI and displays the window.
		"""
		QtGui.QDialog.__init__(self, parent)
		self.initUI()
		self.setWindowTitle(_('EXPORT_MAP_DIALOG_TITLE'))
		self.setModal(True)
		self.show()

	def setThread(self, thread):
		"""
		Set the generator's thread.
		"""
		self._thread = thread
		self._thread.notifyProgressLocal.connect(self.onProgressLocal)
		self._thread.notifyProgressMain.connect(self.onProgressMain)

	def initUI(self):
		"""
		Creates the window GUI.
		The GUI is just two progress bars.
		"""
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
		"""
		Method to update the first progress bar, being the progress of the
		current action.
		"""
		self.progressBarLocal.setValue(i)
		self.messageLabel.setText(message)

	def onProgressMain(self, i, message):
		"""
		Method to update the second progress bar, being the progress of the
		whole export.
		"""
		self.progressBarMain.setValue(i)
		self.messageLabel.setText(message)
