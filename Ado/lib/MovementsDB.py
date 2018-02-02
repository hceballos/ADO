import sqlite3

class MovementsDB():

	TABLE_NAME = 'MovimientosTabla'

	TABLE_COLUMN_CUENTA = "CUENTA"
	TABLE_COLUMN_FECHA = "FECHA"
	TABLE_COLUMN_N_COMPROBANTE = "N_COMPROBANTE"
	TABLE_COLUMN_TIPO = "TIPO"
	TABLE_COLUMN_N_INTERNO = "N_INTERNO"
	TABLE_COLUMN_PRESUP_DE_CAJA = "PRESUP_DE_CAJA"
	TABLE_COLUMN_CENTRO_DE_COSTO = "CENTRO_DE_COSTO"
	TABLE_COLUMN_AUXILIAR = "AUXILIAR"
	TABLE_COLUMN_TIPO_DOC = "TIPO_DOC"
	TABLE_COLUMN_NUMERO_DOC = "NUMERO_DOC"
	TABLE_COLUMN_DETDE_GASTO_INSTFINANCIERO = "DETDE_GASTO_INSTFINANCIERO"
	TABLE_COLUMN_DEBE = "DEBE"
	TABLE_COLUMN_HABER = "HABER"
	TABLE_COLUMN_SALDO = "SALDO"
	TABLE_COLUMN_DESCRIPCION = "DESCRIPCION"
	TABLE_COLUMN_NUM_FACTURA = "NUM_FACTURA"

	def __init__(self, dataBaseFileName):
		self.dataBaseFileName = dataBaseFileName

		self.conection = sqlite3.connect(self.dataBaseFileName)
		self.conection.text_factory = str

		self.cursor = self.conection.cursor()

		self.cursor.execute(
			'DROP TABLE IF EXISTS {}'.format(
				self.TABLE_NAME
			)
		)

		self.cursor.execute(
			'CREATE TABLE {} ({} TEXT, {} TEXT, {} INTEGER, {} TEXT, {} INTEGER, {} INTEGER NULL, {} TEXT, {} TEXT, {} TEXT, {} INTEGER, {} INTEGER NULL, {} INTEGER, {} INTEGER, {} INTEGER, {} TEXT, {} TEXT)'
				.format(
					self.TABLE_NAME,
					self.TABLE_COLUMN_CUENTA,
					self.TABLE_COLUMN_FECHA,
					self.TABLE_COLUMN_N_COMPROBANTE,
					self.TABLE_COLUMN_TIPO,
					self.TABLE_COLUMN_N_INTERNO,
					self.TABLE_COLUMN_PRESUP_DE_CAJA,
					self.TABLE_COLUMN_CENTRO_DE_COSTO,
					self.TABLE_COLUMN_AUXILIAR,
					self.TABLE_COLUMN_TIPO_DOC,
					self.TABLE_COLUMN_NUMERO_DOC,
					self.TABLE_COLUMN_DETDE_GASTO_INSTFINANCIERO,
					self.TABLE_COLUMN_DEBE,
					self.TABLE_COLUMN_HABER,
					self.TABLE_COLUMN_SALDO,
					self.TABLE_COLUMN_DESCRIPCION,
					self.TABLE_COLUMN_NUM_FACTURA
			)
		)

		self.conection.commit()

	def saveRegisters(self, registers):
		for register in registers:
			self.conection.execute(
				'INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'.format(
					self.TABLE_NAME
				),
				register
			)

		self.conection.commit()

	def query(self, queryObject):
		self.cursor.execute(queryObject.getQuery())
		return self.cursor.fetchall()