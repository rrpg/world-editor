# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore
from gui.list.specieslist import speciesList


class speciesListDialog(QtGui.QDialog):
	"""
	Class to list the current world's species.
	"""
	_table = None

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

		self._table = speciesList(self, self._app)

		closeButton = QtGui.QPushButton("Close")
		closeButton.clicked.connect(self.close)

		form = self.creationForm()

		layout.addWidget(self._table)
		layout.addLayout(form)
		layout.addWidget(closeButton)
		self.setLayout(layout)

	def creationForm(self):
		"""
		Method which creates the form to add a species.
		Returns a layout containing the form elements.
		"""
		form = QtGui.QGridLayout()

		self._messageLabel = QtGui.QLabel()
		self._messageLabel.setWordWrap(True)

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

		form.addWidget(self._messageLabel, 0, 0, 1, 2)
		form.addWidget(internalNameLabel, 1, 0)
		form.addWidget(self._internalNameField, 1, 1)
		form.addWidget(nameLabel, 2, 0)
		form.addWidget(self._nameField, 2, 1)
		form.addWidget(descriptionLabel, 3, 0)
		form.addWidget(self._descriptionField, 3, 1)
		form.addWidget(self._saveButton, 4, 1)

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
		internalName = str(self._internalNameField.text()).strip()
		name = str(self._nameField.text()).strip()
		description = str(self._descriptionField.toPlainText()).strip()

		if name is "" or internalName is "":
			return False

		if self._app.hasSpeciesWithName(internalName):
			self.displayMessage("A species already exists with this internal name")
			return False

		self._app.addSpecies(internalName, {
			'name': name,
			'description': description,
			'internalName': internalName
		})
		self._cleanForm()
		self._table.setData()

	def _cleanForm(self):
		self._internalNameField.setText('')
		self._nameField.setText('')
		self._descriptionField.setText('')

	def displayMessage(self, message):
		"""
		Method to display a message in the window.
		"""
		self._messageLabel.setText(message)
		self.adjustSize()
