# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore

class speciesListDialog(QtGui.QDialog):
	"""
	Class to list the current world's species.
	"""
	_tableview = None

	def __init__(self, parent, app):
		"""
		Initialisation of the window, creates the GUI and displays the window.
		"""
		QtGui.QDialog.__init__(self, parent)
		self._app = app
		self._parent = parent
		self.initUI()
		self.setWindowTitle('List species')
		self.setModal(True)
		self.show()

	def initUI(self):
		"""
		Creates the GUI.
		The GUI is composed of a table listing the existing species, a form to
		add a species and a button to close the window.
		"""
		layout = QtGui.QVBoxLayout(self)

		tablemodel = SpeciesTableModel(self._app.map.species.values(), self)
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
		"""
		Method which creates the form to add a species.
		Returns a layout containing the form elements.
		"""
		form = QtGui.QGridLayout()

		nameLabel = QtGui.QLabel("Species name")
		self._nameField = QtGui.QLineEdit()
		self._nameField.textChanged.connect(self.updateCreateButton)

		internalNameLabel = QtGui.QLabel("Species internal name")
		self._internalNameField = QtGui.QLineEdit()
		self._internalNameField.textChanged.connect(self.updateCreateButton)
		descriptionLabel = QtGui.QLabel("Species Description")
		self._descriptionField = QtGui.QTextEdit()
		self._descriptionField.textChanged.connect(self.updateCreateButton)

		self._saveButton = QtGui.QPushButton("Create")
		self._saveButton.setEnabled(False)
		self._saveButton.clicked.connect(self.createSpecies)

		form.addWidget(internalNameLabel, 0, 0)
		form.addWidget(self._internalNameField, 0, 1)
		form.addWidget(nameLabel, 1, 0)
		form.addWidget(self._nameField, 1, 1)
		form.addWidget(descriptionLabel, 2, 0)
		form.addWidget(self._descriptionField, 2, 1)
		form.addWidget(self._saveButton, 3, 1)

		return form

	def updateCreateButton(self):
		"""
		Method called when the form's fields are edited. The "create" button is
		enabled if the name field is not empty.
		"""
		self._saveButton.setEnabled(
			str(self._nameField.text()).strip() != ""
			and str(self._internalNameField.text()).strip() != ""
		)

	def createSpecies(self):
		"""
		Method called when the "create" button is pressed. The filled data are
		checked and if they are correct, the species is created.
		"""
		internalName = str(self._nameField.text()).strip()
		name = str(self._nameField.text()).strip()
		description = str(self._descriptionField.toPlainText()).strip()

		if name is "" or internalName is "":
			return False

		self._app.addSpecies(internalName, name, description)

		tablemodel = SpeciesTableModel(self._app.map.species.values(), self)
		self._tableview.setModel(tablemodel)


class SpeciesTableModel(QtCore.QAbstractTableModel):
	"""
	Model class for the species list
	"""
	def __init__(self, datain, parent = None, *args):
		QtCore.QAbstractTableModel.__init__(self, parent, *args)
		self.arraydata = datain

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

	def flags(self, index):
		"""
		Method to set the table's cells flags
		"""
		return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


class EditableRowDelegate(QtGui.QItemDelegate):
	"""
	Delegate class for the table items.
	Will create a special text or line edit field when a field is edited.
	"""
	_table = None

	def __init__(self, table, *args):
		QtGui.QItemDelegate.__init__(self, *args)
		self._table = table

	def createEditor(self, parent, option, index):
		"""
		Method called when a cell is edited, to create the according field.
		If the cell is a description cell (index 1), a textedit field is
		created, else a lineedit field is created.
		"""
		if index.column() == 1:
			self._editor = QtGui.QTextEdit(parent)
			self._editor.textChanged.connect(self.updateValue)
		else:
			self._editor = QtGui.QLineEdit(parent)
			self._editor.editingFinished.connect(self.updateValue)
		self._editedIndex = index
		return self._editor

	def setEditorData(self, editor, index):
		"""
		Method to fill the field's value.
		"""
		self._editedIndex = index
		editor.setText(index.model().data(index, QtCore.Qt.EditRole));

	def updateValue(self):
		"""
		Method called when a field lose the focus, to update the according
		species's value.
		"""
		try:
			value = self._editor.text()
			if value == "":
				return False
		except AttributeError:
			value = self._editor.toPlainText()

		self._editedIndex.model().setData(self._editedIndex, value, QtCore.Qt.DisplayRole)
		self._table.setModel(self._editedIndex.model())
