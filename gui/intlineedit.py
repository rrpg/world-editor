# -*- coding: utf-8 -*-

from PyQt4 import QtGui


class intLineEdit(QtGui.QLineEdit):
	"""
	Overload of the QLineEdit widget to have only integer values.
	Should be replaced with a spinbox widget
	"""
	def value(self):
		"""
		The value must always return an integer
		"""
		return int(self.text())




