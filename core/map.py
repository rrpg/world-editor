# -*- coding: utf8 -*-

"""
Module to work with world maps (Generation, edition, save...)
"""
import subprocess
import os
from core import config
import sqlite3
import sys

# Import an external check class from the generator
sys.path.insert(0, config.generator['map']['path'])
import checks

class map:
	startCellPosition = None
	cells = dict()

	def generate(self, name, width, height):
		command = config.generator['map']['generator'] % (
			config.tempDir + '/' + name,
			width,
			height
		)
		if not os.path.exists(config.tempDir):
			os.makedirs(config.tempDir)
		subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.loadCells(name)

	def loadCells(self, name):
		# Open text file containing cells infos
		areasFile = open(config.tempDir + '/' + name + '.txt', "r")
		nbAreas = 0
		for area in areasFile:
			a = area.split(' ')
			try:
				self.cells[a[1]];
			except KeyError:
				self.cells[a[1]] = dict()

			self.cells[a[1]][a[2]] = (int(a[0]), int(a[3]))

	def checkForExport(self):
		if self.startCellPosition is None:
			raise exception("No start cell selected")

	def setStartCellPosition(self, position):
		if self.isStartCellValid(position):
			self.startCellPosition = position
		else:
			raise exception("Invalid start cell position")

	def isStartCellValid(self, position):
		areaTypesCodes = checks.getGroundTypes()
		return self.cells[str(position[0])][str(position[1])][0] is not areaTypesCodes['water']

	def export(self, name, thread):
		db = self._exportPrepareDb(thread, name)
		self._exportWorldCreation(thread, db, name)
		thread.notifyProgressMain.emit(50, "")
		self._exportStartCell(thread, db)
		thread.notifyProgressMain.emit(100, "Finished")
		db.commit()
		db.close()

	def _exportPrepareDb(self, thread, name):
		thread.notifyProgressLocal.emit(0, "Database initialisation")
		fileName = config.db % (name)
		# Delete the file if it already exist
		if os.path.isfile(fileName):
			os.remove(fileName)

		# Open connection
		return sqlite3.connect(fileName)

	def _exportWorldCreation(self, thread, db, name):
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
		query = "INSERT INTO area (id_area_type, id_region, container, x, y, directions) VALUES (?, ?, ?, ?, ?, ?)"
		nbAreas = 0
		for x in self.cells:
			for y in self.cells[x]:
				t = areaTypes[self.cells[x][y][0]]
				if t['name'] == 'water':
					continue

				nbAreas = nbAreas + 1
				areas = [
					areaTypes[self.cells[x][y][0]]['id_area_type'],
					1,
					"world",
					x,
					y,
					self.cells[x][y][1]
				]
				c.execute(query, areas)

		thread.notifyProgressLocal.emit(100, "Areas created")

	def _exportStartCell(self, thread, db):
		c = db.cursor()

		# select start cell ID in DB from coordinates
		query = "SELECT id_area FROM area WHERE x = ? and y = ?"
		c.execute(query, (self.startCellPosition[0], self.startCellPosition[1]))
		result = c.fetchone()

		# insert in setting the id of the starting cell
		query = str("INSERT INTO settings (key, value) VALUES ('START_CELL_ID', ?)")
		c.execute(query, [result[0]])

		thread.notifyProgressLocal.emit(100, "Start cell defined")

class exception(BaseException):
	pass
