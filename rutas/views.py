from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Horario, Ruta
from .map_data import MAP_POINTS

def inicio(request):
    return render(request, 'rutas/inicio.html')

def horarios(request):
    salidas_futuras = Horario.objects.filter(
        activo=True,
        salida__gte=timezone.now(),
    )
    trayectos = Ruta.objects.prefetch_related(
        Prefetch('horarios', queryset=salidas_futuras)
    ).order_by('origen', 'destino')
    return render(request, 'rutas/horarios.html', {'trayectos': trayectos})


def detalle_ruta(request, pk):
    salidas_futuras = Horario.objects.filter(
        activo=True,
        salida__gte=timezone.now(),
    )
    ruta = get_object_or_404(
        Ruta.objects.prefetch_related(
            Prefetch('horarios', queryset=salidas_futuras)
        ),
        pk=pk,
    )
    puntos_mapa = [MAP_POINTS.get(ruta.origen), MAP_POINTS.get(ruta.destino)]
    if any(punto is None for punto in puntos_mapa):
        puntos_mapa = []
    hornopiren_es_referencial = any(
        punto['approximate_reference'] for punto in puntos_mapa
    )

    return render(request, 'rutas/detalle_ruta.html', {
        'ruta': ruta,
        'puntos_mapa': puntos_mapa,
        'hornopiren_es_referencial': hornopiren_es_referencial,
    })
