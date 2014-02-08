# -*- coding: utf8 -*-

from PyQt4 import QtGui
from gui.intlineedit import intLineEdit
from core import config, worker


class newMapDialog(QtGui.QDialog):
	"""
	Window to fill some informations to create a map
	label map name		map name field
	label map width		map width field
	label map height	map height field
	create button		cancel button
	"""
	_app = None
	_parent = None

	_name = None
	_messageLabel = None
	_mapNameField = None
	_mapWidthField = None
	_mapHeightField = None

	_saveButton = None
	_cancelButton = None

	_thread = None

	def __init__(self, parent, app):
		QtGui.QWidget.__init__(self, parent)
		self._app = app
		self._parent = parent
		self.setFixedWidth(250)
		self.initUI()
		self.setWindowTitle('Create new map')
		self.show()

	def initUI(self):
		layout = QtGui.QGridLayout()

		self._messageLabel = QtGui.QLabel()
		self._messageLabel.setWordWrap(True)

		mapNameLabel = QtGui.QLabel("Map name")
		self._mapNameField = QtGui.QLineEdit()

		mapWidthLabel = QtGui.QLabel("Map width")
		self._mapWidthField = intLineEdit()
		self._mapWidthField.setText(str(config.map_default_width))

		mapHeightLabel = QtGui.QLabel("Map height")
		self._mapHeightField = intLineEdit()
		self._mapHeightField.setText(str(config.map_default_height))

		self._saveButton = QtGui.QPushButton("Create")
		self._saveButton.clicked.connect(self.createMap)
		self._cancelButton = QtGui.QPushButton("Cancel")
		self._cancelButton.clicked.connect(self.close)

		layout.addWidget(self._messageLabel, 0, 0, 1, 2)
		layout.addWidget(mapNameLabel, 1, 0)
		layout.addWidget(self._mapNameField, 1, 1)
		layout.addWidget(mapWidthLabel, 2, 0)
		layout.addWidget(self._mapWidthField, 2, 1)
		layout.addWidget(mapHeightLabel, 3, 0)
		layout.addWidget(self._mapHeightField, 3, 1)
		layout.addWidget(self._saveButton, 4, 0)
		layout.addWidget(self._cancelButton, 4, 1)

		self.setLayout(layout)

	def createMap(self):
		valid = True
		try:
			self._name = self._mapNameField.text()
			width = self._mapWidthField.value()
			height = self._mapHeightField.value()

			if width <= 0 or height <= 0:
				self.displayMessage("Positive number expected for the width and the height")
				valid = False
		except ValueError:
			self.displayMessage("Positive number expected for the width and the height")
			valid = False

		if valid:
			self.displayMessage("Generating...")
			self._saveButton.setEnabled(False)
			self._cancelButton.setEnabled(False)
			self._thread = worker.generatorThread(self._app, self._name, width, height)
			self._thread.finished.connect(self.confirmCreation)
			self._thread.start()

	def displayMessage(self, message):
		self._messageLabel.setText(message)
		self.adjustSize()

	def confirmCreation(self):
		filename = self._name + '.bmp'
		filename = config.tempDir + '/' + filename
		self._parent.openMap(self._name, filename)
		self.close()
