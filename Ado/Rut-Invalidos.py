import sqlite3
import json
import re
from jinja2 import Environment, FileSystemLoader


class General:
    def __init__(self, reportes_json_path, ruts_sql_path ):
        self.read_reportes_json(reportes_json_path)
        self.sql_connect("data.db")
        self.read_ruts(ruts_sql_path)

    #Abro y leo el Json, almaceno en 'reportes'
    def read_reportes_json(self, reportes_json_path):
        with open(reportes_json_path) as reportes_json:
            self.reportes = json.load(reportes_json)

    def sql_connect(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.text_factory = str
        self.cur = self.conn.cursor()
        # "coneccion con base de datos"

    def read_ruts(self, ruts_sql_path):
        with open(ruts_sql_path) as sql_file:
            sql_query = sql_file.read()

            registros=[]
            variable = self.cur.execute(sql_query)
            for row in variable:
                registros.append(list(row))

            self.ruts = [x[0] for x in registros]

#-------------------------------------------------
    def init(self):

        render_data = []
        for rut in self.ruts:
            render_data.append(
                self.valida(rut)
            )

        self.No_validos=[]
        for evaluacion in render_data:
            tipo =  evaluacion[0]
            if tipo == 'Invalido':
                self.No_validos.append(evaluacion[1])

#-------------------------------------------------
    def filtra(self, rut):
        caracteres = "1234567890k"
        rutx = ""
        for cambio in rut.lower():
            if cambio in caracteres:
                rutx += cambio
        return rutx

    def valida(self, rut):
        rfiltro = self.filtra(rut)
        rutx = str(rfiltro[0:len(rfiltro)-1])
        digito = str(rfiltro[-1])
        multiplo = 2
        total = 0
        for reverso in reversed(rutx):
            total += int(reverso) * multiplo
            if multiplo == 7:
                multiplo = 2
            else:
                multiplo += 1
            modulus = total % 11
            verificador = 11 - modulus
            if verificador == 10:
                div = "k"
            elif verificador == 11:
                div = "0"
            else:
                if verificador < 10:
                    div = verificador

        if str(div) == str(digito):
            retorno = ["Valido", rut]
        else:
            retorno = ["Invalido", rut]
        return retorno

#-------------------------------------------------

    def init2(self):
        render = []
        for rut in self.No_validos:
            for reporte in self.reportes:
                render.append(
                    self._generar_render_data(reporte, rut)
                )

        self.render(render)



    def _generar_render_data(self, reporte, rut):
        tipo = reporte['tipo']
        if tipo == 'tabla':
            return self._generar_render_data_for_tabla(reporte, rut)

    def _generar_render_data_for_tabla(self, reporte, rut):
        return {
            "type": reporte["tipo"],
            "title": reporte["nombre"],
            "table_data": self.ejecutar_consulta_desde_archivo(reporte['sql_file_path'], rut)
        }

    def ejecutar_consulta_desde_archivo(self, sql_file_path, rut):
        with open(sql_file_path) as sql_file:
            sql_query = sql_file.read()

            cursor = self.cur.execute(sql_query, (rut,))
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


#-------------------------------------------------
    def render(self, render):
        #hacer el render
        env1 = Environment(
            loader=FileSystemLoader('templates')
        )
        template = env1.get_template('Rut-Invalidos.html')
        html_file = open("output/GerenteFinanzas/Rut-Invalidos.html", "wb")
        html_file.write(
            template.render(
                data = render
            )
        )


if __name__ == '__main__':
    reportes_json_path = 'input/Rut-Invalidos.json'
    ruts_sql_path   = 'sql/ruts.sql'


    general = General(reportes_json_path, ruts_sql_path)
    general.init()
    general.init2()