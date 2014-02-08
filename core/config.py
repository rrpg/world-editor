# -*- coding: utf8 -*-
import os

rootPath = os.path.dirname(__file__) + '/..'
externalPath = rootPath + '/externals'
exportPath = rootPath + '/maps'
databasePath = rootPath + '/database'
databaseStructure = databasePath + '/structure.sql'

map_default_width = 400
map_default_height = 400

tempDir = rootPath + '/tmp'

generator = {}
generator['map'] = {
	'path': externalPath + '/map-generator',
	'generator': externalPath + '/map-generator/map -f %s -w %d -h %d'
}

db = exportPath + '/%s.db'
