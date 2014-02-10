# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore

class speciesListDialog(QtGui.QDialog):

	_tableview = None

	def __init__(self, parent, app):
		QtGui.QDialog.__init__(self, parent)
		self._app = app
		self._parent = parent
		self.initUI()
		self.setWindowTitle('List species')
		self.show()

	def initUI(self):
		layout = QtGui.QVBoxLayout(self)

		tablemodel = SpeciesTableModel(self._app.map.species, self)
		self._tableview = QtGui.QTableView()
		self._tableview.setItemDelegate(EditableRowDelegate(self._tableview))
		self._tableview.setModel(tablemodel)

		closeButton = QtGui.QPushButton("Close")
		closeButton.clicked.connect(self.close)

		form = self.creationForm()

		layout.addWidget(self._tableview)
		layout.addLayout(form)
		layout.addWidget(closeButton)
		self.setLayout(layout)

	def creationForm(self):
		form = QtGui.QGridLayout()

		nameLabel = QtGui.QLabel("Species name")
		self._nameField = QtGui.QLineEdit()
		self._nameField.textChanged.connect(self.updateCreateButton)
		descriptionLabel = QtGui.QLabel("Species Description")
		self._descriptionField = QtGui.QTextEdit()
		self._descriptionField.textChanged.connect(self.updateCreateButton)

		self._saveButton = QtGui.QPushButton("Create")
		self._saveButton.setEnabled(False)
		self._saveButton.clicked.connect(self.createSpecies)

		form.addWidget(nameLabel, 0, 0)
		form.addWidget(self._nameField, 0, 1)
		form.addWidget(descriptionLabel, 1, 0)
		form.addWidget(self._descriptionField, 1, 1)
		form.addWidget(self._saveButton, 2, 1)

		return form

	def updateCreateButton(self):
		self._saveButton.setEnabled(str(self._nameField.text()).strip() != "")

	def createSpecies(self):
		name = str(self._nameField.text()).strip()
		description = str(self._descriptionField.toPlainText()).strip()

		if name is "":
			return False

		self._app.addSpecies(name, description)

		tablemodel = SpeciesTableModel(self._app.map.species, self)
		self._tableview.setModel(tablemodel)


class SpeciesTableModel(QtCore.QAbstractTableModel):
	def __init__(self, datain, parent = None, *args):
		QtCore.QAbstractTableModel.__init__(self, parent, *args)
		self.arraydata = datain

	def rowCount(self, parent):
		return len(self.arraydata)

	def columnCount(self, parent):
		if len(self.arraydata) == 0:
			return 0

		return len(self.arraydata[0])

	def setData(self, index, value, role):
		if role == QtCore.Qt.DisplayRole:
			self.arraydata[index.row()][index.column()] = str(value)
			return True
		return False

	def data(self, index, role):
		if not index.isValid():
			return None
		elif role == QtCore.Qt.EditRole:
			return str(self.arraydata[index.row()][index.column()])
		elif role != QtCore.Qt.DisplayRole:
			return None
		return (self.arraydata[index.row()][index.column()])

	def flags(self, index):
		return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


class EditableRowDelegate(QtGui.QItemDelegate):
	_table = None

	def __init__(self, table, *args):
		QtGui.QItemDelegate.__init__(self, *args)
		self._table = table

	def createEditor(self, parent, option, index):
		if index.column() == 1:
			self._editor = QtGui.QTextEdit(parent)
			self._editor.textChanged.connect(self.updateValue)
		else:
			self._editor = QtGui.QLineEdit(parent)
			self._editor.editingFinished.connect(self.updateValue)
		self._editedIndex = index
		return self._editor

	def setEditorData(self, editor, index):
		self._editedIndex = index
		editor.setText(index.model().data(index, QtCore.Qt.EditRole));

	def updateValue(self):
		try:
			value = self._editor.text()
			if value == "":
				return False
		except AttributeError:
			value = self._editor.toPlainText()


		self._editedIndex.model().setData(self._editedIndex, value, QtCore.Qt.DisplayRole)
		self._table.setModel(self._editedIndex.model())
