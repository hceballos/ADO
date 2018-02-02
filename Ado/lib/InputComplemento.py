#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import sqlite3

class InputComplemento():

	TABLE_NAME = 'complemento'

	TABLE_RUT = 'RUT'
	TABLE_NOMBRE = 'NOMBRE'

	def __init__(self, dataBaseFileName):
		self.dataBaseFileName = dataBaseFileName
		print "InputComplemento - Asignacion de nombre de base de datos FILE_DB = 'data.db'"

		self.conection = sqlite3.connect(self.dataBaseFileName)
		self.conection.text_factory = str

		self.cursor = self.conection.cursor()
		print "InputComplemento - conector con base de datos"

		self.cursor.execute(
			'DROP TABLE IF EXISTS {}'.format(
				self.TABLE_NAME
			)
		)

		self.cursor.execute(
			'CREATE TABLE {} ({} TEXT, {} TEXT)'
				.format(
					self.TABLE_NAME,
					self.TABLE_RUT,
					self.TABLE_NOMBRE
			)
		)

		self.conection.commit()
		print "input/InputComplemento - Asignacion de columnas"
		self.saveRegisters()

	def saveRegisters(self):

		registers = []										#creo una lista vacia que almacenara los elementos leidos del .csv
		with codecs.open("input/input_Complemento/complemento.csv", "r",encoding='utf-8', errors='ignore') as infile:
			for line in infile:								#con el iterador for leo linea a linea  en el archivo
				line = line.strip()							#strip() elimina los caracteres especiales al final de la linea "\n \r"
				line = line.replace('"', '')				#reemplazo el "" por algo vacio
				data = line.split(";")      				#agrego a la linea cada elemento y lo separa por una ","
				registers.append(data)


		for register in registers:
			self.conection.execute(
				'INSERT INTO {} VALUES (?, ?)'.format(
					self.TABLE_NAME
				),
				register
			)

		self.conection.commit()
		print "InputComplemento - salvar los datos de 'registers' en base de datos"





