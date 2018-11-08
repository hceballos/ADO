#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import sqlite3
from xlsxwriter.utility import xl_rowcol_to_cell
import pandas as pd

cnx = sqlite3.connect('data.db')

consulta  = "SELECT CUENTA, FECHA, TIPO, NOMBRECCOSTO, DEBE, HABER FROM MovimientosTabla INNER JOIN Ccostos ON MovimientosTabla.CENTRO_DE_COSTO = Ccostos.CCOSTO  WHERE cuenta like '1-01-02-002%' and fecha between date('NOW', 'START OF YEAR') and date('NOW') ORDER BY TIPO DESC "
datos = pd.read_sql_query(consulta, cnx)

datos['SALDO'] = datos['DEBE'] - datos['HABER']

consulta2 = "SELECT CUENTA,  FECHA,  TIPO,  CENTRO_DE_COSTO as NOMBRECCOSTO, sum (debe-haber) as SALDO FROM MovimientosTabla WHERE fecha between '2013-01-01' and '2017-12-31' and cuenta like '1-01-02-002%' ORDER BY TIPO DESC  "
datos2 = pd.read_sql_query(consulta2, cnx)

datos2['FECHA'] = '2018-01-01'
datos2['TIPO'] = "SI"
datos2['NOMBRECCOSTO'] = "SALDO INICIAL"
datos2['DEBE'] = 0
datos2['HABER'] = 0

frames = datos2.append(datos)

df = pd.DataFrame(frames)

df['FECHA'] = pd.DatetimeIndex(df['FECHA']).month


df = pd.pivot_table(df,
                    index = ["CUENTA", "TIPO", "NOMBRECCOSTO"],
                    values = ["SALDO"],
                    columns = ["FECHA"],
                    aggfunc = [np.sum],
                    fill_value = 0,
                    margins = True
                    )

columns = {'sum': 'Costos / Ingresos Relacionados al Banco', 'SALDO': 'Saldo Mensual', 1: 'Ene', 2: 'Feb', 3: 'Mar',4: 'Abr', 5: 'May', 6: 'Jun',7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov',12: 'Dic', 'All': 'Acumulado'}
index = {'All': ' Total'}

x = df.rename(columns=columns, index=index)
x.style.format("{:,.0f}")

writer = pd.ExcelWriter('Fuentes y uso de fondos.xlsx', engine='xlsxwriter')
x.to_excel(writer, sheet_name='Pandas')
writer.save()