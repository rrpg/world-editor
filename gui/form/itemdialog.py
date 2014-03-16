# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from core import map
from core.localisation import _


class itemDialog(QtGui.QDialog):
	"""
	Window to fill some informations to create an item
	All items contains two fields for their coordinates if the item is edited
	"""
	_app = None
	_parent = None
	_coordinates = None

	_messageLabel = None

	_saveButton = None
	_cancelButton = None

	itemAdded = QtCore.pyqtSignal(str, int, int)
	itemUpdated = QtCore.pyqtSignal(str, int, int)

	def __init__(self, parent, app, coordinates=None, row=None):
		"""
		Creates the window GUI and displays the window
		"""
		QtGui.QDialog.__init__(self, parent)
		self._app = app
		self._parent = parent
		self._editedRow = None
		if coordinates is None and row is None:
			raise BaseException("At least a row or a tuple of coordinates is needed")
		elif coordinates is None:
			self._editedRow = row['internalName']
			self._coordinates = (row['x'], row['y'])
		else:
			self._coordinates = coordinates

		self._row = row
		self.setFixedWidth(250)
		self.initUI()
		self.setWindowTitle(self._title)
		self.setModal(True)
		self.connectSignals()
		self.show()

	def initUI(self):
		"""
		Creates the UI
		"""
		layout = QtGui.QGridLayout()

		self._messageLabel = QtGui.QLabel()
		self._messageLabel.setWordWrap(True)

		if self._editedRow is not None:
			itemXLabel = QtGui.QLabel(_('ITEM_X_LABEL'))
			self._itemXField = QtGui.QSpinBox()
			self._itemXField.setMinimum(0)
			self._itemXField.setMaximum(self._app.map.width)
			self._itemXField.setValue(self._row['x'])

			itemYLabel = QtGui.QLabel(_('ITEM_Y_LABEL'))
			self._itemYField = QtGui.QSpinBox()
			self._itemYField.setMinimum(0)
			self._itemYField.setMaximum(self._app.map.height)
			self._itemYField.setValue(self._row['y'])

		fieldsLayout = self.getFields(self._row)

		if self._editedRow is not None:
			self._saveButton = QtGui.QPushButton(_('EDIT_BUTTON'))
		else:
			self._saveButton = QtGui.QPushButton(_('CREATE_BUTTON'))
		self._saveButton.clicked.connect(self.saveItem)
		self._cancelButton = QtGui.QPushButton(_('CANCEL_BUTTON'))
		self._cancelButton.clicked.connect(self.close)

		layout.addWidget(self._messageLabel, 0, 0, 1, 2)
		gridRow = 0
		if self._editedRow is not None:
			layout.addWidget(itemXLabel, 1, 0)
			layout.addWidget(self._itemXField, 1, 1)
			layout.addWidget(itemYLabel, 2, 0)
			layout.addWidget(self._itemYField, 2, 1)
			gridRow = 2
		layout.addLayout(fieldsLayout, 1 + gridRow, 0, 1, 2)
		layout.addWidget(self._saveButton, 2 + gridRow, 0)
		layout.addWidget(self._cancelButton, 2 + gridRow, 1)

		self.setLayout(layout)

	def connectSignals(self):
		"""
		Connect a signal to unselect the cell if the window is rejected
		"""
		self.rejected.connect(self._parent.unselectCell)

	def displayMessage(self, message):
		"""
		Method to display a message in the window.
		"""
		self._messageLabel.setText(message)
		self.adjustSize()

	def saveItem(self):
		"""
		Method called when the "Create" button is pressed.
		The filled values are checked and if they are correct, an entity is
		created or updated
		"""
		x = self._coordinates[0]
		y = self._coordinates[1]
		if self._editedRow is not None:
			x = int(self._itemXField.value())
			y = int(self._itemYField.value())


		if not self._app.map.isCellOnLand((x, y)):
			self.displayMessage(_('ERROR_ITEM_IN_WATER'))
			data = False
		else:
			data = self.validateFormData()

		if data is not False:
			if self._editedRow is not None:
				self._app.deleteEntity(self.entityType, self._editedRow)

			data['x'] = x
			data['y'] = y
			self._app.addEntity(self.entityType, data['internalName'], data)

			if self._editedRow is not None:
				self._editedRow = None
				self.itemUpdated.emit(self.entityType, x, y)
			else:
				self.itemAdded.emit(self.entityType, x, y)
			self.accept()
			self.close()

