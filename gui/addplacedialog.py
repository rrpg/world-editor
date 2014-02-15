# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore
from core import map


class addPlaceDialog(QtGui.QDialog):
	"""
	Window to fill some informations to create a place
	label place type	place type field
	label place name	place name field
	label place size	place size field
	create button		cancel button
	"""
	_app = None
	_parent = None
	_coordinates = None

	_messageLabel = None
	_placeTypeField = None
	_placeNameField = None
	_placeSizeField = None

	_saveButton = None
	_cancelButton = None

	placeAdded = QtCore.pyqtSignal(int, int)

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
		self.setWindowTitle('Create new place')
		self.setModal(True)
		self.show()

	def initUI(self):
		"""
		Creates the UI
		"""
		layout = QtGui.QGridLayout()

		self._messageLabel = QtGui.QLabel()
		self._messageLabel.setWordWrap(True)

		placeTypeLabel = QtGui.QLabel("Place type")
		self._placeTypeField = QtGui.QComboBox()
		self._placeTypeField.addItems(map.map.getPlaceTypesLabels())

		placeNameLabel = QtGui.QLabel("Place name")
		self._placeNameField = QtGui.QLineEdit()

		placeSizeLabel = QtGui.QLabel("Place size")
		self._placeSizeField = QtGui.QComboBox()
		self._placeSizeField.addItems(map.map.getPlaceSizesLabels())

		self._saveButton = QtGui.QPushButton("Create")
		self._cancelButton = QtGui.QPushButton("Cancel")
		self._cancelButton.clicked.connect(self.close)

		layout.addWidget(self._messageLabel, 0, 0, 1, 2)
		layout.addWidget(placeTypeLabel, 1, 0)
		layout.addWidget(self._placeTypeField, 1, 1)
		layout.addWidget(placeNameLabel, 2, 0)
		layout.addWidget(self._placeNameField, 2, 1)
		layout.addWidget(placeSizeLabel, 3, 0)
		layout.addWidget(self._placeSizeField, 3, 1)
		layout.addWidget(self._saveButton, 4, 0)
		layout.addWidget(self._cancelButton, 4, 1)

		self.setLayout(layout)

	def displayMessage(self, message):
		"""
		Method to display a message in the window.
		"""
		self._messageLabel.setText(message)
		self.adjustSize()

