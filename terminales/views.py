from django.shortcuts import render
from .models import Terminal

def lista_terminales(request):
    # Usa .all() en lugar de .filter(estado='operativo') para mostrar todos los estados
    terminales = Terminal.objects.all()
    return render(request, 'terminales/lista.html', {'terminales': terminales})