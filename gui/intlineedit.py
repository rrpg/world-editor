# -*- coding: utf8 -*-

from PyQt4 import QtGui


class intLineEdit(QtGui.QLineEdit):
	def value(self):
		return int(self.text())




