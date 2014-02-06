# -*- coding: utf8 -*-
import os

rootPath = os.path.dirname(__file__)
externalPath = rootPath + '/externals'

map_default_width = 400
map_default_height = 400

generator = {}
generator['map'] = {
	'destination-dir': rootPath + '/maps',
	'generator': externalPath + '/map-generator/map -f %s -w %d -h %d'
}

