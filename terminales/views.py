from django.shortcuts import render

def lista_terminales(request):
    contexto = {
        'terminales': [
            {'nombre': 'Rampa Pargua', 'comuna': 'Calbuco', 'marea': 'Pleamar (Alta)', 'estado': 'Operativa'},
            {'nombre': 'Rampa Chacao', 'comuna': 'Ancud', 'marea': 'Pleamar (Alta)', 'estado': 'Operativa'},
            {'nombre': 'Terminal Embarcadero Hornopirén', 'comuna': 'Hualaihué', 'marea': 'Bajamar (Baja)', 'estado': 'Precaución por rampla seca'},
        ]
    }
    return render(request, 'terminales/lista.html', contexto)
