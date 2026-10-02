from django.urls import path
from . import views

app_name = 'rutas'

urlpatterns = [
    path('', views.horarios, name='horarios'),
    path('crear/', views.crear_ruta, name='crear'),
    path('editar/<int:pk>/', views.editar_ruta, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_ruta, name='eliminar'),
]