"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.utils import unittest

from ftplib import FTP
from quemepongo.cargadatos.models import ManejadorFichero, DescargadorFichero, GestorPrevisiones, PrevisionGeolocalizada
from quemepongo.consejero.models import Localidad, Provincia
import os.path
import os
import glob
import datetime
import tempfile


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
        
        today = datetime.datetime.today()
        fileName = str(today.year) + "%02d" % today.month + "%02d" % today.day + '000000_sfc_fc03'
        descargador = DescargadorFichero(self.url)
        descargador.ObtenerFichero(self.path + "/00", fileName, ".")
        localFilePath = self.localPath + "/" + fileName
        self.assertTrue(os.path.exists(localFilePath) and os.path.isfile(localFilePath), 'No existe el fichero ' + localFilePath)
        
        
    def testDescargarPrevision(self):
        
        descargador = DescargadorFichero(self.url)
        descargador.ObtenerFicherosPrevisiones(datetime.datetime.now(), self.path, '00', self.localPath)
        
        fileList = glob.glob(self.localPath + '/??????????0000_sfc_fc??')
        
        self.assertTrue(len(fileList) == 5, "Faltan archivos")
        

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
        
class PruebasRegistroPrevisiones(unittest.TestCase):
    
    def setUp(self):
        PrevisionGeolocalizada.objects.all().delete()
        
        self.url = "ftpdatos.aemet.es"
        self.remote_path = "/modelos_numericos/hirlam016/"
        self.local_path = tempfile.gettempdir()
        
        fileList = glob.glob(self.local_path + '/??????????0000_sfc_fc??')
        for fileName in fileList:
            os.remove(fileName)        
        
    def tearDown(self):
        
        fileList = glob.glob(self.local_path + '/??????????0000_sfc_fc??')
        for fileName in fileList:
            os.remove(fileName)
    
    def test_registrar_prevision(self):
        
        g = GestorPrevisiones()
        time_stamp = datetime.datetime(2011, 5, 7, 18, 0, 0)
        
        g.guardar_prevision(-3.67, 40.3, time_stamp, 300, 2.5)
                
        prevision = PrevisionGeolocalizada.objects.get(longitud = -3.67, latitud = 40.3, fecha_prevision = time_stamp)
        
        self.assertNotEqual(prevision, None)
        self.assertEqual(prevision.temperatura, 300)
        self.assertEqual(prevision.precipitacion, 2.5)
        
    def test_actualizar_prevision_existente(self):

        time_stamp = datetime.datetime(2011, 5, 7, 18, 0, 0)
        
        g = GestorPrevisiones()
        g.guardar_prevision(-3.67, 40.3, time_stamp, 300, 2.5)
        g.guardar_prevision(-3.67, 40.3, time_stamp, 330, 5)
        
        prevision = PrevisionGeolocalizada.objects.get(longitud = -3.67, latitud = 40.3, fecha_prevision = time_stamp)
        
        self.assertNotEqual(prevision, None)
        self.assertEqual(prevision.temperatura, 330)
        self.assertEqual(prevision.precipitacion, 5)
        
    def test_obtener_prevision_existente(self):
        
        time_stamp = datetime.datetime(2011, 5, 7, 18, 0, 0)
        lon = 40.3
        lat = -3.67
        temp = 350
        prec = 5
        
        p = PrevisionGeolocalizada(longitud = lon, latitud = lat, fecha_prevision = time_stamp, temperatura = temp, precipitacion = prec)
        p.save()
        
        g = GestorPrevisiones()
        p2 = g.obtener_prevision(lon, lat, time_stamp)
        self.assertEqual(p, p2)

    def test_obtener_prevision_no_existe(self):
        
        g = GestorPrevisiones()
        self.assertEqual(g.obtener_prevision(40, -3, datetime.datetime(2011, 5, 8, 11, 11, 0)), None)

    
    def test_existe_prevision(self):

        time_stamp = datetime.datetime(2011, 5, 7, 18, 0, 0)
        lon = 40.3
        lat = -3.67
        temp = 350
        prec = 5
        
        p = PrevisionGeolocalizada(longitud = lon, latitud = lat, fecha_prevision = time_stamp, temperatura = temp, precipitacion = prec)
        p.save()
        
        g = GestorPrevisiones()
        self.assertTrue(g.existe_prevision(lon, lat, time_stamp))
       
    def test_no_existe_prevision(self):

        time_stamp = datetime.datetime(2011, 5, 7, 18, 0, 0)
        lon = 40.3
        lat = -3.67
      
        g = GestorPrevisiones()
        self.assertFalse(g.existe_prevision(lon, lat, time_stamp))    
    
    def test_actualizar_previsiones(self):
        
        if os.path.exists('20110508120000_sfc_fc03'):
            print 'Ya existe'
        else:
            print 'No existe'
        
        g = GestorPrevisiones()
        g.actualizar_previsiones(self.url, self.remote_path)
        
        self.assertTrue(PrevisionGeolocalizada.objects.count() > 0)
        
    def test_obtener_prevision_cercana_existente(self):
        
        time_stamp = datetime.datetime(2011, 5, 7, 18, 0, 0)
        lon = 40.3
        lat = -3.67
        temp = 350
        prec = 5
        
        p = PrevisionGeolocalizada(longitud = lon, latitud = lat, fecha_prevision = time_stamp, temperatura = temp, precipitacion = prec)
        p.save()
        
        g = GestorPrevisiones()
        p2 = g.obtener_prevision(lon - 0.007, lat - 0.007, time_stamp)
        self.assertEqual(p, p2)

    
    def test_existe_prevision_cercana(self):

        time_stamp = datetime.datetime(2011, 5, 7, 18, 0, 0)
        lon = 40.3
        lat = -3.67
        temp = 350
        prec = 5
        
        p = PrevisionGeolocalizada(longitud = lon, latitud = lat, fecha_prevision = time_stamp, temperatura = temp, precipitacion = prec)
        p.save()
        
        g = GestorPrevisiones()
        self.assertTrue(g.existe_prevision(lon - 0.007, lat - 0.007, time_stamp))
       
    def test_no_existe_prevision_cercana(self):

        time_stamp = datetime.datetime(2011, 5, 7, 18, 0, 0)
        lon = 40.3
        lat = -3.67
      
        g = GestorPrevisiones()
        self.assertFalse(g.existe_prevision(lon - 0.007, lat - 0.007, time_stamp))  

