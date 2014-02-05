# -*- coding: utf8 -*-

"""
Module to work with world maps (Generation, edition, save...)
"""
from subprocess import call

import config

class map:
	@staticmethod
	def generate(name, width, height):
		command = config.generator['map']['generator'] % (config.generator['map']['destination-dir'] + '/' + name, width, height)
		call(command, shell=True)
