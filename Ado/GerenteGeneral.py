import sqlite3
import json
from jinja2 import Environment, FileSystemLoader


class General:
    def __init__(self, reportes_json_path):
        self.read_reportes_json(reportes_json_path)
        self.sql_connect("data.db")

    #Abro y leo el Json, almaceno en 'reportes'
    def read_reportes_json(self, reportes_json_path):
        with open(reportes_json_path) as reportes_json:
            self.reportes = json.load(reportes_json)

    def sql_connect(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.text_factory = str
        self.cur = self.conn.cursor()
        # "coneccion con base de datos"

    def init(self):
        #meter en data la informacion lista para el render
        render_data = []
        for reporte in self.reportes:
            render_data.append(
                self._generar_render_data(reporte)
            )

        self.render(render_data)


    def _generar_render_data(self, reporte):
        tipo = reporte['tipo']
        if tipo == 'tabla':
            return self._generar_render_data_for_tabla(reporte)
        if tipo == 'grafico':
            return self._generar_render_data_for_grafico(reporte)
        if tipo == 'gauge':
            return self._generar_render_data_for_gauge(reporte)

    def _generar_render_data_for_gauge(self, reporte):
        return {
            "type": reporte["tipo"],
            "title": reporte["nombre"],
            "table_data": self.ejecutar_consulta_desde_archivo_gauge(reporte['sql_file_path']),
            # json.dumps() para sacar el unicode u'string'
            "options": json.dumps(reporte['options'])
        }

    def ejecutar_consulta_desde_archivo_gauge(self, sql_file_path):
        with open(sql_file_path) as sql_file:
            sql_query = sql_file.read()

            cursor = self.cur.execute(sql_query)
            result_list = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]
            data= [list(i) for i in result_list]
            return column_names + list(i)

    def _generar_render_data_for_tabla(self, reporte):
        return {
            "type": reporte["tipo"],
            "title": reporte["nombre"],
            "table_data": self.ejecutar_consulta_desde_archivo(reporte['sql_file_path'])
        }

    def ejecutar_consulta_desde_archivo(self, sql_file_path):
        with open(sql_file_path) as sql_file:
            sql_query = sql_file.read()

            cursor = self.cur.execute(sql_query)
            result_list = cursor.fetchall()
            result = []
            for tupla in result_list:
                t = []
                for numero in tupla:
                    f = ('{:,}'.format(int(numero)).replace(',','.'))
                    t.append(f)
                result.append(t)

            column_names = [i[0] for i in cursor.description]
            return [column_names] + result

    def _generar_render_data_for_grafico(self, reporte):
        return {
            "type": reporte["tipo"],
            "title": reporte["nombre"],
            "graph_data": {
                "haxis": reporte["haxis"],
                "vaxis": reporte["vaxis"],
                "labels" : self.obtener_labels_del_grafico(reporte),
                "lines" : self.objener_lineas_del_grafico(reporte)
            }
        }

    def objener_lineas_del_grafico(self, reporte):
        lineas = []
        for linea in reporte['lineas']:
            lineas.append({
                    "name" : self.obtener_name(linea['nombre']),
                    "data" : self.ejecutar_consulta_lines(linea['sql_file_path'])
                })
        return lineas

    def obtener_labels_del_grafico(self, reporte):
        if len(reporte['lineas']) == 0:
            return None

        linea = reporte['lineas'][0]
        return self.ejecutar_consulta_labels(linea['sql_file_path'])

    def ejecutar_consulta_labels(self, sql_file_path):
        with open(sql_file_path) as sql_file:
            sql_query = sql_file.read()

            cursor = self.cur.execute(sql_query)
            result_list = cursor.fetchall()
            return [i[0] for i in cursor.description[1:]]


    def obtener_name(self, linea_nombre):
        nombre=[]
        nombre.append(linea_nombre)

        name= ''.join(nombre)
        return name

    def ejecutar_consulta_lines(self, sql_file_path):
        with open(sql_file_path) as sql_file:
            sql_query = sql_file.read()

            cursor = self.cur.execute(sql_query)
            result_list = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]
            data= [list(i) for i in result_list]
            return self.eldata(data)

    def eldata(self, data):
            for elemento in data:
                return elemento[1:]

    def render(self, render_data):
        #hacer el render
        env1 = Environment(
            loader=FileSystemLoader('templates')
        )
        template = env1.get_template('GerenteGeneral.html')
        html_file = open("output/GerenteGeneral/Gerencia.html", "wb")
        html_file.write(
            template.render(
                data = render_data
            )
        )

#---------------------------------------------------------------
if __name__ == '__main__':
    general = General('input/GerenteGeneral.json')
    general.init()
    #general.render_test()