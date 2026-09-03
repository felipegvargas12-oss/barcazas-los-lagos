from django.urls import path
from . import views

app_name = 'rutas'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('horarios/', views.horarios, name='horarios'),
]