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
		self._tableview.setModel(tablemodel)

		form = QtGui.QGridLayout()

		nameLabel = QtGui.QLabel("Species name")
		self._nameField = QtGui.QLineEdit()
		descriptionLabel = QtGui.QLabel("Species Description")
		self._descriptionField = QtGui.QTextEdit()

		self._saveButton = QtGui.QPushButton("Create")
		self._saveButton.clicked.connect(self.createSpecies)
		closeButton = QtGui.QPushButton("Close")
		closeButton.clicked.connect(self.close)

		form.addWidget(nameLabel, 0, 0)
		form.addWidget(self._nameField, 0, 1)
		form.addWidget(descriptionLabel, 1, 0)
		form.addWidget(self._descriptionField, 1, 1)
		form.addWidget(self._saveButton, 2, 1)

		layout.addWidget(self._tableview)
		layout.addLayout(form)
		layout.addWidget(closeButton)
		self.setLayout(layout)

	def createSpecies(self):
		name = str(self._nameField.text())
		description = str(self._descriptionField.toPlainText())

		if name is "" or description is "":
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

	def data(self, index, role):
		if not index.isValid():
			return None
		elif role != QtCore.Qt.DisplayRole:
			return None
		return (self.arraydata[index.row()][index.column()])

	def flags(self, index):
		return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
