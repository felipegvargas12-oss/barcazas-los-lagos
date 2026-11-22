from django.contrib import admin
from .models import Terminal

@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marea', 'comuna', 'estado')
    list_filter = ('marea', 'comuna', 'estado')
    search_fields = ('nombre', 'comuna')