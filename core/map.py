# -*- coding: utf-8 -*-

"""
Module to work with world maps (Generation, edition, save...)
"""
import subprocess
import os
from core import config
import sqlite3
import sys
import tarfile
import csv
from core.localisation import _

# Import an external check class from the generator
sys.path.insert(0, config.generator['map']['path'])
import checks

class map:
	"""
	Class to interface with a map DB.
	The generation and export are done here.
	"""
	_file = None
	startCellPosition = None
	cells = dict()
	places = dict()
	npc = dict()
	species = {'human': {'name': _('HUMANS_NAME'), 'description': '', 'internalName': _('HUMANS_INTERNAL_NAME')}}

	_entitiesDesc = {
		'places': (('internalName', 'str'), ('type', 'int'), ('name', 'str'), ('x', 'int'), ('y', 'int'), ('size', 'int')),
		'npc': (('internalName', 'str'), ('name', 'str'), ('gender', 'int'), ('species', 'int'), ('x', 'int'), ('y', 'int')),
		'species': (('internalName', 'str'), ('name', 'str'), ('description', 'str'))
	}
	_placesTypes = {'dungeon': _('PLACE_TYPE_DUNGEON'), 'cave': _('PLACE_TYPE_CAVE')}
	_genders = [_('GENDER_MALE'), _('GENDER_FEMALE')]

	def __init__(self):
		self._file = None
		self.startCellPosition = None
		self.cells = dict()
		self.places = dict()
		self.npc = dict()

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

		self._file = name
		self.loadCells()

	def loadCells(self):
		"""
		Method which load a map's cells. The cells are read from a text file
		and saved in a list.
		"""
		# Open text file containing cells infos
		areasFile = open(self._file + '.txt', "r")
		nbAreas = 0
		for area in areasFile:
			a = area.split(' ')
			try:
				self.cells[a[1]];
			except KeyError:
				self.cells[a[1]] = dict()

			self.cells[a[1]][a[2]] = (int(a[0]), int(a[3]))

	def loadEntity(self, entity):
		"""
		Method to load the world's NPC from a text file

		@param entity (npc|places|species)
		"""
		f = open(self._file + '_' + entity + '.csv', "r")
		entities = dict()
		csvreader = csv.reader(f, delimiter=' ',
			quotechar='"', quoting=csv.QUOTE_MINIMAL)
		entityFields = [e[0] for e in self._entitiesDesc[entity]]
		entityTypes = [e[1] for e in self._entitiesDesc[entity]]
		for e in csvreader:
			entities[e[0]] = dict(zip(
				entityFields,
				# Cast the values if integers are expected
				[int(v) if entityTypes[k] == 'int' else v for k, v in enumerate(e)]
			))

		return entities

	def checkForExport(self):
		"""
		Method to check if a cell is ready to be exported (start cell selected)
		"""
		if self.startCellPosition is None:
			raise exception(_('ERROR_NO_START_CELL_SELECTED'))

	def setStartCellPosition(self, position):
		"""
		Method to set the start cell. The selected position must be a valid
		position.
		"""
		if self.isCellOnLand(position):
			self.startCellPosition = position
		else:
			raise exception(_('ERROR_INVALID_START_CELL_POSITION'))

	def isCellOnLand(self, position):
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
		thread.notifyProgressMain.emit(12, "")

		self._exportCreateDbStructure(thread, db)
		thread.notifyProgressMain.emit(25, "")

		self._exportCreateGenders(thread, db)
		thread.notifyProgressMain.emit(37, "")

		self._exportSpecies(thread, db)
		thread.notifyProgressMain.emit(50, "")

		self._exportWorldCreation(thread, db, name)
		thread.notifyProgressMain.emit(62, "")

		self._exportStartCell(thread, db)
		thread.notifyProgressMain.emit(75, "")

		self._exportPlaces(thread, db)
		thread.notifyProgressMain.emit(87, "")

		self._exportNpc(thread, db)
		thread.notifyProgressMain.emit(100, "")

		db.commit()
		db.close()

	def _exportPrepareDb(self, thread, name):
		"""
		Method to create the DB
		"""
		thread.notifyProgressLocal.emit(0, _('LOCAL_PROGRESS_DATABASE_CREATION'))
		fileName = config.db % (name)
		d = os.path.dirname(fileName)

		# Delete the file if it already exist
		if os.path.isfile(fileName):
			os.remove(fileName)

		if not os.path.isdir(d):
			raise BaseException("The folder %s does not exist" % d)

		thread.notifyProgressLocal.emit(100, _('LOCAL_PROGRESS_FINISHED'))
		# Open connection
		return sqlite3.connect(fileName)

	def _exportCreateDbStructure(self, thread, db):
		"""
		Method to create the DB structure
		"""
		c = db.cursor()

		thread.notifyProgressLocal.emit(0, _('LOCAL_PROGRESS_DATABASE_STRUCTURE_CREATION'))
		f = open(config.databaseStructure, 'r')
		sql = f.read()
		c.executescript(sql)
		f.close()
		thread.notifyProgressLocal.emit(100, _('LOCAL_PROGRESS_FINISHED'))

	def _exportCreateGenders(self, thread, db):
		"""
		Method to create the genders in DB
		"""
		c = db.cursor()

		thread.notifyProgressLocal.emit(0, _('LOCAL_PROGRESS_GENDERS_CREATION'))
		query = str("INSERT INTO gender (name) VALUES (?)")
		for g in self._genders:
			c.execute(query, [g])
		thread.notifyProgressLocal.emit(100, _('LOCAL_PROGRESS_FINISHED'))

	def _exportSpecies(self, thread, db):
		"""
		Method to export the world's species in the DB.
		"""
		c = db.cursor()

		thread.notifyProgressLocal.emit(0, _('LOCAL_PROGRESS_SPECIES_CREATION'))
		query = str("INSERT INTO species (name, description) VALUES (?, ?)")
		for s in self.species.values():
			c.execute(query, (s['name'], s['description']))
		thread.notifyProgressLocal.emit(100, _('LOCAL_PROGRESS_FINISHED'))

	def _exportWorldCreation(self, thread, db, name):
		"""
		Method to export the world in the DB.
		"""
		c = db.cursor()

		thread.notifyProgressLocal.emit(0, _('LOCAL_PROGRESS_REGIONS_CREATION'))
		# Create main region
		query = str("INSERT INTO region (region_name) VALUES (?)")
		c.execute(query, [name])

		thread.notifyProgressLocal.emit(33, _('LOCAL_PROGRESS_AREA_TYPES_CREATION'))
		# Create area types
		query = "INSERT INTO area_type (name) VALUES "
		areaTypesCodes = checks.getGroundTypes()
		valuesInsert = list()
		for t in self._placesTypes.keys():
			valuesInsert.append("('" + t + "')")
		values = list()
		for t in areaTypesCodes:
			valuesInsert.append("(?)")
			values.append(t)
		query = query + ', '.join(valuesInsert)
		c.execute(query, values)

		thread.notifyProgressLocal.emit(66, _('LOCAL_PROGRESS_AREAS_CREATION'))
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

		thread.notifyProgressLocal.emit(100, _('LOCAL_PROGRESS_FINISHED'))

	def _exportStartCell(self, thread, db):
		"""
		Method to export the start cell in the DB.
		"""
		c = db.cursor()

		thread.notifyProgressLocal.emit(0, _('LOCAL_PROGRESS_START_CELL'))
		# select start cell ID in DB from coordinates
		query = "SELECT id_area FROM area WHERE x = ? and y = ?"
		c.execute(query, (self.startCellPosition[0], self.startCellPosition[1]))
		result = c.fetchone()

		# insert in setting the id of the starting cell
		query = str("INSERT INTO settings (key, value) VALUES ('START_CELL_ID', ?)")
		c.execute(query, [result[0]])
		thread.notifyProgressLocal.emit(100, _('LOCAL_PROGRESS_FINISHED'))

	def _exportPlaces(self, thread, db):
		"""
		Method to export the map's places in the DB.
		"""
		if len(self.places) == 0:
			return

		c = db.cursor()

		thread.notifyProgressLocal.emit(0, _('LOCAL_PROGRESS_PLACES'))

		# query to insert places
		query = str("\
			INSERT INTO place \
				(id_area, id_area_type, name, place_size) \
				VALUES (\
					(SELECT id_area FROM area WHERE x = ? and y = ?), \
					(SELECT id_area_type FROM area_type WHERE name = ?), \
					?,\
					?\
				)")

		placeTypePercent = 100 / len(self.places)
		placeTypesKeys = self._placesTypes.keys()
		for i, p in enumerate(self.places.values()):
			c.execute(
				query,
				[
					p['x'],
					p['y'],
					placeTypesKeys[p['type']],
					p['name'],
					p['size']
				]
			)

			# One-cell place, the area can be directly inserted
			if p['size'] == 0:
				placeId = c.lastrowid
				queryArea = "INSERT INTO area \
					(id_area_type, id_region, container, x, y, directions) \
					VALUES (\
						(SELECT id_area_type FROM area_type WHERE name = ?), \
						(SELECT id_region FROM area WHERE x = ? and y = ?), \
						?, \
						0, 0, 0\
					)"

				c.execute(
					queryArea,
					[
						placeTypesKeys[p['type']],
						p['x'],
						p['y'],
						placeTypesKeys[p['type']] + '_' + str(c.lastrowid)
					]
				)

				c.execute(
					"UPDATE place set entrance_id = ? WHERE id_place = ?",
					[c.lastrowid, placeId]
				)

			thread.notifyProgressLocal.emit((i + 1) * placeTypePercent, "")
		thread.notifyProgressLocal.emit(100, _('LOCAL_PROGRESS_FINISHED'))

	def _exportNpc(self, thread, db):
		"""
		Method to export the NPCs in the DB.
		"""
		if len(self.npc) == 0:
			return
		c = db.cursor()

		thread.notifyProgressLocal.emit(0, _('LOCAL_PROGRESS_NPC'))
		# query to insert places
		query = str("\
			INSERT INTO `character` \
				(name, id_species, id_gender, id_area) \
				VALUES (\
					?,\
					(SELECT id_species FROM species WHERE name = ?), \
					(SELECT id_gender FROM gender WHERE name = ?), \
					(SELECT id_area FROM area WHERE x = ? and y = ?)\
				)")

		npcPercent = 100 / len(self.npc)
		speciesNames = self.getSpeciesNames()
		genders = map.getGenders()
		for i, p in enumerate(self.npc.values()):
			c.execute(
				query,
				[
					p['name'],
					speciesNames[p['species']],
					genders[p['gender']],
					p['x'],
					p['y']
				]
			)

			thread.notifyProgressLocal.emit((i + 1) * npcPercent, "")
		thread.notifyProgressLocal.emit(100, _('LOCAL_PROGRESS_FINISHED'))

	@staticmethod
	def getPlaceTypesLabels():
		"""
		Method to get the list of the place types.
		"""
		return map._placesTypes.values()

	@staticmethod
	def getPlaceSizesLabels():
		"""
		Method to get the list of the place sizes.
		"""
		return [_('SIZE_ONE_CELL'), _('SIZE_SMALL'), _('SIZE_MEDIUM'), _('SIZE_LARGE')]

	@staticmethod
	def getGenders():
		"""
		Method to get the list of the available genders.
		"""
		return map._genders

	def getSpeciesNames(self):
		"""
		Return the list of species' names
		"""
		return list(s['name'] for s in self.species.values())

	def save(self, fileName):
		"""
		Method to save the map in a .map file, which is just a .tar.gz renamed
		file.
		"""
		if os.path.exists(fileName):
			os.remove(fileName)

		tar = tarfile.open(fileName, "w:gz")

		nameFile = os.path.dirname(self._file) + '/__NAME__'
		f = open(nameFile, 'w')
		f.write(os.path.basename(self._file))
		f.close()
		tar.add(nameFile, arcname=os.path.basename(nameFile))
		os.remove(nameFile)

		tar.add(self._file + '.bmp', arcname=os.path.basename(self._file) + '.bmp')
		tar.add(self._file + '.txt', arcname=os.path.basename(self._file) + '.txt')

		self.saveEntity(tar, 'places', self.places.values())
		self.saveEntity(tar, 'npc', self.npc.values())
		self.saveEntity(tar, 'species', self.species.values())

		f = open(self._file + '_start_cell.txt', 'w')
		if self.startCellPosition is not None:
			f.write(str(self.startCellPosition[0]) + ' ' + str(self.startCellPosition[1]))
		f.close()
		tar.add(
			self._file + '_start_cell.txt',
			arcname=os.path.basename(self._file) + '_start_cell.txt'
		)
		tar.close()
		os.remove(self._file + '_start_cell.txt')

	def saveEntity(self, tar, entityName, values):
		"""
		Method to save the values of an entity
		"""
		f = open(self._file + '_' + entityName + '.csv', 'wb')
		csvwriter = csv.writer(f, delimiter=' ',
			quotechar='"', quoting=csv.QUOTE_MINIMAL)
		entityFields = [e[0] for e in self._entitiesDesc[entityName]]
		for p in values:
			csvwriter.writerow([p[v] for v in entityFields])
		f.close()
		tar.add(
			self._file + '_' + entityName + '.csv',
			arcname=os.path.basename(self._file) + '_' + entityName + '.csv'
		)
		os.remove(self._file + '_' + entityName + '.csv')

	def open(self, fileName, tempFolder):
		"""
		Method to open a filename and instanciate the map object
		"""
		tar = tarfile.open(fileName, 'r')
		tmpDir = tempFolder + '/'

		try:
			for item in tar:
				tar.extract(item, tmpDir)
				if item.path == '__NAME__':
					worldNameFile = open(tmpDir + item.path, "r")
					worldName = worldNameFile.readline()
					self._file = tmpDir + worldName
					worldNameFile.close()
				elif item.path[-15:] == '_start_cell.txt':
					startCellFile = open(tmpDir + item.path, "r")
					startCell = startCellFile.readline()

					if startCell != '':
						startCell = startCell.split()
						self.startCellPosition = (int(startCell[0]), int(startCell[1]))
					startCellFile.close()

			self.loadCells()
			self.places = self.loadEntity('places')
			self.npc = self.loadEntity('npc')
			self.species = self.loadEntity('species')
		except IOError:
			raise exception(_('ERROR_OPENING_MAP_FILE'))

		return (self._file, worldName)


class exception(BaseException):
	pass
