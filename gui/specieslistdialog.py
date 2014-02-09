# -*- coding: utf8 -*-

from PyQt4 import QtGui


class speciesListDialog(QtGui.QDialog):

	_instance = None

	def __init__(self, parent, app):
		QtGui.QDialog.__init__(self, parent)
		self._app = app
		self._parent = parent
		self.initUI()
		self.setWindowTitle('List species')
		self.show()

	def initUI(self):
		pass
