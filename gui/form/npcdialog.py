# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from core import map
import gui.form.entitydialog
from core.localisation import _


class formNpcDialog(gui.form.entitydialog.entityDialog):
	"""
	Window to fill some informations to create a NPC
	label npc name      npc name field
	label npc species   npc species field
	label npc gender    npc gender field
	create button       cancel button
	"""
	_npcInternalNameField = None
	_npcNameField = None
	_npcTypeField = None
	_npcSizeField = None

	_title = _('NEW_NPC_DIALOG_TITLE')

	def __init__(self, parent, app, coordinates=None, row=None):
		"""
		Creates the window GUI and displays the window
		"""
		gui.form.entitydialog.entityDialog.__init__(self, parent, app, coordinates, row)
		self.entityType = 'npc'

	def getFields(self, npc=None):
		"""
		Creates the UI
		"""
		layout = QtGui.QGridLayout()

		npcInternalNameLabel = QtGui.QLabel(_('NPC_INTERNAL_NAME_LABEL'))
		self._npcInternalNameField = QtGui.QLineEdit()

		npcNameLabel = QtGui.QLabel(_('NPC_NAME_LABEL'))
		self._npcNameField = QtGui.QLineEdit()

		npcSpeciesLabel = QtGui.QLabel(_('NPC_SPECIES_LABEL'))
		self._npcSpeciesField = QtGui.QComboBox()
		self._npcSpeciesField.addItems(self._app.map.getSpeciesNames())

		npcGenderLabel = QtGui.QLabel(_('NPC_GENDER_LABEL'))
		self._npcGenderField = QtGui.QComboBox()
		self._npcGenderField.addItems(map.map.getGenders())

		if npc is not None:
			self._npcNameField.setText(npc['name'])
			self._npcInternalNameField.setText(npc['internalName'])
			self._npcSpeciesField.setCurrentIndex(npc['species'])
			self._npcGenderField.setCurrentIndex(npc['gender'])

		layout.addWidget(npcInternalNameLabel, 0, 0)
		layout.addWidget(self._npcInternalNameField, 0, 1)
		layout.addWidget(npcNameLabel, 1, 0)
		layout.addWidget(self._npcNameField, 1, 1)
		layout.addWidget(npcSpeciesLabel, 2, 0)
		layout.addWidget(self._npcSpeciesField, 2, 1)
		layout.addWidget(npcGenderLabel, 3, 0)
		layout.addWidget(self._npcGenderField, 3, 1)

		return layout

	def validateFormData(self):
		valid = True
		internalName = str(self._npcInternalNameField.text()).strip()
		name = str(self._npcNameField.text()).strip()
		species = int(self._npcSpeciesField.currentIndex())
		gender = int(self._npcGenderField.currentIndex())

		if internalName == "":
			self.displayMessage(_('ERROR_EMPTY_NPC_INTERNAL_NAME'))
			valid = False
		elif self._editedRow != internalName and self._app.hasEntityWithName(self.entityType, internalName):
			self.displayMessage(_('ERROR_DUPLICATE_NPC_INTERNAL_NAME'))
			valid = False
		if name == "":
			self.displayMessage(_('ERROR_EMPTY_NPC_NAME'))
			valid = False
		if species < 0 or species >= len(self._app.map.getSpeciesNames()):
			self.displayMessage(_('ERROR_INVALID_NPC_SPECIES'))
			valid = False
		if gender < 0 or gender >= len(map.map.getGenders()):
			self.displayMessage(_('ERROR_INVALID_NPC_GENDER'))
			valid = False

		if valid is False:
			return False

		return {
			'name': name,
			'gender': self._npcGenderField.currentIndex(),
			'species': self._npcSpeciesField.currentIndex(),
			'internalName': internalName
		}
