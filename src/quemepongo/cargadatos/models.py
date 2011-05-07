from django.db import models
import pygrib

# Create your models here.

class ManejadorFichero(object):
    ruta = ''
    fichero = None
    
    def __init__(self, ruta = '/'):
        self.ruta = ruta
    
    def abrir(self):
        self.fichero = pygrib.open(self.ruta)
    
    def leer_temperatura(self, x, y):
        temperaturas = self.fichero[2]
        valores = temperaturas.values
        latitudes, longitudes = temperaturas.latlons()
        return { 'temperatura': valores[x][y], 'latitud': latitudes[x][y], 'longitud': longitudes[x][y]}
    