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
localesDir = rootPath + '/locales'

generator = {}
generator['map'] = {
	'path': externalPath + '/map-generator',
	'generator': externalPath + '/map-generator/map -t -f %s -w %d -h %d'
}

db = exportPath + '/%s.db'

colors = {}
colors['selected-cell'] = [None, (0, 0, 0)]
colors['start-cell'] = [(0, 0, 0), (0, 0, 0)]
colors['place'] = [(127, 127, 127), (127, 127, 127)]
colors['npc'] = [(127, 127, 127), (127, 127, 127)]

scaleFactor = 30.0
zoomDelta = .25
