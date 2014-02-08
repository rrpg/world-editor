# -*- coding: utf8 -*-

from PyQt4 import QtGui


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
		window._exportAction.triggered.connect(window.exportMap)

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
