# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from gui.mainwindow import mainWindow
from core import map, config
import sys
import shutil
import os
from core.localisation import _


class application(QtGui.QApplication):
	"""
	Class for the application. it is here that the main window is created.
	"""
	_name = None
	_fileName = None
	_saveFileName = None

	mapOpened = QtCore.pyqtSignal()

	_hasUnsavedChanges = False

	def __init__(self):
		"""
		a() -> editorGUI.application

		Construct of the class. Set the data and creates the main window.

		@param data list of elements to display in the table.
		@param headers titles of the table's columns.
		"""
		self._prepareFolders()

		super(application, self).__init__(sys.argv)
		self.initMap()
		self.widget = mainWindow(self)

		self.aboutToQuit.connect(self.clean)

	def _prepareFolders(self):
		"""
		Method called when the application is started.
		It creates the temp and the maps folders if they don't exist
		"""
		tmpDir = self.getTempFolder()
		if not os.path.exists(tmpDir):
			os.makedirs(tmpDir)
		if not os.path.exists(config.exportPath):
			os.makedirs(config.exportPath)

	def run(self):
		"""
		Execute the application
		"""
		return self.exec_()

	def clean(self):
		"""
		Method called when the application is closed, to delete the temp folder
		"""
		tmpDir = self.getTempFolder()
		if os.path.exists(tmpDir):
			shutil.rmtree(tmpDir)
		if os.listdir(config.tempDir) == []:
			shutil.rmtree(config.tempDir)

# Operations on the map files
	def initMap(self):
		"""
		Method to init the map object
		"""
		self.map = map.map()

	def createMap(self, width, height):
		"""
		must call a map class's method to generate the map with the external
		generator, and then open the map in the editor
		"""
		self._saveFileName = None
		self.initMap()
		self.map.generate(self._fileName, width, height)

	def openMap(self, fileName):
		"""
		Method to open an existing map (.map file)
		"""
		self.initMap()
		self.setSaveMapName(str(fileName))
		(fileName, worldName) = self.map.open(self._saveFileName, self.getTempFolder())
		self.setMapFileName(fileName)
		self.setMapName(worldName)
		self.mapOpened.emit()

	def exportMap(self, thread):
		"""
		Method to export the map to a usable DB
		"""
		self.map.export(self._name, self.escapeName(self._name), thread)

	def saveMap(self):
		"""
		Method which save the map in a .map file. A .map file can be reopened later
		to be edited.
		"""
		if self._saveFileName is None:
			raise BaseException("No file name defined to save the map")

		self.map.save(self._saveFileName)
		self.flagAsSaved()
# End Operations on the map files

# Methods to add elements in the map
	def addSpecies(self, key, informations):
		"""
		Method to add a species in the world
		"""
		self.map.species[key] = informations

	def addPlace(self, key, informations):
		"""
		Add a place to the map's places list
		"""
		self.map.places[key] = informations

	def addNpc(self, key, informations):
		"""
		Add a npc to the map's npc list
		"""
		self.map.npc[key] = informations
# End Methods to add elements in the map

# Names operations (file names, map name...)
	def escapeName(self, name):
		"""
		Method to escape a world name to remove any non alnum characters.
		The escaped name is used for the different needed filenames.
		"""
		return ''.join(e for e in name if e.isalnum())

	def getMapName(self):
		"""
		Return the world's name, unescaped
		"""
		return self._name

	def getMapFileName(self):
		"""
		Return the world's file name, escaped
		"""
		return self._fileName

	def setMapName(self, name):
		"""
		Set the world's name, unescaped
		"""
		self._name = name

	def setMapFileName(self, name):
		"""
		Set the world's file name
		"""
		self._fileName = name

	def getSaveFileName(self):
		"""
		Return the map's name used to save the map
		"""
		return self._saveFileName

	def setSaveMapName(self, name):
		"""
		Set the map's name used to save the map
		"""
		name = str(name)
		if not os.path.exists(os.path.dirname(name)):
			raise BaseException(_('ERROR_UNEXISTING_FOLDER'))
		elif os.path.exists(name) and not os.path.isfile(name):
			raise BaseException(_('ERROR_NOT_A_FILE'))
		self._saveFileName = name
# end Names operations (file names, map name...)

	def hasPlaceWithName(self, name):
		return name in self.map.places.keys()

	def hasNpcWithName(self, name):
		return name in self.map.npc.keys()

	def hasSpeciesWithName(self, name):
		return name in self.map.species.keys()

	def getTempFolder(self):
		return config.tempDir + '/' + str(os.getpid())

	def hasUnsavedChanges(self):
		return self._hasUnsavedChanges

	def flagAsUnsaved(self):
		self._hasUnsavedChanges = True

	def flagAsSaved(self):
		self._hasUnsavedChanges = False
