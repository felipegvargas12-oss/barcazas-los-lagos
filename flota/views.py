from django.shortcuts import render

def lista_flota(request):
    contexto = {
        'barcazas': [
            {'nombre': 'El Trauco', 'capacidad_vehiculos': 30, 'capacidad_pasajeros': 150, 'operativa': True},
            {'nombre': 'Caupolicán', 'capacidad_vehiculos': 45, 'capacidad_pasajeros': 200, 'operativa': True},
            {'nombre': 'Pincoya', 'capacidad_vehiculos': 20, 'capacidad_pasajeros': 100, 'operativa': False},
        ]
    }
    return render(request, 'flota/lista.html', contexto)