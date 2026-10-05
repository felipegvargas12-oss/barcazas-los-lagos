from django.shortcuts import get_object_or_404, render

from rutas.map_data import MAP_POINTS
from .models import Terminal


def lista_terminales(request):
    terminales = Terminal.objects.all()
    return render(request, 'terminales/lista.html', {'terminales': terminales})


def detalle_terminal(request, pk):
    terminal = get_object_or_404(Terminal, pk=pk)
    punto_mapa = MAP_POINTS.get(str(terminal))
    return render(request, 'terminales/detalle.html', {
        'terminal': terminal,
        'punto_mapa': punto_mapa,
    })
