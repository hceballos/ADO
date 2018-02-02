from ERP2016Parser import ERP2016Parser

import os

class InputProcessor():

	def setInputFolder(self, inputFolder):
		self.inputFolder = inputFolder

	def setCSVFolder(self, csvFolder):
		self.csvFolder = csvFolder

	def process(self):
		#get all input files
		inputFileNames = self._getFileNamesFrom(self.inputFolder)

		for filename in inputFileNames:
			parser = ERP2016Parser()
			parser.setInputFileName(self.inputFolder + filename)
			parser.setOutputFileName(self.csvFolder + filename)
			parser.generate()

	def _getFileNamesFrom(self, folder):
		files = []
		for file in os.listdir(folder):
			if not file.startswith('.'):
				files.append(file)
		return files
