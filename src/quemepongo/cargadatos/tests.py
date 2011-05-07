"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils import unittest
from ftplib import FTP
from models import DescargadorFichero
import os.path
import os
import glob

class ConjuntoPruebasDescargaArchivo(unittest.TestCase):
    
    def setUp(self):
        
        fileList = glob.glob('./??????????0000_sfc_fc??')
        for fileName in fileList:
            os.remove(fileName)
        
        self.url = "ftpdatos.aemet.es"
        self.path = "/modelos_numericos/hirlam016/"
        self.localPath = "."
        
    def tearDown(self):
        fileList = glob.glob(self.localPath + '/??????????0000_sfc_fc??')
        for fileName in fileList:
            os.remove(fileName)
    
    def testPruebaConexion(self):
        try:
            ftp = FTP(self.url)
            ftp.login()
            ftp.quit()
        except:
            self.fail("No se ha podido conectar a " + self.url)
            
    def testDescargaArchivo(self):
        
        fileName = '20110507000000_sfc_fc03'
        descargador = DescargadorFichero(self.url)
        descargador.ObtenerFichero(self.path + "/00", fileName, ".")
        localFilePath = self.localPath + "/" + fileName
        self.assertTrue(os.path.exists(localFilePath) and os.path.isfile(localFilePath), 'No existe el fichero ' + localFilePath)
        
        
    def testDescargarPrevision(self):
        
        descargador = DescargadorFichero(self.url)
        descargador.ObtenerFicherosPrevisiones(self.path, '00', self.localPath)
        
        fileList = glob.glob(self.localPath + '/??????????0000_sfc_fc??')
        
        self.assertTrue(len(fileList) == 10, "Faltan archivos")
        
        
        
