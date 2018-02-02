#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import re, sys
import sqlite3
import os
from jinja2 import Environment, PackageLoader
reload(sys)  
sys.setdefaultencoding('Cp1252')

class JefeContable:

	def __init__(self):
		print "inicio"

	def activo(self):
#-------------------------------------------------------------------------------------------------------------------------
		self.conn = sqlite3.connect('data.db')
		self.conn.text_factory = str
		self.cur= self.conn.cursor()

		registros=[]	
		variable= self.cur.execute('SELECT DISTINCT cuenta FROM MovimientosTabla ORDER BY cuenta ASC')
		for row in variable:
			registros.append(list(row))

		lista_registros = [x[0] for x in registros]
		# Nombre cuenta :
		for elemento in lista_registros:

		    if re.match	('^[1]', elemento):
				print "vengo de activo", elemento
				self.cur = self.conn.cursor()
#-------------------------------------------------------------------------------------------------------------------------
			#Nombre de cuenta
				lista_nomCuenta=[]			
				nomCuenta= self.cur.execute("SELECT nombrecuenta FROM MovimientosTabla INNER JOIN ADO ON MovimientosTabla.CUENTA = ado.CUENTA2 WHERE cuenta=? GROUP BY cuenta HAVING cuenta", (elemento,) )
				for row in nomCuenta:
					lista_nomCuenta.append(list(row))
				
				nueva_lista_nomCuenta = [x[0] for x in lista_nomCuenta]

				for elemento_nueva_lista_nomCuenta in nueva_lista_nomCuenta:
					print elemento_nueva_lista_nomCuenta, "elemento_nueva_lista_nomCuenta"
#-------------------------------------------------------------------------------------------------------------------------
			#Numero de cuenta
				lista_numCuenta=[]
				numCuenta= self.cur.execute("SELECT codcuenta FROM MovimientosTabla INNER JOIN ADO ON MovimientosTabla.CUENTA = ado.CUENTA2 WHERE  cuenta=? GROUP BY cuenta HAVING cuenta", (elemento,) )

				for row in numCuenta:
					lista_numCuenta.append(list(row))
				
				nueva_lista_numCuenta = [x[0] for x in lista_numCuenta]

				for elemento_lista_numCuenta in nueva_lista_numCuenta:
					print elemento_lista_numCuenta, "elemento_lista_numCuenta"

#-------------------------------------------------------------------------------------------------------------------------
			# Saldo :
				lista_saldo=[]
				saldo= self.cur.execute("SELECT	sum(debe - haber) as SALDO_SEMANA_ACTUAL FROM MovimientosTabla	 WHERE cuenta=? GROUP BY cuenta HAVING cuenta", (elemento,) )

				for row in saldo:
					lista_saldo.append(list(row))
				
				lista_saldo_cuenta = [x[0] for x in lista_saldo]

				for elemento_lista_saldo_cuenta in lista_saldo_cuenta:
					print elemento_lista_saldo_cuenta, "elemento_lista_saldo_cuenta"
#-------------------------------------------------------------------------------------------------------------------------
			# Grafico
				grafico= self.cur.execute("SELECT fecha, SALDO FROM MovimientosTabla WHERE fecha between '01-01-2013' AND DATE('NOW') AND cuenta=? ORDER BY fecha asc", (elemento,) )
				lista_grafico=[]				
				for row in grafico:
					lista_grafico.append(list(row))

				print lista_grafico
#-------------------------------------------------------------------------------------------------------------------------
			# Tabla 1
				Movimientos_Cuenta= self.cur.execute("SELECT lower(descripcion), lower(nombre) as NOMBRE, fecha, N_comprobante as VOUCHER, debe as CARGOS, haber as ABONOS FROM MovimientosTabla INNER JOIN complemento ON MovimientosTabla.AUXILIAR = complemento.rut WHERE cuenta=? GROUP BY fecha HAVING fecha between '01-01-2014' and date('now') ORDER BY fecha desc LIMIT 10", (elemento,) )
				lista_Movimientos_Cuenta=[]
				for row in Movimientos_Cuenta:
					lista_Movimientos_Cuenta.append(list(row))

				#Concicionante , si la cuenta usa rut > 0 , entonces muestra la tabla
				cantidad_Movimientos_Cuenta = len(lista_Movimientos_Cuenta)

				Movimientos_Cuenta_2= self.cur.execute("SELECT lower(descripcion), fecha, N_comprobante as VOUCHER, debe as CARGOS, haber as ABONOS FROM MovimientosTabla WHERE cuenta=? GROUP BY fecha HAVING fecha between '01-01-2013' and date('now') ORDER BY fecha desc LIMIT 10", (elemento,) )
				lista_Movimientos_Cuenta_2=[]
				for row in Movimientos_Cuenta_2:
					lista_Movimientos_Cuenta_2.append(list(row))
