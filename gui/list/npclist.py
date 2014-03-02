# -*- coding: utf8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
import gui.list.itemlist
from core.localisation import _


class npcList(gui.list.itemlist.itemList):

	_columns = (_('NAME_COLUMN'), _('X_COLUMN'), _('Y_COLUMN'), _('INTERNAL_NAME_COLUMN'), _('LOCATE_COLUMN'))

	def insertItem(self, index, row):
		self.setItem(index, 0, QtGui.QTableWidgetItem(row['name']))
		self.setItem(index, 1, QtGui.QTableWidgetItem(str(row['x'])))
		self.setItem(index, 2, QtGui.QTableWidgetItem(str(row['y'])))
		self.setItem(index, 3, QtGui.QTableWidgetItem(row['internalName']))
		self.setCellWidget(index, 4, gui.list.itemlist.itemLocatorButton(self, index, _('LOCATE_BUTTON')))
		self.resizeColumnsToContents()

	def getData(self):
		return self._app.map.npc.values()

	def getCoordinatesFromIndex(self, index):
		"""
		This methods return a item's coordinates from its index in the table.
		"""
		return (
			int(self.item(index, 1).text()),
			int(self.item(index, 2).text())
		)
