# -*- coding: utf8 -*-

from PyQt4 import QtGui
from gui.mainwindow import mainWindow
from core import map, config
import sys
import shutil
import os


class application(QtGui.QApplication):
	"""
	Class for the application. it is here that the main window is created.
	"""

	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(application, cls).__new__(
								cls, *args, **kwargs)
			cls._instance.initMap()

		return cls._instance

	@classmethod
	def getInstance(cls):
		return cls._instance

	def __init__(self):
		"""
		a() -> editorGUI.application

		Construct of the class. Set the data and creates the main window.

		@param data list of elements to display in the table.
		@param headers titles of the table's columns.
		"""
		super(application, self).__init__(sys.argv)
		self.widget = mainWindow(self)

		self.aboutToQuit.connect(self.clean)

	def run(self):
		"""
		Execute the application
		"""
		return self.exec_()

	def createMap(self, name, width, height):
		"""
		must call a map class's method to generate the map with the external
		generator, and then open the map in the editor
		"""
		self.map.generate(name, width, height)

	def initMap(self):
		self.map = map.map()

	def exportMap(self, thread):
		self.map.export(self._name, thread)

	def clean(self):

		if os.path.exists(config.tempDir):
			shutil.rmtree(config.tempDir)
