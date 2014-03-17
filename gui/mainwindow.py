# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
from gui.menu import menu
from gui.newmapdialog import newMapDialog
from gui.exportmapdialog import exportMapDialog
from gui.specieslistdialog import speciesListDialog
from gui.form.placedialog import formPlaceDialog
from gui.form.npcdialog import formNpcDialog
from gui.list.placeslist import placesList
from gui.list.npclist import npcList
from core import worker, config, color
from core.localisation import _
import imghdr
import os


class mainWindow(QtGui.QMainWindow):
	"""
	Class for the main window of the application.
	"""

	_imageScene = None
	_scrollArea = None
	_scaleFactor = 1.0

	_isRecording = False

	_selectPixelEvent = QtCore.pyqtSignal(int, int)
	_selectedCellRect = None
	_pixmaps = dict()

	_placesWidget = None
	_npcWidget = None
	_recordingLabel = None

	_thread = None

	_selectCellSpecificAction = None

	def __init__(self, app):
		"""
		Class's construct.

		@param app QtGui.QApplication Application containing the window.
		"""
		super(mainWindow, self).__init__()
		self._app = app
		self.addWidget = None
		#creation of the UI
		self.initUI()
		self.initSignals()

	def initUI(self):
		"""
		Initialization of the UI:
		- creation of the menu bar,
		- creation of the status bar,
		- creation of the window's content,
		- definition of the window informations (size, position),
		- display of the window.
		"""
		#top menu
		self.setMenuBar(menu(self))
		self.setStatusBar(QtGui.QStatusBar())
		#creation fo the window
		self._create()
		#definition if window informations (size, position, title)
		self._setWindowInfos()
		#display the Whole Thing
		self.show()

	def initSignals(self):
		"""
		Method which initialise some signals.
		For the moment, the only signal is the application's mapOpened,
		triggered when a map file is opened. At this moment, the places' widget
		is populated to list the existing places.
		"""
		self._app.mapOpened.connect(self._placesWidget.setData)
		self._app.mapOpened.connect(self._npcWidget.setData)

	def _create(self):
		"""
		Method which create the UI
		The window elements are created here.
		For the moment, the window contains only a QGraphicsView displaying the
		world's map.
		"""
		splitter = QtGui.QSplitter()
		splitter.setOrientation(QtCore.Qt.Orientation(QtCore.Qt.Horizontal))

		self._placesWidget = placesList(self, self._app)
		self._placesWidget.entityDeleted.connect(self.refreshEntity)
		self._placesWidget.cellDoubleClicked.connect(self.editPlace)
		self._npcWidget = npcList(self, self._app)
		self._npcWidget.entityDeleted.connect(self.refreshEntity)
		self._npcWidget.cellDoubleClicked.connect(self.editNpc)

		tabWidget = QtGui.QTabWidget()
		tabWidget.addTab(self._placesWidget, _('PLACES_TAB'))
		tabWidget.addTab(self._npcWidget, _('NPC_TAB'))

		self._imageScene = QtGui.QGraphicsScene()
		self._imageView = QtGui.QGraphicsView()
		self._imageView.setScene(self._imageScene)

		layout = QtGui.QVBoxLayout()
		layout.setSpacing(0)
		layout.setMargin(0)

		messageLayout = QtGui.QHBoxLayout()
		messageLayout.setSpacing(4)
		messageLayout.setMargin(3)
		viewTopWidget = QtGui.QWidget()
		self._recordingLabel = QtGui.QLabel("")
		messageLayout.addWidget(self._recordingLabel)
		viewTopWidget.setLayout(messageLayout)

		layout.addWidget(viewTopWidget)
		layout.addWidget(self._imageView)

		viewWidget = QtGui.QWidget()
		viewWidget.setLayout(layout)

		splitter.addWidget(tabWidget)
		splitter.addWidget(viewWidget)
		splitter.setStretchFactor(1, 1)

		self.setCentralWidget(splitter);

	def _setWindowInfos(self):
		"""
		Define window informations
		"""
		# default size
		self.setGeometry(300, 300, 600, 600)
		self.setWindowTitle(_('MAIN_WINDOW_TITLE'))

	def displayMessage(self, text):
		"""
		Displays a message in the status bar.
		"""
		self.statusBar().showMessage(text)

	def alert(self, message):
		"""
		Method to display an alert message. Create just an critical QMessageBox.
		"""
		QtGui.QMessageBox.critical(self, _('ERROR_BOX_TITLE'), message)

