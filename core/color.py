# -*- coding: utf8 -*-

from core import config
from PyQt4.QtGui import QColor

COLOR_BRUSH = 0
COLOR_PEN = 1

def getColorFromConfig(section, paint_type):
	if section not in config.colors.keys():
		raise BaseException("Unknown color section")

	if paint_type != COLOR_BRUSH and paint_type != COLOR_PEN:
		raise BaseException("Unknown paint type")

	if config.colors[section][paint_type] is None:
		return QColor(0, 0, 0, 0)

	return QColor(
		config.colors[section][paint_type][0],
		config.colors[section][paint_type][1],
		config.colors[section][paint_type][2]
	)
