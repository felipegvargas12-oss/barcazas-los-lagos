from django.shortcuts import render


from .models import Terminal


def lista_terminales(request):
    terminales = Terminal.objects.all()
    return render(request, 'terminales/lista.html', {'terminales': terminales})