# Actions
	def newMapAction(self):
		"""
		Action triggered when the menu's "new" button is pressed.
		The user is then invited to select a map name and size.
		"""
		newmap = newMapDialog(self, self._app)

	def openMapAction(self):
		"""
		Action triggered when the menu's "open" button is pressed.
		The user is then invited to select a map on his computer. The map must
		be a picture file.
		"""
		fileName = QtGui.QFileDialog.getOpenFileName(
			self,
			_('OPEN_FILE_DIALOG_TITLE'),
			QtCore.QDir.currentPath(),
			_('MAP_FILE_TYPE %s') % "(*.map)"
		)

		if fileName == "":
			return

		try:
			self._app.openMap(fileName)
			self.openMap()
		except BaseException as e:
			self.alert(e.message)

	def saveMapAction(self):
		"""
		This method is called when the "Save" button from the menu is pressed.
		If the map's save file name is set, the map is saved in this file,
		else the "Save as" action is called.
		"""
		if self._app.getSaveFileName() is None:
			return self.saveMapAsAction()
		else:
			self._app.saveMap()
			return True

	def saveMapAsAction(self):
		"""
		This method asks the user to select a file on his computer, and then
		save the map in this file.`
		"""
		fileName = QtGui.QFileDialog.getSaveFileName(
			self,
			_('SAVE_FILE_DIALOG_TITLE'),
			QtCore.QDir.currentPath(),
			_('MAP_FILE_TYPE %s') % "(*.map)"
		)

		if fileName == "":
			return False

		if fileName[-4:] != '.map':
			fileName = fileName + '.map'

		self._app.setSaveMapName(fileName)
		self._app.saveMap()
		return True

	def listSpeciesAction(self):
		"""
		Method called to display a dialog listing the map's species.
		"""
		specieswindow = speciesListDialog(self, self._app)
		specieswindow.show()

	def zoomInMapAction(self):
		"""
		Wrapper method to zoom in the map, calls scaleImage().
		"""
		self._scaleFactor *= 1 + config.zoomDelta
		self.scaleImage()

	def zoomOutMapAction(self):
		"""
		Wrapper method to zoom out the map, calls scaleImage().
		"""
		self._scaleFactor *= 1 - config.zoomDelta
		self.scaleImage()

	def exportMapAction(self, customAction=None):
		"""
		Method to export a map.
		Will check if the map can be exported, and if it is, the export will be
		run and a dialog will be displayed with a progress bar to show the
		export progression.
		"""
		try:
			self._app.map.checkForExport()
		except BaseException as e:
			self.alert(e.message)
			return

		exportDialog = exportMapDialog(self)

		self._thread = worker.exporterThread(self._app)
		if customAction is not None:
			self._thread.finished.connect(customAction)
		self._thread.finished.connect(exportDialog.close)
		self._thread.exportError.connect(self.alert)

		exportDialog.setThread(self._thread)
		self._thread.start()

	def setAsDefaultAction(self):
		"""
		Define the map as default map. The map must already be exported.
		If the map is not exported, the user is asked to export it.
		"""
		if self._app.isExported() is False:
			msgBox = QtGui.QMessageBox()
			msgBox.setWindowTitle(_('SET_AS_DEFAULT_QUESTION'))
			msgBox.setText(_('ERROR_EXPORT_NEEDED'))
			msgBox.addButton(QtGui.QPushButton(_('YES_BUTTON')), QtGui.QMessageBox.AcceptRole)
			msgBox.addButton(QtGui.QPushButton(_('NO_BUTTON')), QtGui.QMessageBox.RejectRole)
			ret = msgBox.exec_()

			if ret == QtGui.QMessageBox.AcceptRole:
				self.exportMapAction(self._app.setAsDefault)
			return

		self._app.setAsDefault()
# End Actions

# Actions to interact on the map to add elements
	def recordSelectStartCell(self):
		"""
		Method called when the user has to select a starting cell. A record mode
		will be enabled and the user will have to click on a cell in the map.
		"""
		if self.isRecording():
			self.disableRecordingMode()

		self._selectCellSpecificAction = self.selectStartCell
		self.enableRecordingMode(_('RECORDING_START_CELL_MESSAGE'))

	def recordAddPlaceCell(self):
		"""
		Method called when the user has to select a cell to add a place in the
		world. A record mode will be enabled and the user will have to click on
		a cell in the map
		"""
		if self.isRecording():
			self.disableRecordingMode()

		self._selectCellSpecificAction = self.addPlace
		self.enableRecordingMode(_('RECORDING_PLACE_MESSAGE'))

	def recordAddNpcCell(self):
		"""
		Method called when the user has to select a cell to add a NPC in the
		world. A record mode will be enabled and the user will have to click on
		a cell in the map
		"""
		if self.isRecording():
			self.disableRecordingMode()

		self._selectCellSpecificAction = self.addNpc
		self.enableRecordingMode(_('RECORDING_NPC_MESSAGE'))
# End Actions to interact on the map to add elements

