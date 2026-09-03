from django.urls import path
from . import views

app_name = 'terminales'

urlpatterns = [
    path('', views.lista_terminales, name='lista'),
]