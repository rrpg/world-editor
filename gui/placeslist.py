# -*- coding: utf8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore


class placesList(QtGui.QTableView):

	_columns = ('Name', 'Type', 'X', 'Y')
	_app = None

	def __init__(self, parent, app):
		"""
		Initialisation of the window, creates the GUI and displays the window.
		"""
		self._app = app
		QtGui.QTableView.__init__(self, parent)
		self.refresh()

	def refresh(self):
		tablemodel = placesTableModel(self._prepareData(), self._columns, self)
		self.setModel(tablemodel)
		self.resizeColumnsToContents();

	def _prepareData(self):
		data = list()
		for r in self._app.map.places:
			data.append([
				r['name'],
				self._app.map.getPlaceTypesLabels()[r['type']],
				r['coordinates'][0],
				r['coordinates'][1]
			])
		return data

class placesTableModel(QtCore.QAbstractTableModel):
	"""
	Model class for the places list
	"""
	def __init__(self, datain, headerdata, parent = None, *args):
		QtCore.QAbstractTableModel.__init__(self, parent, *args)
		self.arraydata = datain
		self.headerdata = headerdata

	def headerData(self, col, orientation=QtCore.Qt.Horizontal, role=QtCore.Qt.DisplayRole):
		if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole and len(self.headerdata) > 0:
			return self.headerdata[col]

	def rowCount(self, parent):
		"""
		Method to get the number of rows of the table.
		"""
		return len(self.arraydata)

	def columnCount(self, parent):
		"""
		Method to get the number of columns of the table.
		"""
		if len(self.arraydata) == 0:
			return 0

		return len(self.arraydata[0])

	def setData(self, index, value, role):
		"""
		Method to update a cell of the table, depending on a given role.
		"""
		if role == QtCore.Qt.DisplayRole:
			self.arraydata[index.row()][index.column()] = str(value)
			return True
		return False

	def data(self, index, role):
		"""
		Method to get the value of a cell of the table, depending on a given
		role.
		"""
		if not index.isValid():
			return None
		elif role == QtCore.Qt.EditRole:
			return str(self.arraydata[index.row()][index.column()])
		elif role != QtCore.Qt.DisplayRole:
			return None
		return (self.arraydata[index.row()][index.column()])
