from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView


urlpatterns = patterns('fotos.views',
     url(r'^index/$', 'principal'),
     url(r'^index/galerias/$', 'galeria'),
     url(r'^index/galerias/(?P<titulo>\w+)$', 'album'),
     url(r'^index/galerias/(?P<titulo>\w+)/(?P<album>\w+)/$', 'listaFotos'),
     url(r'^index/galerias/(?P<titulo>\w+)/(?P<album>[\w-]+)/$', 'listaFotos'),
    url(r'^index/?[\w-]+/$','sobreMi'), #para campos slug
)
