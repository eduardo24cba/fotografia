from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from fotos.models import *
from django.core import serializers
import json

def principal(request):
    return render_to_response('index.html',{'imagen':ImagenDePortada.objects.get(pk="1")},context_instance=RequestContext(request))

def galeria(request):
    albumes=Album.objects.filter(portada_galeria="S")
    fotografias=[]
    for identificador in albumes:
        fotografias.append(Fotos.objects.get(relacion=identificador.id,foto_de_portada="S"))
    return render_to_response('album.html',{"albumes":albumes,"fotografias":fotografias},context_instance=RequestContext(request))

def sobreMi(request):
    return render_to_response('sobre mi.html',{'sobremi':Datos.objects.all()},context_instance=RequestContext(request))

def album(request,titulo):
    albumes=Album.objects.filter(galerias=titulo[:4])
    fotografias=[]
    galeria=""
    for identificador in albumes:
        fotografias.append(Fotos.objects.get(relacion=identificador.id,foto_de_portada="S"))
        galeria=identificador.get_galerias_display().lower()
    paginator= Paginator(albumes,3)
    pagina=request.GET.get("page")
    try:
        listaAlbumes = paginator.page(pagina)
    except PageNotAnInteger:
        #si no es un entero la pagina
        listaAlbumes=paginator.page(1)
    except EmptyPage:
        #si esta vacia la pagina
        listaAlbumes=paginator.page(paginator.num_pages)
    
    return render_to_response("galeria.html",{"albumes":listaAlbumes,"fotografias":fotografias,"galeria":galeria},context_instance=RequestContext(request))

def listaFotos(request,album,titulo):
    albumes=Album.objects.filter(urlTitulo=album)
    fotogra=[]
    fotografias=[]
    if albumes:
        fotogra=Fotos.objects.filter(relacion=albumes[0].id)
        for x in json.loads(serializers.serialize("json",fotogra)):
            fotografias.append(x["fields"]["fotos"])
    
    return render_to_response('fotografias.html',{"fotografias":fotogra,"datos":",".join(fotografias)},context_instance=RequestContext(request))

""" agregamos el join para unir la cadena y ponemos media para completar nuestra ruta
json load transforma a diccionario para despues poder acceder al campo foto"""