#-------------------------------------------------------------------------------------------------------------------------
			# Tabla 2
				auxiliares= self.cur.execute("SELECT auxiliar, lower(nombre) as NOMBRE,  sum (debe - haber) as SALDO_SEMANA_ACTUAL FROM MovimientosTabla INNER JOIN complemento ON MovimientosTabla.AUXILIAR = complemento.rut WHERE cuenta=? GROUP BY auxiliar HAVING auxiliar and SALDO_SEMANA_ACTUAL  ORDER BY SALDO_SEMANA_ACTUAL desc LIMIT 10", (elemento,) )
				lista_auxiliares=[]
				for row in auxiliares:
					lista_auxiliares.append(list(row))
#-------------------------------------------------------------------------------------------------------------------------
			# Tabla 3
				Saldo_contra_naturaleza= self.cur.execute("SELECT auxiliar, lower(nombre) as NOMBRE, sum (debe - haber) as SALDO_SEMANA_ACTUAL FROM MovimientosTabla INNER JOIN complemento ON MovimientosTabla.AUXILIAR = complemento.rut WHERE cuenta=? GROUP BY auxiliar HAVING auxiliar and SALDO_SEMANA_ACTUAL<0  ORDER BY SALDO_SEMANA_ACTUAL asc LIMIT 10", (elemento,) )
				lista_contra_naturaleza=[]
				for row in Saldo_contra_naturaleza:
					lista_contra_naturaleza.append(list(row))

				#Concicionante , si la cuenta tiene ruts en contra su naturaleza....
				cantidad_Movimientos_Cuenta = len(lista_contra_naturaleza)

				contra_naturaleza= self.cur.execute("SELECT auxiliar, lower(nombre) as NOMBRE, sum (debe - haber) as SALDO_SEMANA_ACTUAL FROM MovimientosTabla INNER JOIN complemento ON MovimientosTabla.AUXILIAR = complemento.rut WHERE cuenta=? GROUP BY auxiliar HAVING auxiliar and SALDO_SEMANA_ACTUAL<0  ORDER BY SALDO_SEMANA_ACTUAL asc LIMIT 10", (elemento,) )
				lista_contra_naturaleza=[]
				for row in contra_naturaleza:
					lista_contra_naturaleza.append(list(row))
#-------------------------------------------------------------------------------------------------------------------------
			# Tabla 4
				Movimientos_CCostos= self.cur.execute("SELECT centro_de_costo, lower(nombreccosto), sum (debe - haber) as SALDO_SEMANA_ACTUAL FROM MovimientosTabla INNER JOIN Ccostos ON MovimientosTabla.centro_de_costo = Ccostos.ccosto WHERE cuenta=? GROUP BY centro_de_costo HAVING centro_de_costo and SALDO_SEMANA_ACTUAL  ORDER BY SALDO_SEMANA_ACTUAL desc LIMIT 10", (elemento,) )
				lista_Movimientos_CCostos=[]
				for row in Movimientos_CCostos:
					lista_Movimientos_CCostos.append(list(row))

				#Concicionante , si la cuenta usa cc > 0 , entonces muestra la tabla
				cantidad_Movimientos_CCostos = len(lista_Movimientos_CCostos)
