# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore
from core import map
import gui.form.itemdialog
from core.localisation import _


class formPlaceDialog(gui.form.itemdialog.itemDialog):
	"""
	Window to fill some informations to create a place
	label place type	place type field
	label place name	place name field
	label place size	place size field
	create button		cancel button
	"""

	_placeInternalNameField = None
	_placeNameField = None
	_placeTypeField = None
	_placeSizeField = None

	_title = _('NEW_PLACE_DIALOG_TITLE')

	def getFields(self):
		"""
		Creates the UI
		"""
		layout = QtGui.QGridLayout()

		placeInternalNameLabel = QtGui.QLabel(_('PLACE_INTERNAL_NAME_LABEL'))
		self._placeInternalNameField = QtGui.QLineEdit()

		placeNameLabel = QtGui.QLabel(_('PLACE_NAME_LABEL'))
		self._placeNameField = QtGui.QLineEdit()

		placeTypeLabel = QtGui.QLabel(_('PLACE_TYPE_LABEL'))
		self._placeTypeField = QtGui.QComboBox()
		self._placeTypeField.addItems(map.map.getPlaceTypesLabels())

		placeSizeLabel = QtGui.QLabel(_('PLACE_SIZE_LABEL'))
		self._placeSizeField = QtGui.QComboBox()
		self._placeSizeField.addItems(map.map.getPlaceSizesLabels())

		layout.addWidget(placeInternalNameLabel, 0, 0)
		layout.addWidget(self._placeInternalNameField, 0, 1)
		layout.addWidget(placeNameLabel, 1, 0)
		layout.addWidget(self._placeNameField, 1, 1)
		layout.addWidget(placeTypeLabel, 2, 0)
		layout.addWidget(self._placeTypeField, 2, 1)
		layout.addWidget(placeSizeLabel, 3, 0)
		layout.addWidget(self._placeSizeField, 3, 1)

		return layout

	def createItem(self):
		"""
		Method called when the "Create" button is pressed.
		The filled values are checked and if they are correct, a place is created
		"""
		valid = True
		name = str(self._placeNameField.text()).strip()
		internalName = str(self._placeInternalNameField.text()).strip()

		if internalName == "":
			self.displayMessage(_('ERROR_EMPTY_PLACE_INTERNAL_NAME'))
			valid = False
		elif self._app.hasPlaceWithName(internalName):
			self.displayMessage(_('ERROR_DUPLICATE_PLACE_INTERNAL_NAME'))
			valid = False
		if name == "":
			self.displayMessage(_('ERROR_EMPTY_PLACE_NAME'))
			valid = False

		if valid:
			self._app.addPlace(internalName, {
				'name': name,
				'type': self._placeTypeField.currentIndex(),
				'size': self._placeSizeField.currentIndex(),
				'x': self._coordinates[0],
				'y': self._coordinates[1],
				'internalName': internalName
			})
			self.itemAdded.emit(self._coordinates[0], self._coordinates[1])
			self.accept()
			self.close()
