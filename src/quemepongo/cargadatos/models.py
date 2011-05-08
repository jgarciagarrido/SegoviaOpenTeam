from django.db import models

from ftplib import FTP
import pygrib
import tempfile
import datetime
import os.path
import glob

# Create your models here.
class DescargadorFichero(object):    
    
    def __init__(self, url):
        self._url = url
    
    def ObtenerFichero(self, remotePath, file, local_dir):
        
        self.ftp = FTP(self._url)
        self.ftp.login()
        ftpCommand = 'RETR ' + remotePath + '/' + file
        local_path = local_dir + "/" + file
        
        print ftpCommand
        print local_path
       
        if os.path.exists(local_path):
            os.remove(local_path)
        self.ftp.retrbinary(ftpCommand, open(local_path, 'wb').write)
        self.ftp.quit()
        
    def ObtenerFicherosPrevisiones(self, forecastDate, remotePath, blockName, localPath):

        dateStr = "%04d" % forecastDate.year + "%02d" % forecastDate.month + "%02d" % forecastDate.day
        
                
        seq = range(3,60,12)
        for i in seq:
            self.ObtenerFichero(remotePath + "/" + blockName + "/", dateStr + blockName + "0000_sfc_fc" + "%02d" % (i), localPath)
            

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
    
    def tamanno_matriz(self):
        temperaturas = self.fichero[2]
        valores = temperaturas.values
        return {'num_columnas':len(valores), 'num_filas':len(valores[0])}
    
class GestorPrevisiones(object):
    
    
    def guardar_prevision(self, lon, lat, fecha_prev, temp, prec):
        
        if self.existe_prevision(lon, lat, fecha_prev):
            prevision = PrevisionGeolocalizada.objects.get(longitud = lon, latitud = lat, fecha_prevision = fecha_prev)
            prevision.temperatura = temp
            prevision.precipitacion = prec
        else:
            prevision = PrevisionGeolocalizada(longitud = lon, latitud = lat, fecha_prevision = fecha_prev, temperatura = temp, precipitacion = prec)     

        prevision.save()
        
    def existe_prevision(self, lon, lat, fecha_prev):
        lon_inicio = lon - 0.8
        lon_final = lon + 0.8
        lat_inicio = lat - 0.8
        lat_final = lat + 0.8
        
        return (len(PrevisionGeolocalizada.objects.filter(longitud__range = (lon_inicio, lon_final), latitud__range = (lat_inicio, lat_final), fecha_prevision = fecha_prev)) > 0)
        
    def obtener_prevision(self, lon, lat, fecha_prev):        
        
        if(self.existe_prevision(lon, lat, fecha_prev)):
            lon_inicio = lon - 0.8
            lon_final = lon + 0.8
            lat_inicio = lat - 0.8
            lat_final = lat + 0.8
            prevision = PrevisionGeolocalizada.objects.get(longitud__range = (lon_inicio, lon_final), latitud__range = (lat_inicio, lat_final), fecha_prevision = fecha_prev)         
        else:
            prevision = None
            
        return prevision
    
    def actualizar_previsiones(self, direccion_ftp, directorio_datos):
        
        local_path = tempfile.gettempdir()        
        
        fecha_realizacion_prevision = datetime.datetime.utcnow()
        bloque_prevision = str((fecha_realizacion_prevision.hour/6)*6)
        descFich = DescargadorFichero(direccion_ftp)
        descFich.ObtenerFicherosPrevisiones(fecha_realizacion_prevision, directorio_datos, bloque_prevision, local_path)
        
        lista_archivos = glob.glob(local_path + '/??????????0000_sfc_fc??')
        for ruta_archivo in lista_archivos:
            nombre_archivo = os.path.basename(ruta_archivo)
            delta = datetime.timedelta(hours=int(nombre_archivo[21:23]))
            fecha_prev = datetime.datetime(int(nombre_archivo[0:4]), int(nombre_archivo[4:6]), int(nombre_archivo[6:8]),int(nombre_archivo[8:10]),0,0) + delta
            
            print nombre_archivo + " " + str(datetime.datetime.now())
            
            gestor_grib = ManejadorFichero(ruta_archivo)
            gestor_grib.abrir()
            tamanno_matriz = gestor_grib.tamanno_matriz()
            num_columnas = tamanno_matriz['num_columnas']
            num_filas = tamanno_matriz['num_filas']
            
            for i in range(num_filas):
                for j in range(num_columnas):
                    temp_geolocalizada = gestor_grib.leer_temperatura(j, i)
                    self.guardar_prevision(temp_geolocalizada['longitud'], temp_geolocalizada['latitud'], fecha_prev, temp_geolocalizada['temperatura'], 0)
            
            os.remove(ruta_archivo)
         
    
class PrevisionGeolocalizada(models.Model):
    longitud = models.FloatField()
    latitud = models.FloatField()
    temperatura = models.FloatField("K")
    precipitacion = models.FloatField("l/m2")
    fecha_prevision = models.DateTimeField("Fecha y hora de la prevision")
    
    def __unicode__(self):
        return "lon = %(lon); lat = %(lat); temp = %(temp); prec = %(prec); fecha = %(fecha)" % \
            {"lon":self.longitud, "lat":self.latitud, "temp":self.temperatura, "prec":self.precipitacion, "fecha":self.fecha_prevision}
    
    
    
        
    