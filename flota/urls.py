from django.urls import path
from . import views

app_name = 'flota'

urlpatterns = [
    path('', views.lista_flota, name='lista'),
]