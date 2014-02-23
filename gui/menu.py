# -*- coding: utf8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore


class menu(QtGui.QMenuBar):
	"""
	Class to create the window's menu.
	"""

	# actions
	_exportAction = None
	_saveAction = None
	_saveAsAction = None
	_zoominAction = None
	_zoomoutAction = None
	_selectStartCellAction = None
	_listSpeciesAction = None
	_addPlaceAction = None

	mapOpened = QtCore.pyqtSignal()
	mapZoomed = QtCore.pyqtSignal(float)

	def __init__(self, window):
		"""
		Construct of the menu. The menu's items are defined here.
		"""
		super(menu, self).__init__(window)

		self.mapOpened.connect(self.enableMenuItems)
		self.mapZoomed.connect(self.checkZoomMenuItems)

		# new action
		newAction = QtGui.QAction('&New...', window)
		newAction.setShortcut('Ctrl+N')
		newAction.setStatusTip('Create new map')
		newAction.triggered.connect(window.newMap)

		# save action
		self._saveAction = QtGui.QAction('&Save', window)
		self._saveAction.setShortcut('Ctrl+S')
		self._saveAction.setStatusTip('Save map')
		self._saveAction.triggered.connect(window.saveMapAction)

		# save as action
		self._saveAsAction = QtGui.QAction('&Save as...', window)
		self._saveAsAction.setStatusTip('Save map as')
		self._saveAsAction.triggered.connect(window.saveMapAsAction)

		# open action
		openAction = QtGui.QAction('&Open...', window)
		openAction.setShortcut('Ctrl+O')
		openAction.setStatusTip('Open map')
		openAction.triggered.connect(window.openMapAction)

		# export action
		self._exportAction = QtGui.QAction('&Export', self)
		self._exportAction.setShortcut('Ctrl+E')
		self._exportAction.setStatusTip('Export map')
		self._exportAction.triggered.connect(window.exportMap)

		# exit action
		exitAction = QtGui.QAction('&Exit', window)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(QtGui.qApp.quit)

		# zoom in action
		self._zoominAction = QtGui.QAction('Zoom &in', self)
		self._zoominAction.setShortcut('Ctrl++')
		self._zoominAction.setStatusTip('Zoom in')
		self._zoominAction.triggered.connect(window.zoomInMap)

		# zoom out action
		self._zoomoutAction = QtGui.QAction('Zoom o&ut', self)
		self._zoomoutAction.setShortcut('Ctrl+-')
		self._zoomoutAction.setStatusTip('Zoom out')
		self._zoomoutAction.triggered.connect(window.zoomOutMap)

		# select start cell action
		self._selectStartCellAction = QtGui.QAction('Select start cell', self)
		self._selectStartCellAction.setStatusTip('Select the starting cell of the game')
		self._selectStartCellAction.triggered.connect(window.recordSelectStartCell)

		# Add a place action
		self._addPlaceAction = QtGui.QAction('Add a place', self)
		self._addPlaceAction.setStatusTip('Select a cell to add a place there')
		self._addPlaceAction.triggered.connect(window.recordAddPlaceCell)

		# Add a npc action
		self._addNpcAction = QtGui.QAction('Add a NPC', self)
		self._addNpcAction.setStatusTip('Select a cell to add a NPC there')

		# list species action
		self._listSpeciesAction = QtGui.QAction('List species...', self)
		self._listSpeciesAction.setStatusTip('List the existing species of the world')
		self._listSpeciesAction.triggered.connect(window.listspecies)

		self._saveAction.setEnabled(False)
		self._saveAsAction.setEnabled(False)
		self._exportAction.setEnabled(False)
		self._zoominAction.setEnabled(False)
		self._zoomoutAction.setEnabled(False)
		self._selectStartCellAction.setEnabled(False)
		self._listSpeciesAction.setEnabled(False)
		self._addPlaceAction.setEnabled(False)
		self._addNpcAction.setEnabled(False)

		fileMenu = self.addMenu('&File')
		mapMenu = self.addMenu('&Map')
		worldMenu = self.addMenu('&World')

		fileMenu.addAction(newAction)
		fileMenu.addAction(openAction)
		fileMenu.addSeparator()
		fileMenu.addAction(self._saveAction)
		fileMenu.addAction(self._saveAsAction)
		fileMenu.addAction(self._exportAction)
		fileMenu.addSeparator()
		fileMenu.addAction(exitAction)

		mapMenu.addAction(self._zoominAction)
		mapMenu.addAction(self._zoomoutAction)

		worldMenu.addAction(self._selectStartCellAction)
		worldMenu.addAction(self._addPlaceAction)
		worldMenu.addAction(self._addNpcAction)
		worldMenu.addSeparator()
		worldMenu.addAction(self._listSpeciesAction)

	def enableMenuItems(self):
		"""
		Method to enable some menu items when a map is generated or loaded.
		"""
		self._zoominAction.setEnabled(True)
		self._zoomoutAction.setEnabled(True)
		self._exportAction.setEnabled(True)
		self._saveAction.setEnabled(True)
		self._saveAsAction.setEnabled(True)
		self._selectStartCellAction.setEnabled(True)
		self._addPlaceAction.setEnabled(True)
		self._addNpcAction.setEnabled(True)
		self._listSpeciesAction.setEnabled(True)

	def checkZoomMenuItems(self, scaleFactor):
		"""
		Method to enable the zoom buttons depending on the map's zoom value.
		"""
		self._zoominAction.setEnabled(scaleFactor < 30.0);
		self._zoomoutAction.setEnabled(scaleFactor > 0.75);
