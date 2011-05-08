# -*- coding: utf-8 -*.
from django.shortcuts import render_to_response
from models import Vestuario, Localidad
from quemepongo.cargadatos.models import GestorPrevisiones
import datetime

# Create your views here.
def recomendar_temperatura(request):
    if request.GET.has_key("temperatura"):   
        temperatura = float(request.GET['temperatura'])
        return render_to_response("recomendar.html", obtener_recomendacion(temperatura))
    else:
        return render_to_response("meter_temperatura.html", {})
 
def recomendar_localidad(request):
    if request.GET.has_key("localidad"):
        nombre_localidad = request.GET['localidad']
        localidad = Localidad()
        coordenadas = localidad.obtener_coordenadas(nombre_localidad)
        if len(coordenadas)>0:
            prevision = datetime.datetime.utcnow()
            prevision.day = prevision.day + 1
            temperatura = GestorPrevisiones.obtener_prevision( coordenadas['longitud'], 
                                                               coordenadas['latitud'], 
                                                               prevision)
            return render_to_response("recomendar.html", obtener_recomendacion(temperatura))
        else:
            return render_to_response("meter_localidad.html", {})
    else:
        return render_to_response("meter_localidad.html", {})
    
def obtener_recomendacion(temperatura):
    vestuario = Vestuario()
    vestido = vestuario.recomendar(temperatura)
    return {'vestido':vestido,
            'hombre': vestuario.img_hombres(vestido),
            'mujer': vestuario.img_mujeres(vestido)
            }