# Recording methods
	def isRecording(self):
		"""
		Method to know if the recording mode is enabled.
		"""
		return self._isRecording

	def enableRecordingMode(self, message):
		"""
		Method to enable the recording mode.
		"""
		self._isRecording = True
		self._recordingLabel.setText(message)
		self._selectPixelEvent.connect(self.selectCell)

		if self._selectCellSpecificAction is not None:
			self._selectPixelEvent.connect(self._selectCellSpecificAction)


	def disableRecordingMode(self):
		"""
		Method to disable the recording mode.
		"""
		self._isRecording = False
		self._recordingLabel.setText("")
		if self._selectCellSpecificAction is not None:
			self._selectPixelEvent.disconnect(self._selectCellSpecificAction)
			self._selectCellSpecificAction = None
		self._selectPixelEvent.disconnect(self.selectCell)

# End Recording methods

# Map operations
	def openMap(self):
		"""
		Method to open a map from a filename
		"""
		fileName = self._app.getMapFileName() + '.bmp'

		image = QtGui.QImage(fileName)
		if image is None or imghdr.what(str(fileName)) != "bmp":
			QtGui.QMessageBox.information(
				self,
				_('IMAGE_VIEWER'),
				_('ERROR_OPEN_%s') % (fileName)
			)
			return

		self._imageScene.clear()
		mapPixmap = QtGui.QPixmap.fromImage(image)
		mapPixmap = QtGui.QGraphicsPixmapItem(mapPixmap, None, self._imageScene)
		mapPixmap.mousePressEvent = self.pixelSelect

		self._pixmaps = dict()
		self._pixmaps['map'] = mapPixmap

		self.refreshEntities()

		if self._app.map.startCellPosition is not None:
			self.displayStartCell(self._app.map.startCellPosition[0], self._app.map.startCellPosition[1])

		self._scaleFactor = 1.0

		self.menuBar().mapOpened.emit()

		if self._app.getSaveFileName() is None:
			self._app.flagAsUnsaved()

	def scaleImage(self):
		"""
		Method to resize the map after a zoom action.
		Once the map is resized, if the scale factor is lower or equal than
		0.75, the zoom out button is disabled and if the scale factor is higher
		or equal than 30.0, the zoom in button is disabled.
		"""
		self._imageView.resetTransform()
		transform = self._imageView.transform()
		transform.scale(self._scaleFactor, self._scaleFactor)
		self._imageView.setTransform(transform)

		self.menuBar().mapZoomed.emit(self._scaleFactor)

	def pixelSelect(self, event):
		"""
		Action called when the map is clicked, to get the clicked pixel.
		"""
		(x, y) = (int(event.pos().x()), int(event.pos().y()))
		self._selectPixelEvent.emit(x, y)

	def centerMapOnCoordinates(self, coordinates):
		"""
		This method does a maximum zoom on a selected cell of the map.
		"""
		self._imageView.fitInView(coordinates[0] - 1, coordinates[1] - 1, 3, 3)
		self._scaleFactor = config.scaleFactor
		self.scaleImage()

	def selectCell(self, x, y):
		"""
		This method is called when the record mode is enabled and a cell of
		the map is clicked. At this moment, the cell is highlighted with a
		black border arround it.
		"""
		if self._selectedCellRect is not None:
			self.unselectCell()

		self._selectedCellRect = QtGui.QGraphicsRectItem(x, y, 1, 1, None, self._imageScene)
		self._selectedCellRect.setBrush(QtGui.QBrush(color.getColorFromConfig('selected-cell', color.COLOR_BRUSH)))
		self._selectedCellRect.setPen(QtGui.QPen(color.getColorFromConfig('selected-cell', color.COLOR_PEN)))

	def unselectCell(self):
		"""
		Method to remove the pixel of the previously selected cell.
		"""
		self._imageScene.removeItem(self._selectedCellRect)
		self._selectedCellRect = None
# End Map operations

