# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
import gui.list.itemlist
from core.localisation import _


class speciesList(gui.list.itemlist.itemList):

	_columns = (_('NAME_COLUMN'), _('DESCRIPTION_COLUMN'), _('INTERNAL_NAME_COLUMN'))

	confirmDeleteMessage = _('CONFIRMATION_DELETE_SPECIES')

	def insertItem(self, index, row):
		self.setItem(index, 0, QtGui.QTableWidgetItem(row['name']))
		self.setItem(index, 1, QtGui.QTableWidgetItem(row['description']))
		self.setItem(index, 2, QtGui.QTableWidgetItem(row['internalName']))
		self.resizeColumnsToContents()
		return 3

	def getData(self):
		return self._app.map.species.values()

	def deleteItem(self, index):
		"""
		Delete the selected item
		"""
		self._app.deleteSpecies(str(self.item(index, 2).text()))
		self.itemDeleted.emit()
