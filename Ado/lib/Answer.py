import sqlite3

class Answer:
	def __init__(self, sql):
		self.sql=sql

	def Connect(self):
		#coneccion con base de datos
		self.conn = sqlite3.connect('data.db')
		self.conn.text_factory = str
		self.cur = self.conn.cursor()

	def Read(self):
		#leer consulta almacenada en fichero txt
		file = open(self.sql, "r")
		self.sql=file.read()
		file.close()


	def Query(self):
		#ingresar consulta leida al excecute
		data = self.cur.execute(self.sql)

	def Print(self):
		#imprimir resultados en consola
		rows = self.cur.fetchall() 
		print rows
		self.cur.close()
