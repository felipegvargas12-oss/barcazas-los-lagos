from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Ruta
from .serializers import RutaSerializer

# ==========================================
# 1. VISTAS WEB BÁSICAS (HTML)
# ==========================================

def inicio(request):
    return render(request, 'rutas/inicio.html')

def horarios(request):
    trayectos = Ruta.objects.all().order_by('-fecha_creacion')
    return render(request, 'rutas/horarios.html', {'trayectos': trayectos})

def detalle_ruta(request, pk):
    ruta = get_object_or_404(Ruta, pk=pk)
    return render(request, 'rutas/detalle_ruta.html', {'ruta': ruta})


# ==========================================
# 2. VISTA API REST (JSON / DRF)
# ==========================================

class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all().order_by('-id')
    serializer_class = RutaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]