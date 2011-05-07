"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils import unittest
from quemepongo.cargadatos.models import ManejadorFichero


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
        
        