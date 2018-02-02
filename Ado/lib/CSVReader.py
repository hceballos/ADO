#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import csv
import os

from ERP2016Parser import ERP2016Parser

class CSVReader():
	
	def __init__(self, path):
		self.path = path
		self.registers = []

		self.readCSV()

	def readCSV(self):
		filenames = self._getFileNamesFrom(self.path)

		for filename in filenames:
			csvReader = csv.reader(codecs.open(self.path + filename, "r",encoding='utf-8', errors='ignore'), delimiter = ERP2016Parser.DELIMITER_OUTPUT)

			for row in csvReader:
				self.registers.append(row)

	def _getFileNamesFrom(self, folder):
		return os.listdir(folder)