from django.contrib import admin
from .models import Ruta

@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('origen', 'destino', 'duracion_horas', 'precio_base', 'activa')
    list_filter = ('activa', 'origen')
    search_fields = ('origen', 'destino')