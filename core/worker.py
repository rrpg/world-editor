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

	generatorError = QtCore.pyqtSignal(str)
	generatorSuccess = QtCore.pyqtSignal()

	def __init__(self, app, width, height, parent=None):
		QtCore.QThread.__init__(self, parent)
		self._app = app
		self._width = width
		self._height = height

	def run(self):
		try:
			self._app.createMap(self._width, self._height)
			self.generatorSuccess.emit()
		except BaseException as e:
			self.generatorError.emit(str(e))
			self.exit(1)

class exporterThread(QtCore.QThread):
	"""
	Thread called to export a map
	"""
	_app = None

	notifyProgressLocal = QtCore.pyqtSignal(int, str)
	notifyProgressMain = QtCore.pyqtSignal(int, str)

	exportError = QtCore.pyqtSignal(str)

	def __init__(self, app, parent=None):
		QtCore.QThread.__init__(self, parent)
		self._app = app

	def run(self):
		try:
			self._app.exportMap(self)
		except BaseException as e:
			self.exportError.emit(str(e))
