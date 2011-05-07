"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils import unittest
from ftplib import FTP
from models import DescargadorFichero
from quemepongo.cargadatos.models import ManejadorFichero
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
        

class PruebaLecturaArchivo(unittest.TestCase):
    
    ruta = '/tmp/fichero'
    def setUp(self):
        self.Archivo = ManejadorFichero(self.ruta)

    def test_comprobar_instancia(self):
        self.assertIsInstance(self.Archivo, ManejadorFichero)
    
    def test_comprobar_ruta(self):
        self.assertEqual(self.Archivo.ruta, self.ruta)
    
    def test_abrir_fichero(self):
        self.Archivo.abrir()
        self.assertIsNotNone(self.Archivo.fichero)
    
    def test_comprobar_temperatura(self):
        self.Archivo.abrir()
        temperatura_posicion = self.Archivo.leer_temperatura( 0, 0)
        self.assertIsNotNone(temperatura_posicion['temperatura'])
        self.assertAlmostEqual(temperatura_posicion['temperatura'], 300.626235962)
    
    def test_comprobar_precipitacion(self):
        self.Archivo.abrir()
        precipitacion_posicion = self.Archivo.leer_precipitacion( 0, 0)
        self.assertIsNotNone(precipitacion_posicion['precipitacion'])
        self.assertAlmostEqual(precipitacion_posicion['precpitacion'], 300.626235962)
        