class TestLocalidades(unittest.TestCase):
    def setUp(self):
        Localidad.objects.create(nombre="Segovia", latitud=10, longitud=20)        
        self.localidad = Localidad()
        archivo = os.path.join(os.path.dirname(__file__),"provincia.csv")
        provincias = Provincia()
        provincias.cargar(archivo)
        
    def test_buscarLocalidad(self):    
        resultado = self.localidad.buscar("Segovia")
        self.assertEquals(len(resultado),1)
        self.assertEqual(resultado[0].nombre, "Segovia")
    
    def test_buscarLocalidadInexistente(self):
        resultado = self.localidad.buscar("Whasinton")
        self.assertEquals(len(resultado),0) 
        
    def test_obtenerCoordenadasRegistradas(self):
        resultado = self.localidad.obtener_coordenadas("Segovia");
        self.assertAlmostEqual(resultado['latitud'], 10)
        self.assertAlmostEqual(resultado['longitud'], 20)
    
    def test_obtenerCoordenadasInternet(self):
        resultado = self.localidad.obtener_coordenadas_web("Palazuelos de Eresma")
        self.assertAlmostEqual(resultado['latitud'], 40.924187714)
        self.assertAlmostEqual(resultado['longitud'], -4.013027219766)
    def test_crear(self):
        valores={'nombre': 'ALHUCEMAS',
                 'provincia_id': 53
                }
        resultado = self.localidad.crear(valores)
        self.assertIsInstance(resultado,Localidad)

    def test_carga(self):
        archivo = os.path.join(os.path.dirname(__file__),"poblacion.csv")
        resultado = self.localidad.cargar(archivo)
        self.assertEqual(resultado, 71035)
         
            
class TestProvincias(unittest.TestCase):
    def test_crear(self):
        valores ={'nombre': 'Alicante',
                  'cod_migracion': 4
                  } 
        provincias = Provincia()
        resultado = provincias.crear(valores)
        self.assertIsInstance(resultado,Provincia)
    def test_carga(self):
        archivo = os.path.join(os.path.dirname(__file__),"provincia.csv")
        provincias = Provincia()
        resultado = provincias.cargar(archivo)
        self.assertEqual(resultado, 53)
