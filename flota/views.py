from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from .forms import EmbarcacionForm
from .models import Embarcacion


def lista_embarcaciones(request):
    embarcaciones = Embarcacion.objects.all().order_by('nombre')
    return render(request, 'flota/lista.html', {'embarcaciones': embarcaciones})


def crear_embarcacion(request):
    if request.method == 'POST':
        form = EmbarcacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Embarcación creada exitosamente.')
            return redirect('flota:lista_embarcaciones')
    else:
        form = EmbarcacionForm()

    return render(request, 'flota/formulario_embarcacion.html', {'form': form, 'titulo': 'Registrar embarcación'})


def editar_embarcacion(request, pk):
    embarcacion = get_object_or_404(Embarcacion, pk=pk)

    if request.method == 'POST':
        form = EmbarcacionForm(request.POST, instance=embarcacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Embarcación actualizada exitosamente.')
            return redirect('flota:lista_embarcaciones')
    else:
        form = EmbarcacionForm(instance=embarcacion)

    return render(request, 'flota/formulario_embarcacion.html', {'form': form, 'titulo': 'Editar embarcación'})


def eliminar_embarcacion(request, pk):
    embarcacion = get_object_or_404(Embarcacion, pk=pk)

    if request.method == 'POST':
        embarcacion.delete()
        messages.success(request, 'Embarcación eliminada exitosamente.')
        return redirect('flota:lista_embarcaciones')

    return render(request, 'flota/eliminar_embarcacion.html', {'embarcacion': embarcacion})