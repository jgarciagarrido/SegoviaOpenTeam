# -*- coding: utf-8 -*.
from django.db import models
import urllib
import urllib2
import json

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
    
class Localidad(models.Model):
    nombre = models.CharField(max_length=100)
    latitud = models.FloatField(null=True)
    longitud = models.FloatField(null=True)
    def buscar(self, nombre):
        return Localidad.objects.filter(nombre=nombre)
    def obtener_coordenadas_registradas(self,nombre):
        registros = self.buscar(nombre)
        return {'latitud': registros[0].latitud,
                'longitud': registros[0].longitud}
        
    def obtener_coordenadas_web(self, nombre):
        nombre_formateado = nombre.replace(' ', '+')
        url_original = "http://open.mapquestapi.com/nominatim/v1/search?q=" + nombre_formateado + "&format=json&limit=1"
        url = urllib.quote(url_original, safe="%/:=&?~#+!$,;'@()*[]")
        respuesta = urllib2.urlopen(url)
        contenido = respuesta.read()
        datos = json.loads(contenido)
        if len(datos)>0:
            latitud = float(datos[0]['lat'])
            longitud = float(datos[0]['lon'])
            return {'latitud': latitud,
                    'longitud': longitud}
        else:
            return {}
    
    def obtener_coordenadas(self, nombre):
        registros = self.buscar(nombre)
        if len(registros) > 0:
            coordenadas = self.obtener_coordenadas_registradas(nombre)
        else:
            coordenadas = self.obtener_coordenadas_web(nombre)
            if len(coordenadas)>0:
                localidad = Localidad()
                localidad.nombre = nombre
                localidad.latitud = coordenadas['latitud']
                localidad.longitud = coordenadas['longitud']
                localidad.save()
        return coordenadas
    