# Methods to add elements on the map
	def selectStartCell(self, x, y):
		"""
		Method called when the user click on a cell in the map to select a
		starting cell.
		"""
		try:
			self._app.map.setStartCellPosition((x, y))
			self.displayStartCell(x, y)
			self._app.flagAsUnsaved()
		except BaseException as e:
			self.alert(e.message)
			return

		self.disableRecordingMode()

	def addPlace(self, x, y):
		"""
		Method called when the user click on a cell in the map to add a place.
		"""

		if not self._app.map.isCellOnLand((x, y)):
			self.alert(_('ERROR_PLACE_IN_WATER'))
			return

		dialog = formPlaceDialog(self, self._app, coordinates=(x, y))
		dialog.entityAdded.connect(self.unselectCell)
		dialog.entityAdded.connect(self.displayEntity)
		dialog.entityAdded.connect(self._placesWidget.setData)
		dialog.entityAdded.connect(self._app.flagAsUnsaved)

		self.disableRecordingMode()

	def editPlace(self, place):
		"""
		Method called when the user double clicks on a place in the list.
		"""
		row = self._placesWidget.getRowValues(place)
		self.selectCell(row['x'], row['y'])
		dialog = formPlaceDialog(self, self._app, row=row)
		dialog.entityUpdated.connect(self.unselectCell)
		dialog.entityUpdated.connect(self.refreshEntity)
		dialog.entityUpdated.connect(self._placesWidget.setData)
		dialog.entityUpdated.connect(self._app.flagAsUnsaved)

	def addNpc(self, x, y):
		"""
		Method called when the user click on a cell in the map to add a NPC.
		"""
		if not self._app.map.isCellOnLand((x, y)):
			self.alert(_('ERROR_NPC_IN_WATER'))
			return

		dialog = formNpcDialog(self, self._app, coordinates=(x, y))
		dialog.entityAdded.connect(self.unselectCell)
		dialog.entityAdded.connect(self.displayEntity)
		dialog.entityAdded.connect(self._npcWidget.setData)
		dialog.entityAdded.connect(self._app.flagAsUnsaved)

		self.disableRecordingMode()

	def editNpc(self, npc):
		"""
		Method called when the user double clicks on a npc in the list.
		"""
		row = self._npcWidget.getRowValues(npc)
		self.selectCell(row['x'], row['y'])
		dialog = formNpcDialog(self, self._app, row=row)
		dialog.entityUpdated.connect(self.unselectCell)
		dialog.entityUpdated.connect(self.refreshEntity)
		dialog.entityUpdated.connect(self._npcWidget.setData)
		dialog.entityUpdated.connect(self._app.flagAsUnsaved)
# End Methods to add elements on the map

# Methods to display an element on the map
	def refreshEntities(self):
		for e in self._app.map.entities.keys():
			self.refreshEntity(e)

	def refreshEntity(self, entityType):
		entityType = str(entityType)
		if entityType in self._pixmaps.keys():
			self._cleanScene(self._pixmaps[entityType])
			del self._pixmaps[entityType]
		for p in self._app.map.entities[entityType].values():
			self.displayEntity(entityType, p['x'], p['y'])

	def displayEntity(self, entityType, x, y):
		"""
		This method creates a pixmap in the map for each desired entity of the map.
		"""
		entityType = str(entityType)
		if entityType not in self._pixmaps.keys():
			self._pixmaps[entityType] = list()

		rect = QtGui.QGraphicsRectItem(x, y, 1, 1, None, self._imageScene)
		rect.setBrush(QtGui.QBrush(color.getColorFromConfig(entityType, color.COLOR_BRUSH)))
		rect.setPen(QtGui.QPen(color.getColorFromConfig(entityType, color.COLOR_PEN)))
		self._pixmaps[entityType].append(rect)

	def _cleanScene(self, pixmapsList):
		for p in pixmapsList:
			self._imageScene.removeItem(p)

	def displayStartCell(self, x, y):
		"""
		Here the start cell is displayed in the map, as a new pixmap
		"""
		if 'start-cell' in self._pixmaps.keys():
			self._imageScene.removeItem(self._pixmaps['start-cell'])
			self._pixmaps['start-cell'] = None

		rect = QtGui.QGraphicsRectItem(x, y, 1, 1, None, self._imageScene)
		rect.setBrush(QtGui.QBrush(color.getColorFromConfig('start-cell', color.COLOR_BRUSH)))
		rect.setPen(QtGui.QPen(color.getColorFromConfig('start-cell', color.COLOR_PEN)))
		self._pixmaps['start-cell'] = rect
# End Methods to display an element on the map

	def exit(self):
		"""
		On exit, if the map is not saved, the user is prompted to save it or
		cancel or discard the changes
		"""
		if self._app.hasUnsavedChanges():
			msgBox = QtGui.QMessageBox()
			msgBox.setWindowTitle(_('UNSAVED_CHANGES'))
			msgBox.setText(_('CLOSE_WITH_UNSAVED_CHANGES'))
			msgBox.addButton(QtGui.QPushButton(_('SAVE_BUTTON')), QtGui.QMessageBox.AcceptRole)
			msgBox.addButton(QtGui.QPushButton(_('DISCARD_BUTTON')), QtGui.QMessageBox.DestructiveRole)
			msgBox.addButton(QtGui.QPushButton(_('CANCEL_BUTTON')), QtGui.QMessageBox.RejectRole)
			ret = msgBox.exec_()

			# This is not logical, I would have expected to have to use
			# RejectRole, but this one seems to do the job...
			if ret == QtGui.QMessageBox.DestructiveRole:
				return
			elif ret == QtGui.QMessageBox.AcceptRole and self.saveMapAction() is False:
				return
		QtGui.qApp.quit()
