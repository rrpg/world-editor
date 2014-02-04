# -*- coding: utf8 -*-

"""
Module to handle the GUI application
"""

from PyQt4 import QtCore
from PyQt4 import QtGui
import sys


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
	_imageLabel = None
	_scrollArea = None
	_scaleFactor = 1.0


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
		The window elements are created here (table, button...)
		"""

		self._imageLabel = QtGui.QLabel()
		self._imageLabel.setBackgroundRole(QtGui.QPalette.Base)
		self._imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
		self._imageLabel.setScaledContents(True)

		self._scrollArea = QtGui.QScrollArea();
		self._scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
		self._scrollArea.setWidget(self._imageLabel)

		self.setCentralWidget(self._scrollArea)

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
		fileName = QtGui.QFileDialog.getOpenFileName(self, "Open file", QtCore.QDir.currentPath())

		if fileName is not None:
			image = QtGui.QImage(fileName)

			if image is None or image.format() == QtGui.QImage.Format_Invalid:
				QtGui.QMessageBox.information(self, "Image Viewer", "Cannot open %s." % (fileName))
				return;

			self._imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
			self._scaleFactor = 1.0

			self._imageLabel.adjustSize();


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

		fileMenu = self.addMenu('&File')
		fileMenu.addAction(openAction)
		fileMenu.addAction(exitAction)

