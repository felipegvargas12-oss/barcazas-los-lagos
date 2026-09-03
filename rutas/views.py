from django.shortcuts import render

def inicio(request):
    return render(request, 'rutas/inicio.html')

def horarios(request):
    contexto = {
        'temporada': 'Alta (Verano)',
        'trayectos': [
            {'origen': 'Pargua', 'destino': 'Chacao', 'frecuencia': 'Cada 15 min', 'activo': True},
            {'origen': 'Caleta La Arena', 'destino': 'Puelche', 'frecuencia': 'Cada 45 min', 'activo': True},
            {'origen': 'Hornopirén', 'destino': 'Caleta Gonzalo', 'frecuencia': '2 viajes al día', 'activo': False},
        ]
    }
    return render(request, 'rutas/horarios.html', contexto)