from django.contrib import admin
from .models import Terminal


@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'comuna', 'estado', 'marea', 'es_demostracion')
	list_filter = ('comuna', 'estado', 'es_demostracion')
	search_fields = ('nombre', 'comuna', 'estado', 'marea')
