from django.contrib import admin

from .models import Embarcacion


@admin.register(Embarcacion)
class EmbarcacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'matricula', 'capacidad_pasajeros', 'capacidad_vehicular', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'matricula')
