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
	_name = None
	_fileName = None
	_saveFileName = None

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
		self._prepareFolders()

		super(application, self).__init__(sys.argv)
		self.widget = mainWindow(self)

		self.aboutToQuit.connect(self.clean)

	def _prepareFolders(self):
		if not os.path.exists(config.tempDir):
			os.makedirs(config.tempDir)
		if not os.path.exists(config.exportPath):
			os.makedirs(config.exportPath)

	def run(self):
		"""
		Execute the application
		"""
		return self.exec_()

	def createMap(self, width, height):
		"""
		must call a map class's method to generate the map with the external
		generator, and then open the map in the editor
		"""
		self._saveFileName = None
		self.initMap()
		self.map.generate(self._fileName, width, height)

	def initMap(self):
		"""
		Method to init the map object
		"""
		self.map = map.map()

	def exportMap(self, thread):
		"""
		Method to export the map to a usable DB
		"""
		self.map.export(self._name, self.escapeName(self._name), thread)

	def clean(self):
		"""
		Method called when the application is closed, to delete the temp folder
		"""
		if os.path.exists(config.tempDir):
			shutil.rmtree(config.tempDir)

	def addSpecies(self, name, description):
		"""
		Method to add a species in the world
		"""
		self.map.species.append([name, description])

	def escapeName(self, name):
		return ''.join(e for e in name if e.isalnum())

	def getMapName(self):
		return self._name

	def getMapFileName(self):
		return self._fileName

	def setMapName(self, name):
		self._name = name

	def setMapFileName(self, name):
		self._fileName = name

	def addPlace(self, informations):
		self.map.places.append(informations)

	def getSaveFileName(self):
		return self._saveFileName

	def setSaveMapName(self, name):
		name = str(name)
		if not os.path.exists(os.path.dirname(name)):
			raise BaseException("The selected folder does not exist")
		elif os.path.exists(name) and not os.path.isfile(name):
			raise BaseException("The selected path is not a file")
		self._saveFileName = name

