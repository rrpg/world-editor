# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
from core.localisation import _


class entityList(QtGui.QTableWidget):

	_app = None
	_parent = None
	_defaultColumns = (_('DELETE_COLUMN'),)

	entityDeleted = QtCore.pyqtSignal(str)

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
		data = self.getData()
		nbRowsToInsert = len(data)
		for index, row in enumerate(data):
			if self.rowCount() < nbRowsToInsert:
				self.insertRow(index)
			entitisNumber = self.insertEntity(index, row)
			self.setCellWidget(index, entitisNumber, entityDeleteButton(self, index, _('DELETE_BUTTON')))

		while self.rowCount() > nbRowsToInsert:
			self.removeRow(self.rowCount() - 1)
		self.resizeColumnsToContents()


class entityLocatorButton(QtGui.QPushButton):
	"""
	QPushButton extended to connect the action _locateEntity when it is clicked.
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
		self.clicked.connect(self._locateEntity)

	def _locateEntity(self):
		"""
		When a locate button is clicked, the map is centered on the
		corresponding entity.
		"""
		self._table._parent.centerMapOnCoordinates(
			self._table.getCoordinatesFromIndex(self._index)
		)


class entityDeleteButton(QtGui.QPushButton):
	"""
	QPushButton extended to connect the action _deleteEntity when it is clicked.
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
		self.clicked.connect(self._deleteEntity)

	def _deleteEntity(self):
		"""
		When a delete button is clicked, a confirmation dialog is displayed and
		then the entity is deleted
		"""
		msgBox = QtGui.QMessageBox()
		msgBox.setWindowTitle(_('DELETE_CONFIRMATION'))
		msgBox.setText(self._table.confirmDeleteMessage)
		msgBox.addButton(QtGui.QPushButton(_('DELETE_BUTTON')), QtGui.QMessageBox.AcceptRole)
		msgBox.addButton(QtGui.QPushButton(_('CANCEL_BUTTON')), QtGui.QMessageBox.RejectRole)
		ret = msgBox.exec_()

		if ret == QtGui.QMessageBox.AcceptRole:
			self._table.deleteEntity(self._index)
