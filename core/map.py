# -*- coding: utf8 -*-

"""
Module to work with world maps (Generation, edition, save...)
"""
import subprocess
import os
from core import config
import sqlite3
import sys


class map:
	startCellPosition = None

	def generate(self, name, width, height):
		command = config.generator['map']['generator'] % (
			config.tempDir + '/' + name,
			width,
			height
		)
		if not os.path.exists(config.tempDir):
			os.makedirs(config.tempDir)
		subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	def export(self, name, thread):
		thread.notifyProgressLocal.emit(0, "Database initialisation")
		fileName = config.db % (name)
		# Delete the file if it already exist
		if os.path.isfile(fileName):
			os.remove(fileName)

		# Open connection
		db = sqlite3.connect(fileName)

		# Import an external check class from the generator
		sys.path.insert(0, config.generator['map']['path'])
		import checks

		c = db.cursor()

		f = open(config.databaseStructure, 'r')
		sql = f.read()
		c.executescript(sql)
		f.close()

		thread.notifyProgressLocal.emit(25, "Regions creation")

		# Create main region
		query = str("INSERT INTO region (region_name) VALUES ('" + name + "')")
		c.execute(query)

		thread.notifyProgressLocal.emit(50, "Area types creation")

		# Create area types
		query = "INSERT INTO area_type (name) VALUES "
		areaTypesCodes = checks.getGroundTypes()
		valuesInsert = list()
		valuesInsert.append("('dungeon')")
		values = list()
		for t in areaTypesCodes:
			valuesInsert.append("(?)")
			values.append(t)
		query = query + ', '.join(valuesInsert)
		c.execute(query, values)

		thread.notifyProgressLocal.emit(75, "Areas creation")

		# Get area types IDs
		query = "SELECT id_area_type, name FROM area_type"
		c.execute(query)
		result = c.fetchall()
		areaTypes = dict()
		for r in result:
			if r[1] in areaTypesCodes:
				code = areaTypesCodes[r[1]]
				areaTypes[code] = {'id_area_type': r[0], 'name': r[1]}

		# Open text file containing cells infos
		areasFile = open(config.tempDir + '/' + name + '.txt', "r")
		query = "INSERT INTO area (id_area_type, id_region, container, x, y, directions) VALUES (?, ?, ?, ?, ?, ?)"
		nbAreas = 0
		for area in areasFile:
			a = area.split(' ')
			t = areaTypes[int(a[0])]

			if t['name'] == 'water':
				continue

			nbAreas = nbAreas + 1
			areas = [
				areaTypes[int(a[0])]['id_area_type'],
				1,
				"world",
				a[1],
				a[2],
				a[3]
			]
			c.execute(query, areas)

		thread.notifyProgressLocal.emit(100, "Areas created")
		areasFile.close()

		db.commit()

		thread.notifyProgressMain.emit(100, "Finished")
		db.close()
