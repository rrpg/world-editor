# -*- coding: utf8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
import gui.list.itemlist
from core.localisation import _


class speciesList(gui.list.itemlist.itemList):

	_columns = (_('NAME_COLUMN'), _('DESCRIPTION_DESCRIPTION'), _('INTERNAL_NAME_COLUMN'))

	def insertItem(self, index, row):
		self.setItem(index, 0, QtGui.QTableWidgetItem(row['name']))
		self.setItem(index, 1, QtGui.QTableWidgetItem(row['description']))
		self.setItem(index, 2, QtGui.QTableWidgetItem(row['internalName']))
		self.resizeColumnsToContents()

	def getData(self):
		return self._app.map.species.values()
