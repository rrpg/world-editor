# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from gui.intlineedit import intLineEdit
from core import config, worker
from core.localisation import _


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

	_messageLabel = None
	_mapNameField = None
	_mapWidthField = None
	_mapHeightField = None

	_saveButton = None
	_cancelButton = None

	_thread = None

	def __init__(self, parent, app):
		"""
		Creates the window GUI and displays the window
		"""
		QtGui.QDialog.__init__(self, parent)
		self._app = app
		self._parent = parent
		self.setFixedWidth(250)
		self.initUI()
		self.setWindowTitle(_('NEW_MAP_DIALOG_TITLE'))
		self.setModal(True)
		self.show()

	def initUI(self):
		"""
		Creates the UI
		"""
		layout = QtGui.QGridLayout()

		self._messageLabel = QtGui.QLabel()
		self._messageLabel.setWordWrap(True)

		mapNameLabel = QtGui.QLabel(_('MAP_NAME_LABEL'))
		self._mapNameField = QtGui.QLineEdit()

		mapWidthLabel = QtGui.QLabel(_('MAP_WIDTH_LABEL'))
		self._mapWidthField = QtGui.QSpinBox()
		self._mapWidthField.setMinimum(config.map_minimum_width)
		self._mapWidthField.setMaximum(config.map_maximum_width)
		self._mapWidthField.setValue(config.map_default_width)

		mapHeightLabel = QtGui.QLabel(_('MAP_HEIGHT_LABEL'))
		self._mapHeightField = QtGui.QSpinBox()
		self._mapHeightField.setMinimum(config.map_minimum_height)
		self._mapHeightField.setMaximum(config.map_maximum_height)
		self._mapHeightField.setValue(config.map_default_height)

		self._saveButton = QtGui.QPushButton(_('CREATE_BUTTON'))
		self._saveButton.clicked.connect(self.createMap)
		self._cancelButton = QtGui.QPushButton(_('CANCEL_BUTTON'))
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
		"""
		Method called when the "Create" button is pressed.
		The filled values are checked and if they are correct, a map is
		generated, in a thread
		"""
		valid = True
		try:
			name = str(self._mapNameField.text()).strip()
			width = self._mapWidthField.value()
			height = self._mapHeightField.value()

			if width <= 0 or height <= 0:
				self.displayMessage(_('ERROR_INVALID_WIDTH_HEIGHT_VALUE'))
				valid = False
			elif name == "":
				self.displayMessage(_('ERROR_EMPTY_MAP_NAME'))
				valid = False
		except ValueError:
			self.displayMessage(_('ERROR_INVALID_WIDTH_HEIGHT_VALUE'))
			valid = False

		if valid:
			self._app.setMapName(name)
			name = config.tempDir + '/' + self._app.escapeName(name)
			self._app.setMapFileName(name)
			self.displayMessage(_('LOADING_GENERATION_TEXT'))
			self._saveButton.setEnabled(False)
			self._cancelButton.setEnabled(False)
			self._thread = worker.generatorThread(self._app, width, height)
			self._thread.generatorError.connect(self.displayMessage)
			self._thread.generatorSuccess.connect(self._parent.openMap)
			self._thread.generatorSuccess.connect(self.close)
			self._thread.start()

	def displayMessage(self, message):
		"""
		Method to display a message in the window.
		"""
		self._messageLabel.setText(message)
		self.adjustSize()

