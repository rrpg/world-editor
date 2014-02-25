# -*- coding: utf8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
import gui.itemlist


class placesList(gui.itemlist.itemList):

	_columns = ('Name', 'Type', 'X', 'Y', 'Locate')

	def insertItem(self, index, row):
		self.setItem(index, 0, QtGui.QTableWidgetItem(row['name']))
		self.setItem(index, 1, QtGui.QTableWidgetItem(self._app.map.getPlaceTypesLabels()[row['type']]))
		self.setItem(index, 2, QtGui.QTableWidgetItem(str(row['coordinates'][0])))
		self.setItem(index, 3, QtGui.QTableWidgetItem(str(row['coordinates'][1])))
		self.setCellWidget(index, 4, gui.itemlist.itemLocatorButton(self, index, "Locate"))
		self.resizeColumnsToContents()

	def getData(self):
		return self._app.map.places.values()
