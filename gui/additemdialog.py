# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore
from core import map


class addItemDialog(QtGui.QDialog):
	"""
	Window to fill some informations to create an item
	label npc gender	npc gender field
	create button		cancel button
	"""
	_app = None
	_parent = None
	_coordinates = None

	_messageLabel = None

	_saveButton = None
	_cancelButton = None

	itemAdded = QtCore.pyqtSignal(int, int)

	def __init__(self, parent, app, coordinates):
		"""
		Creates the window GUI and displays the window
		"""
		QtGui.QDialog.__init__(self, parent)
		self._app = app
		self._parent = parent
		self._coordinates = coordinates
		self.setFixedWidth(250)
		self.initUI()
		self.setWindowTitle(self._title)
		self.setModal(True)
		self.show()

	def initUI(self):
		"""
		Creates the UI
		"""
		layout = QtGui.QGridLayout()

		self._messageLabel = QtGui.QLabel()
		self._messageLabel.setWordWrap(True)

		fieldsLayout = self.getFields()

		self._saveButton = QtGui.QPushButton("Create")
		self._saveButton.clicked.connect(self.createItem)
		self._cancelButton = QtGui.QPushButton("Cancel")
		self._cancelButton.clicked.connect(self._parent.unselectCell)
		self._cancelButton.clicked.connect(self.close)

		layout.addWidget(self._messageLabel, 0, 0, 1, 2)
		layout.addLayout(fieldsLayout, 1, 0, 1, 2)
		layout.addWidget(self._saveButton, 2, 0)
		layout.addWidget(self._cancelButton, 2, 1)

		self.setLayout(layout)

	def displayMessage(self, message):
		"""
		Method to display a message in the window.
		"""
		self._messageLabel.setText(message)
		self.adjustSize()


