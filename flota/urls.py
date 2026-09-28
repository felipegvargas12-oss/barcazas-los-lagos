from django.urls import path

from . import views

app_name = 'flota'

urlpatterns = [
    path('', views.lista_embarcaciones, name='lista_embarcaciones'),
    path('nuevo/', views.crear_embarcacion, name='crear_embarcacion'),
    path('editar/<int:pk>/', views.editar_embarcacion, name='editar_embarcacion'),
    path('eliminar/<int:pk>/', views.eliminar_embarcacion, name='eliminar_embarcacion'),
]