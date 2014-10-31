# -*- coding: cp1252 -*- 
from django.contrib import admin
from fotos.models import *
from django.forms.widgets import RadioSelect

TEXTO_AYUDA= ' '.join(["""<p>No puedes subir una foto igual, si intentas subir dos fotos con el mismo nombre lanzar&aacute; error<br/>
                          <p>Debes elegir tambi&eacute;n una foto como foto de portada de lo contrario lanzar&aacute; error en el sitio"""])

#otra forma de registrar es @admin.register(nombreDelModelo)

class FotosInline(admin.StackedInline):
    model = Fotos
    extra = 1
    form=FormChoices
    #raw_id_fields = ("relacion",)
    readonly_fields = ('image_tag',)

class AlbumAdmin(admin.ModelAdmin):
    model = Album
    inlines = [FotosInline]
    list_display = ('album','galerias','portada_galeria')
    exclude=('urlTitulo',)
    fieldsets = [
        ('album', {
            'fields':('album','galerias','portada_galeria'),
            'description': '<div class="help">%s</div>' %TEXTO_AYUDA,
        }),
    ]
    class Media:
        js=("/static/js/django_event.js",)
        
class DatosAdmin(admin.ModelAdmin):
    model = Datos
    list_display = ('image_tag',)
    readonly_fields = ('image_tag',)

    
class FlatPageAdmin(admin.ModelAdmin):
    fields = ('album',)

class ImagenDePortadaAdmin(admin.ModelAdmin):
    model = ImagenDePortada
    list_display = ('image_tag',)
    readonly_fields = ('image_tag',)


admin.site.register(Album,AlbumAdmin)
admin.site.register(Datos,DatosAdmin)
admin.site.register(ImagenDePortada,ImagenDePortadaAdmin)
