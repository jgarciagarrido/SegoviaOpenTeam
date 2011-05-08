# -*- coding: utf-8 -*.
from django.db import models

# Create your models here.
class Vestuario():
    hombres={ 'abrigo': "hombre_abrigo.png",
                  'manga larga': "hombre_larga.png",
                  'manga corta': "hombre_corta.png",
                  'bañador': "hombre_bañador.png"
                 }
    mujeres={ 'abrigo': "mujer_abrigo.png",
                  'manga larga': "mujer_larga.png",
                  'manga corta': "mujer_corta.png",
                  'bañador': "mujer_bañador.png"
                 }
    def recomendar(self, temperatura):
        if temperatura > 10 and temperatura<=20:
            return "manga larga"
        elif temperatura > 20 and temperatura<=30:
            return "manga corta"
        elif temperatura > 30: 
            return "bañador"
        return "abrigo";
    
    def img_hombres(self, vestido):
        return self.hombres[vestido]
    
    def img_mujeres(self, vestido):
        return self.mujeres[vestido]