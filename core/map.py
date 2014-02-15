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
	"""
	Class to interface with a map DB.
	The generation and export are done here.
	"""
	startCellPosition = None
	cells = dict()
	species = [['Humans', '']]

	def generate(self, name, width, height):
		"""
		Method which generates a map and load the cells in an attribute of the
		class.
		"""
		command = config.generator['map']['generator'] % (
			name,
			width,
			height
		)

		p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		result = p.communicate()
		if len(result[1]) > 0:
			raise BaseException(result[1])

		self.loadCells(name)

	def loadCells(self, name):
		"""
		Method which load a map's cells. The cells are read from a text file
		and saved in a list.
		"""
		# Open text file containing cells infos
		areasFile = open(name + '.txt', "r")
		nbAreas = 0
		for area in areasFile:
			a = area.split(' ')
			try:
				self.cells[a[1]];
			except KeyError:
				self.cells[a[1]] = dict()

			self.cells[a[1]][a[2]] = (int(a[0]), int(a[3]))

	def checkForExport(self):
		"""
		Method to check if a cell is ready to be exported (start cell selected)
		"""
		if self.startCellPosition is None:
			raise exception("No start cell selected")

	def setStartCellPosition(self, position):
		"""
		Method to set the start cell. The selected position must be a valid
		position.
		"""
		if self.isStartCellValid(position):
			self.startCellPosition = position
		else:
			raise exception("Invalid start cell position")

	def isStartCellValid(self, position):
		"""
		Checks if the given position is a valid position for a start cell (must
		not be a water cell).
		"""
		areaTypesCodes = checks.getGroundTypes()
		return self.cells[str(position[0])][str(position[1])][0] is not areaTypesCodes['water']

	def export(self, name, fileName, thread):
		"""
		Function to export the map in a SQLite Db.
		For each step of the export, the progression will be updated through
		the given thread.
		"""
		thread.notifyProgressMain.emit(0, "")
		db = self._exportPrepareDb(thread, fileName)
		thread.notifyProgressMain.emit(16, "")

		self._exportCreateDbStructure(thread, db)
		thread.notifyProgressMain.emit(33, "")

		self._exportCreateGenders(thread, db)
		thread.notifyProgressMain.emit(49, "")

		self._exportSpecies(thread, db)
		thread.notifyProgressMain.emit(66, "")

		self._exportWorldCreation(thread, db, name)
		thread.notifyProgressMain.emit(82, "")

		self._exportStartCell(thread, db)
		thread.notifyProgressMain.emit(100, "")

		db.commit()
		db.close()

	def _exportPrepareDb(self, thread, name):
		"""
		Method to create the DB
		"""
		thread.notifyProgressLocal.emit(0, "Database creation")
		fileName = config.db % (name)
		d = os.path.dirname(fileName)

		# Delete the file if it already exist
		if os.path.isfile(fileName):
			os.remove(fileName)

		if not os.path.isdir(d):
			raise BaseException("The folder %s does not exist" % d)

		thread.notifyProgressLocal.emit(100, "Finished")
		# Open connection
		return sqlite3.connect(fileName)

	def _exportCreateDbStructure(self, thread, db):
		"""
		Method to create the DB structure
		"""
		c = db.cursor()

		thread.notifyProgressLocal.emit(0, "Database structure creation")
		f = open(config.databaseStructure, 'r')
		sql = f.read()
		c.executescript(sql)
		f.close()
		thread.notifyProgressLocal.emit(100, "Finished")

	def _exportCreateGenders(self, thread, db):
		"""
		Method to create the genders in DB
		"""
		c = db.cursor()

		thread.notifyProgressLocal.emit(0, "Genders creation")
		query = str("INSERT INTO gender (name) VALUES ('male')")
		c.execute(query)
		query = str("INSERT INTO gender (name) VALUES ('female')")
		c.execute(query)
		thread.notifyProgressLocal.emit(100, "Finished")

	def _exportSpecies(self, thread, db):
		"""
		Method to export the world's species in the DB.
		"""
		c = db.cursor()

		thread.notifyProgressLocal.emit(0, "Species creation")
		query = str("INSERT INTO species (name, description) VALUES (?, ?)")
		for s in self.species:
			c.execute(query, s)
		thread.notifyProgressLocal.emit(100, "Finished")

	def _exportWorldCreation(self, thread, db, name):
		"""
		Method to export the world in the DB.
		"""
		c = db.cursor()

		thread.notifyProgressLocal.emit(0, "Regions creation")
		# Create main region
		query = str("INSERT INTO region (region_name) VALUES (?)")
		c.execute(query, [name])

		thread.notifyProgressLocal.emit(33, "Area types creation")
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

		thread.notifyProgressLocal.emit(66, "Areas creation")
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

		thread.notifyProgressLocal.emit(100, "Finished")

	def _exportStartCell(self, thread, db):
		"""
		Method to export the start cell in the DB.
		"""
		c = db.cursor()

		thread.notifyProgressLocal.emit(0, "Start cell saving")
		# select start cell ID in DB from coordinates
		query = "SELECT id_area FROM area WHERE x = ? and y = ?"
		c.execute(query, (self.startCellPosition[0], self.startCellPosition[1]))
		result = c.fetchone()

		# insert in setting the id of the starting cell
		query = str("INSERT INTO settings (key, value) VALUES ('START_CELL_ID', ?)")
		c.execute(query, [result[0]])
		thread.notifyProgressLocal.emit(100, "Finished")

	@staticmethod
	def getPlaceTypesLabels():
		return ['Dungeon', 'Cave']

	@staticmethod
	def getPlaceSizesLabels():
		return ['1 cell', 'Small', 'Medium', 'Large']


class exception(BaseException):
	pass
