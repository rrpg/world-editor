# -*- coding: utf8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore


class placesList(QtGui.QTableWidget):

	_columns = ('Name', 'Type', 'X', 'Y', 'Locate')
	_app = None
	_parent = None

	def __init__(self, parent, app):
		"""
		Initialisation of the window, creates the GUI and displays the window.
		"""
		self._app = app
		QtGui.QTableView.__init__(self, parent)
		self._parent = parent
		self.setColumnCount(len(self._columns))
		self.setHorizontalHeaderLabels(self._columns)
		self.verticalHeader().setVisible(False)
		self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.setData()

	def setData(self):
		self.clearContents()
		nbRowsToInsert = len(self._app.map.places)
		for index, row in enumerate(self._app.map.places):
			if self.rowCount() < nbRowsToInsert:
				self.insertRow(index)
			self.setItem(index, 0, QtGui.QTableWidgetItem(row['name']))
			self.setItem(index, 1, QtGui.QTableWidgetItem(self._app.map.getPlaceTypesLabels()[row['type']]))
			self.setItem(index, 2, QtGui.QTableWidgetItem(str(row['coordinates'][0])))
			self.setItem(index, 3, QtGui.QTableWidgetItem(str(row['coordinates'][1])))
			self.setCellWidget(index, 4, QtGui.QPushButton("Locate"))
		self.resizeColumnsToContents()
