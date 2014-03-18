# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
import gui.list.entitylist
from core.localisation import _


class placesList(gui.list.entitylist.entityList):

	_columns = (_('NAME_COLUMN'), _('TYPE_COLUMN'), _('X_COLUMN'), _('Y_COLUMN'), _('INTERNAL_NAME_COLUMN'), _('LOCATE_COLUMN'))

	confirmDeleteMessage = _('CONFIRMATION_DELETE_PLACE')

	def insertEntity(self, index, row):
		self.setItem(index, 0, QtGui.QTableWidgetItem(row['name']))
		self.setItem(index, 1, QtGui.QTableWidgetItem(self._app.map.getPlaceTypesLabels()[row['type']]))
		self.setItem(index, 2, QtGui.QTableWidgetItem(str(row['x'])))
		self.setItem(index, 3, QtGui.QTableWidgetItem(str(row['y'])))
		self.setItem(index, 4, QtGui.QTableWidgetItem(row['internalName']))
		self.setCellWidget(index, 5, gui.list.entitylist.entityLocatorButton(self, index, _('LOCATE_BUTTON')))
		self.resizeColumnsToContents()
		return 6

	def getRowValues(self, index):
		"""
		Return a dict containing the values of the row at index
		"""
		return self._app.getEntity('places', str(self.item(index, 4).text()))

	def getData(self):
		return self._app.getEntity('places').values()

	def getCoordinatesFromIndex(self, index):
		"""
		This methods return a entity's coordinates from its index in the table.
		"""
		return (
			int(self.item(index, 2).text()),
			int(self.item(index, 3).text())
		)

	def deleteEntity(self, index):
		"""
		Delete the selected entity
		"""
		self._app.deleteEntity('places', str(self.item(index, 4).text()))
		self.entityDeleted.emit('places')
