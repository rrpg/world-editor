# -*- coding: utf8 -*-
import os

rootPath = os.path.dirname(__file__)
externalPath = rootPath + '/externals'

generator = {}
generator['map'] = {
	'destination-dir': rootPath + '/maps',
	'generator': externalPath + '/map-generator/map -f %s -w %d -h %d'
}

