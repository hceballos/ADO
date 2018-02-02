import sqlite3
import json
import re
from jinja2 import Environment, FileSystemLoader


class General:
    def __init__(self, reportes_json_path, cuentas_sql_path ):
        self.read_reportes_json(reportes_json_path)
        self.sql_connect("data.db")
        self.read_Cuentas(cuentas_sql_path)

    #Abro y leo el Json, almaceno en 'reportes'
    def read_reportes_json(self, reportes_json_path):
        with open(reportes_json_path) as reportes_json:
            self.reportes = json.load(reportes_json)


    def sql_connect(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.text_factory = str
        self.cur = self.conn.cursor()
        # "coneccion con base de datos"

    def read_Cuentas(self, cuentas_sql_path):
        with open(cuentas_sql_path) as sql_file:
            sql_query = sql_file.read()

            registros=[]
            variable = self.cur.execute(sql_query)
            for row in variable:
                registros.append(list(row))

            self.cuentas = [x[0] for x in registros]

    def init(self):
        #meter en data la informacion lista para el render
        for cuenta in self.cuentas:
            render_data = []
            for reporte in self.reportes:
                render_data.append(
                    self._generar_render_data(reporte, cuenta)
                )

            self.render(render_data, cuenta)
            #print render_data


    def _generar_render_data(self, reporte, cuenta):
        tipo = reporte['tipo']
        if tipo == 'tabla':
            return self._generar_render_data_for_tabla(reporte, cuenta)
        if tipo == 'grafico':
            return self._generar_render_data_for_grafico(reporte, cuenta)

    def _generar_render_data_for_grafico(self, reporte, cuenta):
        return {
            "type": reporte["tipo"],
            "title": reporte["nombre"],
            "graph_data": {
                "haxis": reporte["haxis"],
                "vaxis": reporte["vaxis"],
                "labels" : self.obtener_labels_del_grafico(reporte, cuenta),
                "lines" : self.objener_lineas_del_grafico(reporte, cuenta)
            }
        }

    def obtener_labels_del_grafico(self, reporte, cuenta):
        sql_name_a_ejecutar = self._obtener_consulta_segun_cuenta(cuenta)
        if len(reporte['lineas']) == 0:
            return None

        linea = reporte['lineas'][0]
        return self.ejecutar_consulta_labels(linea['sql_file_path'][sql_name_a_ejecutar], cuenta)

    def ejecutar_consulta_labels(self, sql_file_path, cuenta):
        with open(sql_file_path) as sql_file:
            sql_query = sql_file.read()

            cursor = self.cur.execute(sql_query, (cuenta,))
            result_list = cursor.fetchall()
            return [i[0] for i in cursor.description[1:]]

    def objener_lineas_del_grafico(self, reporte, cuenta):
        sql_name_a_ejecutar = self._obtener_consulta_segun_cuenta(cuenta)
        lineas = []
        for linea in reporte['lineas']:
            lineas.append({
                    "name" : self.obtener_name(linea['nombre']),
                    "data" : self.ejecutar_consulta_lines(linea['sql_file_path'][sql_name_a_ejecutar], cuenta)
                })
        return lineas

    def obtener_name(self, linea_nombre):
        nombre=[]
        nombre.append(linea_nombre)

        name= ''.join(nombre)
        return name

    def ejecutar_consulta_lines(self, sql_file_path, cuenta):
        with open(sql_file_path) as sql_file:
            sql_query = sql_file.read()

            cursor = self.cur.execute(sql_query, (cuenta,))
            result_list = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]
            data= [list(i) for i in result_list]
            return self.eldata(data)

    def eldata(self, data):
            for elemento in data:
                return elemento[1:]


    def _generar_render_data_for_tabla(self, reporte, cuenta):
        sql_name_a_ejecutar = self._obtener_consulta_segun_cuenta(cuenta)
        return {
            "type": reporte["tipo"],
            "title": reporte["nombre"],
            "table_data": self.ejecutar_consulta_desde_archivo(reporte['sql_file_path'][sql_name_a_ejecutar], cuenta)
        }

    def _obtener_consulta_segun_cuenta(self, cuenta):
        if re.match('^\s*1', cuenta):
            return "activo"
        if re.match('^\s*2', cuenta):
            return "pasivo"
        if re.match('^\s*3', cuenta):
            return "patrimonio"
        if re.match('^\s*4', cuenta):
            return "ingresos"
        if re.match('^\s*5', cuenta):
            return "egresos"
        if re.match('^\s*6', cuenta):
            return "impuestos"
        if re.match('^\s*7', cuenta):
            return "derechos"
        if re.match('^\s*8', cuenta):
            return "responsabilidad"
        if re.match('^\s*9', cuenta):
            return "orden"
        raise Exception("Tipo de cuenta no encontrado: {}".format(cuenta))

    def ejecutar_consulta_desde_archivo(self, sql_file_path, cuenta):
        with open(sql_file_path) as sql_file:
            sql_query = sql_file.read()

            cursor = self.cur.execute(sql_query, (cuenta,))
            result_list = cursor.fetchall()

            result = []
            for tupla in result_list:
                t = []
                for valor in tupla:
                    t.append(self._agregar_puntos_decimales_si_es_que_es_un_numero(valor))
                result.append(t)

            column_names = [i[0] for i in cursor.description]
            return [column_names] + result

    def _agregar_puntos_decimales_si_es_que_es_un_numero(self, valor):
        if isinstance(valor, int):
            return ('{:,}'.format(int(valor)).replace(',','.'))
        return valor

#-----------INICIO render-----------------------
    def render(self, render_data, cuenta):
        #hacer el render

        env = Environment(
        loader=FileSystemLoader('templates')

        )
        template = env.get_template('JefeContable.html')
        Html_file = open("output/JefeContable/AnalisisCuenta/"+str(cuenta)+".html", "wb")
        Html_file.write(
        template.render(
            data = render_data
         )
        )
#-----------FIN render-----------------------

#---------------------------------------------------------------
if __name__ == '__main__':
    reportes_json_path = 'input/JefeContable.json'
    cuentas_sql_path   = 'sql/Cuentas.sql'

    general = General(reportes_json_path, cuentas_sql_path)
    general.init()