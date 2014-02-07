# -*- coding: utf8 -*-
from PyQt4 import QtCore

class generatorThread(QtCore.QThread):
	"""
	Thread called to generate a map
	"""
	_app = None
	_args = None
	_width = None
	_height = None

	def __init__(self, app, name, width, height, parent=None):
		QtCore.QThread.__init__(self, parent)
		self._app = app
		self._name = name
		self._width = width
		self._height = height

	def run(self):
		self._app.createMap(self._name, self._width, self._height)
