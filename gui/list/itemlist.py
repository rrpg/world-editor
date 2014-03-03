# -*- coding: utf8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore


class itemList(QtGui.QTableWidget):

	_app = None
	_parent = None

	def __init__(self, parent, app):
		"""
		Initialisation of the widget, creates the GUI and displays the widget.
		"""
		self._app = app
		QtGui.QTableWidget.__init__(self, parent)
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
		nbRowsToInsert = len(self.getData())
		for index, row in enumerate(self.getData()):
			if self.rowCount() < nbRowsToInsert:
				self.insertRow(index)
			self.insertItem(index, row)
		while self.rowCount() > nbRowsToInsert:
			self.removeRow(self.rowCount() - 1)
		self.resizeColumnsToContents()


class itemLocatorButton(QtGui.QPushButton):
	"""
	QPushButton extended to connect the action _locateItem when it is clicked.
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
		self.clicked.connect(self._locateItem)

	def _locateItem(self):
		"""
		When a locate button is clicked, the map is centered on the
		corresponding item.
		"""
		self._table._parent.centerMapOnCoordinates(
			self._table.getCoordinatesFromIndex(self._index)
		)
