from django.shortcuts import render, redirect, get_object_or_404
from .models import Ruta
from .forms import RutaForm

def inicio(request):
    return render(request, 'rutas/inicio.html')
# 1. LISTAR
def horarios(request):
    trayectos = Ruta.objects.all().order_by('-fecha_creacion')
    return render(request, 'rutas/horarios.html', {'trayectos': trayectos})

# 2. CREAR
def crear_ruta(request):
    if request.method == 'POST':
        form = RutaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rutas:horarios')
    else:
        form = RutaForm()
    return render(request, 'rutas/form_ruta.html', {'form': form, 'titulo': 'Registrar Nueva Ruta'})

# 3. EDITAR
def editar_ruta(request, pk):
    ruta = get_object_or_404(Ruta, pk=pk)
    if request.method == 'POST':
        form = RutaForm(request.POST, instance=ruta)
        if form.is_valid():
            form.save()
            return redirect('rutas:horarios')
    else:
        form = RutaForm(instance=ruta)
    return render(request, 'rutas/form_ruta.html', {'form': form, 'titulo': f'Editar Ruta: {ruta}'})

# 4. ELIMINAR (POST Obligatorio)
def eliminar_ruta(request, pk):
    ruta = get_object_or_404(Ruta, pk=pk)
    if request.method == 'POST':
        ruta.delete()
        return redirect('rutas:horarios')
    return render(request, 'rutas/confirmar_eliminar.html', {'ruta': ruta})