#-------------------------------------------------------------------------------------------------------------------------
			# Tabla 5 resumen
				resumen= self.cur.execute("SELECT ANO_ANT.CUENTA, ANO_ANT.SALDO AS SALDO_ANO_ANTERIOR, MES_ANT.SALDO AS SALDO_MES_ANTERIOR, SEM_ANT.SALDO AS SALDO_SEMANA_ANTERIOR, SEM_ACT.SALDO AS SALDO_SEMANA_ACTUAL FROM (SELECT cuenta, SUM(DEBE-HABER) SALDO FROM MovimientosTabla WHERE fecha BETWEEN DATE('NOW', '-5 YEARS', 'START OF YEAR') AND DATE('NOW', '-1 YEAR') AND cuenta=? GROUP BY cuenta) ANO_ANT LEFT JOIN (SELECT cuenta, SUM(DEBE-HABER) SALDO FROM MovimientosTabla WHERE fecha BETWEEN DATE('NOW', '-5 YEARS', 'START OF YEAR') AND DATE('NOW', '-1 MONTHS') AND cuenta=? GROUP BY cuenta) MES_ANT ON mes_ant.cuenta = ano_ant.cuenta LEFT JOIN (SELECT cuenta, SUM(DEBE-HABER) SALDO FROM MovimientosTabla WHERE fecha BETWEEN DATE('NOW', '-5 YEARS', 'START OF YEAR') AND DATE('NOW', '-7 DAYS') AND cuenta=? GROUP BY cuenta ) SEM_ANT ON  sem_ant.cuenta= ano_ant.cuenta LEFT JOIN (SELECT cuenta, SUM(DEBE-HABER) SALDO FROM MovimientosTabla WHERE fecha BETWEEN DATE('NOW', '-5 YEARS', 'START OF YEAR') AND DATE('NOW') AND cuenta=? GROUP BY cuenta) SEM_ACT ON sem_act.cuenta= ano_ant.cuenta LIMIT 10", (elemento, elemento, elemento, elemento) )
				lista_resumen=[]
				for row in resumen:
					lista_resumen.append(list(row))
#-------------------------------------------------------------------------------------------------------------------------
			# Tabla 6 resumen
				resumen2= self.cur.execute("SELECT strftime('%Y', fecha) as YEAR, sum(case strftime('%m', fecha) when '01' then (DEBE-HABER) else 0 end) Ene, sum(case strftime('%m', fecha) when '02' then (DEBE-HABER) else 0 end) Feb, sum(case strftime('%m', fecha) when '03' then (DEBE-HABER) else 0 end) Mar, sum(case strftime('%m', fecha) when '04' then (DEBE-HABER) else 0 end) Abr,sum(case strftime('%m', fecha) when '05' then (DEBE-HABER) else 0 end) May,sum(case strftime('%m', fecha) when '06' then (DEBE-HABER) else 0 end) Jun, sum(case strftime('%m', fecha) when '07' then (DEBE-HABER)  else 0 end) Jul,sum(case strftime('%m', fecha) when '08' then (DEBE-HABER) else 0 end) Ago,sum(case strftime('%m', fecha) when '09' then (DEBE-HABER) else 0 end) Sep, sum(case strftime('%m', fecha) when '10' then (DEBE-HABER) else 0 end) Oct,sum(case strftime('%m', fecha) when '11' then (DEBE-HABER) else 0 end) Nov, sum(case strftime('%m', fecha) when '12' then (DEBE-HABER) else 0 end) Dic from  MovimientosTabla WHERE cuenta=? group by YEAR order by YEAR desc", (elemento,))

				lista_resumen2=[]
				for row in resumen2:
					lista_resumen2.append(list(row))
				print lista_resumen2

			# Grafico 2
				grafico2= self.cur.execute("SELECT lower(nombre) as NOMBRE,  sum (debe - haber) as SALDO_SEMANA_ACTUAL FROM MovimientosTabla INNER JOIN complemento ON MovimientosTabla.AUXILIAR = complemento.rut WHERE cuenta=? GROUP BY auxiliar HAVING auxiliar and SALDO_SEMANA_ACTUAL  ORDER BY SALDO_SEMANA_ACTUAL desc LIMIT 10", (elemento,) )
				lista_grafico2=[['Nombre', 'Miles de pesos'],]
				for row in grafico2:
					lista_grafico2.append(list(row))
				print "                                                                                                                                        "
				print lista_grafico2
				print "                                                                                                                                        "

				env1 = Environment(
				loader=PackageLoader('JefeContable', 'templates')
			    )
				templateX = env1.get_template('JefeContable_AnalisisCuenta.html')
				Html_file = open("output/JefeContable/AnalisisCuenta/"+str(elemento)+".html", "wb")
			  	Html_file.write(
				templateX.render(
				nombre_cuenta = elemento,
				nombre = elemento_nueva_lista_nomCuenta,
				cuenta = elemento_lista_numCuenta, 				
				elemento_lista_saldo_cuenta = (('{:,}'.format(elemento_lista_saldo_cuenta).replace(',','.'))),		
				texto = lista_grafico,
				Movimientos_Cuenta = lista_Movimientos_Cuenta,

				cantidad_Movimientos_Cuenta = cantidad_Movimientos_Cuenta,
				lista_Movimientos_Cuenta = lista_Movimientos_Cuenta,
				lista_Movimientos_Cuenta_2 = lista_Movimientos_Cuenta_2,

				lista_auxiliares = lista_auxiliares,
				lista_contra_naturaleza = lista_contra_naturaleza,

				cantidad_Movimientos_CCostos = cantidad_Movimientos_CCostos,
				lista_Movimientos_CCostos = lista_Movimientos_CCostos,
				resumen = lista_resumen,
				lista_resumen2=lista_resumen2,

				lista_grafico2=lista_grafico2,
			   	 )
			   	)

