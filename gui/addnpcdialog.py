# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore
from core import map
import gui.additemdialog


class addNpcDialog(gui.additemdialog.addItemDialog):
	"""
	Window to fill some informations to create a NPC
	label npc name      npc name field
	label npc species   npc species field
	label npc gender    npc gender field
	create button       cancel button
	"""
	_npcTypeField = None
	_npcNameField = None
	_npcSizeField = None

	_title = "Create a new NPC"

	def getFields(self):
		"""
		Creates the UI
		"""
		layout = QtGui.QGridLayout()

		npcNameLabel = QtGui.QLabel("NPC Name")
		self._npcNameField = QtGui.QLineEdit()

		npcSpeciesLabel = QtGui.QLabel("NPC Species")
		self._npcSpeciesField = QtGui.QComboBox()
		self._npcSpeciesField.addItems(self._app.map.getSpeciesNames())

		npcGenderLabel = QtGui.QLabel("NPC Gender")
		self._npcGenderField = QtGui.QComboBox()
		self._npcGenderField.addItems(map.map.getGenders())

		layout.addWidget(npcNameLabel, 0, 0)
		layout.addWidget(self._npcNameField, 0, 1)
		layout.addWidget(npcSpeciesLabel, 1, 0)
		layout.addWidget(self._npcSpeciesField, 1, 1)
		layout.addWidget(npcGenderLabel, 2, 0)
		layout.addWidget(self._npcGenderField, 2, 1)

		return layout

	def createItem(self):
		"""
		Method called when the "Create" button is pressed.
		The filled values are checked and if they are correct, a npc is created
		"""
		valid = True
		name = str(self._npcNameField.text()).strip()
		species = int(self._npcSpeciesField.currentIndex())
		gender = int(self._npcGenderField.currentIndex())

		if name == "":
			self.displayMessage("A place name must be provided")
			valid = False
		if species < 0 or species >= len(self._app.map.getSpeciesNames()):
			self.displayMessage("The selected species is not valid")
			valid = False
		if gender < 0 or gender >= len(map.map.getGenders()):
			self.displayMessage("The selected gender is not valid")
			valid = False

		if valid:
			self._app.addNpc({
				'name': name,
				'gender': self._npcGenderField.currentIndex(),
				'species': self._npcSpeciesField.currentIndex(),
				'coordinates': self._coordinates
			})
			self.itemAdded.emit(self._coordinates[0], self._coordinates[1])
			self.close()
