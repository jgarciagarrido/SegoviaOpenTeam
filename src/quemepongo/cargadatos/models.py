from django.db import models

from ftplib import FTP
import pygrib

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
    
