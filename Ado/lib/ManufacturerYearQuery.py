from MovementsDB import MovementsDB

class ManufacturerYearQuery():

	def __init__(self):
		pass

	def setManufacturer(self, manufacturerName):
		self.manufacturerName = manufacturerName

	def setYear(self, year):
		self.year = year

	def getQuery(self):
		return 'SELECT * FROM {} WHERE {}="{}" AND {}={}'.format(
			MovementsDB.TABLE_NAME,
			MovementsDB.TABLE_COLUMN_MANUFACTURER,
			self.manufacturerName,
			MovementsDB.TABLE_COLUMN_YEAR,
			self.year
		)