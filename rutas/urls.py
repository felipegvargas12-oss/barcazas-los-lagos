from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'rutas'

# Configuración del Router para la API REST
router = DefaultRouter()
router.register(r'api/rutas', views.RutaViewSet, basename='api-rutas')

urlpatterns = [
    # Rutas Web existentes (HTML)
    path('', views.inicio, name='inicio'),
    path('horarios/', views.horarios, name='horarios'),
    path('crear/', views.crear_ruta, name='crear'),
    path('editar/<int:pk>/', views.editar_ruta, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_ruta, name='eliminar'),
    
    # Endpoints de la API REST (/api/rutas/ y /api/rutas/<id>/)
    path('', include(router.urls)),
]