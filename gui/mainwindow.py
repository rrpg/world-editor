# -*- coding: utf8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
from gui.menu import menu
from gui.newmapdialog import newMapDialog
from gui.exportmapdialog import exportMapDialog
from gui.specieslistdialog import speciesListDialog
from core import worker
import imghdr
import os


class mainWindow(QtGui.QMainWindow):
	"""
	Class for the main window of the application.
	"""

	_instance = None
	_imageScene = None
	_scrollArea = None
	_scaleFactor = 1.0

	_isRecording = False

	_selectPixelEvent = QtCore.pyqtSignal(int, int)

	_pixmaps = dict()

	_thread = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(mainWindow, cls).__new__(
								cls, *args, **kwargs)
		return cls._instance

	@classmethod
	def getInstance(cls):
		return cls._instance

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

	def _create(self):
		"""
		Method which create the UI
		The window elements are created here.
		For the moment, the window contains only a QGraphicsView displaying the
		world's map.
		"""

		self._imageScene = QtGui.QGraphicsScene()
		self._imageView = QtGui.QGraphicsView()
		self._imageView.setScene(self._imageScene)

		self.setCentralWidget(self._imageView)

	def displayMessage(self, text):
		"""
		Displays a message in the status bar.
		"""
		self.statusBar().showMessage(text)

	def _setWindowInfos(self):
		"""
		Define window informations
		"""
		# default size
		self.setGeometry(300, 300, 600, 600)
		#~ self.setWidth()
		self.setWindowTitle('World editor')

	def newMap(self):
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
			"Open file",
			QtCore.QDir.currentPath(),
			"Images (*.bmp)"
		)

		if fileName == "":
			return

		self.openMap("tmpname", fileName)

	def zoomInMap(self):
		"""
		Wrapper method to zoom in the map, calls scaleImage().
		"""
		self.scaleImage(1.25);

	def zoomOutMap(self):
		"""
		Wrapper method to zoom out the map, calls scaleImage().
		"""
		self.scaleImage(0.75);

	def scaleImage(self, factor):
		"""
		Method to resize the map after a zoom action.
		Once the map is resized, if the scale factor is lower or equal than
		0.75, the zoom out button is disabled and if the scale factor is higher
		or equal than 30.0, the zoom in button is disabled.
		"""
		self._scaleFactor *= factor;

		self._imageView.resetTransform();
		transform = self._imageView.transform();
		transform.scale(self._scaleFactor, self._scaleFactor);
		self._imageView.setTransform(transform);

		self.menuBar().mapZoomed.emit(self._scaleFactor)

	def pixelSelect(self, event):
		"""
		Action called when the map is clicked, to get the clicked pixel.
		"""
		(x, y) = (int(event.pos().x()), int(event.pos().y()))
		self._selectPixelEvent.emit(x, y)

	def openMap(self):
		"""
		Method to open a map from a filename
		"""
		fileName = self._app.getMapFileName() + '.bmp'

		image = QtGui.QImage(fileName)
		if image is None or imghdr.what(str(fileName)) != "bmp":
			QtGui.QMessageBox.information(
				self,
				"Image Viewer",
				"Cannot open %s." % (fileName)
			)
			return;

		self._imageScene.clear()
		mapPixmap = QtGui.QPixmap.fromImage(image)
		mapPixmap = QtGui.QGraphicsPixmapItem(mapPixmap, None, self._imageScene)
		mapPixmap.mousePressEvent = self.pixelSelect

		self._pixmaps['map'] = mapPixmap

		self._scaleFactor = 1.0

		self.menuBar().mapOpened.emit()

		self._app.initMap()

	def exportMap(self):
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
		self._thread.finished.connect(exportDialog.close)
		self._thread.exportError.connect(self.alert)

		exportDialog.setThread(self._thread)
		self._thread.start()

	def recordSelectStartCell(self):
		"""
		Method called when the user has to select a starting cell. A record mode
		will be enabled and the user will have to click on a cell in the map.
		"""
		if not self._isRecording:
			self._isRecording = True
			self._selectPixelEvent.connect(self.selectStartCell)

	def selectStartCell(self, x, y):
		"""
		Method called when the user click on a cell in the map to select a
		starting cell.
		"""
		try:
			self._app.map.setStartCellPosition((x, y))
			if 'start-cell' in self._pixmaps.keys():
				self._imageScene.removeItem(self._pixmaps['start-cell'])
				self._pixmaps['start-cell'] = None

			rect = QtGui.QGraphicsRectItem(x, y, 1, 1, None, self._imageScene)
			rect.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
			self._pixmaps['start-cell'] = rect
		except BaseException as e:
			self.alert(e.message)

		self._isRecording = False
		self._selectPixelEvent.disconnect(self.selectStartCell)

	def alert(self, message):
		"""
		Method to display an alert message. Create just an critical QMessageBox.
		"""
		QtGui.QMessageBox.critical(self, "An error occured", message)

	def listspecies(self):
		"""
		Method called to display a dialog listing the map's species.
		"""
		specieswindow = speciesListDialog(self, self._app)
		specieswindow.show()
