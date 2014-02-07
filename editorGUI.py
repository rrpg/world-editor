# -*- coding: utf8 -*-

"""
Module to handle the GUI application
"""

from PyQt4 import QtCore
from PyQt4 import QtGui
import sys
import imghdr
import worker
import map
import config


class application(QtGui.QApplication):
	"""
	Class for the application. it is here that the main window is created.
	"""

	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(application, cls).__new__(
								cls, *args, **kwargs)
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
		map.map.generate(name, width, height)

	def exportMap(self):
		map.map.export(self._name)


class mainWindow(QtGui.QMainWindow):
	"""
	Class for the main window of the application.
	"""

	_instance = None
	_imageScene = None
	_scrollArea = None
	_scaleFactor = 1.0

	# actions
	_exportAction = None
	_zoominAction = None
	_zoomoutAction = None

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
		newmap = newMapWindow(self, self._app)

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

		self._zoominAction.setEnabled(self._scaleFactor < 30.0);
		self._zoomoutAction.setEnabled(self._scaleFactor > 0.75);

	def pixelSelect(self, event):
		"""
		Action called when the map is clicked, to get the clicked pixel.
		"""
		pixelPosition = (int(event.pos().x()), int(event.pos().y()))
		self.setWindowTitle('Pixel position = ' + str(pixelPosition))

	def openMap(self, mapName, fileName):
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
		self._scaleFactor = 1.0

		self._zoominAction.setEnabled(True)
		self._zoomoutAction.setEnabled(True)
		self._exportAction.setEnabled(True)

		self._app._name = mapName

class newMapWindow(QtGui.QDialog):
	"""
	Window to fill some informations to create a map
	label map name		map name field
	label map width		map width field
	label map height	map height field
	create button		cancel button
	"""
	_app = None
	_parent = None

	_name = None
	_messageLabel = None
	_mapNameField = None
	_mapWidthField = None
	_mapHeightField = None

	_saveButton = None
	_cancelButton = None

	_thread = None

	def __init__(self, parent, app):
		QtGui.QWidget.__init__(self, parent)
		self._app = app
		self._parent = parent
		self.setFixedWidth(250)
		self.initUI()
		self.setWindowTitle('Create new map')
		self.show()

	def initUI(self):
		layout = QtGui.QGridLayout()

		self._messageLabel = QtGui.QLabel()
		self._messageLabel.setWordWrap(True)

		mapNameLabel = QtGui.QLabel("Map name")
		self._mapNameField = QtGui.QLineEdit()

		mapWidthLabel = QtGui.QLabel("Map width")
		self._mapWidthField = intWidget()
		self._mapWidthField.setText(str(config.map_default_width))

		mapHeightLabel = QtGui.QLabel("Map height")
		self._mapHeightField = intWidget()
		self._mapHeightField.setText(str(config.map_default_height))

		self._saveButton = QtGui.QPushButton("Create")
		self._saveButton.clicked.connect(self.createMap)
		self._cancelButton = QtGui.QPushButton("Cancel")
		self._cancelButton.clicked.connect(self.close)

		layout.addWidget(self._messageLabel, 0, 0, 1, 2)
		layout.addWidget(mapNameLabel, 1, 0)
		layout.addWidget(self._mapNameField, 1, 1)
		layout.addWidget(mapWidthLabel, 2, 0)
		layout.addWidget(self._mapWidthField, 2, 1)
		layout.addWidget(mapHeightLabel, 3, 0)
		layout.addWidget(self._mapHeightField, 3, 1)
		layout.addWidget(self._saveButton, 4, 0)
		layout.addWidget(self._cancelButton, 4, 1)

		self.setLayout(layout)

	def createMap(self):
		valid = True
		try:
			self._name = self._mapNameField.text()
			width = self._mapWidthField.value()
			height = self._mapHeightField.value()

			if width <= 0 or height <= 0:
				self.displayMessage("Positive number expected for the width and the height")
				valid = False
		except ValueError:
			self.displayMessage("Positive number expected for the width and the height")
			valid = False

		if valid:
			self.displayMessage("Generating...")
			self._saveButton.setEnabled(False)
			self._cancelButton.setEnabled(False)
			self._thread = worker.generatorThread(self._app, self._name, width, height)
			self._thread.finished.connect(self.confirmCreation)
			self._thread.start()

	def displayMessage(self, message):
		self._messageLabel.setText(message)
		self.adjustSize()

	def confirmCreation(self):
		filename = self._name + '.bmp'
		filename = config.generator['map']['destination-dir'] + '/' + filename
		self._parent.openMap(self._name, filename)
		self.close()


class intWidget(QtGui.QLineEdit):
	def value(self):
		return int(self.text())


class menu(QtGui.QMenuBar):
	"""
	Class to create the window's menu.
	"""

	def __init__(self, window):
		"""
		Construct of the menu. The menu's items are defined here.
		"""
		super(menu, self).__init__(window)

		# new action
		newAction = QtGui.QAction('&New...', window)
		newAction.setShortcut('Ctrl+N')
		newAction.setStatusTip('Create new map')
		newAction.triggered.connect(window.newMap)

		# open action
		openAction = QtGui.QAction('&Open...', window)
		openAction.setShortcut('Ctrl+O')
		openAction.setStatusTip('Open map')
		openAction.triggered.connect(window.openMapAction)

		# export action
		window._exportAction = QtGui.QAction('&Export', window)
		window._exportAction.setShortcut('Ctrl+E')
		window._exportAction.setStatusTip('Export map')
		window._exportAction.triggered.connect(window._app.exportMap)

		# exit action
		exitAction = QtGui.QAction('&Exit', window)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(QtGui.qApp.quit)

		# zoom in action
		window._zoominAction = QtGui.QAction('Zoom &in', window)
		window._zoominAction.setShortcut('Ctrl++')
		window._zoominAction.setStatusTip('Zoom in')
		window._zoominAction.triggered.connect(window.zoomInMap)

		# zoom out action
		window._zoomoutAction = QtGui.QAction('Zoom o&ut', window)
		window._zoomoutAction.setShortcut('Ctrl+-')
		window._zoomoutAction.setStatusTip('Zoom out')
		window._zoomoutAction.triggered.connect(window.zoomOutMap)

		window._exportAction.setEnabled(False)
		window._zoominAction.setEnabled(False)
		window._zoomoutAction.setEnabled(False)

		fileMenu = self.addMenu('&File')
		mapMenu = self.addMenu('&Map')

		fileMenu.addAction(newAction)
		fileMenu.addAction(openAction)
		fileMenu.addAction(window._exportAction)
		fileMenu.addAction(exitAction)

		mapMenu.addAction(window._zoominAction)
		mapMenu.addAction(window._zoomoutAction)

