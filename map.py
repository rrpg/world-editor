# -*- coding: utf8 -*-

"""
Module to work with world maps (Generation, edition, save...)
"""
import subprocess
import os
import config


class map:
	@staticmethod
	def generate(name, width, height):
		command = config.generator['map']['generator'] % (
			config.generator['map']['destination-dir'] + '/' + name,
			width,
			height
		)
		if not os.path.exists(config.generator['map']['destination-dir']):
			os.makedirs(config.generator['map']['destination-dir'])
		subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
