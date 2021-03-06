# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
import gui.list.entitylist
from core.localisation import _


class speciesList(gui.list.entitylist.entityList):

	_columns = (_('NAME_COLUMN'), _('DESCRIPTION_COLUMN'), _('INTERNAL_NAME_COLUMN'))

	confirmDeleteMessage = _('CONFIRMATION_DELETE_SPECIES')

	def insertEntity(self, index, row):
		self.setItem(index, 0, QtGui.QTableWidgetItem(row['name']))
		self.setItem(index, 1, QtGui.QTableWidgetItem(row['description']))
		self.setItem(index, 2, QtGui.QTableWidgetItem(row['internalName']))
		self.resizeColumnsToContents()
		return 3

	def getRowValues(self, index):
		"""
		Return a dict containing the values of the row at index
		"""
		return {
			'name': str(self.item(index, 0).text()),
			'internalName': str(self.item(index, 2).text()),
			'description': str(self.item(index, 1).text())
		}

	def getData(self):
		return self._app.map.species.values()

	def deleteEntity(self, index):
		"""
		Delete the selected entity
		"""
		self._app.deleteSpecies(str(self.item(index, 2).text()))
		self.entityDeleted.emit('species')
