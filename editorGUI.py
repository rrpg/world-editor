# -*- coding: utf8 -*-

"""
Module to handle the GUI application
"""

from PyQt4 import QtCore
from PyQt4 import QtGui
import sys
import imghdr


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


class mainWindow(QtGui.QMainWindow):
	"""
	Class for the main window of the application.
	"""

	_instance = None
	_imageScene = None
	_scrollArea = None
	_scaleFactor = 1.0

	# actions
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

	def openMap(self):
		"""
		Action triggered when the menu's "open" button is pressed.
		The user is then invited to select a map on his computer. The map must
		be a picture file.
		"""
		fileName = QtGui.QFileDialog.getOpenFileName(self, "Open file", QtCore.QDir.currentPath(), "Images (*.bmp)")

		if fileName == "":
			return

		image = QtGui.QImage(fileName)
		if image is None or imghdr.what(str(fileName)) != "bmp":
			QtGui.QMessageBox.information(self, "Image Viewer", "Cannot open %s." % (fileName))
			return;

		mapPixmap = QtGui.QPixmap.fromImage(image)
		mapPixmap = QtGui.QGraphicsPixmapItem(mapPixmap, None, self._imageScene)
		mapPixmap.mousePressEvent = self.pixelSelect
		self._scaleFactor = 1.0

		self._zoominAction.setEnabled(True)
		self._zoomoutAction.setEnabled(True)

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


class menu(QtGui.QMenuBar):
	"""
	Class to create the window's menu.
	"""

	def __init__(self, window):
		"""
		Construct of the menu. The menu's items are defined here.
		"""
		super(menu, self).__init__(window)

		# open action
		openAction = QtGui.QAction('&Open...', window)
		openAction.setShortcut('Ctrl+O')
		openAction.setStatusTip('Open map')
		openAction.triggered.connect(window.openMap)

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

		window._zoominAction.setEnabled(False)
		window._zoomoutAction.setEnabled(False)

		fileMenu = self.addMenu('&File')
		mapMenu = self.addMenu('&Map')

		fileMenu.addAction(openAction)
		fileMenu.addAction(exitAction)

		mapMenu.addAction(window._zoominAction)
		mapMenu.addAction(window._zoomoutAction)

