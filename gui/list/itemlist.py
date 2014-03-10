# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
from core.localisation import _


class itemList(QtGui.QTableWidget):

	_app = None
	_parent = None
	_defaultColumns = (_('DELETE_COLUMN'),)

	def __init__(self, parent, app):
		"""
		Initialisation of the widget, creates the GUI and displays the widget.
		"""
		self._app = app
		QtGui.QTableWidget.__init__(self, parent)
		self._parent = parent
		self.setColumnCount(len(self._columns) + len(self._defaultColumns))
		self.setHorizontalHeaderLabels(self._columns + self._defaultColumns)
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
			itemsNumber = self.insertItem(index, row)
			self.setCellWidget(index, itemsNumber, itemDeleteButton(self, index, _('DELETE_BUTTON')))

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


class itemDeleteButton(QtGui.QPushButton):
	"""
	QPushButton extended to connect the action _deleteItem when it is clicked.
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
		self.clicked.connect(self._deleteItem)

	def _deleteItem(self):
		"""
		When a delete button is clicked, a confirmation dialog is displayed and
		then the item is deleted
		"""
		self._table.deleteItem(self._index)
