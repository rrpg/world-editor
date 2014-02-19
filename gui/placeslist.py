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
		"""
		This methods populates the table with the places list from self._app.map
		"""
		self.clearContents()
		nbRowsToInsert = len(self._app.map.places)
		for index, row in enumerate(self._app.map.places):
			if self.rowCount() < nbRowsToInsert:
				self.insertRow(index)
			self.setItem(index, 0, QtGui.QTableWidgetItem(row['name']))
			self.setItem(index, 1, QtGui.QTableWidgetItem(self._app.map.getPlaceTypesLabels()[row['type']]))
			self.setItem(index, 2, QtGui.QTableWidgetItem(str(row['coordinates'][0])))
			self.setItem(index, 3, QtGui.QTableWidgetItem(str(row['coordinates'][1])))
			self.setCellWidget(index, 4, placeLocatorButton(self, index, "Locate"))
		self.resizeColumnsToContents()

	def getCoordinatesFromIndex(self, index):
		"""
		This methods return a place's coordinates from its index in the table.
		"""
		return (
			int(self.item(index, 2).text()),
			int(self.item(index, 3).text())
		)


class placeLocatorButton(QtGui.QPushButton):
	"""
	QPushButton extended to connect the action _locatePlace when it is clicked.
	"""
	_table = None
	_index = None

	def __init__(self, table, index, *args):
		"""
		Construct
		"""
		QtGui.QItemDelegate.__init__(self, *args)
		self._table = table
		self._index = index
		self.clicked.connect(self._locatePlace)

	def _locatePlace(self):
		"""
		When a locate button is clicked, the map is centered on the
		corresponding place.
		"""
		self._table._parent.centerMapOnCoordinates(
			self._table.getCoordinatesFromIndex(self._index)
		)
