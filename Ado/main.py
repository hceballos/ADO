import shutil
from lib.CSVReader import CSVReader
from lib.MovementsDB import MovementsDB
from lib.ManufacturerYearQuery import ManufacturerYearQuery
from lib.InputProcessor import InputProcessor
from lib.Answer import Answer
from lib.InputCCostos import InputCCostos
from lib.InputAdo import InputAdo
from lib.InputComplemento import InputComplemento
from lib.JefeContable import JefeContable

if __name__ == '__main__':
    FILE_DB = 'data.db'
    FOLDER_INPUT = 'input/input_Mayores/'
    FOLDER_CSV = 'csv/'
    FILE_QUERY='sql/TodasLasCuentas.txt'

    FOLDER_INPUT_CCOSTOS = 'input_Ccostos/'

    DISTINCT_CUENTA='sql/DistinctCuenta.txt'
    SALDO='sql/Saldo.txt'

    #eliminar la carpeta de salida csv
    shutil.rmtree('csv')



    #process the input files, remove uneeded data,
    #and generate ready to read CSV files of each input
    inputProcessor = InputProcessor()
    inputProcessor.setInputFolder(FOLDER_INPUT)
    inputProcessor.setCSVFolder(FOLDER_CSV)
    inputProcessor.process()

    #read the generated CSV files
    reader = CSVReader(FOLDER_CSV)

    #take the data from the CSV files and create a
    #database with the data
    db = MovementsDB(FILE_DB)
    db.saveRegisters(reader.registers)


    InputCCostos = InputCCostos(FILE_DB)
    InputAdo = InputAdo(FILE_DB)
    InputComplemento = InputComplemento(FILE_DB)
    #read sql file and make a SQL query against
    #the database and print the output
    #TODO

    #JefeContable= JefeContable()
    #JefeContable.activo()

    #NOTA: se pueden eliminar las carpetas:
        # csv
        # Resultado/index.html
        # data.db

