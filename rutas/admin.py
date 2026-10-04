from django.contrib import admin
from .models import Horario, Ruta

@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('origen', 'destino', 'duracion_horas', 'precio_base', 'activa', 'es_demostracion')
    list_filter = ('activa', 'es_demostracion', 'origen')
    search_fields = ('origen', 'destino')


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('ruta', 'salida', 'activo')
    list_filter = ('activo', 'salida')
    search_fields = ('ruta__origen', 'ruta__destino')