#-------------------------------------------------------------------------------------------------------------------------
	def pasivo(self):

		self.conn = sqlite3.connect('data.db')
		self.conn.text_factory = str
		self.cur= self.conn.cursor()

		registros=[]	
		variable= self.cur.execute('SELECT DISTINCT cuenta FROM MovimientosTabla ORDER BY cuenta ASC')
		for row in variable:
			registros.append(list(row))

		lista_registros = [x[0] for x in registros]
		# Nombre cuenta :
		for elemento in lista_registros:

		    if re.match	('^[2]', elemento):
				print "vengo de activo", elemento
				self.cur = self.conn.cursor()
#-------------------------------------------------------------------------------------------------------------------------
			#Nombre de cuenta
				nomCuenta= self.cur.execute("SELECT nombrecuenta FROM MovimientosTabla INNER JOIN ADO ON MovimientosTabla.CUENTA = ado.CUENTA2 WHERE cuenta=? GROUP BY cuenta HAVING cuenta", (elemento,) )

				lista_nomCuenta=[]
				for row in nomCuenta:
					lista_nomCuenta.append(list(row))
				
				nueva_lista_nomCuenta = [x[0] for x in lista_nomCuenta]

				for elemento_nueva_lista_nomCuenta in nueva_lista_nomCuenta:
					print elemento_nueva_lista_nomCuenta, "elemento_nueva_lista_nomCuenta"
#-------------------------------------------------------------------------------------------------------------------------
			#Numero de cuenta
				numCuenta= self.cur.execute("SELECT codcuenta FROM MovimientosTabla INNER JOIN ADO ON MovimientosTabla.CUENTA = ado.CUENTA2 WHERE  cuenta=? GROUP BY cuenta HAVING cuenta", (elemento,) )

				lista_numCuenta=[]
				for row in numCuenta:
					lista_numCuenta.append(list(row))
				
				nueva_lista_numCuenta = [x[0] for x in lista_numCuenta]

				for elemento_lista_numCuenta in nueva_lista_numCuenta:
					print elemento_lista_numCuenta, "elemento_lista_numCuenta"

#-------------------------------------------------------------------------------------------------------------------------
			# Saldo :
				saldo= self.cur.execute("SELECT	sum(haber-debe) as SALDO_SEMANA_ACTUAL FROM MovimientosTabla WHERE cuenta=? GROUP BY cuenta HAVING cuenta", (elemento,) )

				lista_saldo=[]
				for row in saldo:
					lista_saldo.append(list(row))
				
				lista_saldo_cuenta = [x[0] for x in lista_saldo]

				for elemento_lista_saldo_cuenta in lista_saldo_cuenta:
					print elemento_lista_saldo_cuenta, "elemento_lista_saldo_cuenta"
