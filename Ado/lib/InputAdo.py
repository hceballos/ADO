#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import sqlite3

class InputAdo():

	TABLE_NAME = 'ado'

	TABLE_CUENTA2 = 'CUENTA2'
	TABLE_CODCUENTA = 'CODCUENTA'
	TABLE_NOMBRECUENTA = 'NOMBRECUENTA'
	TABLE_CLASIFICACION = 'CLASIFICACION'
	TABLE_FINANCIAMIENTO = 'FINANCIAMIENTO'
	TABLE_IDENTIFICACION = 'IDENTIFICACION'
	TABLE_GRUPO = 'GRUPO'

	def __init__(self, dataBaseFileName):
		self.dataBaseFileName = dataBaseFileName
		print "InputAdo - Asignacion de nombre de base de datos FILE_DB = 'data.db'"

		self.conection = sqlite3.connect(self.dataBaseFileName)
		self.conection.text_factory = str

		self.cursor = self.conection.cursor()
		print "InputAdo - conector con base de datos"

		self.cursor.execute(
			'DROP TABLE IF EXISTS {}'.format(
				self.TABLE_NAME
			)
		)

		self.cursor.execute(
			'CREATE TABLE {} ({} TEXT, {} TEXT, {} TEXT, {} TEXT, {} TEXT, {} TEXT, {} TEXT)'
				.format(
					self.TABLE_NAME,
					self.TABLE_CUENTA2,
					self.TABLE_CODCUENTA,
					self.TABLE_NOMBRECUENTA,
					self.TABLE_CLASIFICACION,
					self.TABLE_FINANCIAMIENTO,
					self.TABLE_IDENTIFICACION,
					self.TABLE_GRUPO
			)
		)

		self.conection.commit()
		print "InputAdo - Asignacion de columnas"
		self.saveRegisters()
		
	def saveRegisters(self):

		registers = []										#creo una lista vacia que almacenara los elementos leidos del .csv
		with codecs.open("input/input_ado/ado.csv", "r",encoding='utf-8', errors='ignore') as infile:
			for line in infile:								#con el iterador for leo linea a linea  en el archivo
				line = line.strip()							#strip() elimina los caracteres especiales al final de la linea "\n \r"
				line = line.replace('"', '')				#reemplazo el "" por algo vacio
				data = line.split(";")      				#agrego a la linea cada elemento y lo separa por una ","
				registers.append(data)


		for register in registers:
			self.conection.execute(
				'INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?)'.format(
					self.TABLE_NAME
				),
				register
			)

		self.conection.commit()
		print "InputAdo - salvar los datos de 'registers' en base de datos"




