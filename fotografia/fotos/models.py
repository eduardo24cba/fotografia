# -*- coding: cp1252 -*-
from django.db import models
from fotografia import settings
from django.template.defaultfilters import slugify
from django.core.files.storage import FileSystemStorage
import os
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.forms import ModelForm
from django import forms
from django.core.exceptions import NON_FIELD_ERRORS



BASE_FOTOS =os.path.join(settings.MEDIA_ROOT, 'archivos\\fotos\\')
BASE_FOTO_PERFIL =os.path.join(settings.MEDIA_ROOT, 'archivos\\fotoPerfil\\')
BASE_FOTO_PORTADA =os.path.join(settings.MEDIA_ROOT, 'archivos\\fotos\\')

FOTOS_CHOICES=(
    ("arti","Artistica"),
    ("retr","Retratos"),
    ("book","Books"),
    ("soci","Sociales"),
    ("otro","Otros"),
    ("vide","Videos"),

    )
opciones={
    ("S","Si"),
    ("N","No"),
    }
class Album(models.Model):
    urlTitulo=models.SlugField(db_index=True)
    album=models.CharField(max_length=100,unique=True)
    portada_galeria=models.CharField(max_length=2,choices=opciones,default="N",blank=False,null=True,verbose_name="foto de portada")
    galerias= models.CharField(max_length=5, choices=FOTOS_CHOICES)
    class Meta:
        verbose_name_plural = u"album"
        
    def __unicode__(self):
        return "%s" % self.album

    def get_absolute_url(self):
        return "http://127.0.0.1:8000/index/galerias/%s/%s/" % (self.get_galerias_display().lower(),self.urlTitulo)

##    def validate_unique(self, exclude=None):
        #qs = query set
##        qs = Album.objects.filter(portada_galeria=True)
    
    def save(self):
        self.urlTitulo = slugify(self.album)
        super(Album, self).save()

class Fotos(models.Model):
#always in python add 'u' before of save
    fileStorage=FileSystemStorage(location=BASE_FOTOS)
    fileStorage.file_permissions_mode = 0644
    existe=False
    path='C:/Users/7/Desktop/fotografia/fotografia/fotografia/media/archivos/fotos/'
    fotos=models.ImageField(upload_to='archivos/fotos')
    foto_de_portada=models.CharField(max_length=2,choices=opciones,default="N",blank=False,null=True,verbose_name="foto de portada")
    relacion=models.ForeignKey(Album)
    class Meta:
        verbose_name_plural = "Fotos"
   
    def __unicode__(self):
        return u"%s" % (self.fotos)


    def clean(self):
        if self.fileStorage.exists(self.fotos.name) and self.pk is not None :
            self.existe=True
            raise ValidationError('El nombre de la fotografia '+ self.fotos.name +' ya existe o estas haciendo algo que no se puede.')
            
            
    def image_tag(self):
        if self.fotos and not self.existe:
            return u'<img width="200px" height="200px" src="%s" />' %(self.fotos.url)
        else:
            return '(Sin imagen)'
    image_tag.short_description = 'Imagen subida'
    image_tag.allow_tags = True

        
    def save(self):
        fileStorage=FileSystemStorage(location=BASE_FOTOS)
        fileStorage.file_permissions_mode = 0644
        if fileStorage.exists(self.fotos.name):
                raise ValidationError('El nombre o la foto ya existe.')
        elif self.pk is not None:
            foto_original = Fotos.objects.get(pk=self.pk)
            if foto_original.fotos != self.fotos:
                os.remove(os.path.join(settings.MEDIA_ROOT, foto_original.fotos.name))
                super(Fotos, self).save()
        super(Fotos, self).save()
            
        
    def delete(self):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.fotos.name))
        super(Fotos, self).delete()

class Datos(models.Model):
    sobreMi=models.TextField(max_length=1000,verbose_name="sobre mi")
    telefono=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    fotoPerfil=models.ImageField(upload_to='archivos/fotoPerfil', verbose_name="foto de perfil")

    def __unicode__(self):
        return u"%s" % (self.sobreMi)

    class Meta:
        verbose_name_plural = "sobre mi"

    def imagePerfil(self):
        return u'<img width="200px" height="200px" src="%s" />' %(self.fotoPerfil.url)

    def image_tag(self):
        if self.fotoPerfil:
            return u'<img width="200px" height="200px" src="%s" />' %(self.fotoPerfil.url)
        else:
            return '(Sin Foto de Perfil)'
    image_tag.short_description = 'Foto de Perfil'
    image_tag.allow_tags = True

    def get_absolute_url(self):
        return "http://127.0.0.1:8000/index/sobre-mi"

class ImagenDePortada(models.Model):
    fileStorage=FileSystemStorage(location=BASE_FOTO_PERFIL)
    fondoDePortada=models.ImageField(upload_to='archivos/fondoDePortada',verbose_name="foto de portada")

    def __unicode__(self):
        return u"%s" % (self.fondoDePortada)

    def clean(self):
        if self.fileStorage.exists(self.fondoDePortada.name):
            raise ValidationError('El nombre de la fotografia '+self.fondoDePortada.name+' ya existe')
        else:
            pass
    def image_tag(self):
        if self.fondoDePortada:
            return u'<img width="200px" height="200px" src="%s" />' %(self.fondoDePortada.url)
        else:
            return '(Sin imagen)'
    image_tag.short_description = 'Imagen subida'
    image_tag.allow_tags = True

    def get_absolute_url(self):
        return "http://127.0.0.1:8000/index/"
    
    def save(self):
        if self.pk is not None:
            foto_original = ImagenDePortada.objects.get(pk=self.pk)
            if foto_original.fondoDePortada != self.fondoDePortada:
                os.remove(os.path.join(settings.MEDIA_ROOT, foto_original.fondoDePortada.name))
        super(ImagenDePortada, self).save()

class FormChoices(ModelForm):
    class Meta:
        model= Fotos
        widgets={'foto_de_portada':forms.RadioSelect(),}