#-------------------------------------------------------------------------------------------------------------------------
			# Grafico
				grafico= self.cur.execute("SELECT fecha, SALDO*(-1) FROM MovimientosTabla WHERE fecha between '01-01-2013' AND DATE('NOW') AND cuenta=? ORDER BY fecha asc", (elemento,) )
				lista_grafico=[]				
				for row in grafico:
					lista_grafico.append(list(row))

				print lista_grafico
#-------------------------------------------------------------------------------------------------------------------------
			# Tabla 1
				Movimientos_Cuenta= self.cur.execute("SELECT lower(descripcion), lower(nombre) as NOMBRE, fecha, N_comprobante as VOUCHER, debe as CARGOS, haber as ABONOS FROM MovimientosTabla INNER JOIN complemento ON MovimientosTabla.AUXILIAR = complemento.rut WHERE cuenta=? GROUP BY fecha HAVING fecha between '01-01-2014' and date('now') ORDER BY fecha desc LIMIT 10", (elemento,) )
				lista_Movimientos_Cuenta=[]
				for row in Movimientos_Cuenta:
					lista_Movimientos_Cuenta.append(list(row))

				#Concicionante , si la cuenta usa rut > 0 , entonces muestra la tabla
				cantidad_Movimientos_Cuenta = len(lista_Movimientos_Cuenta)

				Movimientos_Cuenta_2= self.cur.execute("SELECT lower(descripcion), fecha, N_comprobante as VOUCHER, debe as CARGOS, haber as ABONOS FROM MovimientosTabla WHERE cuenta=? GROUP BY fecha HAVING fecha between '01-01-2013' and date('now') ORDER BY fecha desc LIMIT 10", (elemento,) )
				lista_Movimientos_Cuenta_2=[]
				for row in Movimientos_Cuenta_2:
					lista_Movimientos_Cuenta_2.append(list(row))
#-------------------------------------------------------------------------------------------------------------------------
			# Tabla 2
				auxiliares= self.cur.execute("SELECT auxiliar, lower(nombre) as NOMBRE,  sum (haber - debe) as SALDO_SEMANA_ACTUAL FROM MovimientosTabla INNER JOIN complemento ON MovimientosTabla.AUXILIAR = complemento.rut WHERE cuenta=? GROUP BY auxiliar HAVING auxiliar and SALDO_SEMANA_ACTUAL  ORDER BY SALDO_SEMANA_ACTUAL desc LIMIT 10", (elemento,) )
				lista_auxiliares=[]
				for row in auxiliares:
					lista_auxiliares.append(list(row))
#-------------------------------------------------------------------------------------------------------------------------
			# Tabla 3
				Saldo_contra_naturaleza= self.cur.execute("SELECT auxiliar, lower(nombre) as NOMBRE, sum (haber - debe) as SALDO_SEMANA_ACTUAL FROM MovimientosTabla INNER JOIN complemento ON MovimientosTabla.AUXILIAR = complemento.rut WHERE cuenta=? GROUP BY auxiliar HAVING auxiliar and SALDO_SEMANA_ACTUAL<0  ORDER BY SALDO_SEMANA_ACTUAL asc LIMIT 10", (elemento,) )
				lista_contra_naturaleza=[]
				for row in Saldo_contra_naturaleza:
					lista_contra_naturaleza.append(list(row))

				#Concicionante , si la cuenta tiene ruts en contra su naturaleza....
				cantidad_Movimientos_Cuenta = len(lista_contra_naturaleza)

				contra_naturaleza= self.cur.execute("SELECT auxiliar, lower(nombre) as NOMBRE, sum (haber - debe) as SALDO_SEMANA_ACTUAL FROM MovimientosTabla INNER JOIN complemento ON MovimientosTabla.AUXILIAR = complemento.rut WHERE cuenta=? GROUP BY auxiliar HAVING auxiliar and SALDO_SEMANA_ACTUAL<0  ORDER BY SALDO_SEMANA_ACTUAL asc LIMIT 10", (elemento,) )
				lista_contra_naturaleza=[]
				for row in contra_naturaleza:
					lista_contra_naturaleza.append(list(row))
