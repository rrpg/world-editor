# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
from core.localisation import _


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
		newAction = QtGui.QAction(_('CREATE_MAP_MENU_ITEM'), window)
		newAction.setShortcut('Ctrl+N')
		newAction.setStatusTip(_('CREATE_MAP_MENU_ITEM_TIP'))
		newAction.triggered.connect(window.newMapAction)

		# save action
		self._saveAction = QtGui.QAction(_('SAVE_MAP_MENU_ITEM'), window)
		self._saveAction.setShortcut('Ctrl+S')
		self._saveAction.setStatusTip(_('SAVE_MAP_MENU_ITEM_TIP'))
		self._saveAction.triggered.connect(window.saveMapAction)

		# save as action
		self._saveAsAction = QtGui.QAction(_('SAVE_MAP_AS_MENU_ITEM'), window)
		self._saveAsAction.setStatusTip(_('SAVE_MAP_AS_MENU_ITEM_TIP'))
		self._saveAsAction.triggered.connect(window.saveMapAsAction)

		# open action
		openAction = QtGui.QAction(_('OPEN_MAP_MENU_ITEM'), window)
		openAction.setShortcut('Ctrl+O')
		openAction.setStatusTip(_('OPEN_MAP_MENU_ITEM_TIP'))
		openAction.triggered.connect(window.openMapAction)

		# export action
		self._exportAction = QtGui.QAction(_('EXPORT_MAP_MENU_ITEM'), self)
		self._exportAction.setShortcut('Ctrl+E')
		self._exportAction.setStatusTip(_('EXPORT_MAP_MENU_ITEM_TIP'))
		self._exportAction.triggered.connect(window.exportMapAction)

		# exit action
		exitAction = QtGui.QAction(_('EXIT_APPLICATION_MENU_ITEM'), window)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip(_('EXIT_APPLICATION_MENU_ITEM_TIP'))
		exitAction.triggered.connect(window.exit)

		# zoom in action
		self._zoominAction = QtGui.QAction(_('ZOOM_IN_MENU_ITEM'), self)
		self._zoominAction.setShortcut('Ctrl++')
		self._zoominAction.setStatusTip(_('ZOOM_IN_MENU_ITEM_TIP'))
		self._zoominAction.triggered.connect(window.zoomInMapAction)

		# zoom out action
		self._zoomoutAction = QtGui.QAction(_('ZOOM_OUT_MENU_ITEM'), self)
		self._zoomoutAction.setShortcut('Ctrl+-')
		self._zoomoutAction.setStatusTip(_('ZOOM_OUT_MENU_ITEM_TIP'))
		self._zoomoutAction.triggered.connect(window.zoomOutMapAction)

		# select start cell action
		self._selectStartCellAction = QtGui.QAction(_('SELECT_START_CELL_MENU_ITEM'), self)
		self._selectStartCellAction.setStatusTip(_('SELECT_START_CELL_MENU_ITEM_TIP'))
		self._selectStartCellAction.triggered.connect(window.recordSelectStartCell)

		# Add a place action
		self._addPlaceAction = QtGui.QAction(_('ADD_PLACE_MENU_ITEM'), self)
		self._addPlaceAction.setStatusTip(_('ADD_PLACE_MENU_ITEM_TIP'))
		self._addPlaceAction.triggered.connect(window.recordAddPlaceCell)

		# Add a npc action
		self._addNpcAction = QtGui.QAction(_('ADD_NPC_MENU_ITEM'), self)
		self._addNpcAction.setStatusTip(_('ADD_NPC_MENU_ITEM_TIP'))
		self._addNpcAction.triggered.connect(window.recordAddNpcCell)

		# list species action
		self._listSpeciesAction = QtGui.QAction(_('LIST_SPECIES_MENU_ITEM'), self)
		self._listSpeciesAction.setStatusTip(_('LIST_SPECIES_MENU_ITEM_TIP'))
		self._listSpeciesAction.triggered.connect(window.listSpeciesAction)

		self._saveAction.setEnabled(False)
		self._saveAsAction.setEnabled(False)
		self._exportAction.setEnabled(False)
		self._zoominAction.setEnabled(False)
		self._zoomoutAction.setEnabled(False)
		self._selectStartCellAction.setEnabled(False)
		self._listSpeciesAction.setEnabled(False)
		self._addPlaceAction.setEnabled(False)
		self._addNpcAction.setEnabled(False)

		fileMenu = self.addMenu(_('FILE_MENU'))
		mapMenu = self.addMenu(_('MAP_MENU'))
		worldMenu = self.addMenu(_('WORLD_MENU'))

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
