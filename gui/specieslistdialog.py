# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from gui.list.specieslist import speciesList
from core.localisation import _


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
		self.setWindowTitle(_('LIST_SPECIES_DIALOG_TITLE'))
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
		self._table.itemDeleted.connect(self._table.setData)

		closeButton = QtGui.QPushButton(_('CLOSE_BUTTON'))
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

		nameLabel = QtGui.QLabel(_('SPECIES_NAME_LABEL'))
		self._nameField = QtGui.QLineEdit()
		self._nameField.textChanged.connect(self.updateCreateButton)

		internalNameLabel = QtGui.QLabel(_('SPECIES_INTERNAL_NAME_LABEL'))
		self._internalNameField = QtGui.QLineEdit()
		self._internalNameField.textChanged.connect(self.updateCreateButton)
		descriptionLabel = QtGui.QLabel(_('SPECIES_DESCRIPTION_LABEL'))
		self._descriptionField = QtGui.QTextEdit()
		self._descriptionField.textChanged.connect(self.updateCreateButton)

		self._saveButton = QtGui.QPushButton(_('CREATE_BUTTON'))
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
			self.displayMessage(_('ERROR_ALREADY_EXISTING_SPECIES'))
			return False

		self._app.addSpecies(internalName, {
			'name': name,
			'description': description,
			'internalName': internalName
		})
		self._cleanForm()
		self._table.setData()

	def _populateForm(self, row):
		"""
		Populate the form with the values in the dict row
		"""
		self._internalNameField.setText(row['internalName'])
		self._nameField.setText(row['name'])
		self._descriptionField.setText(row['description'])

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
