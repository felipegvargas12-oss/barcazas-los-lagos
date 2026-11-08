from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'rutas'

# Configuración del Router para los endpoints de la API REST (/api/rutas/)
router = DefaultRouter()
router.register(r'api/rutas', views.RutaViewSet, basename='api-rutas')

urlpatterns = [
    # Páginas Web HTML existentes
    path('', views.inicio, name='inicio'),
    path('horarios/', views.horarios, name='horarios'),
    path('horarios/<int:pk>/', views.detalle_ruta, name='detalle'),
    
    # Endpoints de la API REST
    path('', include(router.urls)),
]