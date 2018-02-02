#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import os
import csv
import re


class ERP2016Parser():

    DELIMITER_INPUT = '\t'
    DELIMITER_OUTPUT = '\t'

    def setInputFileName(self, inputFileName):
        self.inputFileName = inputFileName

    def setOutputFileName(self, outputFileName):
        self.outputFileName = outputFileName

    def generate(self):
        #create output folder if not exist
        if not os.path.exists(os.path.dirname(self.outputFileName)):
            try:
                os.makedirs(os.path.dirname(self.outputFileName))
            except OSError as e: # Guard against race condition
                if e.errno != errno.EEXIST:
                    raise

        print 'Processing: {}'.format(self.inputFileName)

        csvReader = csv.reader(codecs.open(self.inputFileName, 'rU' ,encoding='utf-8', errors='ignore'), delimiter = self.DELIMITER_INPUT)
        csvWriter = csv.writer(codecs.open(self.outputFileName, 'w+',encoding='utf-8', errors='ignore'), delimiter = self.DELIMITER_OUTPUT)

        #remove first 11 rows that contains useless information
        for n in range(11):
            csvReader.next()
        print "Remover primeras 11 lineas que contienen informacion innecesaria"

        for row in csvReader:
            if self._isRowUseful(row):
                #strip out spaces
                row = self._stripColumns(row)
                #normalize date
                row[1] = self._normalizeDate(row[1])

                row[0] = self._normalizeSlash(row[0])
                #save to file

                # inicio obtener numero de factura
                vacio=' '
                descripcion= row[8]+vacio+row[9]+vacio+row[14]
                row.append('***ERROR***')
                try:
                    regex= re.compile(r'(FC|Fact#|FACT#|Fact|FACT|FC-|FC/|F-|F/)\s*(\d+)')
                    x= regex.search(descripcion).group(2)
                    row[len(row)-1] = int(x)
                except AttributeError as e:
                    row[len(row)-1] = ''
                # fin obtener numero de factura


                csvWriter.writerow(row)
        print "Primera Columna, '_isRowUseful' remover lineas que empiezan con 'SALDO ANTERIOR'"

    def _isRowUseful(self, row):
        firstColumn = row[0]

        emptyRegexp = re.compile('^\s*$|^SALDO')
        if emptyRegexp.match(firstColumn):
            return False

        return True

    def _stripColumns(self, row):
        return [column.strip() for column in row]

    def _normalizeDate(self, dateString):
        return re.sub('(\d{2}).(\d{2}).(\d{2})?(\d{2})', '20\g<4>-\g<2>-\g<1>', dateString)

    def _normalizeSlash(self, dateSLash):
        return re.sub("/", "-", dateSLash)