#-------------------------------------------------------------------------------------------------------------------------
			# Tabla 4
				Movimientos_CCostos= self.cur.execute("SELECT centro_de_costo, lower(nombreccosto), sum (haber - debe) as SALDO_SEMANA_ACTUAL FROM MovimientosTabla INNER JOIN Ccostos ON MovimientosTabla.centro_de_costo = Ccostos.ccosto WHERE cuenta=? GROUP BY centro_de_costo HAVING centro_de_costo and SALDO_SEMANA_ACTUAL  ORDER BY SALDO_SEMANA_ACTUAL desc LIMIT 10", (elemento,) )
				lista_Movimientos_CCostos=[]
				for row in Movimientos_CCostos:
					lista_Movimientos_CCostos.append(list(row))

				#Concicionante , si la cuenta usa cc > 0 , entonces muestra la tabla
				cantidad_Movimientos_CCostos = len(lista_Movimientos_CCostos)
#-------------------------------------------------------------------------------------------------------------------------
			# Tabla 5 resumen
				resumen= self.cur.execute("SELECT ANO_ANT.CUENTA, ANO_ANT.SALDO AS SALDO_ANO_ANTERIOR, MES_ANT.SALDO AS SALDO_MES_ANTERIOR, SEM_ANT.SALDO AS SALDO_SEMANA_ANTERIOR, SEM_ACT.SALDO AS SALDO_SEMANA_ACTUAL FROM (SELECT cuenta, SUM(haber - debe) SALDO FROM MovimientosTabla WHERE fecha BETWEEN DATE('NOW', '-5 YEARS', 'START OF YEAR') AND DATE('NOW', '-1 YEAR') AND cuenta=? GROUP BY cuenta) ANO_ANT LEFT JOIN (SELECT cuenta, SUM(haber - debe) SALDO FROM MovimientosTabla WHERE fecha BETWEEN DATE('NOW', '-5 YEARS', 'START OF YEAR') AND DATE('NOW', '-1 MONTHS') AND cuenta=? GROUP BY cuenta) MES_ANT ON mes_ant.cuenta = ano_ant.cuenta LEFT JOIN (SELECT cuenta, SUM(haber - debe) SALDO FROM MovimientosTabla WHERE fecha BETWEEN DATE('NOW', '-5 YEARS', 'START OF YEAR') AND DATE('NOW', '-7 DAYS') AND cuenta=? GROUP BY cuenta ) SEM_ANT ON  sem_ant.cuenta= ano_ant.cuenta LEFT JOIN (SELECT cuenta, SUM(haber - debe) SALDO FROM MovimientosTabla WHERE fecha BETWEEN DATE('NOW', '-5 YEARS', 'START OF YEAR') AND DATE('NOW') AND cuenta=? GROUP BY cuenta) SEM_ACT ON sem_act.cuenta= ano_ant.cuenta LIMIT 10", (elemento, elemento, elemento, elemento) )
				lista_resumen=[]
				for row in resumen:
					lista_resumen.append(list(row))
