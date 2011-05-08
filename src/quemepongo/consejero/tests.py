# -*- coding: utf-8 -*.
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Vestuario

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
    
    
    
    
    
