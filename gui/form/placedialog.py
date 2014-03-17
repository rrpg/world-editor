# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from core import map
import gui.form.entitydialog
from core.localisation import _


class formPlaceDialog(gui.form.entitydialog.entityDialog):
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

	def __init__(self, parent, app, coordinates=None, row=None):
		"""
		Creates the window GUI and displays the window
		"""
		gui.form.entitydialog.entityDialog.__init__(self, parent, app, coordinates, row)
		self.entityType = 'places'

	def getFields(self, place=None):
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

		if place is not None:
			self._placeNameField.setText(place['name'])
			self._placeInternalNameField.setText(place['internalName'])
			self._placeTypeField.setCurrentIndex(place['type'])
			self._placeSizeField.setCurrentIndex(place['size'])

		layout.addWidget(placeInternalNameLabel, 0, 0)
		layout.addWidget(self._placeInternalNameField, 0, 1)
		layout.addWidget(placeNameLabel, 1, 0)
		layout.addWidget(self._placeNameField, 1, 1)
		layout.addWidget(placeTypeLabel, 2, 0)
		layout.addWidget(self._placeTypeField, 2, 1)
		layout.addWidget(placeSizeLabel, 3, 0)
		layout.addWidget(self._placeSizeField, 3, 1)

		return layout

	def validateFormData(self):
		valid = True
		name = str(self._placeNameField.text()).strip()
		internalName = str(self._placeInternalNameField.text()).strip()

		if internalName == "":
			self.displayMessage(_('ERROR_EMPTY_PLACE_INTERNAL_NAME'))
			valid = False
		elif self._editedRow != internalName and self._app.hasEntityWithName(self.entityType, internalName):
			self.displayMessage(_('ERROR_DUPLICATE_PLACE_INTERNAL_NAME'))
			valid = False
		if name == "":
			self.displayMessage(_('ERROR_EMPTY_PLACE_NAME'))
			valid = False

		if valid is False:
			return False

		return {
			'name': name,
			'type': self._placeTypeField.currentIndex(),
			'size': self._placeSizeField.currentIndex(),
			'internalName': internalName
		}