#-------------------------------------------------------------------------------------------------------------------------
			# Tabla 6 resumen
				resumen2= self.cur.execute("SELECT strftime('%Y', fecha) as YEAR, sum(case strftime('%m', fecha) when '01' then (haber - debe) else 0 end) Ene, sum(case strftime('%m', fecha) when '02' then (haber - debe) else 0 end) Feb, sum(case strftime('%m', fecha) when '03' then (haber - debe) else 0 end) Mar, sum(case strftime('%m', fecha) when '04' then (haber - debe) else 0 end) Abr,sum(case strftime('%m', fecha) when '05' then (haber - debe) else 0 end) May,sum(case strftime('%m', fecha) when '06' then (haber - debe) else 0 end) Jun, sum(case strftime('%m', fecha) when '07' then (haber - debe)  else 0 end) Jul,sum(case strftime('%m', fecha) when '08' then (haber - debe) else 0 end) Ago,sum(case strftime('%m', fecha) when '09' then (haber - debe) else 0 end) Sep, sum(case strftime('%m', fecha) when '10' then (haber - debe) else 0 end) Oct,sum(case strftime('%m', fecha) when '11' then (haber - debe) else 0 end) Nov, sum(case strftime('%m', fecha) when '12' then (haber - debe) else 0 end) Dic from  MovimientosTabla WHERE cuenta=? group by YEAR order by YEAR desc", (elemento,))

				lista_resumen2=[]
				for row in resumen2:
					lista_resumen2.append(list(row))
				print lista_resumen2


				env1 = Environment(
				loader=PackageLoader('JefeContable', 'templates')
			    )
				templateX = env1.get_template('JefeContable_AnalisisCuenta.html')
				Html_file = open("output/JefeContable/AnalisisCuenta/"+str(elemento)+".html", "wb")
			  	Html_file.write(
				templateX.render(
				nombre_cuenta = elemento,
				nombre = elemento_nueva_lista_nomCuenta,
				cuenta = elemento_lista_numCuenta, 				
				elemento_lista_saldo_cuenta = (('{:,}'.format(elemento_lista_saldo_cuenta).replace(',','.'))),		
				texto = lista_grafico,
				Movimientos_Cuenta = lista_Movimientos_Cuenta,

				cantidad_Movimientos_Cuenta = cantidad_Movimientos_Cuenta,
				lista_Movimientos_Cuenta = lista_Movimientos_Cuenta,
				lista_Movimientos_Cuenta_2 = lista_Movimientos_Cuenta_2,

				lista_auxiliares = lista_auxiliares,
				lista_contra_naturaleza = lista_contra_naturaleza,

				cantidad_Movimientos_CCostos = cantidad_Movimientos_CCostos,
				lista_Movimientos_CCostos = lista_Movimientos_CCostos,
				resumen = lista_resumen,
				lista_resumen2=lista_resumen2,
			   	 )
			   	)
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

	def auxiliares(self):
#-------------------------------------------------------------------------------------------------------------------------
		self.conn = sqlite3.connect('data.db')
		self.conn.text_factory = str
		self.cur= self.conn.cursor()


		variable= self.cur.execute('SELECT DISTINCT auxiliar FROM MovimientosTabla ORDER BY auxiliar ASC')
		registros=[]			
		for row in variable:
			registros.append(list(row))

		lista_registros = [x[0] for x in registros]
		# Nombre cuenta :
		for elemento in lista_registros:

		    if re.match	('^[A-Za-z0-9_.]', elemento):
				print "vengo de activo", elemento
				self.cur = self.conn.cursor()
#-------------------------------------------------------------------------------------------------------------------------
			# Nombre :
				nomAux= self.cur.execute("SELECT nombre FROM MovimientosTabla INNER JOIN COMPLEMENTO ON MovimientosTabla.auxiliar = COMPLEMENTO.RUT WHERE auxiliar=? ", (elemento,) )
				lista_nomAux=[]
				for row in nomAux:
					lista_nomAux.append(list(row))
				
				nueva_lista_nomAux = [x[0] for x in lista_nomAux]

				for elemento_nueva_lista_nomAux in nueva_lista_nomAux:
					print elemento_nueva_lista_nomAux, "elemento_nueva_lista_nomCuenta"
#-------------------------------------------------------------------------------------------------------------------------
			# Saldo :
				saldo= self.cur.execute("SELECT	sum(debe - haber) as SALDO_SEMANA_ACTUAL FROM MovimientosTabla WHERE auxiliar=? GROUP BY auxiliar HAVING auxiliar", (elemento,) )
				lista_saldo=[]
				for row in saldo:
					lista_saldo.append(list(row))
					
				lista_saldo_cuenta = [x[0] for x in lista_saldo]

				for elemento_lista_saldo_cuenta in lista_saldo_cuenta:
					print elemento_lista_saldo_cuenta, "elemento_lista_saldo_cuenta"


				env1 = Environment(
				loader=PackageLoader('JefeContable', 'templates')
			    )
				templateX = env1.get_template('JefeContable_Auxiliares.html')
				Html_file = open("output/JefeContable/Auxiliares/"+str(elemento)+".html", "wb")
			  	Html_file.write(
				templateX.render(
				numero = elemento,
				nombre = elemento_nueva_lista_nomAux,
				saldo = (('{:,}'.format(elemento_lista_saldo_cuenta).replace(',','.'))),
			   	 )
			   	)


