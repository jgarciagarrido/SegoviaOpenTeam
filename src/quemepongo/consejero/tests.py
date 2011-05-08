# -*- coding: utf-8 -*.
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Vestuario, Localidad

#class SimpleTest(TestCase):
#    def test_basic_addition(self):
#        """
#        Tests that 1 + 1 always equals 2.
#        """
#        self.assertEqual(1 + 1, 2)

class VestuarioTest(TestCase):
    def setUp(self):
        self.vestuario = Vestuario()
        
    def test_abrigo(self):
        
        temperatura = 0
        resultado = self.vestuario.recomendar(temperatura)
        
        self.assertEquals(resultado, "abrigo")
    def test_temperaturasAbrigo(self):
        temperaturas = range (-20,10)
        for temperatura in temperaturas:
            resultado = self.vestuario.recomendar(temperatura)
            self.assertEquals(resultado, "abrigo")
    
    def test_mangaLarga(self):
        temperatura = 15
        vestuario = Vestuario()

        resultado = vestuario.recomendar(temperatura)
        
        self.assertEquals(resultado, "manga larga")
        
    def test_temperaturasMangaLarga(self):
        temperaturas = range (11,20)
        for temperatura in temperaturas:
            resultado = self.vestuario.recomendar(temperatura)
            self.assertEquals(resultado, "manga larga")
    
    def test_temperaturasMangaCorta(self):
        temperaturas = range (21,30)
        for temperatura in temperaturas:
            resultado = self.vestuario.recomendar(temperatura)
            self.assertEquals(resultado, "manga corta")
    
    def test_temperaturasBanyador(self):
        temperaturas = range (31,50)
        for temperatura in temperaturas:
            resultado = self.vestuario.recomendar(temperatura)
            self.assertEquals(resultado, "bañador")
        
class TestLocalidades(TestCase):
    def setUp(self):
        Localidad.objects.create(nombre="Segovia", latitud=10, longitud=20)
        TestLocalidades
        self.localidad = Localidad()
        
    def test_buscarLocalidad(self):    
        resultado = self.localidad.buscar("Segovia")
        self.assertEquals(len(resultado),1)
        self.assertEqual(resultado[0].nombre, "Segovia")
    
    def test_buscarLocalidadInexistente(self):
        resultado = self.localidad.buscar("Whasinton")
        self.assertEquals(len(resultado),0) 
        
    def test_obtenerCoordenadasRegistradas(self):
        resultado = self.localidad.obtener_coordenadas_registradas("Segovia");
        self.assertAlmostEqual(resultado['latitud'], 10)
        self.assertAlmostEqual(resultado['longitud'], 20)
    
    def test_obtenerCoordenadasInternet(self):
        resultado = self.localidad.obtener_coordenadas_web("Palazuelos de Eresma")
        self.assertAlmostEqual(resultado['latitud'], 40.924187714)
        self.assertAlmostEqual(resultado['longitud'], -4.013027219766)
    
    def test_obtenerCoordenadas(self):
        resultado = self.localidad.obtener_coordenadas("Segovia");
        self.assertAlmostEqual(resultado['latitud'], 10)
        self.assertAlmostEqual(resultado['longitud'], 20)
        resultado = self.localidad.obtener_coordenadas("San Cristobal de Segovia")
        self.assertAlmostEqual(resultado['latitud'], 40.95314378724)
        self.assertAlmostEqual(resultado['longitud'], -4.076507924923)
    
    def test_obtenerCoordenadasYGuardar(self):
        resultado = self.localidad.obtener_coordenadas("Zamarramala")
        self.assertAlmostEqual(resultado['latitud'], 40.9667290000)
        self.assertAlmostEqual(resultado['longitud'], -4.133350499999)
        resultado = self.localidad.obtener_coordenadas_registradas("Zamarramala");
        self.assertAlmostEqual(resultado['latitud'], 40.9667290000)
        self.assertAlmostEqual(resultado['longitud'], -4.133350499999)
    
    def test_NoExisteLocalidad(self):
        resultado = self.localidad.obtener_coordenadas("Entropía humanística")
        self.assertEquals(len(resultado), 0)
        
        
        
    
    
    
    
    
