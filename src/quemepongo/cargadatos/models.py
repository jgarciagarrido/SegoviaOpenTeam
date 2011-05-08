from django.db import models

from ftplib import FTP
import pygrib
import urllib
import urllib2
import json
import unicodedata


# Create your models here.
class DescargadorFichero:    
    
    def __init__(self, url):
        self._url = url
    
    def ObtenerFichero(self, remotePath, file, localPath):
                
        self.ftp = FTP(self._url)
        self.ftp.login()
        ftpCommand = 'RETR ' + remotePath + '/' + file
        #print ftpCommand
        self.ftp.retrbinary(ftpCommand, open(localPath + "/" + file, 'wb').write)
        self.ftp.quit()
        
    def ObtenerFicherosPrevisiones(self, remotePath, blockName, localPath):
        
        seq = range(3,60,6)
        for i in seq:
            self.ObtenerFichero(remotePath + "/" + blockName + "/", "20110507" + blockName + "0000_sfc_fc" + "%02d" % (i), localPath)
            

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
    
class Localidad(models.Model):
    nombre = models.CharField(max_length=100)
    latitud = models.FloatField(null=True)
    longitud = models.FloatField(null=True)
    def buscar(self, nombre):
        return Localidad.objects.filter(nombre=nombre)
    def obtener_coordenadas(self,nombre):
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
        latitud = float(datos[0]['lat'])
        longitud = float(datos[0]['lon'])
        return {'latitud': latitud,
                'longitud': longitud}
        #http://open.mapquestapi.com/nominatim/v1/search?q=Palazuelos+de+Eresma&format=json&limit=1

if __name__ == '__main__':
    localidad = Localidad()
    hola = localidad.obtener_coordenadas_web('Palazuelos de Eresma')
    
        
    